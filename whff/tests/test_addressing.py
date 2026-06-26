"""Tests for the WHFF addressing module."""

import numpy as np
import pytest
from hypothesis import given, strategies as st

from whff.spec import RESOLUTION
from whff.addressing import (morton_encode, morton_decode,
                             coordinate_to_morton, morton_to_coordinate,
                             grid_to_mortons, morton_to_grid)


def test_morton_encode_decode_roundtrip():
    for x in [0, 1, 2, 3, 100, 255]:
        for y in [0, 1, 2, 3, 100, 255]:
            for z in [0, 1, 2, 3, 100, 255]:
                code = morton_encode(x, y, z)
                rx, ry, rz = morton_decode(code)
                assert (rx, ry, rz) == (x, y, z)


@given(st.integers(min_value=0, max_value=255),
       st.integers(min_value=0, max_value=255),
       st.integers(min_value=0, max_value=255))
def test_morton_property_roundtrip(x, y, z):
    code = morton_encode(x, y, z)
    rx, ry, rz = morton_decode(code)
    assert (rx, ry, rz) == (x, y, z)


@given(st.integers(min_value=0, max_value=255),
       st.integers(min_value=0, max_value=255),
       st.integers(min_value=0, max_value=255))
def test_coordinate_morton_roundtrip(x, y, z):
    code = coordinate_to_morton(x, y, z)
    rx, ry, rz = morton_to_coordinate(code)
    assert (rx, ry, rz) == (x, y, z)


def test_coordinate_morton_clamps():
    code = coordinate_to_morton(256, 256, 256)
    rx, ry, rz = morton_to_coordinate(code)
    # 256 & 255 = 0
    assert (rx, ry, rz) == (0, 0, 0)


def test_grid_to_mortons_empty():
    grid = np.zeros((RESOLUTION, RESOLUTION, RESOLUTION), dtype=np.uint8)
    mortons = grid_to_mortons(grid)
    assert len(mortons) == 0


def test_grid_to_mortons_single():
    grid = np.zeros((RESOLUTION, RESOLUTION, RESOLUTION), dtype=np.uint8)
    grid[42, 17, 99] = 1
    mortons = grid_to_mortons(grid)
    assert len(mortons) == 1
    code = coordinate_to_morton(42, 17, 99)
    assert mortons[code] == 1


def test_morton_to_grid_roundtrip():
    grid = np.zeros((16, 16, 16), dtype=np.uint8)
    grid[5, 7, 3] = 1
    grid[1, 2, 4] = 2
    grid[15, 15, 15] = 1
    mortons = grid_to_mortons(grid)
    restored = morton_to_grid(mortons, shape=(16, 16, 16))
    np.testing.assert_array_equal(restored, grid)
