import numpy as np
import librosa
from core import (generate_ifs_waveform, generate_walsh_waveform,
                  compute_ifas_harmonic_mask, compute_walsh_harmonic_mask,
                  get_fractal_wave_value)


def option_a_resynth(audio: np.ndarray, sr: int, pitch_samples: np.ndarray,
                     tile_bits: tuple, depth: int = 6) -> np.ndarray:
    """Full IFS resynthesis: pitch → IFS carrier, original audio discarded."""
    print(f"  Running Option A (IFS resynthesis)...")
    out = generate_ifs_waveform(sr, pitch_samples, tile_bits, depth)
    return out


def option_b_fb_4k(audio: np.ndarray, sr: int, pitch_samples: np.ndarray,
                   tile_bits: tuple, depth: int = 6) -> np.ndarray:
    """Spectral masking: original audio filtered through IFS harmonic mask (4^k)."""
    print(f"  Running Option B (4^k filter bank)...")

    hop_length = 512
    fft_size = 2048

    masks, freqs = compute_ifas_harmonic_mask(
        sr, pitch_samples, tile_bits, depth, hop_length, fft_size)

    D = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length,
                     window="hann", center=True)
    n_frames = min(D.shape[1], masks.shape[0])

    for frame_idx in range(n_frames):
        # mask is additive gain around 1.0
        mask = 1.0 + masks[frame_idx, :len(D)]
        D[:, frame_idx] *= mask[:D.shape[0]]

    out = librosa.istft(D, hop_length=hop_length, window="hann", center=True,
                        length=len(audio))
    mx = np.max(np.abs(out))
    if mx > 0:
        out /= mx
    return out


def option_b_fb_walsh(audio: np.ndarray, sr: int, pitch_samples: np.ndarray,
                      walsh_coeffs: np.ndarray, num_octaves: int = 6) -> np.ndarray:
    """Spectral masking: original audio filtered through Walsh φ harmonic mask."""
    print(f"  Running Option B (Walsh φ filter bank)...")

    hop_length = 512
    fft_size = 2048

    masks, freqs = compute_walsh_harmonic_mask(
        sr, pitch_samples, walsh_coeffs, num_octaves, hop_length, fft_size)

    D = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length,
                     window="hann", center=True)
    n_frames = min(D.shape[1], masks.shape[0])

    for frame_idx in range(n_frames):
        mask = 1.0 + masks[frame_idx, :len(D)]
        D[:, frame_idx] *= mask[:D.shape[0]]

    out = librosa.istft(D, hop_length=hop_length, window="hann", center=True,
                        length=len(audio))
    mx = np.max(np.abs(out))
    if mx > 0:
        out /= mx
    return out


def option_c_vocoder(audio: np.ndarray, sr: int, pitch_samples: np.ndarray,
                     tile_bits: tuple, walsh_coeffs: np.ndarray,
                     depth: int = 6) -> np.ndarray:
    """Vocoder/cross-synthesis: |STFT_input| × exp(j·∠STFT_IFS_carrier)."""
    print(f"  Running Option C (vocoder)...")

    hop_length = 512
    fft_size = 2048

    # generate IFS carrier at tracked pitch
    ifs_carrier = generate_ifs_waveform(sr, pitch_samples, tile_bits, depth)

    # STFT both signals
    D_orig = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length,
                          window="hann", center=True)
    D_ifs = librosa.stft(ifs_carrier, n_fft=fft_size, hop_length=hop_length,
                         window="hann", center=True)

    n_frames = min(D_orig.shape[1], D_ifs.shape[1])
    D_orig = D_orig[:, :n_frames]
    D_ifs = D_ifs[:, :n_frames]

    mag_orig = np.abs(D_orig) + 1e-10
    phase_ifs = np.angle(D_ifs)

    # cross-synthesis: magnitude from input, phase from IFS carrier
    D_out = mag_orig * np.exp(1j * phase_ifs)

    out = librosa.istft(D_out, hop_length=hop_length, window="hann",
                        center=True, length=len(audio))
    mx = np.max(np.abs(out))
    if mx > 0:
        out /= mx
    return out


def shepard_canon(audio: np.ndarray, sr: int, pitch_samples: np.ndarray,
                  tile_bits: tuple, depth: int = 4,
                  stagger_delay: float = 2.0, crossfade: float = 0.3) -> np.ndarray:
    """Multi-voice Shepard canon.

    Each voice k plays the IFS waveform at f0 × 4^k, enters at delay k×stagger_delay,
    with gain 1/2^k.  Creates the ascending staircase effect.
    """
    print(f"  Running Shepard canon (depth={depth}, stagger={stagger_delay}s)...")
    num_samples = len(audio)
    output = np.zeros(num_samples, dtype=np.float64)

    for k in range(depth):
        freq_mult = 4.0 ** k
        gain = 1.0 / (2.0 ** k)
        delay_samp = int(k * stagger_delay * sr)

        # generate IFS waveform at transposed pitch
        pitch_k = pitch_samples * freq_mult
        voice = generate_ifs_waveform(sr, pitch_k, tile_bits, depth)

        if delay_samp >= num_samples:
            continue

        # apply delay
        delayed = np.zeros(num_samples, dtype=np.float64)
        avail = num_samples - delay_samp
        delayed[delay_samp:] = voice[:avail]

        # fade in
        flen = min(int(crossfade * sr), avail)
        if flen > 0 and k > 0:
            delayed[delay_samp:delay_samp + flen] *= np.linspace(0.0, 1.0, flen)

        # fade out the last voice if it would end abruptly
        # (all voices naturally end together at num_samples)

        output += gain * delayed

    mx = np.max(np.abs(output))
    if mx > 0:
        output /= mx
    return output


def shepard_zoom_sweep(audio: np.ndarray, sr: int, pitch_samples: np.ndarray,
                       tile_bits: tuple, depth: int = 6,
                       sweep_period: float = 4.0) -> np.ndarray:
    """Continuous zoom sweep — replicates the web app's zoomPower ramp.

    fineWeight sweeps 0→1 repeatedly over sweep_period, creating a
    continuous Shepard glissando within the tracked pitch contour.
    """
    print(f"  Running Shepard zoom sweep (period={sweep_period}s)...")
    num_samples = len(audio)
    out = np.zeros(num_samples, dtype=np.float64)
    phase = 0.0

    for i in range(num_samples):
        f0 = pitch_samples[i]
        if f0 > 0:
            phase += f0 / sr
        phase %= 1.0

        t = i / sr
        fine_weight = (t % sweep_period) / sweep_period

        out[i] = get_fractal_wave_value(tile_bits, phase, depth, fine_weight)

    mx = np.max(np.abs(out))
    if mx > 0:
        out /= mx
    return out


def shepard_pure_glissando(sr: int, duration: float,
                           tile_bits: tuple, depth: int = 4,
                           start_freq: float = 110.0,
                           end_freq: float = 220.0,
                           stagger_delay: float = 2.0,
                           crossfade: float = 0.3) -> np.ndarray:
    """Pure Shepard glissando — no speech input.

    A single frequency sweeps from start_freq to end_freq.
    Staggered voices at 4^k transpositions create the ascending staircase.
    Demonstrates the pure tile character without melodic interference.
    """
    print(f"  Running pure Shepard glissando ({start_freq}→{end_freq}Hz"
          f", depth={depth}, stagger={stagger_delay}s)...")
    num_samples = int(duration * sr)
    num_samples += int((depth - 1) * stagger_delay * sr)
    t = np.arange(num_samples, dtype=np.float64) / sr

    freq_curve = np.linspace(start_freq, end_freq, num_samples)

    output = np.zeros(num_samples, dtype=np.float64)

    for k in range(depth):
        freq_mult = 4.0 ** k
        gain = 1.0 / (2.0 ** k)
        delay_samp = int(k * stagger_delay * sr)

        pitch_k = freq_curve * freq_mult

        # generate IFS waveform at the shifted frequency
        voice = generate_ifs_waveform(sr, pitch_k, tile_bits, depth)

        if delay_samp >= num_samples:
            continue

        delayed = np.zeros(num_samples, dtype=np.float64)
        avail = num_samples - delay_samp
        delayed[delay_samp:] = voice[:avail]

        flen = min(int(crossfade * sr), avail)
        if flen > 0 and k > 0:
            delayed[delay_samp:delay_samp + flen] *= np.linspace(0.0, 1.0, flen)

        output += gain * delayed

    # trim to the active region
    last_active = 0
    for i in range(num_samples - 1, -1, -1):
        if np.abs(output[i]) > 1e-6:
            last_active = i + 1
            break
    output = output[:last_active]

    mx = np.max(np.abs(output))
    if mx > 0:
        output /= mx
    return output, sr
