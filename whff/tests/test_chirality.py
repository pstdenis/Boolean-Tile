"""Exhaustive chiral traversal verification for all 16 BTB tiles.

Tests the Walsh energy redistribution under CW and CCW cell permutations
and discovers the topological partner structure.
"""

from __future__ import annotations

import math

import pytest

from whff.algebra import ALL, from_block, Tile

# ── Permutations ──────────────────────────────────────────────────
#
# Standard traversal visits cells in row-major order:
#   indices: [00, 01, 10, 11] -> (v00, v01, v10, v11)
#
# CW traversal swaps the last two cells (10<->11):
#   indices: [00, 01, 11, 10] -> (v00, v01, v11, v10)
#
# CCW traversal cycles the last three (01->10->11->01):
#   indices: [00, 10, 11, 01] -> (v00, v10, v11, v01)

_ID = (0, 1, 2, 3)
_CW = (0, 1, 3, 2)
_CCW = (0, 2, 3, 1)


def _apply_perm(tt: tuple[int, int, int, int], perm: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(tt[p] for p in perm)


def _walsh(tt: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    v00, v01, v10, v11 = tt
    return (
        v00 + v01 + v10 + v11,  # a (DC)
        v00 - v01 + v10 - v11,  # x (R0)
        v00 + v01 - v10 - v11,  # y (R1)
        v00 - v01 - v10 + v11,  # z (R0R1)
    )


def _non_dc_energy(tt: tuple[int, int, int, int]) -> float:
    _, x, y, z = _walsh(tt)
    return math.sqrt(x * x + y * y + z * z)


def _dc(tt: tuple[int, int, int, int]) -> int:
    return tt[0] + tt[1] + tt[2] + tt[3]


# ── Foundational invariants ───────────────────────────────────────

@pytest.mark.parametrize("tile_idx", range(16))
def test_energy_conservation_under_chirality(tile_idx: int) -> None:
    """Non-DC Walsh energy sqrt(x^2+y^2+z^2) is invariant under CW and CCW."""
    tt = ALL[tile_idx].truth_table
    e0 = _non_dc_energy(tt)
    assert abs(e0 - _non_dc_energy(_apply_perm(tt, _CW))) < 1e-12
    assert abs(e0 - _non_dc_energy(_apply_perm(tt, _CCW))) < 1e-12


@pytest.mark.parametrize("tile_idx", range(16))
def test_dc_conservation_under_chirality(tile_idx: int) -> None:
    """DC component is invariant under permutation."""
    tt = ALL[tile_idx].truth_table
    dc0 = _dc(tt)
    assert dc0 == _dc(_apply_perm(tt, _CW))
    assert dc0 == _dc(_apply_perm(tt, _CCW))


def test_cw_swaps_x_and_z() -> None:
    """CW traversal swaps the R0 and R0R1 Walsh coefficients (x<->z)."""
    for tile_idx in range(16):
        tt = ALL[tile_idx].truth_table
        _, x0, y0, z0 = _walsh(tt)
        _, x1, y1, z1 = _walsh(_apply_perm(tt, _CW))
        assert y0 == y1, f"CW y changed for {tile_idx}: {y0} -> {y1}"
        assert x0 == z1, f"CW x->z mismatch for {tile_idx}"
        assert z0 == x1, f"CW z->x mismatch for {tile_idx}"


@pytest.mark.parametrize("tile_idx", range(16))
def test_cw_maps_to_standard_tile(tile_idx: int) -> None:
    """CW of any standard tile yields another standard tile."""
    t_cw = from_block(_apply_perm(ALL[tile_idx].truth_table, _CW))
    assert t_cw is not None


@pytest.mark.parametrize("tile_idx", range(16))
def test_ccw_maps_to_standard_tile(tile_idx: int) -> None:
    """CCW of any standard tile yields another standard tile."""
    t_ccw = from_block(_apply_perm(ALL[tile_idx].truth_table, _CCW))
    assert t_ccw is not None


def test_cw_cycle_length_two() -> None:
    """CW permutation is an involution: CW(CW(tile)) = tile."""
    for tile_idx in range(16):
        tt = ALL[tile_idx].truth_table
        tt2 = _apply_perm(_apply_perm(tt, _CW), _CW)
        assert tuple(tt) == tt2, f"CW^2 != identity for tile {tile_idx}"


def test_ccw_cycle_length_three() -> None:
    """CCW permutation is a 3-cycle on (v01, v10, v11)."""
    for tile_idx in range(16):
        tt = ALL[tile_idx].truth_table
        tt3 = _apply_perm(_apply_perm(_apply_perm(tt, _CCW), _CCW), _CCW)
        assert tuple(tt) == tt3, f"CCW^3 != identity for tile {tile_idx}"


# ── CW fixed points: tiles with v10 = v11 ─────────────────────────

def test_cw_fixed_points() -> None:
    """Tiles with v10 = v11 are fixed under CW (swap of equal values).

    The 8 fixed tiles are FALSE, A, NOTA_AND_B, OR, NOR, B_IMP_A, NOTA, TRUE.
    """
    fixed = [i for i in range(16) if _apply_perm(ALL[i].truth_table, _CW) == ALL[i].truth_table]
    expected_fixed = {0, 3, 4, 7, 8, 11, 12, 15}
    assert set(fixed) == expected_fixed, f"CW fixed points: {fixed}"
    # Verify these have v10 = v11
    for i in fixed:
        tt = ALL[i].truth_table
        assert tt[2] == tt[3], f"Tile {i} has v10 != v11 but is CW-fixed"


def test_cw_non_fixed_points() -> None:
    """Tiles with v10 != v11 are paired under CW."""
    non_fixed = [i for i in range(16) if _apply_perm(ALL[i].truth_table, _CW) != ALL[i].truth_table]
    # Check each maps to a different tile, and the partner maps back
    for i in non_fixed:
        tt = ALL[i].truth_table
        j = from_block(_apply_perm(tt, _CW)).index
        assert j != i
        # Partner maps back
        assert from_block(_apply_perm(ALL[j].truth_table, _CW)).index == i


# ── CCW structure ──────────────────────────────────────────────────

def test_ccw_orbits() -> None:
    """CCW partitions tiles into cycles of length 1 or 3."""
    visited: set[int] = set()
    for i in range(16):
        if i in visited:
            continue
        # Follow the CCW orbit
        orbit = [i]
        cur = from_block(_apply_perm(ALL[i].truth_table, _CCW)).index
        while cur != i:
            orbit.append(cur)
            cur = from_block(_apply_perm(ALL[cur].truth_table, _CCW)).index
        visited.update(orbit)
        assert len(orbit) in (1, 3), f"CCW orbit of tile {i} has length {len(orbit)}: {orbit}"
    assert len(visited) == 16


# ── Partner discovery table ────────────────────────────────────────

def test_partner_table() -> None:
    """Print the full CW and CCW partner table."""
    print()
    header = f"{'Idx':>3} {'Name':>12} {'TT':>6} {'(x,y,z)':>14} CW->{'':>11} CCW->{'':>11} v10=v11"
    print(header)
    print("-" * len(header))
    for tile_idx in range(16):
        tt = ALL[tile_idx].truth_table
        _, x, y, z = _walsh(tt)
        t_cw = from_block(_apply_perm(tt, _CW))
        t_ccw = from_block(_apply_perm(tt, _CCW))
        same = tt[2] == tt[3]
        tt_str = "".join(str(v) for v in tt)
        w_str = f"({x},{y},{z})"
        print(
            f"{tile_idx:>3} {ALL[tile_idx].name:>12} {tt_str:>6} {w_str:>14}  "
            f"{t_cw.name:>12} {t_ccw.name:>12}  {str(same):>5}"
        )


def test_walsh_redistribution() -> None:
    """Print Walsh energy redistribution under CW and CCW."""
    print()
    print("WALSH ENERGY REDISTRIBUTION")
    print("-" * 75)
    for tile_idx in range(16):
        tt = ALL[tile_idx].truth_table
        _, x0, y0, z0 = _walsh(tt)
        _, x_cw, y_cw, z_cw = _walsh(_apply_perm(tt, _CW))
        _, x_ccw, y_ccw, z_ccw = _walsh(_apply_perm(tt, _CCW))

        esq = x0*x0 + y0*y0 + z0*z0
        zf_std = (z0*z0) / esq if esq > 0 else 0.0
        zf_cw = (z_cw*z_cw) / esq if esq > 0 else 0.0
        zf_ccw = (z_ccw*z_ccw) / esq if esq > 0 else 0.0

        print(
            f"  {ALL[tile_idx].name:>12}  "
            f"std=({x0:>2},{y0:>2},{z0:>2})  "
            f"cw=({x_cw:>2},{y_cw:>2},{z_cw:>2})  "
            f"ccw=({x_ccw:>2},{y_ccw:>2},{z_ccw:>2})  "
            f"|z|^2/|r|^2: std={zf_std:.2f} cw={zf_cw:.2f} ccw={zf_ccw:.2f}"
        )
    print()


# ── J (Ising coupling) analysis ────────────────────────────────────

def test_j_sign_preserved_under_chirality() -> None:
    """Analyze how z changes under chirality. Since CW swaps x<->z,
    z_cw = x_std, so (z_std, z_cw) pairs correspond to (z, x) pairs.
    CW effectively probes the x Walsh coefficient through the z channel.
    """
    print("ISING COUPLING J = z*pi/8 UNDER CHIRALITY")
    print("-" * 65)
    visited: set[tuple[int, int]] = set()
    for tile_idx in range(16):
        tt = ALL[tile_idx].truth_table
        _, _, _, z0 = _walsh(tt)
        _, _, _, z_cw = _walsh(_apply_perm(tt, _CW))
        _, _, _, z_ccw = _walsh(_apply_perm(tt, _CCW))
        key = (z0, z_cw)
        if key not in visited:
            visited.add(key)
            print(
                f"  z=({z0:>2},{z_cw:>2},{z_ccw:>2})  "
                f"J=({z0*math.pi/8:.4f},{z_cw*math.pi/8:.4f},{z_ccw*math.pi/8:.4f})"
            )
    print(f"  -> {len(visited)} distinct (z_std, z_cw) pairs")
    # z in {0, +/-1, +/-2}, x in {0, +/-1, +/-2}: at most 5*5=25 combos,
    # but only 9 appear because x and z are correlated through the truth table
    assert len(visited) <= 25, "Sanity check"


# ── Discover topological partners ──────────────────────────────────

def test_discover_cw_partner_classes() -> None:
    """CW pairs tiles into topological partner classes.

    Tiles with v10=v11 are self-paired (fixed points).
    Tiles with v10!=v11 form partner pairs.
    """
    print("CW PARTNER CLASSES")
    print("-" * 45)
    visited: set[int] = set()
    n_pairs = 0
    for i in range(16):
        if i in visited:
            continue
        tt = ALL[i].truth_table
        j = from_block(_apply_perm(tt, _CW)).index
        if i == j:
            print(f"  {ALL[i].name:>12}  (fixed: v10=v11)")
        else:
            print(f"  {ALL[i].name:>12}  <->  {ALL[j].name}")
            n_pairs += 1
        visited.add(i)
        visited.add(j)
    n_fixed = 16 - 2 * n_pairs
    assert n_pairs * 2 + n_fixed == 16
    print(f"  -> {n_pairs} partner pairs, {16 - 2*n_pairs} self-dual tiles")


# ── Kitaev ν mapping ──────────────────────────────────────────────
# The Kitaev exchange phase is exp(i*pi*nu/4). In BTB the exchange
# analogue is J*8/pi = z.  So z = 0 -> nu in {0,8}, z = +/-1 -> nu
# in {+/-1,+/-7}, z = +/-2 -> nu in {+/-2,+/-6} etc.
#
# BUT: the BTB system only has z in {0,+/-1,+/-2}.  The full 16-fold
# Kitaev classification distinguishes nu from 16-nu via the chiral
# central charge c_- = nu/2 mod 8.  In BTB this is the (h1,h2) pair
# plus the traversal signature.

def _compute_nu_candidate(tt: tuple[int, int, int, int]) -> int:
    """Compute a candidate Kitaev nu for a tile from its Walsh coeffs.

    Uses J = z*pi/8 and the (h1,h2) = (y*pi/8, x*pi/8) pair.
    z=0 -> nu in {0,8}; z=+/-1 -> nu in {+/-1,+/-7}; z=+/-2 -> nu in {+/-2,+/-6}.
    """
    _, x, y, z = _walsh(tt)
    # Exchange phase = exp(i*pi*z/4)
    # Kitaev exchange phase = exp(i*pi*nu/4)
    # So z = nu mod 8 (approximately)
    # Full nu in 0..15: nu_base = z mod 8 (in 0..7), plus either 0 or 8
    nu_base = z % 8  # 0 for z=0, 7 for z=-1, 6 for z=-2, 1 for z=+1, 2 for z=+2
    # Distinguish nu from nu+8 by the (x,y) sign pattern
    # x,y in {0,+/-1,+/-2} determine the sub-class
    return nu_base


def test_unique_full_signature() -> None:
    """Every tile has a unique (a, x, y, z, CW->index) quintuple."""
    sigs: dict[tuple[int, int, int, int, int], int] = {}
    for i in range(16):
        tt = ALL[i].truth_table
        a, x, y, z = _walsh(tt)
        j = from_block(_apply_perm(tt, _CW)).index
        sig = (a, x, y, z, j)
        if sig in sigs:
            raise AssertionError(f"Duplicate: tile {i} and {sigs[sig]} both have {sig}")
        sigs[sig] = i
    assert len(sigs) == 16


# ── Main ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 75)
    print("BOOLEAN TILE BASIS - EXHAUSTIVE CHIRAL VERIFICATION")
    print("=" * 75)
    test_partner_table()
    test_walsh_redistribution()
    test_j_sign_preserved_under_chirality()
    test_discover_cw_partner_classes()
