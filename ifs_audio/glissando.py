"""Pitch ramp: speech pitches up by one octave across its duration.

Segmented approach: pitch-shift the full audio at N different amounts,
extract segments, crossfade between adjacent segments via raised-cosine windows."""

import os, sys
import numpy as np
import soundfile as sf
import librosa

SR = 44100
N_SEMITONES = 12
N_SEGMENTS = 20
XFADE_FRAC = 0.25

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "output")
REF_PATH = os.path.join(OUT_DIR, f"reference_{SR}.wav")
OUT_PATH = os.path.join(OUT_DIR, "glissando_1oct.wav")

# --- Load ---
if not os.path.exists(REF_PATH):
    print(f"Reference not found. Run dist.py first.")
    sys.exit(1)

audio, sr = sf.read(REF_PATH)
if audio.ndim > 1:
    audio = audio.mean(axis=1)
audio = audio.astype(np.float64)
N = len(audio)
dur = N / sr
print(f"Audio: {dur:.3f}s @ {sr}Hz ({N} samples)")

# --- Boundaries ---
boundaries = np.linspace(0, N, N_SEGMENTS + 1).astype(np.int64)
print(f"Segments: {N_SEGMENTS} (crossfade={XFADE_FRAC:.0%})")
print(f"Pitch ramp: 0 to +{N_SEMITONES} semitones", flush=True)

# --- Precompute all pitch-shifted versions ---
versions = []
for si in range(N_SEGMENTS):
    semis = N_SEMITONES * si / (N_SEGMENTS - 1)
    print(f"  Shift {si:2d}/{N_SEGMENTS-1}: {semis:.1f} semitones", flush=True)
    shifted = librosa.effects.pitch_shift(
        audio, sr=sr, n_steps=semis, res_type='soxr_hq')
    versions.append(shifted)

# --- Overlap-add with raised-cosine windows ---
out = np.zeros(N, dtype=np.float64)
weight = np.zeros(N, dtype=np.float64)

for si in range(N_SEGMENTS):
    start = boundaries[si]
    end = boundaries[si + 1]
    seg_len = end - start
    if seg_len < 1:
        continue

    seg = versions[si][start:end].copy()

    fade_len = min(int(seg_len * XFADE_FRAC), seg_len // 2)
    env = np.ones(seg_len, dtype=np.float64)
    if fade_len > 0:
        if si > 0:
            env[:fade_len] = np.linspace(0.0, 1.0, fade_len)
        if si < N_SEGMENTS - 1:
            env[-fade_len:] = np.linspace(1.0, 0.0, fade_len)

    out[start:end] += seg * env
    weight[start:end] += env

weight = np.maximum(weight, 1e-10)
out /= weight

# Normalize amplitude
pk = np.max(np.abs(out))
if pk > 0:
    out /= pk

# Trim 10ms from each edge to remove any edge artifact
trim = int(0.01 * sr)
out = out[trim:-trim].copy()

sf.write(OUT_PATH, out.astype(np.float32), sr)
size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
print(f"\nWritten: {OUT_PATH}  ({size_mb:.1f} MB)")
print(f"  Output: {len(out)/sr:.3f}s")
