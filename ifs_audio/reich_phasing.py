"""
Reich-style phasing + IFS tile fractal Shepard layer.

6 speech voices (time-stretched, pitch preserved) drift in and out of phase.
An optional IFS tile voice adds a slowly-revealing fractal harmonic structure
that evolves across the full duration.
"""

import numpy as np
import librosa
import soundfile as sf
import os
from core import get_fractal_wave_value


def smoothstep(t, t0, t1):
    x = np.clip((t - t0) / max(t1 - t0, 1e-10), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def _gen_ifas_raw(sr, freq_hz, tile_bits, depth, num_samples):
    """Generate IFS waveform at constant frequency, no normalization."""
    out = np.zeros(num_samples, dtype=np.float64)
    phase = 0.0
    for i in range(num_samples):
        if freq_hz > 0:
            phase += freq_hz / sr
        phase %= 1.0
        out[i] = get_fractal_wave_value(tile_bits, phase, depth)
    return out


def make_ifas_voice_loop(N, sr, freq_hz, tile_bits, depth,
                         shift, depth_minutes):
    """
    Generate an IFS tile loop with Shepard depth reveal.

    Returns (loop_audio, loop_len) for the time-stretched IFS voice.
    The loop has the Shepard reveal envelope baked in (time-based gains
    on each depth level).
    """
    # Generate at shifted frequency so the loop length = N * shift
    shifted_freq = freq_hz / shift
    loop_len = int(N * shift)

    ifs_full = _gen_ifas_raw(sr, shifted_freq, tile_bits, depth, loop_len)
    prev = None
    levels = []
    for d in range(1, depth + 1):
        w = _gen_ifas_raw(sr, shifted_freq, tile_bits, d, loop_len)
        if prev is not None:
            levels.append(w - prev)
        else:
            levels.append(w)
        prev = w

    t = np.arange(loop_len, dtype=np.float64) / sr
    mixed = np.zeros(loop_len, dtype=np.float64)
    total_sec = loop_len / sr
    for k, lv in enumerate(levels):
        t0 = depth_minutes[k] * 60.0 if k < len(depth_minutes) else total_sec * 0.8
        t1 = depth_minutes[k + 1] * 60.0 if k + 1 < len(depth_minutes) else total_sec
        gain = smoothstep(t, t0, t1)
        mixed += gain * lv
    return mixed, loop_len


def make_reich_phasing(audio_path: str, output_dir: str,
                       sr: int = 16000,
                       speed_shifts: list = None,
                       cycle_count: int = 100,
                       crossfade: float = 2.0,
                       ifs_tile: dict = None):
    if speed_shifts is None:
        speed_shifts = [1.0, 1.01, 0.99, 1.02, 0.98, 1.03]

    # --- Load and resample ---
    print(f"Loading: {audio_path}")
    audio, orig_sr = sf.read(audio_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if orig_sr != sr:
        print(f"  Resampling {orig_sr} -> {sr} Hz...")
        audio = librosa.resample(audio, orig_sr=orig_sr, target_sr=sr)

    N = len(audio)
    total_samples = N * cycle_count
    total_duration = total_samples / sr
    cf_samples = int(crossfade * sr)
    dur_min = total_duration / 60

    print(f"  Original: {N/sr:.3f}s @ {sr}Hz ({N} samples)")
    print(f"  Output:   {total_duration:.1f}s ({dur_min:.1f} min), "
          f"{total_samples} samples")
    print(f"  Speech voices: {len(speed_shifts)} {speed_shifts}")
    if ifs_tile:
        print(f"  IFS tile:      {ifs_tile['name']} "
              f"(freq={ifs_tile.get('freq', 110)}Hz, "
              f"shift={ifs_tile.get('shift', 1.015)})")
    print(f"  Crossfade:{crossfade}s at seam")

    # --- Seam analysis ---
    print("  Seam offsets (speech voices):")
    for vi, shift in enumerate(speed_shifts):
        N_i = N * shift
        cycles = total_samples / N_i
        frac = cycles - np.floor(cycles)
        offset_samp = frac * N_i
        print(f"    V{vi+1} (shift={shift:.4f}): offset={offset_samp/sr:.3f}s")

    # --- Generate mix ---
    mix = np.zeros(total_samples, dtype=np.float64)

    # Speech voices
    for vi, shift in enumerate(speed_shifts):
        print(f"  Speech V{vi+1}: shift={shift:.4f} ", end="", flush=True)
        rate = 1.0 / shift
        stretched = librosa.effects.time_stretch(audio, rate=rate)
        loop_len = len(stretched)
        print(f"(loop={loop_len/sr:.3f}s)", flush=True)
        for start in range(0, total_samples, loop_len):
            end = min(start + loop_len, total_samples)
            mix[start:end] += stretched[:end - start]

    # IFS tile voice
    if ifs_tile is not None:
        bits = ifs_tile["bits"]
        name = ifs_tile["name"]
        freq = ifs_tile.get("freq", 110.0)
        shift = ifs_tile.get("shift", 1.015)
        depth = ifs_tile.get("depth", 4)
        depth_times = ifs_tile.get("depth_times",
                                    [0.0, 2.0, 5.0, 10.0, 15.0])

        print(f"  IFS {name}: shift={shift:.4f}, freq={freq}Hz, "
              f"depth={depth}", end="", flush=True)

        ifs_loop, loop_len = make_ifas_voice_loop(
            N, sr, freq, bits, depth, shift, depth_times)
        print(f" (loop={loop_len/sr:.3f}s)", flush=True)

        # Pan IFS slightly left for spatial separation
        ifs_gain = ifs_tile.get("gain", 0.5)

        for start in range(0, total_samples, loop_len):
            end = min(start + loop_len, total_samples)
            mix[start:end] += ifs_gain * ifs_loop[:end - start]

    # --- Normalize ---
    mx = np.max(np.abs(mix))
    if mx > 0:
        mix /= mx
    print(f"  Normalized: peak={mx:.3f} -> 1.0")

    # --- Crossfade at loop seam ---
    fade_out = np.linspace(1.0, 0.0, cf_samples)
    fade_in = np.linspace(0.0, 1.0, cf_samples)
    mix[-cf_samples:] *= fade_out
    mix[:cf_samples] *= fade_in
    print(f"  Crossfade: {crossfade}s applied")

    # --- Write stereo (IFS panned slightly left) ---
    if ifs_tile is not None and ifs_tile.get("pan", False):
        left = mix.copy()
        right = mix.copy()
        ifs_pan = ifs_tile.get("pan_amount", 0.3)
        # subtract IFS from right, add to left
        # For simplicity, just write mono to stereo
    stereo = np.column_stack((mix, mix))
    os.makedirs(output_dir, exist_ok=True)
    suffix = f"_{ifs_tile['name']}" if ifs_tile else ""
    name = f"reich_phasing{suffix}_{dur_min:.0f}min.wav"
    path = os.path.join(output_dir, name)
    sf.write(path, stereo.astype(np.float32), sr)
    print(f"\nSaved: {path}")
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"       {size_mb:.1f} MB")
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    ref = os.path.join(out, "reference_original.wav")
    if not os.path.exists(ref):
        from audio_io import download_speech
        ref = download_speech(out, "reference_original.wav", sr=16000)

    # Try with tile A
    from tiles import TILE_SIX
    tile = TILE_SIX[1]  # A
    tile["freq"] = 110.0
    tile["shift"] = 1.015
    tile["depth"] = 4
    tile["gain"] = 0.7
    tile["depth_times"] = [0.0, 0.5, 2.0, 4.0, 8.0]  # minutes

    make_reich_phasing(ref, out, sr=16000, cycle_count=100,
                       crossfade=2.0, ifs_tile=tile)
