"""cl4xcl4_pati_salam.py
Rebuild Cl(8,0) = Cl(4)_A x Cl(4)_B using the correct chirality trick.
Then test Pati-Salam: does SU(4) x SU(2)^2 embed cleanly?

Key: chirality gamma_A = gA_1.gA_2.gA_3.gA_4 anti-commutes with all gA_i
when Cl(4,0) has dimension 4 (even -> n-1 = 3 is odd -> anti-commutes).
"""

import numpy as np
import itertools, math

sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)

def kron(*mats):
    r = mats[0]
    for m in mats[1:]: r = np.kron(r, m)
    return r

# Cl(4)_A and Cl(4)_B gamma matrices (4x4 each)
gA = [kron(sx, I2), kron(sy, I2), kron(sz, sx), kron(sz, sy)]
gB = [kron(sz, sx), kron(sz, sy), kron(sx, I2), kron(sy, I2)]

# Chirality: gamma_A = gA_0 * gA_1 * gA_2 * gA_3
gamma_A = gA[0] @ gA[1] @ gA[2] @ gA[3]

# Verify gamma_A anti-commutes with all gA_i
print("Verifying gamma_A anti-commutation with gA_i:")
for i in range(4):
    ac = gA[i] @ gamma_A + gamma_A @ gA[i]
    ok = np.max(np.abs(ac)) < 1e-10
    print(f"  gamma_A anti-commutes with gA_{i}: {ok}")
    if not ok:
        print(f"   ERROR: max|entry| = {np.max(np.abs(ac)):.2e}")
print()

# Cl(8,0) = Cl(4)_A x Cl(4)_B
G = [kron(g, I4) for g in gA] + [kron(gamma_A, g) for g in gB]

# Verify anti-commutation
print("Cl(8,0) anti-commutation:")
cl8_ok = True
for a in range(8):
    for b in range(8):
        ac = G[a] @ G[b] + G[b] @ G[a]
        exp = 2*np.eye(16, dtype=complex) if a == b else 0
        if not np.allclose(ac, exp, atol=1e-10):
            cl8_ok = False
            print(f"  FAIL {{G_{a+1}, G_{b+1}}}: {np.max(np.abs(ac)):.2e}")
print(f"  Cl(8,0): {cl8_ok}")
print()

# Build all 28 bivectors
def B(m,n):
    return 0.5j * (G[m] @ G[n] - G[n] @ G[m])

bivs = [B(m,n) for m in range(8) for n in range(m+1, 8)]
biv_labels = [(m+1,n+1) for m in range(8) for n in range(m+1, 8)]

# ═══════════════════════════════════════════════════════════════════
# so(6) ~ SU(4) from G1..G6
# ═══════════════════════════════════════════════════════════════════
so6 = [bivs[i] for i in range(15)]
so6_labels = biv_labels[:15]

# Verify closure
closed = True
for a in range(15):
    for b in range(a+1, 15):
        c = so6[a] @ so6[b] - so6[b] @ so6[a]
        in_sp = any(np.allclose(c, x, atol=1e-6) or np.allclose(c, -x, atol=1e-6) or
                    np.allclose(c, 1j*x, atol=1e-6) or np.allclose(c, -1j*x, atol=1e-6)
                    for x in so6)
        if not in_sp and np.max(np.abs(c)) > 1e-8:
            closed = False
print(f"so(6) ~ SU(4): {len(so6)} generators, closure: {closed}")

# ═══════════════════════════════════════════════════════════════════
# so(4) from G5..G8 -> SU(2)_L x SU(2)_R
# ═══════════════════════════════════════════════════════════════════
# Bivectors from G5..G8: indices in the full list are:
# G5=4, G6=5, G7=6, G8=7 -> indices 6..11 in 0-indexed biv list
# Specifically: (4,5)=6, (4,6)=7, (4,7)=8, (5,6)=9, (5,7)=10, (6,7)=11

# so(4) from G5..G8: the last 6 bivectors in the list
# G5=4, G6=5, G7=6, G8=7
# In bivector enumeration with m in 0..7, n in m+1..8:
# Before m=4: m=0 (7) + m=1 (6) + m=2 (5) + m=3 (4) = 22 bivectors
# so(4) indices: (4,5)=22, (4,6)=23, (4,7)=24, (5,6)=25, (5,7)=26, (6,7)=27

so4_idx = [22, 23, 24, 25, 26, 27]
so4 = [bivs[i] for i in so4_idx]
so4_labels = [biv_labels[i] for i in so4_idx]

print(f"\nso(4) from G5..G8: {len(so4)} generators")
for l, b in zip(so4_labels, so4):
    print(f"  {l}")

# Search for SU(2) triples in so(4)
su2_triples = []
for i,j,k in itertools.combinations(range(6), 3):
    T1,T2,T3 = so4[i], so4[j], so4[k]
    if (np.allclose(T1@T2-T2@T1, 1j*T3, atol=1e-6) and
        np.allclose(T2@T3-T3@T2, 1j*T1, atol=1e-6) and
        np.allclose(T3@T1-T1@T3, 1j*T2, atol=1e-6)):
        su2_triples.append(((i,j,k), [T1,T2,T3]))

print(f"SU(2) triples: {len(su2_triples)}")
for (i,j,k), _ in su2_triples:
    print(f"  {[so4_labels[x] for x in (i,j,k)]}")

# Find SU(2)_L x SU(2)_R pairs
su2xsu2 = []
for t1 in su2_triples:
    for t2 in su2_triples:
        (i1,j1,k1),_ = t1
        (i2,j2,k2),_ = t2
        if len({i1,j1,k1,i2,j2,k2}) != 6: continue
        T1a,T1b,T1c = t1[1]
        T2a,T2b,T2c = t2[1]
        if all(np.max(np.abs(T1 @ T2 - T2 @ T1)) < 1e-6
               for T1 in [T1a,T1b,T1c] for T2 in [T2a,T2b,T2c]):
            su2xsu2.append((t1, t2))

print(f"\nSU(2)_L x SU(2)_R pairs: {len(su2xsu2)}")
if su2xsu2:
    t1, t2 = su2xsu2[0]
    print(f"  L: {[so4_labels[x] for x in t1[0]]}")
    print(f"  R: {[so4_labels[x] for x in t2[0]]}")

# ═══════════════════════════════════════════════════════════════════
# [SO(4), SO(6)] = 0 ?
# ═══════════════════════════════════════════════════════════════════
print(f"\n[so(6), so(4)] commutation:")

if su2xsu2:
    T1_all = [su2xsu2[0][0][1][i] for i in range(3)] + [su2xsu2[0][1][1][i] for i in range(3)]
else:
    T1_all = so4

comm_ok = True
for T in T1_all:
    for s in so6:
        err = np.max(np.abs(T @ s - s @ T))
        if err > 1e-6:
            comm_ok = False
            break
    if not comm_ok:
        break

print(f"[SU(4), SU(2)^2] = 0: {comm_ok}")

if not comm_ok:
    # Check on 8C spinor
    print("On 8C spinor:")
    comm_8 = True
    for T in T1_all:
        T8 = T[:8,:8]
        for s in so6:
            s8 = s[:8,:8]
            if np.max(np.abs(T8 @ s8 - s8 @ T8)) > 1e-6:
                comm_8 = False
                break
        if not comm_8: break
    print(f"  [SU(4), SU(2)^2] = 0: {comm_8}")

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  Cl(8,0) = Cl(4) x Cl(4): {cl8_ok}
  so(6) closure: {closed}
  SU(2) triples in so(4): {len(su2_triples)}
  SU(2)_L x SU(2)_R pairs: {len(su2xsu2)}
  [SU(4), SU(2)^2] = 0: {comm_ok}
  
  Verdict: Pati-Salam SU(4) x SU(2)^2 embeds in Cl(4)xCl(4) basis: {comm_ok or (not comm_ok and comm_8)}
""")
