"""Tests for the WHFF tiles module."""

import numpy as np
import pytest

from whff.spec import TRUTH_TABLES, N_TILES
from whff.tiles import (tile_to_array, project_tile, walsh_transform,
                        walsh_coefficients, bloch_vector, bures_distance,
                        tile_bloch_coords)


def test_tile_to_array_shape():
    for i in range(N_TILES):
        arr = tile_to_array(i)
        assert arr.shape == (2, 2)
        assert arr.dtype == np.uint8


def test_tile_to_array_values():
    for i in range(N_TILES):
        arr = tile_to_array(i)
        assert arr.flat[0] == TRUTH_TABLES[i][0]
        assert arr.flat[1] == TRUTH_TABLES[i][1]
        assert arr.flat[2] == TRUTH_TABLES[i][2]
        assert arr.flat[3] == TRUTH_TABLES[i][3]


def test_project_tile_roundtrip():
    for i in range(N_TILES):
        arr = tile_to_array(i)
        idx = project_tile(arr)
        assert idx == i, f"Failed for tile {i}: got {idx}"


def test_project_tile_invalid():
    block = np.array([[2, 0], [0, 0]], dtype=np.uint8)
    with pytest.raises(ValueError):
        project_tile(block)


def test_walsh_transform_all_zeros():
    block = np.zeros((2, 2), dtype=np.uint8)
    coeffs = walsh_transform(block)
    np.testing.assert_array_equal(coeffs, np.zeros((2, 2)))


def test_walsh_transform_all_ones():
    block = np.ones((2, 2), dtype=np.uint8)
    coeffs = walsh_transform(block)
    expected = np.array([[4, 0], [0, 0]])
    np.testing.assert_array_equal(coeffs, expected)


def test_walsh_transform_checkerboard():
    block = np.array([[1, 0], [0, 1]], dtype=np.uint8)
    coeffs = walsh_transform(block)
    expected = np.array([[2, 0], [0, 2]])
    np.testing.assert_array_equal(coeffs, expected)


def test_walsh_coefficients_length():
    for i in range(N_TILES):
        block = tile_to_array(i)
        coeffs = walsh_coefficients(block)
        assert len(coeffs) == 4


def test_bloch_vector_length():
    for i in range(N_TILES):
        v = bloch_vector(i)
        assert len(v) == 3


def test_bloch_vector_all_zeros():
    # Tile 0: all zeros -> a=0 -> (0,0,0)
    v = bloch_vector(0)
    np.testing.assert_array_equal(v, [0, 0, 0])


def test_bloch_vector_all_ones():
    # Tile 15: all ones -> a=4, x=y=z=0 -> (0,0,0)
    v = bloch_vector(15)
    np.testing.assert_array_equal(v, [0, 0, 0])


def test_bures_distance_range():
    for i in range(N_TILES):
        for j in range(N_TILES):
            d = bures_distance(i, j)
            assert 0.0 <= d <= 2.0 + 1e-10


def test_bures_distance_self():
    for i in range(N_TILES):
        d = bures_distance(i, i)
        assert d == pytest.approx(0.0, abs=1e-10)


def test_bures_distance_tiles_0_15():
    # Both zero vectors, distance should be 0
    d = bures_distance(0, 15)
    assert d == pytest.approx(0.0, abs=1e-10)


def test_tile_bloch_coords():
    for i in range(N_TILES):
        coords = tile_bloch_coords(i)
        assert len(coords) == 3
        assert all(isinstance(c, float) for c in coords)
