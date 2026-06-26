"""Integration tests for WHFF encoder/decoder round-trip."""

import numpy as np
import pytest

from whff.spec import MAGIC, VERSION, MODE_TILE_NATIVE, WHFFHeader
from whff.encoder import encode
from whff.decoder import decode


def _make_test_grid(res: int = 8) -> np.ndarray:
    """Create a test grid with known patterns."""
    grid = np.zeros((res,) * 3, dtype=np.uint8)
    for x in range(0, min(8, res), 2):
        for y in range(0, min(8, res), 2):
            tile_idx = (x // 2) * 4 + (y // 2)
            bits = [
                (tile_idx >> 3) & 1,
                (tile_idx >> 2) & 1,
                (tile_idx >> 1) & 1,
                tile_idx & 1,
            ]
            grid[x, y, 0] = bits[0]          # v00 (x even, y even)
            grid[x, y + 1, 0] = bits[1]       # v01 (x even, y odd)
            grid[x + 1, y, 0] = bits[2]       # v10 (x odd, y even)
            grid[x + 1, y + 1, 0] = bits[3]   # v11 (x odd, y odd)
    return grid


@pytest.mark.parametrize("size", [2, 4, 8])
def test_encode_decode_known_pattern(size):
    grid = _make_test_grid(size)
    data = encode(grid, mode=MODE_TILE_NATIVE)
    decoded = decode(data)
    np.testing.assert_array_equal(decoded, grid)


@pytest.mark.parametrize("size", [2, 4])
@pytest.mark.parametrize("seed", [0, 1, 42])
def test_encode_decode_random(size, seed):
    rng = np.random.default_rng(seed)
    grid = rng.integers(0, 2, size=(size,) * 3, dtype=np.uint8)
    data = encode(grid, mode=MODE_TILE_NATIVE)
    decoded = decode(data)
    np.testing.assert_array_equal(decoded, grid)


def test_encode_decode_all_zeros():
    grid = np.zeros((4, 4, 4), dtype=np.uint8)
    data = encode(grid, mode=MODE_TILE_NATIVE)
    decoded = decode(data)
    np.testing.assert_array_equal(decoded, grid)


def test_encode_decode_all_ones():
    grid = np.ones((4, 4, 4), dtype=np.uint8)
    data = encode(grid, mode=MODE_TILE_NATIVE)
    decoded = decode(data)
    np.testing.assert_array_equal(decoded, grid)


def test_encode_decode_checkerboard():
    grid = np.zeros((4, 4, 4), dtype=np.uint8)
    grid[::2, ::2, :] = 1
    grid[1::2, 1::2, :] = 1
    data = encode(grid, mode=MODE_TILE_NATIVE)
    decoded = decode(data)
    np.testing.assert_array_equal(decoded, grid)


def test_header_in_output():
    grid = np.zeros((4, 4, 4), dtype=np.uint8)
    data = encode(grid, mode=MODE_TILE_NATIVE)
    header = WHFFHeader.from_bytes(data[:64])
    assert header.magic == MAGIC
    assert header.version == VERSION
    assert header.mode == MODE_TILE_NATIVE
    assert header.resolution == 4


def test_invalid_grid_shape():
    grid = np.zeros((3, 4, 4), dtype=np.uint8)
    with pytest.raises(ValueError):
        encode(grid)


def test_invalid_mode():
    grid = np.zeros((4, 4, 4), dtype=np.uint8)
    with pytest.raises(ValueError):
        encode(grid, mode=99)


def test_spectral_mode_not_implemented():
    grid = np.zeros((4, 4, 4), dtype=np.uint8)
    with pytest.raises(NotImplementedError):
        encode(grid, mode=1)
