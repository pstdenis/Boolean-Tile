import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import librosa
import os

OPTION_LABELS = [
    "Original",
    "A — IFS Resynth",
    "B — 4^k Filter Bank",
    "B — Walsh φ Filter Bank",
    "C — Vocoder",
]

SHEPARD_LABELS = [
    "Original",
    "Shepard Canon",
    "Shepard Zoom Sweep",
    "Pure Glissando",
]


def plot_spectrogram(ax, audio, sr, title, max_freq=4000):
    ax.set_title(title, fontsize=9, pad=1)
    D = librosa.amplitude_to_db(
        np.abs(librosa.stft(audio, n_fft=2048, hop_length=512)),
        ref=np.max,
        top_db=80,
    )
    img = librosa.display.specshow(
        D, sr=sr, hop_length=512, x_axis="time", y_axis="hz",
        ax=ax, fmax=max_freq, cmap="magma"
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(labelsize=7)
    return img


def make_comparison_grid(audio_dict: dict, sr: int, tile_name: str,
                         output_dir: str, max_freq: int = 4000):
    keys = [k for k in OPTION_LABELS if k in audio_dict]
    n = len(keys)
    if n == 0:
        return

    fig, axes = plt.subplots(n, 1, figsize=(10, 1.5 * n + 0.5),
                             sharex=True)
    if n == 1:
        axes = [axes]

    for ax, key in zip(axes, keys):
        plot_spectrogram(ax, audio_dict[key], sr, key, max_freq)

    fig.suptitle(f"Tile: {tile_name}", fontsize=12, y=1.01)
    fig.supxlabel("Time (s)", fontsize=9)
    fig.supylabel("Frequency (Hz)", fontsize=9)
    plt.tight_layout()

    path = os.path.join(output_dir, f"{tile_name}_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def make_full_grid(all_audio: dict, sr: int, tiles: list,
                   output_dir: str, max_freq: int = 4000):
    """Create one large grid: rows=tiles, cols=options."""
    n_tiles = len(tiles)
    n_opts = len(OPTION_LABELS)

    fig, axes = plt.subplots(n_tiles, n_opts, figsize=(3 * n_opts + 1,
                                                        1.5 * n_tiles + 1),
                              sharex=True, sharey=True)

    for row_idx, tile_name in enumerate(tiles):
        for col_idx, opt_label in enumerate(OPTION_LABELS):
            ax = axes[row_idx, col_idx]
            key = f"{tile_name}_{opt_label}"
            if key in all_audio:
                plot_spectrogram(ax, all_audio[key], sr, "", max_freq)
            else:
                ax.text(0.5, 0.5, "N/A", ha="center", va="center",
                        transform=ax.transAxes, fontsize=7)
                ax.set_facecolor("0.95")

            if row_idx == 0:
                ax.set_title(opt_label, fontsize=8, pad=1)
            if col_idx == 0:
                ax.set_ylabel(tile_name, fontsize=8, fontweight="bold")

    fig.supxlabel("Time (s)", fontsize=9)
    fig.supylabel("Tile", fontsize=9)
    plt.tight_layout()

    path = os.path.join(output_dir, "full_comparison_grid.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def make_shepard_grid(audio_dict: dict, sr: int, tiles: list,
                      output_dir: str, max_freq: int = 4000):
    """Shepard-specific grid: rows=tiles, cols=canon/zoom/pure."""
    n_tiles = len(tiles)
    n_opts = len(SHEPARD_LABELS)

    fig, axes = plt.subplots(n_tiles, n_opts, figsize=(3 * n_opts + 1,
                                                        1.5 * n_tiles + 1),
                              sharex=True, sharey=True)

    for row_idx, tile_name in enumerate(tiles):
        for col_idx, opt_label in enumerate(SHEPARD_LABELS):
            ax = axes[row_idx, col_idx]
            key = f"{tile_name}_{opt_label}"
            if key in audio_dict:
                plot_spectrogram(ax, audio_dict[key], sr, "", max_freq)
            else:
                ax.text(0.5, 0.5, "N/A", ha="center", va="center",
                        transform=ax.transAxes, fontsize=7)
                ax.set_facecolor("0.95")

            if row_idx == 0:
                ax.set_title(opt_label, fontsize=8, pad=1)
            if col_idx == 0:
                ax.set_ylabel(tile_name, fontsize=8, fontweight="bold")

    fig.supxlabel("Time (s)", fontsize=9)
    fig.supylabel("Tile", fontsize=9)
    plt.tight_layout()

    path = os.path.join(output_dir, "shepard_comparison_grid.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
