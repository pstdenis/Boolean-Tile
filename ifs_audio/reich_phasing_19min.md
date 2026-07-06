# Reich Phasing (Rainbow Passage) — 19-Minute Piece

## Concept

A **Reich-style phasing** piece: multiple identical copies of a short speech loop play simultaneously at **slightly different speeds**. The voices start in sync and gradually drift in and out of phase, creating evolving interference patterns, rhythmic shifts, and spectral comb-filtering effects. The technique is inspired by Steve Reich's *It's Gonna Rain* (1965) and *Piano Phase* (1967).

## Source Material

| Property | Value |
|---|---|
| Text | *Rainbow Passage*: "When the sunlight strikes raindrops in the air, they act like a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors." |
| Generator | Google Text-to-Speech (gTTS), English, normal speed |
| Sample rate | 22050 Hz (original), resampled to **16000 Hz** |
| Duration | **11.160 seconds** (178560 samples at 16 kHz) |
| Channels | Mono (summed to mono if stereo) |
| Format | 32-bit float WAV |

## Method

### Voice Generation

Six speech voices are created from the single source sample via **time-stretching** (librosa's phase vocoder, `librosa.effects.time_stretch`). Time-stretching changes duration while preserving pitch, so each voice has the same intonation but a different loop period.

Each voice has a **speed shift factor** `s` applied as a time-stretch rate `r = 1/s`:

| Voice | Shift `s` | Rate `r` | Loop length | Loop duration |
|---|---|---|---|---|
| V1 | 1.000 | 1.0000× | 178560 samples | 11.160 s |
| V2 | 1.010 | 0.9901× | 180346 samples | 11.272 s |
| V3 | 0.990 | 1.0101× | 176774 samples | 11.048 s |
| V4 | 1.020 | 0.9804× | 182131 samples | 11.383 s |
| V5 | 0.980 | 1.0204× | 174989 samples | 10.937 s |
| V6 | 1.030 | 0.9709× | 183917 samples | 11.495 s |

The loop length for voice `v` is `N × s_v` (rounded to integer samples), where `N` is the original sample count.

### Loop Tiling

Each voice is tiled (repeated end-to-end) for **100 cycles**, producing a total duration of:

```
100 × N / sr = 100 × 178560 / 16000 = 1116.0 seconds = 18.6 minutes
```

Voice V1 (shift=1.0) completes exactly 100 cycles. All other voices complete slightly more or fewer cycles, creating fractional-sample offsets at the loop seam:

| Voice | Shift | Seam offset (samples) | Seam offset (seconds) |
|---|---|---|---|
| V1 | 1.0000 | 0 | 0.000 |
| V2 | 1.0100 | 1786 | 0.112 |
| V3 | 0.9900 | 1786 | 0.112 |
| V4 | 1.0200 | 7144 | 0.446 |
| V5 | 0.9800 | 7144 | 0.446 |
| V6 | 1.0300 | 16068 | 1.004 |

These offsets represent the time misalignment between the start of the next cycle and the actual loop boundary for Voice V1. All offsets are well within the 2-second crossfade window.

### Drift Cycles

Because the speed ratios are near 1.0 (within ±3%), the voices drift slowly. A pair with relative speed difference Δ drifts through a full in-phase/out-of-phase cycle in:

| Pair | Speed difference | Drift period |
|---|---|---|
| V1 vs V2 (/V3) | 1.0% | 111.6 cycles × 11.16s = **18.6 min** |
| V1 vs V4 (/V5) | 2.0% | 55.8 cycles × 11.16s = **9.3 min** |
| V1 vs V6 | 3.0% | 37.2 cycles × 11.16s = **6.2 min** |
| V2 vs V3 | 2.0% | **9.3 min** |
| V4 vs V5 | 4.0% | **4.7 min** |
| V6 vs V3/V2 | 4.0% | **4.7 min** |

The pattern never exactly repeats within the 18.6-minute duration.

### Summing and Normalization

All six voices are summed sample-by-sample:

```
mix[t] = Σ voice_v[t] for v = 1..6
```

The peak amplitude is typically ~1.8–2.1 (since 6 voices don't align perfectly). The mix is normalized to `[-1.0, 1.0]`:

```
mix /= max(|mix|)
```

### Seam Crossfade

A **2-second crossfade** is applied at the loop seam (the boundary between cycle 99 and cycle 0) to prevent a click or discontinuity:

```
mix[last 2s]  ← multiply by linear ramp 1.0 → 0.0
mix[first 2s] ← multiply by linear ramp 0.0 → 1.0
```

After the crossfade, the piece can be played as a seamless loop.

### Output

| Property | Value |
|---|---|
| Filename | `reich_phasing_19min.wav` |
| Sample rate | 16000 Hz |
| Channels | Stereo (identical L/R) |
| Bit depth | 32-bit float |
| Duration | 1116.0 seconds (18:36) |
| File size | ~68 MB |

## Reproduction

```powershell
conda activate ifs-audio
cd ifs_audio
python reich_phasing.py
```

This runs `make_reich_phasing()` with `ifs_tile=None`, producing only the 6 speech voices. The script automatically downloads the Rainbow Passage speech via gTTS if the reference file doesn't exist.

To produce a **CD-quality FLAC** version (44.1 kHz, 16-bit, with metadata):

```powershell
python dist.py
```

This generates `output/Reich_Phasing_Rainbow_Passage.flac`.

## Dependencies

- Python 3.11
- librosa (phase vocoder time-stretching)
- numpy, soundfile
- gTTS (speech generation)
- ffmpeg (FLAC conversion)

See `environment.yml` for the full conda environment.

## References

- Steve Reich, *It's Gonna Rain* (1965) — tape phasing with a preacher's sermon
- Steve Reich, *Piano Phase* (1967) — two pianists at slightly different tempi
- Orbital, *Time Becomes* — electronic phasing inspiration
