"""WHFF decoder: header parsing and tile-native (mode 0) decoding."""

import numpy as np

from whff.spec import (MAGIC, HEADER_SIZE, MODE_TILE_NATIVE,
                       MODE_WALSH_SPECTRAL, TRUTH_TABLES,
                       WHFFHeader)
from whff.bitstream import BitReader


# Precomputed (16, 4) array: tile_values[idx] = (v00, v01, v10, v11)
_TILE_VALUES = np.array([TRUTH_TABLES[i] for i in range(16)], dtype=np.uint8)


def _decode_tile_mode(payload: bytes, resolution: int) -> np.ndarray:
    """Decode tile-native payload into a voxel grid (fully vectorized)."""
    reader = BitReader(payload)
    h = resolution // 2
    n_blocks = h * h * resolution
    tile_ids = np.array([reader.read_bits(4) for _ in range(n_blocks)],
                        dtype=np.uint8)
    values = _TILE_VALUES[tile_ids]  # (n_blocks, 4)

    # Reshape to (res, h, h, 4)
    vals = values.reshape(resolution, h, h, 4)

    grid = np.zeros((resolution,) * 3, dtype=np.uint8)
    # Vectorized placement using strided slicing
    # vals[z, by, bx, k] -> grid position per k
    # transpose (z, by, bx) -> (bx, by, z) to match grid striding
    for k, (xs, ys) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
        grid[xs::2, ys::2, :] = vals[..., k].transpose(2, 1, 0)

    return grid


def decode(data: bytes) -> np.ndarray:
    """Decode a WHFF byte stream back into a voxel grid.

    Args:
        data: Complete WHFF file bytes (header + crc + payload).

    Returns:
        3D numpy array of shape (resolution,) * 3 with uint8 values.
    """
    if len(data) < HEADER_SIZE:
        msg = f"Data too short: {len(data)} bytes"
        raise ValueError(msg)

    header = WHFFHeader.from_bytes(data[:HEADER_SIZE])
    if header.magic != MAGIC:
        msg = f"Invalid magic: {header.magic:#x}"
        raise ValueError(msg)

    expected_crc = int.from_bytes(data[HEADER_SIZE:HEADER_SIZE + 4], 'little')
    actual_crc = header.crc32()
    if actual_crc != expected_crc:
        msg = f"CRC mismatch: {actual_crc:#x} != {expected_crc:#x}"
        raise ValueError(msg)

    payload_offset = HEADER_SIZE + 4
    payload = data[payload_offset:payload_offset + header.payload_size]

    if header.mode == MODE_TILE_NATIVE:
        return _decode_tile_mode(payload, header.resolution)
    elif header.mode == MODE_WALSH_SPECTRAL:
        msg = "Walsh-spectral mode not yet implemented"
        raise NotImplementedError(msg)
    else:
        msg = f"Unknown mode: {header.mode}"
        raise ValueError(msg)
