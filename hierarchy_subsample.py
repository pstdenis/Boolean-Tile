"""hierarchy_subsample.py
Explore the recursive subsampling structure:
  n=3 (8x8, 256 funcs) -> downsample by fixing C -> n=2 (4x4, 16 funcs)
  n=2 (4x4, 16 funcs)  -> downsample by fixing B -> n=1 (2x2, 4 funcs)

This shows that higher-n tiles CONTAIN lower-n tiles as subsamples,
forming a fractal hierarchy matching the IFS structure.
"""

import itertools, collections

# ═══════════════════════════════════════════════════════════════
# 1. Truth tables and Walsh transforms for all n
# ═══════════════════════════════════════════════════════════════

def walsh_1(tt):
    """2-pt Walsh: (a, x)."""
    return (tt[0] + tt[1], tt[0] - tt[1])

def walsh_2(tt):
    """4-pt Walsh: (a, x, y, z)."""
    v00, v01, v10, v11 = tt
    return (v00+v01+v10+v11, v00-v01+v10-v11,
            v00+v01-v10-v11, v00-v01-v10+v11)

def walsh_3(tt):
    """8-pt Walsh via explicit Hadamard matrix: (DC, R_A, R_B, R_AB, R_C, R_AC, R_BC, R_ABC)."""
    h8 = [
        [1,1,1,1,1,1,1,1],
        [1,-1,1,-1,1,-1,1,-1],
        [1,1,-1,-1,1,1,-1,-1],
        [1,-1,-1,1,1,-1,-1,1],
        [1,1,1,1,-1,-1,-1,-1],
        [1,-1,1,-1,-1,1,-1,1],
        [1,1,-1,-1,-1,-1,1,1],
        [1,-1,-1,1,-1,1,1,-1],
    ]
    return tuple(sum(h8[i][j] * tt[j] for j in range(8)) for i in range(8))

# ═══════════════════════════════════════════════════════════════
# 2. The n=1 tiles (4 functions of 1 variable)
# ═══════════════════════════════════════════════════════════════

N1_TABLES = {
    "FALSE": (0,0),
    "P":     (0,1),
    "NOT P": (1,0),
    "TRUE":  (1,1),
}

print("=== n=1: 4 functions of 1 variable ===")
print(f"  {'Name':>8} | tt     | Walsh")
print(f"  {'-'*8}-+------- +-------")
for name, tt in N1_TABLES.items():
    w = walsh_1(tt)
    print(f"  {name:>8} | {tt} | ({w[0]}, {w[1]})")
print()

# ═══════════════════════════════════════════════════════════════
# 3. The n=2 tiles (16 functions of 2 variables)
# ═══════════════════════════════════════════════════════════════

N2_TABLES = {}
for idx in range(16):
    # Build truth table from index bits
    v00 = (idx >> 3) & 1
    v01 = (idx >> 2) & 1
    v10 = (idx >> 1) & 1
    v11 = idx & 1
    tt = (v00, v01, v10, v11)
    w = walsh_2(tt)
    N2_TABLES[idx] = (tt, w)

# Map name -> truth table for n=2 tiles
N2_NAMES = {
    0: "FALSE", 1: "AND", 2: "A_AND_NOTB", 3: "A",
    4: "NOTA_AND_B", 5: "B", 6: "XOR", 7: "OR",
    8: "NOR", 9: "XNOR", 10: "NOTB", 11: "B_IMP_A",
    12: "NOTA", 13: "A_IMP_B", 14: "NAND", 15: "TRUE",
}

print("=== n=2: 16 functions of 2 variables ===")
# Show a few key ones
for idx in [0, 6, 7, 8, 12, 15]:
    tt, w = N2_TABLES[idx]
    print(f"  {N2_NAMES[idx]:>12} | {tt} | Walsh={w}")
print()

# ═══════════════════════════════════════════════════════════════
# 4. Downsampling: n=2 -> n=1 (fix B=0 or B=1)
# ═══════════════════════════════════════════════════════════════

print("=== Downsampling: n=2 -> n=1 ===")
print("  For each n=2 tile, fixing B=0 gives an n=1 tile:")
for idx in range(16):
    tt, w = N2_TABLES[idx]
    # Fix B: the truth table is (v00, v01, v10, v11)
    # Fix B=0: (v00, v10) where A varies
    # Fix B=1: (v01, v11)
    subsample_b0 = (tt[0], tt[2])  # B=0
    subsample_b1 = (tt[1], tt[3])  # B=1
    # Find which n=1 tile this matches
    n1_match_b0 = next((name for name, t in N1_TABLES.items() if t == subsample_b0), "?")
    n1_match_b1 = next((name for name, t in N1_TABLES.items() if t == subsample_b1), "?")
    print(f"  {N2_NAMES[idx]:>12} tt={tt} -> B=0:{n1_match_b0:>7} B=1:{n1_match_b1:>7}")
print()

# ═══════════════════════════════════════════════════════════════
# 5. Downsampling: n=3 -> n=2 (fix C=0 or C=1)
# ═══════════════════════════════════════════════════════════════

def n3_tt(idx):
    """8-row truth table for 3-var function idx (0..255)."""
    return tuple((idx >> (7-i)) & 1 for i in range(8))

# Build all n=3 functions
N3_ALL = [(idx, n3_tt(idx), walsh_3(n3_tt(idx))) for idx in range(256)]

print("=== Downsampling: n=3 -> n=2 ===")
print("  For n=3 tiles, fixing C gives two n=2 tiles.")
print()

# Count how many n=2 tiles appear as C=0 subsamples of n=3 tiles
n2_from_n3_c0 = collections.Counter()
n2_from_n3_c1 = collections.Counter()

for idx, tt, w in N3_ALL:
    # Fix C=0: take positions (A,B,0) = tt[0], tt[2], tt[4], tt[6]
    # Fix C=1: take positions (A,B,1) = tt[1], tt[3], tt[5], tt[7]
    sub0 = (tt[0], tt[2], tt[4], tt[6])
    sub1 = (tt[1], tt[3], tt[5], tt[7])
    # Find which n=2 tile index this matches
    idx0 = (sub0[0] << 3) | (sub0[1] << 2) | (sub0[2] << 1) | sub0[3]
    idx1 = (sub1[0] << 3) | (sub1[1] << 2) | (sub1[2] << 1) | sub1[3]
    n2_from_n3_c0[idx0] += 1
    n2_from_n3_c1[idx1] += 1

print(f"  C=0 subsamples: {len(n2_from_n3_c0)} of 16 n=2 tiles appear")
print(f"  C=1 subsamples: {len(n2_from_n3_c1)} of 16 n=2 tiles appear")
print()

# Show distribution
print("  Distribution of C=0 subsamples per n=2 tile:")
for idx in range(16):
    cnt0 = n2_from_n3_c0.get(idx, 0)
    cnt1 = n2_from_n3_c1.get(idx, 0)
    bar0 = "#" * (cnt0 // 4)
    bar1 = "#" * (cnt1 // 4)
    print(f"    {N2_NAMES[idx]:>12}: C=0 {cnt0:>4} {bar0}")
print()

# ═══════════════════════════════════════════════════════════════
# 6. Example: a specific n=3 function and its two n=2 subsamples
# ═══════════════════════════════════════════════════════════════

print("=== Example: n=3 tile and its n=2 children ===")
# Pick an interesting n=3 function
# Let's find one where both C=0 and C=1 subsamples are "interesting"
for idx, tt, w in N3_ALL:
    sub0 = (tt[0], tt[2], tt[4], tt[6])
    sub1 = (tt[1], tt[3], tt[5], tt[7])
    idx0 = (sub0[0] << 3) | (sub0[1] << 2) | (sub0[2] << 1) | sub0[3]
    idx1 = (sub1[0] << 3) | (sub1[1] << 2) | (sub1[2] << 1) | sub1[3]
    # Pick XOR and NOR as children
    if idx0 == 6 and idx1 == 8:  # XOR(6) and NOR(8)
        print(f"  n=3 idx={idx:>3} tt={tt}")
        print(f"    Walsh={w}")
        print(f"    C=0 -> {N2_NAMES[idx0]} (idx={idx0}) tt={sub0}")
        print(f"    C=1 -> {N2_NAMES[idx1]} (idx={idx1}) tt={sub1}")
        print()
        break

# Find the n=3 function whose both C=0 and C=1 subsamples match
# the n=2 identity element (FALSE=0)
for idx, tt, w in N3_ALL:
    sub0 = (tt[0], tt[2], tt[4], tt[6])
    sub1 = (tt[1], tt[3], tt[5], tt[7])
    idx0 = (sub0[0] << 3) | (sub0[1] << 2) | (sub0[2] << 1) | sub0[3]
    idx1 = (sub1[0] << 3) | (sub1[1] << 2) | (sub1[2] << 1) | sub1[3]
    if idx0 == 0 and idx1 == 0:
        print(f"  n=3 const-0: idx={idx:>3} tt={tt}")
        print(f"    Both C=0 and C=1 -> FALSE")
        print()
        break

# ═══════════════════════════════════════════════════════════════
# 7. The full hierarchy: every n=3 tile decomposes into 2 n=2 tiles
#    which each decompose into 2 n=1 tiles (a binary tree of depth 2)
# ═══════════════════════════════════════════════════════════════

print("=== Recursive subsampling tree ===")
print("  Every n=3 function f(A,B,C) gives:")
print("    C=0 -> f(A,B,0) = n=2 tile")
print("    C=1 -> f(A,B,1) = n=2 tile")
print("  Every n=2 function g(A,B) gives:")
print("    B=0 -> g(A,0) = n=1 tile")
print("    B=1 -> g(A,1) = n=1 tile")
print()

# Verify: 256 n=3 functions x 2 subsamples = 512 n=2 "slots"
# Each n=2 slot maps to one of 16 n=2 tiles
# Expected: each n=2 tile appears 512/16 = 32 times as a C-subsample
c0_total = sum(n2_from_n3_c0.values())
c1_total = sum(n2_from_n3_c1.values())
print(f"  Total C=0 subsamples: {c0_total} (expected {256})")
print(f"  Total C=1 subsamples: {c1_total} (expected {256})")
print(f"  Avg per n=2 tile: {c0_total/16:.1f}")
print()

# ═══════════════════════════════════════════════════════════════
# 8. Connection: the subsampling structure is the IFS attractor
#    The n=3 Boolean functions form an IFS fractal where each
#    n=3 tile is built from n=2 tiles by the IFS rules.
# ═══════════════════════════════════════════════════════════════

print("=== IFS interpretation ===")
print("  The Walsh-Hadamard transform defines the IFS:")
print("    n=1: {FALSE, P, NOT P, TRUE} = IFS attractor at depth 1")
print("    n=2: {16 tiles} = IFS attractor at depth 2")
print("      each tile has 2x2 block structure from n=1 tiles")
print("    n=3: {256 tiles} = IFS attractor at depth 3")
print("      each tile has 2x2 block structure from n=2 tiles")
print()
print("  The subsampling corresponds to the inverse IFS:")
print("    n=3 -> fix C -> two n=2 tiles = two branches of IFS")
print("    n=2 -> fix B -> two n=1 tiles = two branches of IFS")
print()
print("  Consequence: the IFS depth n gives Cl(2n, 0) algebra")
print("  and the n-th Kitaev classification Z_{2^{n-1}}")
print()

# ═══════════════════════════════════════════════════════════════
# 9. Key identities: Walsh coefficients of subsamples
# ═══════════════════════════════════════════════════════════════

print("=== Walsh coefficients of C-subsamples ===")
print("  For an n=3 function with Walsh (a, x, y, z, c, xc, yc, zc):")
print("  The C=0 and C=1 subsamples (at AB positions) mix across Walsh coeffs.")
print("  Using reordered truth table [C=0 entries, C=1 entries]:")
print("    Walsh2(C=0) = ((a+z+c+zc)/2, (x+y+xc+yc)/2, (x-y+xc-yc)/2, (a-z+c-zc)/2)")
print("    Walsh2(C=1) = ((a+z-c-zc)/2, (x+y-xc-yc)/2, (x-y-xc+yc)/2, (a-z-c+zc)/2)")
print()

# Verify with correct reordering
print("  Verification (direct subsample computation):")
for idx in [0, 42, 105, 200]:
    tt, w = None, None
    for i, t, wv in N3_ALL:
        if i == idx:
            tt, w = t, wv
            break
    # C=0 subsample at positions 0,2,4,6 in n=3 order -> reorder to C-first order
    c0 = (tt[0], tt[2], tt[4], tt[6])  # (AB=00,01,10,11)
    c1 = (tt[1], tt[3], tt[5], tt[7])
    w_c0 = walsh_2(c0)
    w_c1 = walsh_2(c1)
    print(f"  idx={idx:>3}: C=0 Walsh={w_c0}, C=1 Walsh={w_c1}")
print()

print("=== Summary ===")
print("  The hierarchy n=3 -> n=2 -> n=1 is a recursive IFS:")
print("  Each Boolean function of k variables contains 2 functions")
print("  of k-1 variables as its C-fixed subsamples.")
print("  The Walsh coefficients transform linearly under subsampling.")
print("  This is the computational foundation of the IFS tile system:")
print("    n=1: 2x2 tile = 4 truth table entries")
print("    n=2: 4x4 tile = 16 entries (4 n=1 tiles)")
print("    n=3: 8x8 tile = 64 entries (16 n=2 tiles)")
print("    n=k: 2^k x 2^k tile = 2^{2k} entries (2^{2^{k-1}} n=k-1 tiles)")
print()
