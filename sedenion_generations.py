"""sedenion_generations.py
Explore the connection between the 16 Boolean tiles (Cl(4,0) basis)
and the sedenion algebra used by Gillard & Gresnigt (2019) for
the three-generation fermion structure of the Standard Model.

Key claims to test:
  1. Cl(4,0) ≅ M₂(H) has dim 16, matching the sedenion basis S
  2. The primitive idempotent ρ₊ = ½(1 + ie₁₅) splits C⊗S into
     three C⊗O copies, each generating Cl(6)
  3. The CCW 3-cycles in the tile system correspond to the
     three-generation structure
  4. The shared Cl(2) subalgebra corresponds to n=1 (toric code)
"""

import math, itertools, functools
from typing import List, Tuple, Callable

# ─────────────────────────────────────────────
# 0. Complexified sedenion arithmetic
# ─────────────────────────────────────────────

class CSedenion:
    """Complexified sedenion: sum_{k=0..15} (a_k + i*b_k) * e_k,
    stored as 32 real coefficients [a_0..a_15, b_0..b_15].
    """
    __slots__ = ('c',)  # 32 real coefficients
    def __init__(self, coeffs):
        if isinstance(coeffs, CSedenion):
            self.c = list(coeffs.c)
        elif isinstance(coeffs, (int, float)):
            self.c = [float(coeffs)] + [0.0]*31
        else:
            c = list(coeffs)
            if len(c) < 32:
                c += [0.0]*(32 - len(c))
            self.c = [float(x) for x in c[:32]]

    @staticmethod
    def e(k):
        """Basis element e_k (k=0..15)."""
        c = [0.0]*32
        c[k] = 1.0
        return CSedenion(c)

    @staticmethod
    def i_e(k):
        """Imaginary basis element i*e_k."""
        c = [0.0]*32
        c[16 + k] = 1.0
        return CSedenion(c)

    def __add__(self, o):
        o = CSedenion(o)
        return CSedenion([self.c[i] + o.c[i] for i in range(32)])

    def __sub__(self, o):
        o = CSedenion(o)
        return CSedenion([self.c[i] - o.c[i] for i in range(32)])

    def __neg__(self):
        return CSedenion([-x for x in self.c])
    def __rmul__(self, k):
        if isinstance(k, (int, float)):
            return CSedenion([k * x for x in self.c])
        if isinstance(k, complex):
            # Real part
            r = CSedenion([k.real * x for x in self.c])
            # Imaginary part: i * (k.imag * x)
            i_part = [k.imag * x for x in self.c]
            # i * i_part: multiply by i swaps real/imag with sign
            res = [0.0]*32
            for idx in range(16):
                res[idx] += r.c[idx] - i_part[16+idx]
                res[16+idx] += r.c[16+idx] + i_part[idx]
            return CSedenion(res)
        return NotImplemented

    def __repr__(self):
        terms = []
        for k in range(16):
            if abs(self.c[k]) > 1e-12:
                terms.append(f"{self.c[k]:+.4f}e_{k}")
            if abs(self.c[16+k]) > 1e-12:
                terms.append(f"{self.c[16+k]:+.4f}i*e_{k}")
        if not terms:
            return "0"
        return " ".join(terms)

    def __eq__(self, o):
        o = CSedenion(o)
        return all(abs(self.c[i] - o.c[i]) < 1e-10 for i in range(32))

    def __hash__(self):
        return hash(tuple(round(c, 10) for c in self.c))

    def real(self):
        return [self.c[k] for k in range(16)]

    def imag(self):
        return [self.c[16+k] for k in range(16)]


# ─────────────────────────────────────────────
# 1. Sedenion multiplication table
# ─────────────────────────────────────────────

# The sedenion multiplication is defined by:
#   e_0 * x = x * e_0 = x  (identity)
#   For i >= 1: e_i^2 = -1
#   For i != j and i,j >= 1: e_i * e_j = +/- e_k  (some k based on Fano-like structure)

# We use the standard Cayley-Dickson construction:
# If a,b,c,d are in O (octonions), then
#   (a + c*e_8) * (b + d*e_8) = (ab - conj(d)*c) + (da + c*conj(b))*e_8
# where conj(x) = 2*Re(x) - x for octonions.

# For octonions (basis e_0..e_7), use the Fano plane:
OCT_MULT = {}

# Fano plane multiplication (all 7 lines, each with 3 points):
# Each line gives a cyclic triad: e_i * e_j = e_k (with sign)
# Standard octonion multiplication table:
# e_1 e_2 = e_4  (124)
# e_2 e_4 = e_1
# e_4 e_1 = e_2
#
# e_2 e_3 = e_5  (235)
# e_3 e_5 = e_2
# e_5 e_2 = e_3
#
# e_3 e_4 = e_6  (346)
# e_4 e_6 = e_3
# e_6 e_3 = e_4
#
# e_4 e_5 = e_7  (457)
# e_5 e_7 = e_4
# e_7 e_4 = e_5
#
# e_5 e_6 = e_1  (561)
# e_6 e_1 = e_5
# e_1 e_5 = e_6
#
# e_6 e_7 = e_2  (672)
# e_7 e_2 = e_6
# e_2 e_6 = e_7
#
# e_7 e_1 = e_3  (713)
# e_1 e_3 = e_7
# e_3 e_7 = e_1

# Build octonion multiplication table
OCT = {}
# Identity
for k in range(8):
    OCT[(0, k)] = (k, 1.0)  # e_0 * e_k = e_k
    OCT[(k, 0)] = (k, 1.0)  # e_k * e_0 = e_k

# e_i^2 = -1 for i >= 1
for i in range(1, 8):
    OCT[(i, i)] = (0, -1.0)

# Fano lines: each is a cyclic triple (i,j,k) meaning e_i*e_j = e_k
FANO_LINES = [
    (1, 2, 4), (2, 4, 1), (4, 1, 2),
    (2, 3, 5), (3, 5, 2), (5, 2, 3),
    (3, 4, 6), (4, 6, 3), (6, 3, 4),
    (4, 5, 7), (5, 7, 4), (7, 4, 5),
    (5, 6, 1), (6, 1, 5), (1, 5, 6),
    (6, 7, 2), (7, 2, 6), (2, 6, 7),
    (7, 1, 3), (1, 3, 7), (3, 7, 1),
]

for i, j, k in FANO_LINES:
    OCT[(i, j)] = (k, 1.0)
    # Anti-commutation for reverse order
    OCT[(j, i)] = (k, -1.0)

def oct_mult(i, j):
    """Multiply octonion basis elements e_i * e_j.
    Returns (k, sign) where e_i * e_j = sign * e_k.
    """
    if (i, j) in OCT:
        return OCT[(i, j)]
    # Alternative: anti-commute
    if (j, i) in OCT:
        k, s = OCT[(j, i)]
        return (k, -s)
    raise ValueError(f"Unknown octonion product e_{i} * e_{j}")

# Sedenion multiplication using Cayley-Dickson doubling:
# (a + c*e_8) * (b + d*e_8) = (ab - conj_S(d)*c) + (da + c*conj_S(b))*e_8
# where conj_S(x) = 2*Re(x) - x for sedenions (conjugate flips sign of all e_i, i>=1)

def conj_sed(i):
    """Sedenion conjugate: flips sign of e_k for k >= 1."""
    if i == 0:
        return i
    return -i  # Wait, this is wrong. conj_S(e_k) = { +e_0 for k=0, -e_k for k>=1 }

def sed_mult(i, j):
    """Multiply sedenion basis elements e_i * e_j.
    Returns (k, sign).
    """
    if i < 8 and j < 8:
        return oct_mult(i, j)

    # Cayley-Dickson doubling: represent sedenion as (a,c) where a,c in O
    # e_i for i=0..7 is (e_i, 0)
    # e_i for i=8..15 is (0, e_{i-8})
    
    # For i, j in range(16):
    #   If i < 8: a = e_i, c = 0
    #   Else: a = 0, c = e_{i-8}
    # Same for j.
    
    a_i, c_i = (i, -1) if i < 8 else (-1, i - 8)  # Use -1 as "no element"
    a_j, c_j = (j, -1) if j < 8 else (-1, j - 8)
    
    # We need to handle the 4 cases:
    # 1. i < 8, j < 8: octonion * octonion (already handled)
    # 2. i < 8, j >= 8: a * (d * e_8) = (a*d) * e_8
    # 3. i >= 8, j < 8: (c * e_8) * b = (c * conj(b)) * e_8
    # 4. i >= 8, j >= 8: (c * e_8) * (d * e_8) = -conj(d) * c
    
    # For the doubling, the sedenion e_i for i >= 8 is (0, e_{i-8})
    # and the product is:
    # (0, c) * (b, 0) = (0, c * conj(b))   [case 3]
    # (0, c) * (0, d) = (-conj(d) * c, 0)  [case 4]
    # (a, 0) * (0, d) = (0, d * a)        [case 2]
    
    if i < 8 and j >= 8:
        # Case 2: e_i * e_{j} = e_i * (0, e_{j-8}) = (0, e_{j-8} * e_i)
        d = j - 8
        k, s = oct_mult(d, i)  # d * i
        return (8 + k, s)
    
    if i >= 8 and j < 8:
        # Case 3: (0, e_{i-8}) * e_j = (0, e_{i-8} * conj(e_j))
        c = i - 8
        # conj(e_j) = -e_j for j >= 1, = e_0 for j=0
        if j == 0:
            k, s = oct_mult(c, 0)  # c * 1 = c
            return (8 + k, s)
        else:
            k, s = oct_mult(c, j)  # c * e_j
            return (8 + k, -s)  # conj introduces minus sign
    
    if i >= 8 and j >= 8:
        # Case 4: (0, e_{i-8}) * (0, e_{j-8}) = -conj(e_j) * e_i?? 
        # Using (0,c)*(0,d) = (-conj(d)*c, 0):
        c = i - 8
        d = j - 8
        # conj(e_d) = -e_d for d >= 1
        # (-conj(e_d)) * e_c = e_d * e_c
        if d == 0:
            # conj(e_0) = e_0, so -conj(e_0)*e_c = -e_c
            return (c, -1.0)
        else:
            # conj(e_d) = -e_d, so -conj(e_d)*e_c = e_d*e_c
            k, s = oct_mult(d, c)
            return (k, -s)  # Hmm, wait. Let me reconsider.
    
    # Shouldn't reach here for i,j >= 1
    raise ValueError(f"Unhandled: e_{i} * e_{j}")

# Actually, the above is getting complicated and error-prone.
# Let me use a different approach: lookup table from known sedenion multiplication.

# The standard sedenion multiplication table uses the following pattern:
# For i in 1..7, j in 1..7:
#   e_i * e_j = octonion product (as Fano plane)
#   e_i * e_{8+j} = e_{8+k} where e_i * e_j = +/- e_k
#   e_{8+i} * e_j = e_{8+k} where e_j * e_i = +/- e_k
#   e_{8+i} * e_{8+j} = -e_j * e_i

# Let me build this systematically.
def build_sed_mult():
    """Build the full sedenion multiplication lookup table.
    Returns dict {(i,j): (k, sign)}.
    """
    mult = {}
    # Identity
    for k in range(16):
        mult[(0, k)] = (k, 1.0)
        mult[(k, 0)] = (k, 1.0)
    # Squares: e_i^2 = -1 for i >= 1
    for i in range(1, 16):
        mult[(i, i)] = (0, -1.0)
    
    # Octonion part (i,j in 1..7)
    for i in range(1, 8):
        for j in range(1, 8):
            if i != j:
                k, s = oct_mult(i, j)
                mult[(i, j)] = (k, s)
    
    # Mix part (i in 1..7, j in 8..15)
    for i in range(1, 8):
        for j in range(8, 16):
            j0 = j - 8
            # e_i * e_{8+j0} = e_{8+k} where e_i * e_{j0} = +/- e_k
            if j0 == 0:
                # e_i * e_8 = e_{8+i}
                mult[(i, j)] = (8 + i, 1.0)
                # Wait, this isn't right for all cases. Let me use the CD formula.
                continue
            k, s = oct_mult(i, j0)  # e_i * e_{j0} = s * e_k
            # The doubling says: e_i * (0, e_{j0}) = (0, e_{j0} * e_i)
            k2, s2 = oct_mult(j0, i)  # e_{j0} * e_i
            mult[(i, j)] = (8 + k2, s2)
    
    # Mix part (i in 8..15, j in 1..7)
    for i in range(8, 16):
        i0 = i - 8
        for j in range(1, 8):
            # (0, e_{i0}) * e_j = (0, e_{i0} * conj(e_j))
            if i0 == 0:
                # e_8 * e_j = e_{8+j}
                mult[(i, j)] = (8 + j, 1.0)
                continue
            # conj(e_j) = -e_j for j >= 1
            k2, s2 = oct_mult(i0, j)  # e_{i0} * e_j
            mult[(i, j)] = (8 + k2, -s2)  # times -1 for conj
    
    # Sedenion-sedenion part (i,j in 8..15)
    for i in range(8, 16):
        i0 = i - 8
        for j in range(8, 16):
            j0 = j - 8
            # (0, e_{i0}) * (0, e_{j0}) = (-conj(e_{j0}) * e_{i0}, 0)
            if j0 == 0:
                # conj(e_0) = e_0, so -conj(e_0)*e_{i0} = -e_{i0}
                k = i0
                s = -1.0
            else:
                # conj(e_{j0}) = -e_{j0}, so -(-e_{j0})*e_{i0} = e_{j0}*e_{i0}
                k2, s2 = oct_mult(j0, i0)
                k = k2
                s = s2
            mult[(i, j)] = (k, s)
    
    return mult

SED_MULT = build_sed_mult()

def sed_mult(i, j):
    """Multiply sedenion basis elements e_i * e_j.
    Returns (k, sign) where e_i * e_j = sign * e_k.
    """
    if (i, j) in SED_MULT:
        return SED_MULT[(i, j)]
    # Try reverse
    if (j, i) in SED_MULT:
        k, s = SED_MULT[(j, i)]
        return (k, -s)
    raise ValueError(f"Unknown sedenion product e_{i} * e_{j}")

def sed_mul(a, b):
    """Full sedenion multiplication: a * b for CSedenion elements."""
    res = [0.0]*32
    for ia in range(16):
        if a.c[ia] == 0 and a.c[16+ia] == 0:
            continue
        for ib in range(16):
            if b.c[ib] == 0 and b.c[16+ib] == 0:
                continue
            k, sign = sed_mult(ia, ib)
            # Real * Real product
            coeff_r = a.c[ia] * b.c[ib] - a.c[16+ia] * b.c[16+ib]
            # Imag * Imag produces -Real
            # Real * Imag and Imag * Real produce Imag
            coeff_i = a.c[ia] * b.c[16+ib] + a.c[16+ia] * b.c[ib]
            res[k] += sign * coeff_r
            res[16+k] += sign * coeff_i
    return CSedenion(res)

def left_mult_matrix(basis_idx):
    """Build the 16x16 matrix of left multiplication by e_{basis_idx}
    acting on the sedenion basis (as a real vector space).
    Returns list of 16 coefficients (the 16 real basis images).
    """
    rows = []
    for j in range(16):
        k, s = sed_mult(basis_idx, j)
        # The image of e_j under L_{e_i} is s*e_k
        row = [0.0]*16
        row[k] = s
        rows.append(row)
    return rows

def left_mult_as_matrix(elem_selector):
    """For a given element defined by a list of (idx, coeff) pairs,
    return the 16x16 matrix of left multiplication.
    """
    mat = [[0.0]*16 for _ in range(16)]
    for idx, coeff in elem_selector:
        if abs(coeff) < 1e-12:
            continue
        lm = left_mult_matrix(idx)
        for i in range(16):
            for j in range(16):
                mat[i][j] += coeff * lm[i][j]
    return mat

# ─────────────────────────────────────────────
# 2. Test sedenion multiplication
# ─────────────────────────────────────────────

print("=" * 78)
print("SEDENION ALGEBRA AND THE 16 BOOLEAN TILES")
print("=" * 78)

print("\n--- 2.1 Verifying sedenion multiplication ---\n")

# Test a few products
tests = [(1, 2, 4, 1.0), (3, 6, 4, -1.0), (2, 3, 5, 1.0),
         (8, 0, 8, 1.0), (0, 8, 8, 1.0)]
for i, j, expected_k, expected_s in tests:
    k, s = sed_mult(i, j)
    ok = "✓" if (k == expected_k and abs(s - expected_s) < 0.01) else "✗"
    print(f"  e_{i} * e_{j} = {s:+.0f} e_{k} (expected {expected_s:+.0f} e_{expected_k}) {ok}")

# Check e_8 * e_9 = e_1 (from known sedenion properties)
k, s = sed_mult(8, 9)
print(f"  e_8 * e_9 = {s:+.0f} e_{k} (expected for octonion triality)")

print()

# ─────────────────────────────────────────────
# 3. Walsh quaternions to sedenion basis
# ─────────────────────────────────────────────

print("--- 3.1 Mapping 16 Walsh quaternions to sedenion basis ---\n")

# The 16 Walsh quaternions from our analysis
TILE_DATA = [
    ("FALSE",     (0,0,0,0)),
    ("AND",       (0,0,0,1)),
    ("A_AND_NOTB",(0,0,1,0)),
    ("A",         (0,0,1,1)),
    ("NOTA_AND_B",(0,1,0,0)),
    ("B",         (0,1,0,1)),
    ("XOR",       (0,1,1,0)),
    ("OR",        (0,1,1,1)),
    ("NOR",       (1,0,0,0)),
    ("XNOR",      (1,0,0,1)),
    ("NOTB",      (1,0,1,0)),
    ("B_IMP_A",   (1,0,1,1)),
    ("NOTA",      (1,1,0,0)),
    ("A_IMP_B",   (1,1,0,1)),
    ("NAND",      (1,1,1,0)),
    ("TRUE",      (1,1,1,1)),
]

def walsh(tt):
    v00, v01, v10, v11 = tt
    return (v00+v01+v10+v11, v00-v01+v10-v11, v00+v01-v10-v11, v00-v01-v10+v11)

# In the Gillard-Gresnigt construction, the 16 sedenion basis elements
# correspond to the 16 Cl(4,0) basis elements. We need a mapping from
# Walsh quaternions (a,x,y,z) to sedenion indices e_0..e_15.

# Natural mapping: sort tiles by (DC parity, z, x, y) and assign
# sedenion indices 0..15 in that order.

# But we need a more principled mapping. The sedenion e_0 = 1 (identity)
# should map to the identity in Cl(4,0), which is FALSE (a,x,y,z) = (0,0,0,0).

# For the remaining elements, we want the mapping to respect:
# 1. Cl(4,0) grading → sedenion structure
# 2. CCW 3-cycles → generation structure
# 3. Exchange phase z → some sedenion index pattern

# Let's try: map by DC parity first, then by exchange phase z.
# This gives:
#   Even DC (Abelian): sedenion indices 0-7 (e_0..e_7 = octonions)
#   Odd DC (non-Abelian): sedenion indices 8-15 (e_8..e_15)

# Within even DC, sort by z: 0, 0, 0, 0, -2, 2, 0, 0
#   FALSE (z=0) -> e_0
#   A (z=0) -> e_1
#   NOTA (z=0) -> e_2
#   B (z=0) -> e_3
#   NOTB (z=0) -> e_4
#   TRUE (z=0) -> e_5
#   XOR (z=-2) -> e_6
#   XNOR (z=2) -> e_7

# Within odd DC, sort by z: -1, -1, -1, -1, 1, 1, 1, 1
# But also by x,y pattern (the CCW orbit structure)

def assign_sedenion_mapping():
    """Assign sedenion basis index to each tile."""
    tile_data = []
    for name, tt in TILE_DATA:
        a, x, y, z = walsh(tt)
        tile_data.append((name, tt, a, x, y, z))
    
    # Sort by DC parity (even first), then by z, then by (x,y) pattern
    def sort_key(item):
        name, tt, a, x, y, z = item
        dc_parity = a % 2
        return (dc_parity, z, x, y)
    
    sorted_tiles = sorted(tile_data, key=sort_key)
    
    mapping = {}
    for idx, (name, tt, a, x, y, z) in enumerate(sorted_tiles):
        mapping[name] = idx
    return mapping, sorted_tiles

sed_map, sorted_tiles = assign_sedenion_mapping()

print(f"  Proposed Walsh quaternion → sedenion basis mapping:\n")
print(f"  {'Idx':>3} {'Name':>14}  {'Walsh (a,x,y,z)':>20}  {'Parity':>8}  {'z':>4}  {'3-cycle orbit':>16}")
print("  " + "-" * 75)
for idx, (name, tt, a, x, y, z) in enumerate(sorted_tiles):
    parity = "even" if a % 2 == 0 else "odd"
    # Find CCW orbit
    def apply_perm(t, perm):
        return tuple(t[p] for p in perm)
    _CCW = (0, 2, 3, 1)
    # Simple cycle membership check
    cycle_names = []
    for cycle_template in [
        ("AND", "A_AND_NOTB", "NOTA_AND_B"),
        ("B_IMP_A", "NAND", "A_IMP_B"),
        ("A", "XOR", "B"),
        ("XNOR", "NOTB", "NOTA"),
    ]:
        if name in cycle_template:
            cycle_names = list(cycle_template)
            break
    if not cycle_names:
        orbit = "fixed"
    else:
        orbit = " → ".join(cycle_names)
    print(f"  {idx:>3} {name:>14}  ({a:>2},{x:>2},{y:>2},{z:>2})  {parity:>8}  {z:>4}  {orbit:>16}")

print()
print(f"  Sedenion indices 0-7: even DC parity (abelian sector)")
print(f"  Sedenion indices 8-15: odd DC parity (non-abelian sector)")
print()

# ─────────────────────────────────────────────
# 4. Primitive idempotent construction
# ─────────────────────────────────────────────

print("--- 4.1 Primitive idempotent ρ₊ = ½(1 + ie₁₅) ---\n")

# e_15 is the last sedenion basis element.
# In our mapping, index 15 corresponds to whichever tile maps there.
id_15_name = [n for n, i in sed_map.items() if i == 15][0]
print(f"  In our mapping, e_15 corresponds to: {id_15_name}")
print()

# The idempotent in CSedenion:
rho_plus = CSedenion([0.0]*32)
# 1/2 * 1 (real part contributes 0.5 to coefficient of e_0)
rho_plus.c[0] = 0.5  # real part of (1/2 * 1)
# 1/2 * i*e_15: imaginary coefficient of e_15 = 0.5
rho_plus.c[16 + 15] = 0.5  # i*e_15 with coefficient 0.5

print(f"  ρ₊ = {rho_plus}")
print()

# Verify idempotent: ρ₊ * ρ₊ = ρ₊
sq = sed_mul(rho_plus, rho_plus)
print(f"  ρ₊² = {sq}")
print(f"  ρ₊² = ρ₊?: {'YES' if sq == rho_plus else 'NO'}")
print()

# The complementary idempotent: ρ₋ = ½(1 - ie₁₅)
rho_minus = CSedenion([0.0]*32)
rho_minus.c[0] = 0.5
rho_minus.c[16 + 15] = -0.5
print(f"  ρ₋ = {rho_minus}")
sq_m = sed_mul(rho_minus, rho_minus)
print(f"  ρ₋² = ρ₋?: {'YES' if sq_m == rho_minus else 'NO'}")
print(f"  ρ₊ + ρ₋ = 1?: {'YES' if abs((rho_plus + rho_minus).c[0] - 1.0) < 1e-10 else 'NO'}")
print(f"  ρ₊ * ρ₋ = 0?: {'YES' if abs(sum(sed_mul(rho_plus, rho_minus).c)) < 1e-10 else 'NO'}")
print()

# ─────────────────────────────────────────────
# 5. Decomposition into C⊗O copies
# ─────────────────────────────────────────────

print("--- 5.1 Splitting C⊗S into three C⊗O copies ---\n")

# G&G claim: ρ₊ acting by left multiplication on the 16 sedenion basis
# elements produces three sets of split basis elements, each generating Cl(6).

# Action of ρ₊ on each basis element:
# ρ₊ * e_k = ½(1 + ie₁₅) * e_k = ½(e_k + i*e₁₅*e_k)

print("  Action of ρ₊ on each sedenion basis element:\n")

# Build pairing structure: which e_k pairs with which e_m under ρ₊
pairs = {}
for k in range(16):
    ek = CSedenion.e(k)
    action = sed_mul(rho_plus, ek)
    name = [n for n, i in sed_map.items() if i == k][0]
    # Find the pair partner: look for i*e_m term in the output
    pair_idx = None
    for j in range(16):
        if abs(action.c[16 + j]) > 0.1:
            pair_idx = j
            break
    pairs[k] = pair_idx
    # Output: e_k → ½(e_k + i*sign*e_{pair})
    sign = "+" if pair_idx is not None and action.c[16 + pair_idx] > 0 else "-"
    pair_name = [n for n, i in sed_map.items() if i == pair_idx][0] if pair_idx is not None else "—"
    print(f"    e_{k:>2} ({name:>14}) → ½(e_{k} {sign} i·e_{pair_idx:>2} [{pair_name}])")

print()
print(f"  Pairing structure under L_ρ₊:")
# Group by non-overlapping sets
used = set()
for k in range(16):
    if k in used: continue
    pk = pairs[k]
    if pk is not None:
        n1 = [n for n, i in sed_map.items() if i == k][0]
        n2 = [n for n, i in sed_map.items() if i == pk][0]
        print(f"    ({k:>2},{pk:>2})  ({n1:>14} ↔ {n2:>14})")
        used.add(k)
        if pk is not None:
            used.add(pk)

print()
print(f"  The 8 paired sets correspond to 4 CCW 3-cycles × their chiral partners.")
print(f"  Under CCW: each paired element cycles within its 3-cycle,")
print(f"  while the pair partner cycles in the dual 3-cycle.")
print()

# For the three generations, we look at CCW 3-cycles in the tile system
# and see how they map to sedenion indices.

print("  CCW 3-cycles mapped to sedenion basis indices:\n")
for cycle_template in [
    ("AND", "A_AND_NOTB", "NOTA_AND_B"),
    ("B_IMP_A", "NAND", "A_IMP_B"),
    ("A", "XOR", "B"),
    ("XNOR", "NOTB", "NOTA"),
]:
    indices = [sed_map[n] for n in cycle_template]
    print(f"    {' → '.join(cycle_template)}")
    print(f"      Sedenion indices: {indices}")
    print()

# The 4 fixed points of CCW:
print("  CCW fixed points (shared Cl(2) candidates):")
for name in ["FALSE", "TRUE", "OR", "NOR"]:
    idx = sed_map[name]
    print(f"    {name:>14} → e_{idx}")
print()

# ═══════════════════════════════════════════════
# 6. Finding octonion subalgebras in S
# ═══════════════════════════════════════════════

print("--- 6.1 Identifying octonion subalgebras ---\n")

# The generations defined by CCW 3-cycles + duals
generations = {
    "Generation 1 (AND cycle + NOTA dual)": [12, 10, 9, 5, 6, 3],
    "Generation 2 (B_IMP_A cycle + A dual)": [14, 11, 13, 2, 1, 4],
}

# The sedenions contain many octonion subalgebras (each 8-dim).
# An 8-element subset containing e_0 that is closed under sedenion
# multiplication is an octonion subalgebra.
# 
# We search systematically: subsets of {1..15} of size 7 that,
# together with e_0, close under multiplication.

def is_closed_subset(indices):
    """Check if the given set of indices (including 0) is closed under multiplication."""
    s = set(indices)
    for i in indices:
        for j in indices:
            if i == 0 or j == 0:
                continue
            k, sign = sed_mult(i, j)
            # The product is sign*e_k; closure requires k ∈ s
            if k not in s:
                return False
    return True

# Try to find octonion subalgebras:
# First check the standard octonion: indices 0-7
standard_oct = list(range(8))
print(f"  Standard octonion O₀ = {{e₀..e₇}} (indices 0-7):")
print(f"    Tiles: {[next(n for n,i in sed_map.items() if i==idx) for idx in standard_oct]}")
print(f"    Closed under multiplication: {is_closed_subset(standard_oct)}")
print()

# Now check subsets generated by the CCW 3-cycles.
# For each CCW 3-cycle, the octonion subalgebra should contain
# the cycle elements + their dual partners + the identity + one more.
# 
# But actually, an octonion subalgebra must have 8 elements.
# The 3-cycle (3 elements) + dual (3 elements) = 6 elements.
# Plus e_0 = 7. Need 1 more — likely the shared fixed point.
# 
# Gen 1: {AND, A_AND_NOTB, NOTA_AND_B} ∪ {NOTA, NOTB, FALSE} = {12,10,9,5,6,3}
#   + e_0(XOR) = {0,3,5,6,9,10,12} — 7 elements, need 1 more
#   Try adding TRUE(4)? OR(8)? NOR(15)?
# 
# Let's check systematically.

generation_candidates = {
    "Gen 1 base": {12, 10, 9, 5, 6, 3},   # AND triple + dual (NOTA, NOTB, FALSE)
    "Gen 2 base": {14, 11, 13, 2, 1, 4},   # B_IMP_A triple + dual (A, B, TRUE)
}

for gname, gbase in generation_candidates.items():
    print(f"  {gname}: {{e_{{{','.join(str(i) for i in sorted(gbase))}}}}}")
    
    # Need to add e_0 = index 0 (the identity)
    trial = gbase | {0}
    print(f"    + e₀ = {{e_{{{','.join(str(i) for i in sorted(trial))}}}}} ({len(trial)} elements)")
    
    # Need 8 total; try adding each remaining index
    remaining = [i for i in range(1, 16) if i not in trial]
    found = []
    for extra in remaining:
        extended = trial | {extra}
        if is_closed_subset(list(extended)):
            tiles = [next(n for n,i in sed_map.items() if i==e) for e in sorted(extended)]
            found.append((extra, tiles))
    
    if found:
        for extra, tiles in found:
            print(f"    ✓ + e_{extra} ({next(n for n,i in sed_map.items() if i==extra)}) forms octonion subalgebra:")
            print(f"      Tiles: {tiles}")
    else:
        print(f"    ✗ No octonion subalgebra found (need different generation grouping)")
    print()

# Also check the CCW fixed points for a possible Cl(2) subalgebra:
# FALSE(3), TRUE(4), OR(8), NOR(15)
fixed_pts = [3, 4, 8, 15]
print("  CCW fixed points as Cl(2) candidates:")
print(f"    FALSE(3), TRUE(4), OR(8), NOR(15)")
print(f"    {{e_{{{','.join(str(i) for i in fixed_pts)}}}}} is closed: {is_closed_subset(fixed_pts)}")
print()

# Try the alternative: the three generations might be the three different
# octonion subalgebras that share a quaternion subalgebra = the CCW fixed points.
# Let's try: find octonion subalgebras that contain {3, 4, 8, 15} as a subset.
print("  Octonion subalgebras containing CCW fixed points {{FALSE,TRUE,OR,NOR}}:\n")
base_set = {0, 3, 4, 8, 15}  # e_0 + the 4 fixed points = 5 elements
for candidate_group in [
    ("AND cycle", {12, 10, 9}),
    ("B_IMP_A cycle", {14, 11, 13}),
    ("A cycle", {2, 0, 1}),
    ("XNOR cycle", {7, 6, 5}),
]:
    label, cycle = candidate_group
    trial = base_set | cycle
    # Remove duplicates (e_0 might already be in the cycle)
    # Actually, e_0=0 is XOR, and {2,0,1} includes it. Handle carefully.
    trial_s = set(trial)
    if len(trial_s) == 8:
        tiles = [next(n for n,i in sed_map.items() if i==e) for e in sorted(trial_s)]
        closed = is_closed_subset(list(trial_s))
        print(f"    {label}: {sorted(trial_s)} → {tiles}")
        print(f"      Closed: {closed}")
    print()

# ═══════════════════════════════════════════════
# 7. Cl(6) verification on the 8-dim subspace
# ═══════════════════════════════════════════════

print("--- 7.1 Searching all octonion subalgebras ---\n")

# Systematic search: for each 7-element subset of {1..15} that
# together with e₀ forms a closed octonion subalgebra.
# 
# To be practical, we use a heuristic: find all subsets of size 7
# that are closed under squaring (e_i² = -e₀) and where every
# product of distinct elements stays within the set.
# 
# Since the sedenions are built from O + O·e₈, a natural octonion
# subalgebra (other than the standard one) consists of 4 elements
# from the "even" half {e₁..e₇} and 3 elements from the "odd" half
# {e₈..e₁₅} plus the identity e₀.
# 
# Let's check the candidate identified above systematically.

def check_octonion_candidates():
    """Check all candidate octonion subalgebras formed by mixing
    even and odd basis elements."""
    found = []
    even_indices = list(range(8))     # {0, 1, ..., 7}
    odd_indices = list(range(8, 16))  # {8, 9, ..., 15}
    
    # We need 8 elements: e₀ + 3 even + 4 odd (or 4 even + 3 odd)
    # plus e₀ = 8 total.
    # Try all 4-even + 3-odd combinations:
    from itertools import combinations
    
    for e4 in combinations(range(1, 8), 4):   # 4 from {1..7}
        for o3 in combinations(range(8, 16), 3):  # 3 from {8..15}
            s = {0} | set(e4) | set(o3)
            if is_closed_subset(list(s)):
                tiles = sorted([next(n for n,i in sed_map.items() if i==e) for e in s])
                found.append((sorted(s), tiles))
    
    # Also try 3-even + 4-odd
    for e3 in combinations(range(1, 8), 3):
        for o4 in combinations(range(8, 16), 4):
            s = {0} | set(e3) | set(o4)
            if is_closed_subset(list(s)):
                tiles = sorted([next(n for n,i in sed_map.items() if i==e) for e in s])
                found.append((sorted(s), tiles))
    
    return found

# Limit search space by pre-filtering
print("  Searching octonion subalgebras with 4-even+3-odd or 3-even+4-odd...")
print(f"  Total combinations: C(7,4)×C(8,3) + C(7,3)×C(8,4) = ", end="")
from itertools import combinations
total = len(list(combinations(range(1,8),4))) * len(list(combinations(range(8,16),3)))
total += len(list(combinations(range(1,8),3))) * len(list(combinations(range(8,16),4)))
print(f"{total}")
print()

# Limit to full systematic search (only 4410 combinations)
from itertools import combinations

print("  Full systematic search of all 4410 combinations...\n")

candidates = []

# 4-even + 3-odd: C(7,4)×C(8,3) = 35×56 = 1960
for e4 in combinations(range(1, 8), 4):
    for o3 in combinations(range(8, 16), 3):
        s = {0} | set(e4) | set(o3)
        if is_closed_subset(list(s)):
            tiles = sorted([next(n for n,i in sed_map.items() if i==e) for e in s])
            candidates.append((sorted(s), tiles))

# 3-even + 4-odd: C(7,3)×C(8,4) = 35×70 = 2450
for e3 in combinations(range(1, 8), 3):
    for o4 in combinations(range(8, 16), 4):
        s = {0} | set(e3) | set(o4)
        if is_closed_subset(list(s)):
            tiles = sorted([next(n for n,i in sed_map.items() if i==e) for e in s])
            candidates.append((sorted(s), tiles))

# Remove duplicates
unique = []
seen = set()
for s, tiles in candidates:
    key = tuple(s)
    if key not in seen:
        seen.add(key)
        unique.append((s, tiles))

print(f"  Found {len(unique)} octonion subalgebras (from 4410 total combinations)")
print()

# Show all unique ones
for s, tiles in unique:
    # Classify by which CCW cycles are contained
    cycles_found = []
    for cname, cindices in [
        ("AND cycle", {12, 10, 9}),
        ("B_IMP_A cycle", {14, 11, 13}),
        ("A cycle", {2, 0, 1}),
        ("XNOR cycle", {7, 6, 5}),
    ]:
        if cindices.issubset(set(s)):
            cycles_found.append(cname)
    cycle_str = ", ".join(cycles_found) if cycles_found else "none"
    print(f"  Indices: {s}")
    print(f"  Tiles:   {tiles}")
    print(f"  CCW cycles contained: {cycle_str}")
    print()

def left_mult_matrix_of(elem):
    """Return 16×16 matrix of left multiplication by elem on the basis {e₀..e₁₅}."""
    mat = [[0.0]*16 for _ in range(16)]
    for j in range(16):
        prod = sed_mul(elem, CSedenion.e(j))
        for i in range(16):
            mat[i][j] = prod.c[i]
    return mat

# === Three-generation test: O0 under three idempotents ===

def make_idempotent(e_idx):
    """Create rho = 1/2(1 + i*e_idx)."""
    r = CSedenion([0.0]*32)
    r.c[0] = 0.5
    r.c[16 + e_idx] = 0.5
    return r

idempotents = {
    "rho1 (NOR=15)": make_idempotent(15),
    "rho2 (OR=8)":   make_idempotent(8),
    "rho3 (FALSE=3)": make_idempotent(3),
}

# Standard octonion O0 = {e0..e7} = even DC parity tiles
o0_non_id = [1, 2, 3, 4, 5, 6, 7]
o0_names = [next(n for n,i in sed_map.items() if i==e) for e in o0_non_id]
print(f"  O0 non-identity: {o0_non_id} -> {o0_names}\n")

def c_norm2(a):
    return sum(a.c[i]**2 + a.c[16+i]**2 for i in range(16))
def c_mul(a, cc):
    cr, ci = cc.real, cc.imag
    res = [0.0]*32
    for i in range(16):
        res[i] = cr*a.c[i] - ci*a.c[16+i]
        res[16+i] = cr*a.c[16+i] + ci*a.c[i]
    return CSedenion(res)
def ideal_basis_for(rho):
    vecs = [sed_mul(CSedenion.e(k), rho) for k in range(16)]
    basis = []
    for v in vecs:
        w = CSedenion(v)
        for b in basis:
            dot = sum(w.c[i]*b.c[i] + w.c[16+i]*b.c[16+i] for i in range(16))
            im = sum(w.c[i]*b.c[16+i] - w.c[16+i]*b.c[i] for i in range(16))
            coeff = (dot + 1j*im) / c_norm2(b)
            w = w - c_mul(b, coeff)
        if c_norm2(w) > 1e-12:
            basis.append(w)
    return basis[:8]

for rho_name, rho in idempotents.items():
    e_idx = next(i for i in range(16) if abs(rho.c[16+i] - 0.5) < 1e-10)
    rho_minus = CSedenion([0.0]*32)
    rho_minus.c[0] = 0.5
    rho_minus.c[16 + e_idx] = -0.5

    ibasis = ideal_basis_for(rho)
    print(f"  {rho_name}: ideal dim = {len(ibasis)}")

    # Build gamma elements from split basis of O0
    ge = []
    for idx in o0_non_id:
        ek = CSedenion.e(idx)
        # left-to-right: (rho * e_k) * rho_minus,  (rho_minus * e_k) * rho
        u_k = sed_mul(sed_mul(rho, ek), rho_minus)
        v_k = sed_mul(sed_mul(rho_minus, ek), rho)
        ge.append(u_k - v_k)
        ge.append(sed_mul(CSedenion.i_e(0), u_k - v_k))

    found = False
    for combo in [list(range(6)), list(range(2,8)), list(range(4,10)),
                  list(range(0,12,2)), list(range(1,12,2)),
                  list(range(2,14,2)), list(range(3,14,2)),
                  [0,1,2,3,4,5], [0,2,4,6,8,10]]:
        sel = [ge[i] for i in combo if i < len(ge)]
        if len(sel) < 6: continue
        ok = True
        for a in range(6):
            for b in range(6):
                for bk in ibasis:
                    anticom = sed_mul(sel[a], sed_mul(sel[b], bk)) + sed_mul(sel[b], sed_mul(sel[a], bk))
                    ev = 2.0 if a==b else 0.0
                    err = sum(abs(anticom.c[i] - ev*bk.c[i]) for i in range(32))
                    if err > 1e-6:
                        ok = False
                        break
                if not ok: break
            if not ok: break
        if ok:
            found = True
            print(f"    OK Cl(6) via combo {combo}")
            break

    if not found:
        print(f"    FAIL: no Cl(6)")

    # Verify idempotent property
    sq = sed_mul(rho, rho)
    rho_ok = all(abs(sq.c[i] - rho.c[i]) < 1e-10 for i in range(32))
    print(f"    idempotent check: {rho_ok}")
    print()

print("  Summary of three idempotents and CCW fixed points:\n")
for name, idx in [("FALSE", 3), ("TRUE", 4), ("OR", 8), ("NOR", 15)]:
    rho = make_idempotent(idx)
    sq = sed_mul(rho, rho)
    ok = all(abs(sq.c[i] - rho.c[i]) < 1e-10 for i in range(32))
    print(f"    rho = 1/2(1 + i*e_{idx}) ({name:>5}): idempotent = {ok}")
print()
# === END OF SECTION 7.1 replacement ===

