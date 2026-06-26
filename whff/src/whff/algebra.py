"""Canonical 16-tile Walsh algebra: single source of truth for all WHFF projections."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

# ──────────────────────────────────────────────
# 1. Foundational constants
# ──────────────────────────────────────────────

N_TILES = 16
H2 = np.array([[1, 1], [1, -1]], dtype=np.int8)

# Boolean function names in informal order
_TILE_NAMES = [
    "FALSE",       # 0
    "AND",         # 1
    "A_AND_NOTB",  # 2
    "A",           # 3
    "NOTA_AND_B",  # 4
    "B",           # 5
    "XOR",         # 6
    "OR",          # 7
    "NOR",         # 8
    "XNOR",        # 9
    "NOTB",        # 10
    "B_IMP_A",     # 11
    "NOTA",        # 12
    "A_IMP_B",     # 13
    "NAND",        # 14
    "TRUE",        # 15
]

# Truth tables: (v00, v01, v10, v11) in {0,1}
_TRUTH_TABLES: tuple[tuple[int, int, int, int], ...] = (
    (0, 0, 0, 0),   # 0  FALSE
    (0, 0, 0, 1),   # 1  AND
    (0, 0, 1, 0),   # 2  A_AND_NOTB
    (0, 0, 1, 1),   # 3  A
    (0, 1, 0, 0),   # 4  NOTA_AND_B
    (0, 1, 0, 1),   # 5  B
    (0, 1, 1, 0),   # 6  XOR
    (0, 1, 1, 1),   # 7  OR
    (1, 0, 0, 0),   # 8  NOR
    (1, 0, 0, 1),   # 9  XNOR
    (1, 0, 1, 0),   # 10 NOTB
    (1, 0, 1, 1),   # 11 B_IMP_A
    (1, 1, 0, 0),   # 12 NOTA
    (1, 1, 0, 1),   # 13 A_IMP_B
    (1, 1, 1, 0),   # 14 NAND
    (1, 1, 1, 1),   # 15 TRUE
)

# ──────────────────────────────────────────────
# 2. Tile class
# ──────────────────────────────────────────────


def _walsh_coeffs(tt: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Compute exact integer Walsh coefficients from truth table.

    Returns (DC, R0, R1, R0R1) using H2 convolution:
      a = v00 + v01 + v10 + v11
      x = v00 - v01 + v10 - v11   (R₀)
      y = v00 + v01 - v10 - v11   (R₁)
      z = v00 - v01 - v10 + v11   (R₀R₁)
    """
    v00, v01, v10, v11 = tt
    return (
        v00 + v01 + v10 + v11,  # a (DC)
        v00 - v01 + v10 - v11,  # x (R₀)
        v00 + v01 - v10 - v11,  # y (R₁)
        v00 - v01 - v10 + v11,  # z (R₀R₁)
    )


def _bloch_vector(
    coeffs: tuple[int, int, int, int],
) -> tuple[float, float, float]:
    """Compute Bloch-like vector from Walsh coefficients.

    Returns (x/a, y/a, z/a) normalized to the unit ball. When |r| > 1
    (which occurs for tiles with DC=1), the vector is projected onto
    the sphere surface (pure state approximation).
    """
    a, x, y, z = coeffs
    if a == 0:
        return (0.0, 0.0, 0.0)
    r = (x / a, y / a, z / a)
    norm_sq = r[0] ** 2 + r[1] ** 2 + r[2] ** 2
    if norm_sq > 1.0:
        n = math.sqrt(norm_sq)
        return (r[0] / n, r[1] / n, r[2] / n)
    return r


def _purity(bloch: tuple[float, float, float]) -> float:
    """Return squared norm of Bloch vector ∈ [0, 1]."""
    return min(bloch[0] ** 2 + bloch[1] ** 2 + bloch[2] ** 2, 1.0)


def _ising_params(
    coeffs: tuple[int, int, int, int],
) -> tuple[float, float, float]:
    """Compute Ising Hamiltonian parameters (J, h1, h2) from Walsh coefficients.

    For a 2-qubit gate U_f = exp(-i H_f) with H_f in Pauli basis:
      H_f = J Z⊗Z + h1 Z⊗I + h2 I⊗Z
    where (J, h1, h2) are proportional to the Walsh coefficients.
    """
    _a, x, y, z = coeffs
    return (z * math.pi / 8, y * math.pi / 8, x * math.pi / 8)


def _gate_class(
    coeffs: tuple[int, int, int, int],
) -> str:
    """Classify as 'product' (J=0) or 'entangling' (J≠0)."""
    return "entangling" if coeffs[3] != 0 else "product"


def _mv_class(tt: tuple[int, int, int, int]) -> str:
    """Classify tile in the MV-algebra hierarchy."""
    if tt == (0, 0, 0, 0) or tt == (1, 1, 1, 1):
        return "literal"
    # XOR and XNOR: the phase-sensitive cases (MV4 violation)
    if tt in ((0, 1, 1, 0), (1, 0, 0, 1)):
        return "entangled"
    return "product"


def _shepard_freq_ratios(
    coeffs: tuple[int, int, int, int],
    base_ratios: tuple[float, float, float, float] = (1.0, 1.5, 2.0, 3.0),
) -> tuple[float, ...]:
    """Return frequency ratios for Shepard tone synthesis.

    Each non-zero Walsh coefficient contributes a harmonic at a
    characteristic ratio.  The ratios (DC, R₀, R₁, R₀R₁) default to
    (1.0, 1.5, 2.0, 3.0) — a just-intonation major triad + octave.
    """
    ratios = []
    for c, r in zip(coeffs, base_ratios):
        if c != 0:
            ratios.append(r)
    return tuple(ratios)


# ──────────────────────────────────────────────
# 3. Tile class
# ──────────────────────────────────────────────


class Tile:
    """One of the 16 Boolean functions of 2 variables — the atomic WHFF primitive.

    Each tile is an immutable object exposing its truth table, Walsh
    coefficients, Bloch vector, Ising parameters, IFS maps, Shepard
    frequency ratios, and algebraic classifications.
    """

    __slots__ = (
        "_index", "_name", "_tt",
        "_walsh", "_bloch", "_purity",
        "_ising", "_gate_cls", "_mv_cls",
        "_shepard",
    )

    def __init__(self, index: int) -> None:
        self._index = index
        self._name = _TILE_NAMES[index]
        self._tt = _TRUTH_TABLES[index]
        self._walsh = _walsh_coeffs(self._tt)
        self._bloch = _bloch_vector(self._walsh)
        self._purity = _purity(self._bloch)
        self._ising = _ising_params(self._walsh)
        self._gate_cls = _gate_class(self._walsh)
        self._mv_cls = _mv_class(self._tt)
        self._shepard = _shepard_freq_ratios(self._walsh)

    # ── Identity ──────────────────────────────

    @property
    def index(self) -> int:
        """Tile index 0–15."""
        return self._index

    @property
    def name(self) -> str:
        """Human-readable name (e.g. 'XOR', 'AND')."""
        return self._name

    @property
    def truth_table(self) -> tuple[int, int, int, int]:
        """Boolean truth table (v00, v01, v10, v11)."""
        return self._tt

    # ── Walsh spectrum ────────────────────────

    @property
    def walsh_coeffs(self) -> tuple[int, int, int, int]:
        """Integer Walsh coefficients (DC, R₀, R₁, R₀R₁)."""
        return self._walsh

    @property
    def dc(self) -> int:
        """DC component = sum of truth table."""
        return self._walsh[0]

    @property
    def r0(self) -> int:
        """R₀ Walsh coefficient (A dependence)."""
        return self._walsh[1]

    @property
    def r1(self) -> int:
        """R₁ Walsh coefficient (B dependence)."""
        return self._walsh[2]

    @property
    def r0r1(self) -> int:
        """R₀R₁ Walsh coefficient (A⊗B dependence)."""
        return self._walsh[3]

    # ── Bloch sphere geometry ─────────────────

    @property
    def bloch_vector(self) -> tuple[float, float, float]:
        """Bloch vector (x, y, z) inside/on the unit sphere."""
        return self._bloch

    @property
    def purity(self) -> float:
        """Squared norm |r|² ∈ [0,1]; 1 = pure, 0 = maximally mixed."""
        return self._purity

    # ── Ising Hamiltonian ─────────────────────

    @property
    def ising_params(self) -> tuple[float, float, float]:
        """Ising coupling (J, h₁, h₂) corresponding to this tile."""
        return self._ising

    @property
    def J(self) -> float:
        """ZZ coupling strength."""
        return self._ising[0]

    @property
    def h1(self) -> float:
        """Local field on qubit 1."""
        return self._ising[1]

    @property
    def h2(self) -> float:
        """Local field on qubit 2."""
        return self._ising[2]

    # ── Algebraic classification ──────────────

    @property
    def gate_class(self) -> str:
        """'product' (J=0) or 'entangling' (J≠0)."""
        return self._gate_cls

    @property
    def mv_class(self) -> str:
        """'literal', 'product', or 'entangled' in the MV-algebra sense."""
        return self._mv_cls

    @property
    def is_entangling(self) -> bool:
        """True iff this tile generates an entangling gate (J ≠ 0)."""
        return self._gate_cls == "entangling"

    @property
    def is_literal(self) -> bool:
        """True iff this tile is a constant (FALSE or TRUE)."""
        return self._mv_cls == "literal"

    # ── Spectral / Shepard ────────────────────

    @property
    def shepard_freq_ratios(self) -> tuple[float, ...]:
        """Frequency ratios for Shepard tone synthesis (weighted by |c|)."""
        return self._shepard

    # ── Algebraic operations ──────────────────

    def negate(self) -> Tile:
        """Return the Boolean negation of this tile."""
        return ALL[15 - self._index]

    def dual(self) -> Tile:
        """Return the dual tile: complementary Walsh coefficients."""
        return ALL[15 - self._index]

    def distance(self, other: Tile) -> float:
        """Bures distance between this tile and another.

        Uses the general mixed-state formula:
          d_B = √(2 - 2√((1 + r·s + √((1 - |r|²)(1 - |s|²))) / 2))
        """
        u = np.array(self._bloch, dtype=np.float64)
        v = np.array(other._bloch, dtype=np.float64)
        dot = float(np.clip(np.dot(u, v), -1.0, 1.0))
        nu2 = float(np.clip(1.0 - np.dot(u, u), 0.0, 1.0))
        nv2 = float(np.clip(1.0 - np.dot(v, v), 0.0, 1.0))
        sqrt_fid = math.sqrt((1.0 + dot + math.sqrt(nu2 * nv2)) / 2.0)
        return math.sqrt(2.0 - 2.0 * sqrt_fid)

    def walsh_weight(self) -> float:
        """Euclidean norm of the non-DC Walsh coefficients √(x²+y²+z²)."""
        _, x, y, z = self._walsh
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def to_2x2(self) -> np.ndarray:
        """Return 2×2 numpy array of the truth table."""
        return np.array(self._tt, dtype=np.uint8).reshape(2, 2)

    # ── Display ───────────────────────────────

    def __repr__(self) -> str:
        return f"<Tile {self._index}: {self._name}>"

    def __int__(self) -> int:
        return self._index

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tile) and self._index == other._index

    def __hash__(self) -> int:
        return hash(self._index)


# ──────────────────────────────────────────────
# 4. All 16 tiles — module-level constant
# ──────────────────────────────────────────────

ALL: tuple[Tile, ...] = tuple(Tile(i) for i in range(N_TILES))

# Named aliases for convenience
FALSE = ALL[0]
AND = ALL[1]
A_AND_NOTB = ALL[2]
A = ALL[3]
NOTA_AND_B = ALL[4]
B = ALL[5]
XOR = ALL[6]
OR = ALL[7]
NOR = ALL[8]
XNOR = ALL[9]
NOTB = ALL[10]
B_IMP_A = ALL[11]
NOTA = ALL[12]
A_IMP_B = ALL[13]
NAND = ALL[14]
TRUE = ALL[15]


# ──────────────────────────────────────────────
# 5. Lookup helpers
# ──────────────────────────────────────────────

# Fast 4D lookup: (v00, v01, v10, v11) → Tile
_LOOKUP_4D: list[list[list[list[Tile]]]] = [
    [[[None for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for _ in range(2)
]
for t in ALL:
    v00, v01, v10, v11 = t.truth_table
    _LOOKUP_4D[v00][v01][v10][v11] = t


def from_block(block: Sequence[int] | np.ndarray) -> Tile:
    """Return the Tile matching a 2×2 boolean block (O(1) lookup).

    Args:
        block: 4-element sequence (v00, v01, v10, v11) or 2×2 array.

    Returns:
        The matching Tile instance.

    Raises:
        ValueError: if no matching tile (block has invalid values).
    """
    if isinstance(block, np.ndarray):
        b = block.ravel()
    else:
        b = block
    v0, v1, v2, v3 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
    if any(v > 1 or v < 0 for v in (v0, v1, v2, v3)):
        msg = f"Invalid block values: ({v0},{v1},{v2},{v3})"
        raise ValueError(msg)
    t = _LOOKUP_4D[v0][v1][v2][v3]
    if t is None:
        msg = f"No matching tile for block: ({v0},{v1},{v2},{v3})"
        raise ValueError(msg)
    return t


def from_index(index: int) -> Tile:
    """Return Tile by index (0–15)."""
    return ALL[index]


def tile_stream_to_indices(tiles: Sequence[Tile]) -> np.ndarray:
    """Convert a sequence of Tiles to a 1D numpy array of indices."""
    return np.array([t.index for t in tiles], dtype=np.uint8)


def indices_to_tile_stream(indices: np.ndarray) -> list[Tile]:
    """Convert a 1D numpy array of indices back to Tile list."""
    return [ALL[i] for i in indices]


# ──────────────────────────────────────────────
# 6. Bures distance matrix (16×16)
# ──────────────────────────────────────────────

_BURES_CACHE: np.ndarray | None = None


def bures_matrix() -> np.ndarray:
    """Return the 16×16 symmetric Bures distance matrix (cached)."""
    global _BURES_CACHE
    if _BURES_CACHE is not None:
        return _BURES_CACHE
    mat = np.zeros((N_TILES, N_TILES), dtype=np.float64)
    for i in range(N_TILES):
        for j in range(i + 1, N_TILES):
            d = ALL[i].distance(ALL[j])
            mat[i, j] = d
            mat[j, i] = d
    _BURES_CACHE = mat
    return mat


# ──────────────────────────────────────────────
# 7. Summary tables
# ──────────────────────────────────────────────


def summary_table() -> str:
    """Return a formatted table of all 16 tiles with their properties."""
    lines = [
        f"{'Idx':>3} {'Name':>12} {'TT':>6} {'DC':>3} {'R0':>3} {'R1':>3} "
        f"{'R0R1':>5} {'Bloch':>18} {'Pur':>5} {'Gate':>10} {'MV':>10}"
    ]
    lines.append("-" * len(lines[0]))
    for t in ALL:
        tt = "".join(str(b) for b in t.truth_table)
        bl = f"({t.bloch_vector[0]:.3f},{t.bloch_vector[1]:.3f},{t.bloch_vector[2]:.3f})"
        lines.append(
            f"{t.index:>3} {t.name:>12} {tt:>6} {t.dc:>3} {t.r0:>3} {t.r1:>3} "
            f"{t.r0r1:>5} {bl:>18} {t.purity:.3f} {t.gate_class:>10} {t.mv_class:>10}"
        )
    return "\n".join(lines)


def ising_table() -> str:
    """Return a formatted table of Ising parameters."""
    lines = ["Idx  Name           J       h1      h2    Gate Class"]
    lines.append("-" * 50)
    for t in ALL:
        lines.append(
            f"{t.index:>3}  {t.name:>12}  {t.J:>6.3f}  {t.h1:>6.3f}  "
            f"{t.h2:>6.3f}  {t.gate_class:>10}"
        )
    return "\n".join(lines)
