"""Spectral projection: Shepard frequency ratios from tile Walsh coefficients."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from whff.algebra import Tile


def shepard_spectrum(tiles: Sequence[Tile]) -> np.ndarray:
    """Compute Shepard frequency ratios for each tile in a stream.

    Each tile's Walsh coefficients (a, x, y, z) map to three
    frequency ratios based on the Shepard tone illusion:
      f_DC  = 1.0  (fundamental, from DC component)
      f_x   = a * φ   when x ≠ 0 else 0
      f_y   = a * φ²  when y ≠ 0 else 0
      f_z   = a * φ³  when z ≠ 0 else 0

    where φ = (1 + √5)/2 is the golden ratio, giving maximally
    dissonant ratios (3-semitone Shepard spacing).

    Returns:
        (n_tiles, 4) float array of [f_DC, f_x, f_y, f_z] amplitudes.
    """
    phi = (1 + np.sqrt(5)) / 2
    out = np.zeros((len(tiles), 4), dtype=np.float64)
    for i, t in enumerate(tiles):
        a, x, y, z = t.walsh_coeffs
        out[i, 0] = 1.0
        if x:
            out[i, 1] = a * phi
        if y:
            out[i, 2] = a * phi**2
        if z:
            out[i, 3] = a * phi**3
    return out


def spectral_centroid(spectrum: np.ndarray) -> float:
    """Mean weighted frequency of a Shepard spectrum."""
    freqs = np.array([1.0, 1.618, 2.618, 4.236])
    weights = spectrum.sum(axis=0)
    return float(np.average(freqs, weights=weights)) if weights.sum() > 0 else 0.0
