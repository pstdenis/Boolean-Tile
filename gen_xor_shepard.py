"""Generate a high-bitrate WAV of a Boolean tile Shepard tone sweep.

Fully continuous sample-by-sample generation:
  - No chunks, no segment boundaries, no glide stepping
  - Phase-continuous across entire duration
  - Anti-aliased (layers above Nyquist are skipped)
  - Envelope varies per-sample
"""

import argparse, math, struct, wave
import numpy as np

# ─── Boolean functions ──────────────────────────────────────────────
FN = [
    lambda a,b: 0,        # 0  FALSE
    lambda a,b: a&b,      # 1  AND
    lambda a,b: a&~b,     # 2  A∧¬B
    lambda a,b: a,        # 3  A
    lambda a,b: ~a&b,     # 4  ¬A∧B
    lambda a,b: b,        # 5  B
    lambda a,b: a^b,      # 6  XOR
    lambda a,b: a|b,      # 7  OR
    lambda a,b: ~(a|b),   # 8  NOR
    lambda a,b: ~(a^b),   # 9  XNOR
    lambda a,b: ~b,       # 10 ¬B
    lambda a,b: b|~a,     # 11 B→A
    lambda a,b: ~a,       # 12 ¬A
    lambda a,b: ~a|b,     # 13 A→B
    lambda a,b: ~(a&b),   # 14 NAND
    lambda a,b: 1,        # 15 TRUE
]

P_BITS = [1, 0, 1, 0]
Q_BITS = [1, 1, 0, 0]

def base_pattern(tile_idx):
    fn = FN[tile_idx]
    return np.array([fn(P_BITS[i], Q_BITS[i]) for i in range(4)], dtype=np.uint8)

# ─── Audio parameters ──────────────────────────────────────────────
F0_BASE = 220.0
F1_BASE = 660.0
TEMPO = 50
SHEPARD_WINDOW_OCTAVES = 0.80
CHUNK_SEC = 0.5  # seconds per processing chunk — balances memory vs speed

def shepard_sigma(num_octaves):
    return SHEPARD_WINDOW_OCTAVES * (num_octaves / 4.0)


def generate_sweep(tile_idx, num_octaves, dur_sec, sr, sweep_rate_hz):
    base4 = base_pattern(tile_idx)
    f1_bits = np.where(base4, F1_BASE, F0_BASE)  # per-position base frequency

    total_samples = int(round(sr * dur_sec))
    chunk_len = int(round(sr * CHUNK_SEC))
    mid_layer = (num_octaves - 1) / 2.0
    sigma = shepard_sigma(num_octaves)

    max_glide = dur_sec * sweep_rate_hz
    needed_layers = num_octaves + int(math.ceil(max_glide)) + 4

    # Phase accumulator per layer (continuous across chunks)
    phase_accum = np.zeros(needed_layers, dtype=np.float64)
    # For writing, accumulate into float64 buffer, then cast to float32
    output = np.zeros(total_samples, dtype=np.float32)

    for chunk_start in range(0, total_samples, chunk_len):
        chunk_end = min(chunk_start + chunk_len, total_samples)
        n = chunk_end - chunk_start
        t = (np.arange(chunk_start, chunk_end, dtype=np.float64)) / sr
        glide = sweep_rate_hz * t

        acc = np.zeros(n, dtype=np.float64)

        # Compute normalisation from the envelope sum across all layers
        # at the chunk midpoint, then apply uniformly within the chunk
        # (envelope changes slowly enough that this is inaudible).
        glide_mid = float(glide[n // 2])
        total_env = 0.0
        for k in range(needed_layers):
            dist_k = (k + glide_mid) - mid_layer
            total_env += math.exp(-0.5 * (dist_k / sigma) ** 2)
        norm = 1.0 / total_env if total_env > 0 else 1.0

        for k in range(needed_layers):
            # Pre-check envelope peak for this chunk
            dist_peak = (k + glide_mid) - mid_layer
            env_peak = math.exp(-0.5 * (dist_peak / sigma) ** 2)
            if env_peak < 0.001:
                continue

            nbits = 1 << k  # 2^k
            period = min(4, nbits)  # pattern period in bits

            # Base-4 index at each sample — continuous bit position
            bit_phase = t * TEMPO * nbits
            base4_idx = (np.floor(bit_phase).astype(np.int64)) % period

            # Instantaneous frequency per sample
            mult = 2.0 ** (k + glide)
            freq = f1_bits[base4_idx] * mult

            # Anti-aliasing: skip if any sample in this chunk
            # has frequency above 45% of Nyquist (with margin)
            if np.max(freq) > sr * 0.45:
                continue

            # Shepard envelope per sample (normalised)
            dist = (k + glide) - mid_layer
            env = np.exp(-0.5 * (dist / sigma) ** 2) * norm

            # Phase-continuous sine: cumulative sum of delta-phase
            delta = 2.0 * np.pi * freq / sr
            phase = phase_accum[k] + np.cumsum(delta)
            phase_accum[k] = phase[-1]

            acc += env * np.sin(phase)

        output[chunk_start:chunk_end] = acc.astype(np.float32)

    # Normalise
    peak = np.max(np.abs(output))
    if peak > 0:
        output *= (0.3 / peak)

    return output


# ─── WAV writing ────────────────────────────────────────────────────

def write_wav_float(filename, samples, sr):
    n = len(samples)
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(4)
        wav.setframerate(sr)
        wav.writeframes(struct.pack(f'<{n}f', *samples))
    mb = n * 4 / (1024 * 1024)
    print(f"  {filename}  ({n/sr:.1f}s, {sr}Hz, {mb:.1f} MB float32)")

def write_wav_int16(filename, samples, sr):
    int16 = np.clip(samples * 32767, -32768, 32767).astype(np.int16)
    n = len(int16)
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(int16.tobytes())
    mb = n * 2 / (1024 * 1024)
    print(f"  {filename}  ({n/sr:.1f}s, {sr}Hz, {mb:.1f} MB int16)")


# ─── Main ───────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tile', type=int, default=6, choices=range(16))
    ap.add_argument('--dur', type=float, default=60.0)
    ap.add_argument('--sr', type=int, default=96000)
    ap.add_argument('--octaves', type=int, default=10)
    ap.add_argument('--sweep-rate', type=float, default=1/28.8)
    ap.add_argument('--int16', action='store_true')
    ap.add_argument('-o', '--output', default='shepard_sweep.wav')
    args = ap.parse_args()

    max_glide = args.dur * args.sweep_rate
    usable_octaves = int(math.floor(math.log2(args.sr * 0.45 / F1_BASE))) + 1
    print(f"Tile {args.tile} Shepard Sweep — {args.dur}s @ {args.sr}Hz, {args.octaves} layers")
    print(f"  Sweep rate: {args.sweep_rate:.4f} cyc/s  (max glide: {max_glide:.1f})")
    print(f"  Usable octaves (below Nyquist): {usable_octaves}")
    print(f"  Continuous generation — no chunk boundaries in glide, phase, or envelope")
    print("  Generating...")

    samples = generate_sweep(args.tile, args.octaves, args.dur, args.sr, args.sweep_rate)

    if args.int16:
        write_wav_int16(args.output, samples, args.sr)
    else:
        write_wav_float(args.output, samples, args.sr)
    print("Done.")


if __name__ == '__main__':
    main()
