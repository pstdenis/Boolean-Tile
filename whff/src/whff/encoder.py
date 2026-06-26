"""WHFF encoder: tile-native (mode 0) and Walsh-spectral (mode 1, reserved)."""

import numpy as np

from whff.spec import (MAGIC, VERSION, HEADER_SIZE, MODE_TILE_NATIVE,
                       MODE_WALSH_SPECTRAL, WHFFHeader)
from whff.bitstream import BitWriter
from whff.tiles import _LOOKUP


def encode(grid: np.ndarray, mode: int = MODE_TILE_NATIVE) -> bytes:
    """Encode a voxel grid into WHFF format.

    Args:
        grid: 3D numpy array with uint8 values, each dimension even.
        mode: 0 for tile-native, 1 for Walsh-spectral (reserved).

    Returns:
        Complete WHFF file as bytes (header + payload).
    """
    if len(grid.shape) != 3:
        msg = f"Grid must be 3D, got shape {grid.shape}"
        raise ValueError(msg)
    for d in grid.shape:
        if d % 2 != 0:
            msg = f"All dimensions must be even, got shape {grid.shape}"
            raise ValueError(msg)

    if mode == MODE_TILE_NATIVE:
        payload = _encode_tile_mode(grid)
    elif mode == MODE_WALSH_SPECTRAL:
        msg = "Walsh-spectral mode not yet implemented"
        raise NotImplementedError(msg)
    else:
        msg = f"Unknown mode: {mode}"
        raise ValueError(msg)

    res = grid.shape[0]
    depth = int(np.log2(res)) if res > 0 else 0
    header = WHFFHeader(
        magic=MAGIC,
        version=VERSION,
        mode=mode,
        resolution=res,
        depth=depth,
        payload_size=len(payload),
    )
    header_bytes = header.to_bytes()
    crc = header.crc32()
    return header_bytes + crc.to_bytes(4, 'little') + payload


def _encode_tile_mode(grid: np.ndarray) -> bytes:
    """Encode grid in tile-native mode using vectorized numpy operations."""
    g = np.asarray(grid, dtype=np.uint8)
    res = g.shape[0]
    h = res // 2

    # Reshape: (h, 2, h, 2, res) -> extract 4 sub-voxels per 2x2 block
    g2 = g.reshape(h, 2, h, 2, res)
    b00 = g2[:, 0, :, 0, :]  # (h, h, res)
    b01 = g2[:, 0, :, 1, :]
    b10 = g2[:, 1, :, 0, :]
    b11 = g2[:, 1, :, 1, :]

    # O(1) lookup per block via 4D array indexing
    tile_ids = _LOOKUP[b00, b01, b10, b11]  # (h, h, res)

    # Flatten in (z, y_block, x_block) order for bitstream
    flat_ids = np.ascontiguousarray(tile_ids.transpose(2, 1, 0)).ravel()

    writer = BitWriter()
    for idx in flat_ids:
        writer.write_bits(int(idx), 4)
    return writer.to_bytes()
