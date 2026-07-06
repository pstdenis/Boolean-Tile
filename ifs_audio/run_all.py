#!/usr/bin/env python3
"""
IFS Audio Comparison — run all 3 options × 6 tiles on a reference speech clip.

Usage:
    python run_all.py [--sr SAMPLE_RATE] [--depth DEPTH] [--octaves OCTAVES]

Output:
    output/
    ├── reference_original.wav
    ├── {TileName}_comparison.png   (per-tile spectrograms)
    ├── full_comparison_grid.png    (all tiles × all options)
    └── {TileName}_{OptionLabel}.wav
"""

import os
import sys
import argparse

import numpy as np

# Ensure the script's directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tiles import TILE_SIX, TILE_NAMES
from audio_io import download_speech, load_audio, write_wav
from pitch_extract import extract_pitch
from options import (option_a_resynth, option_b_fb_4k,
                     option_b_fb_walsh, option_c_vocoder,
                     shepard_canon, shepard_zoom_sweep,
                     shepard_pure_glissando)
from compare import (make_comparison_grid, make_full_grid,
                     make_shepard_grid, OPTION_LABELS, SHEPARD_LABELS)
from phasing_glissando import generate_tile_phasing


def main():
    parser = argparse.ArgumentParser(description="IFS Audio Comparison")
    parser.add_argument("--sr", type=int, default=22050,
                        help="Sample rate (default: 22050)")
    parser.add_argument("--depth", type=int, default=6,
                        help="IFS recursion depth (default: 6)")
    parser.add_argument("--octaves", type=int, default=6,
                        help="Number of octaves for Walsh φ variant (default: 6)")
    args = parser.parse_args()

    SR = args.sr
    DEPTH = args.depth
    OCTAVES = args.octaves
    OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(OUTPUT, exist_ok=True)

    print("=" * 60)
    print("IFS Audio Comparison Pipeline")
    print("=" * 60)

    # ---- Step 1: Reference audio ----
    print("\n[1] Reference audio")
    ref_path = download_speech(OUTPUT, "reference_original.wav", sr=SR)
    audio, sr = load_audio(ref_path, sr=SR)
    print(f"    Loaded: {len(audio) / sr:.1f}s, {sr}Hz")

    # ---- Step 2: Pitch track ----
    print("\n[2] Pitch extraction")
    pitch_samples, _ = extract_pitch(audio, sr)

    # ---- Step 3: Process each tile ----
    print("\n[3] Processing tiles")
    all_audio = {}
    all_audio[f"Original_Original"] = audio

    for tile in TILE_SIX:
        name = tile["name"]
        bits = tile["bits"]
        walsh = tile["walsh"]
        print(f"\n  --- {name} ({tile['desc']}) ---")

        # Option A — IFS resynthesis
        out_a = option_a_resynth(audio, sr, pitch_samples, bits, DEPTH)
        key_a = f"{name}_A — IFS Resynth"
        all_audio[key_a] = out_a
        write_wav(os.path.join(OUTPUT, f"{name}_A_resynth.wav"), out_a, sr)

        # Option B — 4^k filter bank
        out_b4k = option_b_fb_4k(audio, sr, pitch_samples, bits, DEPTH)
        key_b4k = f"{name}_B — 4^k Filter Bank"
        all_audio[key_b4k] = out_b4k
        write_wav(os.path.join(OUTPUT, f"{name}_B_fb_4k.wav"), out_b4k, sr)

        # Option B — Walsh φ filter bank
        out_bw = option_b_fb_walsh(audio, sr, pitch_samples, walsh, OCTAVES)
        key_bw = f"{name}_B — Walsh φ Filter Bank"
        all_audio[key_bw] = out_bw
        write_wav(os.path.join(OUTPUT, f"{name}_B_fb_walsh.wav"), out_bw, sr)

        # Option C — Vocoder
        out_c = option_c_vocoder(audio, sr, pitch_samples, bits, walsh, DEPTH)
        key_c = f"{name}_C — Vocoder"
        all_audio[key_c] = out_c
        write_wav(os.path.join(OUTPUT, f"{name}_C_vocoder.wav"), out_c, sr)

        # Per-tile comparison spectrogram
        tile_dict = {
            "Original": audio,
            f"A — IFS Resynth": out_a,
            f"B — 4^k Filter Bank": out_b4k,
            f"B — Walsh φ Filter Bank": out_bw,
            f"C — Vocoder": out_c,
        }
        make_comparison_grid(tile_dict, sr, name, OUTPUT)

    # ---- Step 4: Shepard canon ----
    print("\n[4] Shepard variants (ascending staircase)")
    shepard_audio = {}
    for tile in TILE_SIX:
        shepard_audio[f"{tile['name']}_Original"] = audio

    for tile in TILE_SIX:
        name = tile["name"]
        bits = tile["bits"]
        walsh = tile["walsh"]
        print(f"\n  --- {name} ---")

        # Shepard canon (staggered voices)
        out_canon = shepard_canon(audio, sr, pitch_samples, bits,
                                  depth=4, stagger_delay=2.0)
        key_canon = f"{name}_Shepard Canon"
        shepard_audio[key_canon] = out_canon
        write_wav(os.path.join(OUTPUT, f"{name}_shepard_canon.wav"), out_canon, sr)

        # Shepard zoom sweep (continuous fineWeight modulation)
        out_zoom = shepard_zoom_sweep(audio, sr, pitch_samples, bits,
                                      depth=6, sweep_period=4.0)
        key_zoom = f"{name}_Shepard Zoom Sweep"
        shepard_audio[key_zoom] = out_zoom
        write_wav(os.path.join(OUTPUT, f"{name}_shepard_zoom.wav"), out_zoom, sr)

        # Pure glissando (no speech, pure demonstration)
        out_pure, _ = shepard_pure_glissando(
            sr, duration=8.0, tile_bits=bits, depth=4,
            start_freq=110.0, end_freq=220.0, stagger_delay=2.0)
        key_pure = f"{name}_Pure Glissando"
        shepard_audio[key_pure] = out_pure
        write_wav(os.path.join(OUTPUT, f"{name}_pure_glissando.wav"), out_pure, sr)

    # Per-tile Shepard comparisons
    print("\n  Per-tile Shepard spectrograms...")
    for tile in TILE_SIX:
        name = tile["name"]
        tile_dict = {"Original": audio}
        for label in SHEPARD_LABELS[1:]:
            key = f"{name}_{label}"
            if key in shepard_audio:
                tile_dict[label] = shepard_audio[key]
        if len(tile_dict) > 1:
            out_labels = ["Original"] + [l for l in SHEPARD_LABELS[1:]
                                         if f"{name}_{l}" in shepard_audio]
            from compare import OPTION_LABELS as _
            # temporarily swap labels
            import compare as cmp
            old_labels = cmp.OPTION_LABELS
            cmp.OPTION_LABELS = out_labels
            make_comparison_grid(tile_dict, sr, f"{name}_shepard", OUTPUT)
            cmp.OPTION_LABELS = old_labels

    # ---- Step 5: Phasing glissando ----
    print("\n[5] Phasing glissando (Reich + Shepard)")
    for tile in TILE_SIX[1:4]:  # A, B, XOR (pure tiles)
        generate_tile_phasing(tile, sr=SR, base_freq=110.0,
                              depth=4, duration=60.0,
                              detune_ratio=0.001,
                              output_dir=OUTPUT)

    # ---- Step 6: Full grids ----
    print("\n[6] Full comparison grids")
    make_full_grid(all_audio, sr, TILE_NAMES, OUTPUT)
    make_shepard_grid(shepard_audio, sr, TILE_NAMES, OUTPUT)

    print("\n" + "=" * 60)
    print("DONE! All outputs in:", OUTPUT)
    print("  + 3 phasing glissando files (A, B, XOR, 60s stereo)")
    print("=" * 60)


if __name__ == "__main__":
    main()
