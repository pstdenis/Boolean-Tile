"""Spatial projection: IFS attractor from tile stream → voxel grid."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from whff.algebra import Tile, from_block


def tile_stream_to_grid(
    tiles: Sequence[Tile],
    resolution: int,
) -> np.ndarray:
    """Build a 3D voxel grid from a tile sequence.

    The tile stream enumerates each 2×2 slab in depth-first Morton
    order: z-loop outermost, then y-block, then x-block.

    Args:
        tiles: Sequence of length (resolution/2)^3.
        resolution: Grid size per dimension (must be even).

    Returns:
        3D uint8 array of shape (resolution, resolution, resolution).
    """
    h = resolution // 2
    grid = np.zeros((resolution,) * 3, dtype=np.uint8)
    vals = np.array(
        [t.truth_table for t in tiles], dtype=np.uint8
    ).reshape(resolution, h, h, 4)

    grid[0::2, 0::2, :] = vals[..., 0].transpose(2, 1, 0)
    grid[0::2, 1::2, :] = vals[..., 1].transpose(2, 1, 0)
    grid[1::2, 0::2, :] = vals[..., 2].transpose(2, 1, 0)
    grid[1::2, 1::2, :] = vals[..., 3].transpose(2, 1, 0)
    return grid


def grid_to_tile_stream(grid: np.ndarray) -> list[Tile]:
    """Convert a voxel grid to a tile sequence.

    Args:
        grid: 3D uint8 array with even dimensions.

    Returns:
        List of Tile instances.
    """
    res = grid.shape[0]
    h = res // 2
    g2 = grid.astype(np.uint8).reshape(h, 2, h, 2, res)

    b00 = g2[:, 0, :, 0, :]
    b01 = g2[:, 0, :, 1, :]
    b10 = g2[:, 1, :, 0, :]
    b11 = g2[:, 1, :, 1, :]

    # Flatten in (z, by, bx) order
    n_blocks = h * h * res
    flat_order = np.ascontiguousarray(
        np.stack([b00, b01, b10, b11], axis=-1).transpose(2, 1, 0, 3)
    ).reshape(-1, 4)

    tiles = []
    for i in range(n_blocks):
        tiles.append(from_block(flat_order[i]))
    return tiles
