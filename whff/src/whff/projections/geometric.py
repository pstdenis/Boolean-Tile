"""Geometric projection: Bloch sphere, Ising, and Bures geometry from tile algebra."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from whff.algebra import Tile, bures_matrix


def block_bloch_vectors(tiles: Sequence[Tile]) -> np.ndarray:
    """Extract Bloch vectors from a tile stream as an (N, 3) array."""
    return np.array([t.bloch_vector for t in tiles], dtype=np.float64)


def block_purities(tiles: Sequence[Tile]) -> np.ndarray:
    """Extract purities from a tile stream as an (N,) array."""
    return np.array([t.purity for t in tiles], dtype=np.float64)


def block_ising(tiles: Sequence[Tile]) -> np.ndarray:
    """Extract Ising parameters as an (N, 3) array [J, h1, h2]."""
    return np.array([t.ising for t in tiles], dtype=np.float64)


def block_gate_classes(tiles: Sequence[Tile]) -> list[str]:
    """Classify each tile as product or entangling."""
    return [t.gate_class for t in tiles]


def tile_type_counts(tiles: Sequence[Tile]) -> dict[str, int]:
    """Count occurrences of each tile name in a stream."""
    counts: dict[str, int] = {}
    for t in tiles:
        counts[t.name] = counts.get(t.name, 0) + 1
    return counts


def bures_distance_between(tiles_a: Sequence[Tile],
                           tiles_b: Sequence[Tile]) -> float:
    """Mean Bures distance between two equal-length tile streams."""
    matrix = bures_matrix()
    idx_a = np.array([t.index for t in tiles_a], dtype=np.uint8)
    idx_b = np.array([t.index for t in tiles_b], dtype=np.uint8)
    return float(matrix[idx_a, idx_b].mean())
