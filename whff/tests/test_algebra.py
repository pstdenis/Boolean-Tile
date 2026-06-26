"""Tests for canonical 16-tile algebra (whff.algebra)."""

from __future__ import annotations

import numpy as np
import pytest

from whff.algebra import (ALL, Tile, from_block, from_index, bures_matrix,
                          summary_table, ising_table)


class TestConstants:
    def test_sixteen_tiles(self) -> None:
        assert len(ALL) == 16

    def test_all_tile_indices(self) -> None:
        for i, t in enumerate(ALL):
            assert t.index == i

    def test_from_block_roundtrip(self) -> None:
        for t in ALL:
            block = t.truth_table
            t2 = from_block(block)
            assert t.index == t2.index

    def test_from_index(self) -> None:
        for i in range(16):
            t = from_index(i)
            assert t.index == i
            assert t.name == ALL[i].name

    def test_tile_names_unique(self) -> None:
        names = [t.name for t in ALL]
        assert len(names) == len(set(names))


class TestWalsh:
    def test_coeffs_shape(self) -> None:
        for t in ALL:
            assert len(t.walsh_coeffs) == 4

    def test_walsh_dc_range(self) -> None:
        for t in ALL:
            a = t.walsh_coeffs[0]
            assert 0 <= a <= 4

    def test_walsh_signature_false_true(self) -> None:
        assert ALL[0].walsh_coeffs == (0, 0, 0, 0)
        assert ALL[15].walsh_coeffs == (4, 0, 0, 0)

    def test_walsh_xor_xnor(self) -> None:
        assert ALL[6].walsh_coeffs == (2, 0, 0, -2)
        assert ALL[9].walsh_coeffs == (2, 0, 0, 2)

    def test_walsh_shortcuts(self) -> None:
        """dc, r0, r1, r0r1 properties should match walsh_coeffs."""
        for t in ALL:
            a, x, y, z = t.walsh_coeffs
            assert t.dc == a
            assert t.r0 == x
            assert t.r1 == y
            assert t.r0r1 == z

    def test_gate_classification(self) -> None:
        assert ALL[7].gate_class == "entangling"
        assert ALL[6].mv_class == "entangled"


class TestBloch:
    def test_bloch_vector_length(self) -> None:
        for t in ALL:
            r = t.bloch_vector
            norm_sq = r[0]**2 + r[1]**2 + r[2]**2
            assert 0 <= norm_sq <= 1.0 + 1e-12

    def test_bloch_purity(self) -> None:
        for t in ALL:
            assert 0.0 <= t.purity <= 1.0 + 1e-12

    def test_purity_zero(self) -> None:
        assert ALL[0].purity == pytest.approx(0.0)
        assert ALL[15].purity == pytest.approx(0.0)

    def test_pure_product_tiles(self) -> None:
        for i in [3, 5, 10, 12]:
            assert ALL[i].purity == pytest.approx(1.0)

    def test_pure_entangled_tiles(self) -> None:
        assert ALL[6].purity == pytest.approx(1.0)
        assert ALL[9].purity == pytest.approx(1.0)

    def test_pure_onebit_tiles(self) -> None:
        for i in [1, 2, 4, 8]:
            assert ALL[i].purity == pytest.approx(1.0)

    def test_mixed_tiles(self) -> None:
        for i in [7, 11, 13, 14]:
            assert ALL[i].purity == pytest.approx(1/3, abs=1e-12)


class TestIsing:
    def test_ising_length(self) -> None:
        for t in ALL:
            assert len(t.ising_params) == 3

    def test_product_j_zero(self) -> None:
        for i in [0, 3, 5, 10, 12, 15]:
            assert ALL[i].ising_params[0] == pytest.approx(0.0)

    def test_entangling_j_nonzero(self) -> None:
        for i in range(16):
            if ALL[i].gate_class == "entangling":
                assert abs(ALL[i].ising_params[0]) > 0.0

    def test_xor_xnor_ising(self) -> None:
        # XOR: z=-2, J = -2 * pi/8 = -pi/4
        assert ALL[6].ising_params[0] == pytest.approx(-np.pi / 4)
        # XNOR: z=2, J = 2 * pi/8 = pi/4
        assert ALL[9].ising_params[0] == pytest.approx(np.pi / 4)

    def test_ising_shortcuts(self) -> None:
        """J, h1, h2 should match ising_params."""
        for t in ALL:
            J, h1, h2 = t.ising_params
            assert t.J == pytest.approx(J)
            assert t.h1 == pytest.approx(h1)
            assert t.h2 == pytest.approx(h2)


class TestBures:
    def test_matrix_shape(self) -> None:
        m = bures_matrix()
        assert m.shape == (16, 16)

    def test_matrix_symmetric(self) -> None:
        m = bures_matrix()
        assert np.allclose(m, m.T)

    def test_self_distance_zero(self) -> None:
        m = bures_matrix()
        for i in range(16):
            assert m[i, i] == pytest.approx(0.0)

    def test_distance_range(self) -> None:
        m = bures_matrix()
        for i in range(16):
            for j in range(16):
                assert 0 <= m[i, j] <= np.sqrt(2) + 1e-12

    def test_tile_distance_via_method(self) -> None:
        d = ALL[0].distance(ALL[6])
        m = bures_matrix()
        assert d == pytest.approx(m[0, 6])

    def test_xor_xnor_distance(self) -> None:
        """XOR and XNOR have opposite Walsh z-coefficients."""
        d = ALL[6].distance(ALL[9])
        assert d > 0.0

    def test_and_or_distance(self) -> None:
        d = ALL[1].distance(ALL[7])
        assert d > 0.0


class TestAlgebraic:
    def test_negate(self) -> None:
        for t in ALL:
            neg = t.negate()
            assert neg.index == 15 - t.index

    def test_dual(self) -> None:
        for t in ALL:
            d = t.dual()
            assert d.index == 15 - t.index

    def test_negate_equals_dual(self) -> None:
        for t in ALL:
            assert t.negate().index == t.dual().index

    def test_negate_twice_is_self(self) -> None:
        for t in ALL:
            assert t.negate().negate().index == t.index

    def test_walsh_weight_zero(self) -> None:
        assert ALL[0].walsh_weight() == pytest.approx(0.0)
        assert ALL[15].walsh_weight() == pytest.approx(0.0)

    def test_walsh_weight_xor(self) -> None:
        # XOR: walsh = (2, 0, 0, -2), weight = sqrt(0+0+4) = 2
        assert ALL[6].walsh_weight() == pytest.approx(2.0)

    def test_walsh_weight_and(self) -> None:
        # AND: walsh = (1, -1, -1, 1), weight = sqrt(1+1+1) = sqrt(3)
        assert ALL[1].walsh_weight() == pytest.approx(np.sqrt(3))

    def test_is_entangling(self) -> None:
        for i in range(16):
            t = ALL[i]
            if t.gate_class == "entangling":
                assert t.is_entangling is True
            else:
                assert t.is_entangling is False

    def test_is_literal(self) -> None:
        assert ALL[0].is_literal is True
        assert ALL[15].is_literal is True
        assert ALL[6].is_literal is False


class TestTables:
    def test_summary_table_length(self) -> None:
        lines = summary_table().split("\n")
        assert len(lines) == 18  # header + sep + 16 data lines

    def test_ising_table_length(self) -> None:
        lines = ising_table().split("\n")
        assert len(lines) == 18
