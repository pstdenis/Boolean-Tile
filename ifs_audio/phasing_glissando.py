"""
IFS Phasing Glissando — Reich-style phasing + Shepard depth reveal.

Generates a stereo piece:
  Left:  IFS waveform at base frequency
  Right: IFS waveform at (base_freq - detune_Hz)

Depth levels fade in one by one, creating the ascending staircase.
"""

import numpy as np
import soundfile as sf
import os
from core import get_fractal_wave_value


def _gen_raw(sr, freq_hz, tile_bits, depth, num_samples):
    """Generate IFS waveform at constant frequency, NO normalization."""
    out = np.zeros(num_samples, dtype=np.float64)
    phase = 0.0
    for i in range(num_samples):
        if freq_hz > 0:
            phase += freq_hz / sr
        phase %= 1.0
        out[i] = get_fractal_wave_value(tile_bits, phase, depth)
    return out


def smoothstep(t, t0, t1):
    """0→1 smooth cubic ramp between times t0 and t1."""
    x = np.clip((t - t0) / max(t1 - t0, 1e-10), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def decompose_depth_levels(sr, freq_hz, tile_bits, depth, num_samples):
    """Decompose the IFS waveform into per-depth component levels.
    
    Returns list of arrays [level_0, level_1, ..., level_{depth-1}].
    level_k contributes the 4^k harmonic with amplitude ±1/2^k.
    """
    levels = []
    prev = None
    for d in range(1, depth + 1):
        w = _gen_raw(sr, freq_hz, tile_bits, d, num_samples)
        if prev is not None:
            levels.append(w - prev)
        else:
            levels.append(w)
        prev = w
    return levels


def make_phasing_glissando(sr=22050, base_freq=110.0, tile_bits=(0, 0, 1, 1),
                           depth=4, duration=60.0, detune_ratio=0.001,
                           level_times=None, output_dir=None):
    """Generate the phasing glissando piece.
    
    Parameters
    ----------
    sr : int
        Sample rate.
    base_freq : float
        Fundamental frequency in Hz (left channel).
    tile_bits : tuple
        4-element tuple of 0/1 for the Boolean tile.
    depth : int
        Number of IFS depth levels.
    duration : float
        Total duration in seconds.
    detune_ratio : float
        Fractional detune for right channel (e.g. 0.001 = 0.1% slower).
    level_times : list of (t_start, t_end) or None
        Fade-in windows for each depth level. If None, uses defaults.
    output_dir : str or None
        If set, save WAV and return path.
    
    Returns
    -------
    stereo_audio : np.ndarray, shape (N, 2)
    """
    num_samples = int(duration * sr)

    # Default fade-in schedule for 4 levels over ~60s
    if level_times is None:
        level_times = [
            (0.0, 3.0),      # level 0: quick fade in
            (5.0, 20.0),     # level 1: slow reveal
            (20.0, 40.0),    # level 2: even slower
            (40.0, 55.0),    # level 3: final shimmer
        ]
    level_times = level_times[:depth]

    # --- Decompose into per-depth levels ---
    print(f"  Decomposing {depth} depth levels @ {base_freq} Hz...")
    levels = decompose_depth_levels(sr, base_freq, tile_bits, depth, num_samples)

    # --- Mix with time-varying gains ---
    print("  Mixing with time-varying gains...")
    t = np.arange(num_samples, dtype=np.float64) / sr
    mix = np.zeros(num_samples, dtype=np.float64)

    for k, (level, (t0, t1)) in enumerate(zip(levels, level_times)):
        gain = smoothstep(t, t0, t1)
        mix += gain * level

    # Normalize mix
    mx = np.max(np.abs(mix))
    if mx > 0:
        mix /= mx

    # --- Left channel: normal ---
    left = mix.copy()

    # --- Right channel: detuned ---
    detune_freq = base_freq * (1.0 - detune_ratio)
    print(f"  Phasing: L={base_freq:.3f} Hz, R={detune_freq:.3f} Hz "
          f"(Δ={base_freq - detune_freq:.4f} Hz, "
          f"{detune_ratio * 100:.2f}%)")

    # Generate right channel separately at detuned frequency
    levels_r = decompose_depth_levels(sr, detune_freq, tile_bits, depth, num_samples)

    mix_r = np.zeros(num_samples, dtype=np.float64)
    for k, (level, (t0, t1)) in enumerate(zip(levels_r, level_times)):
        gain = smoothstep(t, t0, t1)
        mix_r += gain * level

    mx_r = np.max(np.abs(mix_r))
    if mx_r > 0:
        mix_r /= mx_r

    right = mix_r

    # --- Stereo assembly ---
    stereo = np.column_stack((left, right))

    # --- Optionally save ---
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"phasing_glissando.wav")
        sf.write(path, stereo.astype(np.float32), sr)
        print(f"  Saved: {path} ({duration:.0f}s, {sr}Hz, stereo)")
        return stereo, path

    return stereo, None


def generate_tile_phasing(tile_dict, sr=22050, base_freq=110.0,
                          depth=4, duration=60.0, detune_ratio=0.001,
                          output_dir=None):
    """Generate phasing glissando for a single tile definition."""
    bits = tile_dict["bits"]
    name = tile_dict["name"]
    print(f"\n  === {name} ===")

    stereo, path = make_phasing_glissando(
        sr=sr, base_freq=base_freq,
        tile_bits=bits, depth=depth,
        duration=duration, detune_ratio=detune_ratio,
        output_dir=output_dir,
    )
    # Rename to include tile name
    if path and output_dir:
        new_path = os.path.join(output_dir, f"{name}_phasing_glissando.wav")
        os.replace(path, new_path)
        print(f"  Renamed: {new_path}")
        return stereo, new_path

    return stereo, None


if __name__ == "__main__":
    # Quick standalone test
    from tiles import TILE_SIX
    tile = TILE_SIX[1]  # A
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    generate_tile_phasing(tile, output_dir=out_dir)
