"""Morton (Z-order) addressing and octree hierarchy for WHFF."""

import numpy as np

from whff.spec import RESOLUTION, LOG2_RES, MAX_DEPTH


def _split_bits(x: int) -> int:
    """Spread lower 10 bits of x across 32 bits (for Morton code)."""
    x &= 0x3FF
    x = (x | x << 16) & 0x030000FF
    x = (x | x << 8) & 0x0300F00F
    x = (x | x << 4) & 0x030C30C3
    x = (x | x << 2) & 0x09249249
    return x


def _compact_bits(x: int) -> int:
    """Reverse of _split_bits: extract 10 bits from 32-bit Morton."""
    x &= 0x09249249
    x = (x | x >> 2) & 0x030C30C3
    x = (x | x >> 4) & 0x0300F00F
    x = (x | x >> 8) & 0x030000FF
    x = (x | x >> 16) & 0x3FF
    return x


def morton_encode(x: int, y: int, z: int) -> int:
    """Encode (x, y, z) into a 30-bit Morton (Z-order) code."""
    return _split_bits(x) | (_split_bits(y) << 1) | (_split_bits(z) << 2)


def morton_decode(code: int) -> tuple[int, int, int]:
    """Decode a 30-bit Morton code back to (x, y, z) coordinates."""
    x = _compact_bits(code)
    y = _compact_bits(code >> 1)
    z = _compact_bits(code >> 2)
    return x, y, z


def parent_morton(code: int, depth: int) -> int:
    """Compute parent Morton code at a given depth.

    depth 0 = root (single code 0)
    depth up to MAX_DEPTH
    """
    shift = (MAX_DEPTH - depth) * 3
    return code >> shift


def child_morton(code: int, depth: int, child_idx: int) -> int:
    """Compute child Morton code for a given octant (0-7)."""
    shift = (MAX_DEPTH - depth - 1) * 3
    return (code << 3) | (child_idx << shift)


def coordinate_to_morton(x: int, y: int, z: int) -> int:
    """Convert (x, y, z) voxel coordinate to full-depth Morton code."""
    return morton_encode(x & (RESOLUTION - 1),
                         y & (RESOLUTION - 1),
                         z & (RESOLUTION - 1))


def morton_to_coordinate(code: int) -> tuple[int, int, int]:
    """Convert full-depth Morton code back to (x, y, z)."""
    return morton_decode(code)


def grid_to_mortons(grid: np.ndarray) -> dict[int, int]:
    """Convert a 3D voxel grid to a (morton -> value) dictionary.

    Only non-empty voxels are included for sparse encoding.
    """
    result: dict[int, int] = {}
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            for z in range(grid.shape[2]):
                val = int(grid[x, y, z])
                if val:
                    code = coordinate_to_morton(x, y, z)
                    result[code] = val
    return result


def morton_to_grid(mortons: dict[int, int],
                   shape: tuple[int, int, int] | None = None) -> np.ndarray:
    """Convert a (morton -> value) dictionary back to a 3D grid."""
    if shape is None:
        max_code = max(mortons.keys(), default=0)
        coord = morton_to_coordinate(max_code)
        shape = (coord[0] + 1, coord[1] + 1, coord[2] + 1)
    grid = np.zeros(shape, dtype=np.uint8)
    for code, val in mortons.items():
        x, y, z = morton_to_coordinate(code)
        if x < shape[0] and y < shape[1] and z < shape[2]:
            grid[x, y, z] = val
    return grid
