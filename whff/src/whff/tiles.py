"""Walsh tile operations: coefficient extraction, Bloch vectors, Bures distance."""

import numpy as np

from whff.spec import TRUTH_TABLES, N_TILES, TILE_NAMES, WALSH_BASIS


def tile_to_array(tile_idx: int) -> np.ndarray:
    """Return the 2x2 Boolean matrix for a given tile index (0-15)."""
    bits = TRUTH_TABLES[tile_idx]
    return np.array(bits, dtype=np.uint8).reshape(2, 2)


# Precomputed 4D lookup: tile_lookup[v00][v01][v10][v11] -> tile index (0-15)
# This makes tile projection O(1) via simple array indexing.
_LOOKUP = np.full((2, 2, 2, 2), 255, dtype=np.uint8)
for idx in range(N_TILES):
    bits = TRUTH_TABLES[idx]
    _LOOKUP[bits[0], bits[1], bits[2], bits[3]] = idx


def project_tile(block: np.ndarray | tuple) -> int:
    """Given a 2x2 Boolean block, return the best-matching tile index (0-15).

    Uses a precomputed 4D lookup table for O(1) projection.
    """
    if isinstance(block, np.ndarray):
        b = block.ravel()
    else:
        b = block
    v0, v1, v2, v3 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
    if v0 > 1 or v1 > 1 or v2 > 1 or v3 > 1:
        msg = f"No matching tile for block: ({v0},{v1},{v2},{v3})"
        raise ValueError(msg)
    idx = _LOOKUP[v0, v1, v2, v3]
    if idx == 255:
        msg = f"No matching tile for block: ({v0},{v1},{v2},{v3})"
        raise ValueError(msg)
    return int(idx)


def walsh_transform(block: np.ndarray) -> np.ndarray:
    """Compute 2x2 Walsh-Hadamard transform coefficients.

    Uses H2 (the 2x2 Hadamard matrix): [[1,1],[1,-1]].
    Returns 2x2 coefficient array.
    """
    return WALSH_BASIS @ block.astype(np.int8) @ WALSH_BASIS.T


def walsh_coefficients(block: np.ndarray) -> np.ndarray:
    """Return flat array of 4 Walsh coefficients for a 2x2 block."""
    return walsh_transform(block).flatten()


def bloch_vector(tile_idx: int) -> np.ndarray:
    """Compute the 3D Bloch vector for a tile.

    Maps the 4 Walsh coefficients (a, x, y, z) to a 3D point on/inside
    the unit sphere: (x/a, y/a, z/a) for a != 0, else (0,0,0).
    """
    block = tile_to_array(tile_idx)
    coeffs = walsh_coefficients(block)
    a, x, y, z = coeffs
    if a == 0:
        return np.zeros(3, dtype=np.float64)
    return np.array([x / a, y / a, z / a], dtype=np.float64)


def bures_distance(tile_a: int, tile_b: int) -> float:
    """Bures distance between two tiles using their Bloch vectors.

    General formula for single-qubit states:
    d_B = sqrt(2 - 2 * sqrt((1 + r·s + sqrt((1 - |r|^2)(1 - |s|^2))) / 2))
    """
    u = bloch_vector(tile_a)
    v = bloch_vector(tile_b)
    dot = np.clip(np.dot(u, v), -1.0, 1.0)
    nu2 = np.clip(1.0 - np.dot(u, u), 0.0, 1.0)
    nv2 = np.clip(1.0 - np.dot(v, v), 0.0, 1.0)
    sqrt_fidelity = np.sqrt((1.0 + dot + np.sqrt(nu2 * nv2)) / 2.0)
    return float(np.sqrt(2.0 - 2.0 * sqrt_fidelity))


TILE_COLOR_MAP: dict[int, str] = {
    0: "#000000",   # tile 0: all zeros
    1: "#0000FF",   # tile 1
    2: "#00FF00",   # tile 2
    3: "#00FFFF",   # tile 3
    4: "#FF0000",   # tile 4
    5: "#FF00FF",   # tile 5
    6: "#FFFF00",   # tile 6
    7: "#FFFFFF",   # tile 7: all ones
    8: "#888888",   # tile 8
    9: "#AA0000",   # tile 9
    10: "#00AA00",  # tile 10
    11: "#0000AA",  # tile 11
    12: "#AAAA00",  # tile 12
    13: "#00AAAA",  # tile 13
    14: "#AA00AA",  # tile 14
    15: "#888888",  # tile 15
}


def tile_color(tile_idx: int) -> str:
    """Return hex color string for tile visualization."""
    return TILE_COLOR_MAP.get(tile_idx, "#000000")


def tile_bloch_coords(tile_idx: int) -> tuple[float, float, float]:
    """Return (x, y, z) Bloch coordinates for a tile."""
    v = bloch_vector(tile_idx)
    return (float(v[0]), float(v[1]), float(v[2]))
