"""boole_n3.py
Explore the n=3 generalization: 256 Boolean functions of 3 variables,
Cl(8,0), S3 symmetry, and the 8-fold/64-fold Kitaev classification.

For n variables:
  - 2^n truth table rows
  - 2^(2^n) Boolean functions
  - Each embeds in Cl(2^n, 0), the natural n-variable Clifford algebra
  - The Walsh-Hadamard transform H2^(x)n gives 2^n spectral coefficients
  - Permutations of variables act as symmetries (S_n on truth table indices)

n=2:  4 rows    16 functions    Cl(4,0) ≅ M2(H)    16-fold way
n=3:  8 rows   256 functions    Cl(8,0) ≅ M16(R)    ?
"""

import math, itertools, functools, collections

# ═══════════════════════════════════════════════════════════════════
# 1. All 256 truth tables of 3 variables, ordered by index
# ═══════════════════════════════════════════════════════════════════

# For 3 variables (A, B, C), truth table ordering:
# (A,B,C) = (0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)
# index = A*4 + B*2 + C

def make_tt_3(index):
    """Return truth table tuple (v000,...,v111) for given index 0..255."""
    return tuple((index >> (7 - i)) & 1 for i in range(8))

def walsh_3(tt):
    """8-point Walsh-Hadamard transform (H2^3, unnormalized)."""
    # Use the recursion: H2^(n+1) = H2 @ H2^n (Kronecker product)
    # For 3 variables, we can use the 8x8 Hadamard matrix
    h2 = [[1,1],[1,-1]]
    # Build H2^3
    def kron(A, B):
        return [[a*b for a in rowA for b in B_row] for rowA in A for B_row in B]
    h4 = kron(h2, h2)
    h8 = kron(h4, h2)
    result = [0]*8
    for i in range(8):
        s = 0
        for j in range(8):
            s += h8[i][j] * tt[j]
        result[i] = s
    return tuple(result)

# Walsh coefficient indices (Walsh ordering):
# 0: DC (a)
# 1: R0 (A)
# 2: R1 (B)
# 3: R0R1 (A xor B)
# 4: R2 (C)
# 5: R0R2 (A xor C)
# 6: R1R2 (B xor C)
# 7: R0R1R2 (A xor B xor C)

WALSH_NAMES = ["DC", "R_A", "R_B", "R_AB", "R_C", "R_AC", "R_BC", "R_ABC"]

# Build all 256 functions
ALL_3 = []
for idx in range(256):
    tt = make_tt_3(idx)
    w = walsh_3(tt)
    ALL_3.append((idx, tt, w))

print("=" * 80)
print("n=3 GENERALIZATION: 256 BOOLEAN FUNCTIONS, Cl(8,0), KITAEV 8-FOLD WAY")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════
# 2. DC parity and norm distribution
# ═══════════════════════════════════════════════════════════════════

print("\n--- 2.1 DC parity (a = sum of truth table entries) ---\n")

dc_counts = collections.Counter()
for idx, tt, w in ALL_3:
    dc = w[0]
    dc_counts[dc] += 1

print(f"  DC (truth table count) distribution:")
for dc, cnt in sorted(dc_counts.items()):
    parity = "even" if dc % 2 == 0 else "odd"
    print(f"    DC={dc:>2} ({parity}): {cnt:>3} functions")

even_count = sum(cnt for dc, cnt in dc_counts.items() if dc % 2 == 0)
odd_count = sum(cnt for dc, cnt in dc_counts.items() if dc % 2 == 1)
print(f"\n  Even DC: {even_count}, Odd DC: {odd_count}")
print(f"  Ratio: {even_count/odd_count:.2f} (exact: {even_count}/{odd_count})")

print()

# The paper's key insight for n=2: odd DC = non-Abelian tiles.
# For n=3, the DC (Walsh coefficient a) ranges from 0 to 8.

# ═══════════════════════════════════════════════════════════════════
# 3. Graded structure under Cl(8,0)
# ═══════════════════════════════════════════════════════════════════

print("--- 3.1 Cl(8,0) graded structure ---\n")

# In Cl(8,0), the 8 Walsh coefficients span the grade-1 subspace.
# The full algebra has 256 basis elements indexed by subsets of {0,...,7}.
# Each subset S gives the product of basis vectors: e_S = prod_{i in S} e_i.
# The grade of e_S is |S|.

# The Boolean functions correspond to these 256 basis elements via
# the Walsh spectrum: the support of the function in Walsh space defines
# its grade.

# Grade distribution:
grade_counts = collections.Counter()
for idx, tt, w in ALL_3:
    # Grade = number of non-zero Walsh coefficients (excluding DC)
    nz = sum(1 for i, c in enumerate(w) if c != 0)
    grade_counts[nz] += 1

print(f"  Grade (non-zero Walsh coeffs) distribution:")
for grade in sorted(grade_counts.keys()):
    cnt = grade_counts[grade]
    pct = 100 * cnt / 256
    print(f"    Grade {grade} ({grade} non-zero coeffs): {cnt:>3} functions ({pct:.1f}%)")

print()

# Compare with binomial coefficients:
print(f"  Expected for Cl(8,0): C(8,k) for grade k:")
for k in range(9):
    expected = math.comb(8, k)
    actual = grade_counts.get(k, 0)
    print(f"    Grade {k}: expected C(8,{k})={expected:>3}, actual={actual:>3}")

print()
print(f"  Note: The grade distribution does NOT match Cl(8,0) basis")
print(f"  because the Walsh coefficients are integers (0 to 8), not")
print(f"  {0,1} bits. The Boolean functions map to integer vectors in")
print("  Z^8, not F2^8. The Z2 group structure is in function space")
print(f"  (pointwise XOR), which maps to coefficient-wise addition.")
print()

# ═══════════════════════════════════════════════════════════════════
# 4. Exchange phases (generalized)
# ═══════════════════════════════════════════════════════════════════

print("--- 4.1 Generalized exchange phases ---\n")

# For n=2, the exchange phase is theta = e^{i*z*pi/4} where z = w[3] (R0R1).
# For n=3, we have multiple "pairwise" exchange phases:
#   R_AB: theta_AB = e^{i*w[3]*pi/8}  (ZZ coupling on AB)
#   R_AC: theta_AC = e^{i*w[5]*pi/8}  (ZZ coupling on AC)
#   R_BC: theta_BC = e^{i*w[6]*pi/8}  (ZZ coupling on BC)
#   R_ABC: theta_ABC = e^{i*w[7]*pi/8}  (ZZZ coupling on ABC)

# The "total exchange phase" is the product of all non-zero pairwise phases.
# Non-Abelian tiles are those with at least one odd non-zero coupling.

# Let's classify by the pattern of non-zero R coefficients
pattern_counts = collections.Counter()
for idx, tt, w in ALL_3:
    # Pattern of which non-DC coefficients are non-zero
    pattern = tuple(1 if w[i] != 0 else 0 for i in range(1, 8))
    pattern_counts[pattern] += 1

print(f"  Distinct non-zero patterns: {len(pattern_counts)}")
print()

# Focus on the "all non-zero" and "all-zero" extremes
all_nonzero = [p for p, cnt in pattern_counts.items() if sum(p) == 7]
all_zero = [p for p, cnt in pattern_counts.items() if sum(p) == 0]
print(f"  All 7 non-DC coeffs non-zero: {len(all_nonzero)} functions")
print(f"  All 7 non-DC coeffs zero: {len(all_zero)} functions")

# For the "all non-zero" case, show the first few
if all_nonzero:
    print(f"  Example functions with all 7 non-DC coeffs non-zero:")
    count_shown = 0
    for idx, tt, w in ALL_3:
        pattern = tuple(1 if w[i] != 0 else 0 for i in range(1, 8))
        if sum(pattern) == 7 and count_shown < 4:
            # Compute the total exchange phase magnitude
            phases = [abs(w[i]) * math.pi / 8 for i in range(1, 8)]
            total_phase = sum(phases) % (2*math.pi)
            print(f"    idx={idx:>3}: Walsh={w}  |theta|_total={total_phase:.4f}")
            count_shown += 1

print()

# ═══════════════════════════════════════════════════════════════════
# 5. S3 symmetry: permuting the 3 variables
# ═══════════════════════════════════════════════════════════════════

print("--- 5.1 S3 symmetry on truth tables ---\n")

# The 3 variables A, B, C can be permuted by S3.
# This acts on the truth table indices (bit positions).
# E.g., swapping A and B swaps the bit positions for A and B in the index.
# So index i = a*4 + b*2 + c becomes a*4 + c*2 + b under A<->C swap.

def permute_tt(tt, perm):
    """Permute the variables of a 3-variable truth table.
    perm = (pa, pb, pc) where the new variable ordering is (v_pa, v_pb, v_pc).
    """
    result = [0]*8
    for i in range(8):
        # Extract original bits
        a = (i >> 2) & 1
        b = (i >> 1) & 1
        c = i & 1
        bits = [a, b, c]
        # Reorder by permutation
        new_bits = (bits[perm[0]], bits[perm[1]], bits[perm[2]])
        new_idx = new_bits[0]*4 + new_bits[1]*2 + new_bits[2]
        result[new_idx] = tt[i]
    return tuple(result)

# S3 elements as permutations of (A,B,C)
S3 = [
    (0,1,2),  # identity
    (0,2,1),  # swap B<->C
    (1,0,2),  # swap A<->B
    (1,2,0),  # 3-cycle: A->B->C->A
    (2,0,1),  # 3-cycle: A->C->B->A
    (2,1,0),  # swap A<->C
]

S3_NAMES = ["id", "B~C", "A~B", "A>B>C>A", "A>C>B>A", "A~C"]

# Orbit analysis: which functions form orbits under S3?
orbits = {}
unvisited = set(range(256))

while unvisited:
    start = min(unvisited)
    orbit = set()
    stack = [start]
    while stack:
        idx = stack.pop()
        if idx in orbit:
            continue
        orbit.add(idx)
        tt = ALL_3[idx][1]
        for perm in S3:
            perm_tt = permute_tt(tt, perm)
            # Find the index of this permuted tt
            for j in range(256):
                if ALL_3[j][1] == perm_tt:
                    if j not in orbit:
                        stack.append(j)
                    break
    orbits[start] = orbit
    unvisited -= orbit

orbit_sizes = collections.Counter(len(o) for o in orbits.values())
print(f"  S3 orbit sizes:")
for size in sorted(orbit_sizes.keys()):
    cnt = orbit_sizes[size]
    print(f"    Size {size}: {cnt} orbits ({cnt*size} functions)")

print()

# Fixed points of the 3-cycle (the analogue of CCW fixed points):
def find_fixed(perm, perm_name):
    fixed = []
    for idx, tt, w in ALL_3:
        perm_tt = permute_tt(tt, perm)
        if perm_tt == tt:
            fixed.append((idx, tt, w))
    return fixed

print("  Fixed points under the 3-cycle A->B->C->A:")
fixed_3cycle = find_fixed(S3[3], "A>B>C>A")
for idx, tt, w in fixed_3cycle[:8]:
    print(f"    idx={idx:>3}: tt={tt}  Walsh=({w[0]:>2},{w[1]:>2},{w[2]:>2},{w[3]:>2},{w[4]:>2},{w[5]:>2},{w[6]:>2},{w[7]:>2})")
extra = len(fixed_3cycle) - 8
if extra > 0:
    print(f"    ... and {extra} more")
print(f"  Total: {len(fixed_3cycle)} functions fixed under the 3-cycle")

print()

# ═══════════════════════════════════════════════════════════════════
# 6. Kitaev 8-fold way / 64-fold way
# ═══════════════════════════════════════════════════════════════════

print("--- 6.1 Classification analogies ---\n")

# For 3 fermion modes, Kitaev's classification gives 2^3 = 8 distinct
# topological phases (the "8-fold way" for 3 Majorana modes).
# The exchange phase is theta = e^{i*pi*nu/8} for nu in Z_8.

# The Walsh coefficients for n=3 give generalized Ising couplings.
# The "Hamiltonian" for a 3-qubit gate is:
#   H = sum_{S subset of {A,B,C}, S nonempty} J_S * Z^otimes_S
# where J_S = w[S] * pi / 8 (using the Walsh coefficient as coupling).

# Let's compute the analogue of the "non-Abelian" condition:
# tiles where ALL 7 couplings are non-zero (the "maximally entangling" case).
max_entangling = []
for idx, tt, w in ALL_3:
    if all(w[i] != 0 for i in range(1, 8)):
        max_entangling.append((idx, tt, w))

print(f"  Maximally entangling (all 7 non-zero): {len(max_entangling)} functions")
print(f"  Out of 256 total = {100*len(max_entangling)/256:.1f}%")
print()

# Show a few examples
for idx, tt, w in max_entangling[:4]:
    phases = [w[i] * math.pi / 8 for i in range(1, 8)]
    print(f"    idx={idx:>3}: Walsh={w}")
    print(f"      Phases: {[f'{p:.4f}' for p in phases]}")

print()

# ═══════════════════════════════════════════════════════════════════
# 7. Comparison: n=2 vs n=3
# ═══════════════════════════════════════════════════════════════════

print("--- 7.1 n=2 vs n=3 comparison ---\n")

comparison = [
    ("Variables", "2", "3"),
    ("Truth table rows", "4", "8"),
    ("Boolean functions", "16", "256"),
    ("Clifford algebra", "Cl(4,0) ≅ M2(H)", "Cl(8,0) ≅ M16(R)"),
    ("Algebra dimension", "16", "256"),
    ("Non-DC Walsh coeffs", "3", "7"),
    ("Ising parameters", "J, h1, h2", "J_AB, J_AC, J_BC, h_A, h_B, h_C, K_ABC"),
    ("Symmetry group", "C2 (CW/CCW)", "S3 (6 elements)"),
    ("CCW 3-cycles", "On (x,y,z) triple", "On higher orbits under S3"),
    ("Kitaev phases", "nu in Z_16", "nu in Z_8 (?)"),
    ("Max entangling", "8 (50%)", f"{len(max_entangling)} ({100*len(max_entangling)/256:.1f}%)"),
]

print(f"  {'Property':>30}  {'n=2':>25}  {'n=3':>25}")
print("  " + "-" * 82)
for prop, v2, v3 in comparison:
    print(f"  {prop:>30}  {v2:>25}  {v3:>25}")

print()

# ═══════════════════════════════════════════════════════════════════
# 8. The n-parameter hierarchy
# ═══════════════════════════════════════════════════════════════════

print("--- 8.1 The n-parameter hierarchy ---\n")

print("""
  The generalization for n Boolean variables follows the pattern:

    n variables -> 2^n truth table rows -> 2^(2^n) Boolean functions
            |              |                          |
            v              v                          v
      S_n symmetry    Cl(2^n, 0) Clifford algebra    dimension 2^(2^n)

  The Cayley-Dickson "ion" correspondence:

    n=0:  1 row    2 functions   R            Cl(1,0)   dim 2
    n=1:  2 rows   4 functions   C            Cl(2,0)   dim 4
    n=2:  4 rows  16 functions   H            Cl(4,0)   dim 16
    n=3:  8 rows  256 functions  O            Cl(8,0)   dim 256
    n=4: 16 rows  65536 func.    S (sedenions) Cl(16,0) dim 65536

  Bott periodicity: Cl(n+8,0) ≅ Cl(n,0) ⊗ M16(R)
  This 8-fold periodicity of Clifford algebras matches the
  8-fold periodicity of the Kitaev periodic table of
  topological insulators/superconductors!

  Key insight: The paper's "16-fold way" for n=2 is the n=2
  case of a general 2^(n-1)-fold way for n variables. The
  n=3 case would give an 8-fold way, and n=4 would give
  a 4-fold way (repeating every 8 by Bott periodicity).

  The pattern of topological insulators by Altland-Zirnbauer
  symmetry class has 8-fold periodicity. Kitaev's 16 for the
  honeycomb model is specifically 2*8 = 16 because of the
  two-sublattice structure. For n=3 (3 Majorana modes per
  cell), the classification would be mod 8 (the 8-fold way).
""")

print("  Summary of the hierarchy:")
print()
print(f"  {'n':>2} | {'rows':>5} | {'funcs':>6} | {'algebra':>10} | {'dim':>5} | {'Kitaev':>10} | {'division alg':>10}")
print("  " + "-" * 70)
for n in range(0, 5):
    rows = 2**n
    funcs = 2**(2**n)
    alg = f"Cl({2**n},0)"
    dim = 2**(2**n)
    kitaev_phases = 2**(n-1) if n >= 1 else 1
    kitaev_str = f"Z_{kitaev_phases}" if kitaev_phases <= 64 else "?"
    ions = ["R", "C", "H", "O", "S"][n] if n < 5 else "?"
    print(f"  {n:>2} | {rows:>5} | {funcs:>6} | {alg:>10} | {dim:>5} | {kitaev_str:>10} | {ions:>10}")
print()
