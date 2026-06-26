"""pati_salam.py
Test Pati-Salam SU(4) x SU(2)_L x SU(2)_R embedding in Cl(8,0).

Key questions:
1. Does SU(4) = so(6) from G1..G6 commute with SU(2)xSU(2) from G5..G8?
2. Do the 6 so(4) bivectors split into su(2)_L x su(2)_R?
3. Is sigma_z coupling the issue (as with SU(3)xSU(2))?

If yes: Pati-Salam fits in so(8) naturally. SU(3)xU(1) from SU(4) breaking.
If no: need alternative Cl(8,0) basis or Cl(16,0).
"""

import numpy as np
import itertools, math

# ═══════════════════════════════════════════════════════════════════
# 1. Cl(8,0) in sigma_z-extended representation (Rep A)
# ═══════════════════════════════════════════════════════════════════

sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)

def kron(*mats):
    r = mats[0]
    for m in mats[1:]: r = np.kron(r, m)
    return r

G6 = [
    kron(sx, I2, I2), kron(sy, I2, I2),
    kron(sz, sx, I2), kron(sz, sy, I2),
    kron(sz, sz, sx), kron(sz, sz, sy),
]

G = [np.kron(g, sz) for g in G6]  # G1..G6 with sigma_z
G.append(np.kron(I8, sx))          # G7
G.append(np.kron(I8, sy))          # G8

# Verify
print("=" * 70)
print("PATI-SALAM SU(4) x SU(2)^2 IN Cl(8,0)")
print("=" * 70)
cl8_ok = all(np.allclose(G[a]@G[b]+G[b]@G[a],
                         2*np.eye(16,dtype=complex) if a==b else 0,
                         atol=1e-10) for a in range(8) for b in range(8))
print(f"Cl(8,0) verified: {cl8_ok}")

# All 28 bivectors
def B(m,n):
    return 0.5j * (G[m]@G[n] - G[n]@G[m])

biv_list = [B(m,n) for m in range(8) for n in range(m+1,8)]
biv_labels = [(m+1,n+1) for m in range(8) for n in range(m+1,8)]

# ═══════════════════════════════════════════════════════════════════
# 2. so(6) ~ SU(4) from G1..G6: 15 generators
# ═══════════════════════════════════════════════════════════════════

so6 = [B(m,n) for m in range(6) for n in range(m+1,6)]
so6_labels = [(m+1,n+1) for m in range(6) for n in range(m+1,6)]
so6_names = [f"B_{m+1}{n+1}" for m in range(6) for n in range(m+1,6)]

print(f"\nso(6) ~ SU(4) generators: {len(so6)} (expected 15)")

# Verify closure: su(4)
closed = True
for a in range(15):
    for b in range(a+1,15):
        c = so6[a] @ so6[b] - so6[b] @ so6[a]
        in_sp = any(np.allclose(c, x, atol=1e-6) or np.allclose(c, -x, atol=1e-6)
                    or np.allclose(c, 1j*x, atol=1e-6) or np.allclose(c, -1j*x, atol=1e-6)
                    for x in so6)
        if not in_sp and np.max(np.abs(c)) > 1e-8:
            closed = False
print(f"so(6) closure: {closed}")

# ═══════════════════════════════════════════════════════════════════
# 3. so(4) from G5..G8: 6 generators -> su(2)_L x su(2)_R
# ═══════════════════════════════════════════════════════════════════

so4 = [B(m,n) for m in range(4,8) for n in range(m+1,8)]  # G5..G8
so4_labels = [(m+1,n+1) for m in range(4,8) for n in range(m+1,8)]

# Search for SU(2) x SU(2) splitting
# Find all triples that form su(2)
print(f"\nso(4) from G5..G8: {len(so4)} generators")

su2_triples = []
for i,j,k in itertools.combinations(range(6), 3):
    T1,T2,T3 = so4[i], so4[j], so4[k]
    if (np.allclose(T1@T2-T2@T1, 1j*T3, atol=1e-6) and
        np.allclose(T2@T3-T3@T2, 1j*T1, atol=1e-6) and
        np.allclose(T3@T1-T1@T3, 1j*T2, atol=1e-6)):
        su2_triples.append(((i,j,k), [T1,T2,T3]))

print(f"SU(2) triples in so(4): {len(su2_triples)}")

# Two SU(2) factors should be complementary: find pairs of triples
# that commute with each other
su2xsu2_pairs = []
for t1 in su2_triples:
    for t2 in su2_triples:
        (i1,j1,k1), [T1a,T1b,T1c] = t1
        (i2,j2,k2), [T2a,T2b,T2c] = t2
        # Check disjoint indices
        if len({i1,j1,k1,i2,j2,k2}) != 6:
            continue
        # Check commutation: [T1, T2] = 0
        if all(np.max(np.abs(T1 @ T2 - T2 @ T1)) < 1e-6
               for T1 in [T1a,T1b,T1c] for T2 in [T2a,T2b,T2c]):
            su2xsu2_pairs.append((t1, t2))

print(f"SU(2)_L x SU(2)_R pairs: {len(su2xsu2_pairs)}")
if su2xsu2_pairs:
    (i1,j1,k1),_ = su2xsu2_pairs[0][0]
    (i2,j2,k2),_ = su2xsu2_pairs[0][1]
    lab1 = [so4_labels[x] for x in (i1,j1,k1)]
    lab2 = [so4_labels[x] for x in (i2,j2,k2)]
    print(f"  SU(2)_L: {lab1}")
    print(f"  SU(2)_R: {lab2}")

# ═══════════════════════════════════════════════════════════════════
# 4. Commutation: [so(6), so(4)] = 0?
# ═══════════════════════════════════════════════════════════════════

print(f"\n[so(6), so(4)] check:")

if su2xsu2_pairs:
    (i1,j1,k1), [T1a,T1b,T1c] = su2xsu2_pairs[0][0]
    (i2,j2,k2), [T2a,T2b,T2c] = su2xsu2_pairs[0][1]
    su2_all = [T1a,T1b,T1c,T2a,T2b,T2c]
else:
    su2_all = so4

# Check [so(6), each SU(2) generator] = 0
all_comm = True
for T in su2_all:
    for s in so6:
        err = np.max(np.abs(T @ s - s @ T))
        if err > 1e-6:
            all_comm = False
            break
    if not all_comm:
        break

print(f"[SU(4), SU(2)^2] = 0: {all_comm}")

if not all_comm:
    # The sigma_z factor couples them. Try on the 8C spinor (first 8 dims)
    print("Checking on 8C spinor subspace:")
    all_comm_8 = True
    for T in su2_all:
        T8 = T[:8,:8]
        for s in so6:
            s8 = s[:8,:8]
            err = np.max(np.abs(T8 @ s8 - s8 @ T8))
            if err > 1e-6:
                all_comm_8 = False
                break
        if not all_comm_8:
            break
    print(f"[SU(4), SU(2)^2] = 0 on 8C spinor: {all_comm_8}")

    if all_comm_8:
        print("\nSU(4) x SU(2)^2 embeds in Cl(8,0) on the 8C spinor!")
        print("Pati-Salam verified in this basis.")
    else:
        print("\nSU(4) x SU(2)^2 does NOT embed in this Cl(8,0) basis.")
        print("Need Cl(6) x Cl(2) with separate tensor factors.")

# ═══════════════════════════════════════════════════════════════════
# 5. 8C spinor decomposition under SU(4)
# ═══════════════════════════════════════════════════════════════════

print(f"\n5. 8C spinor under SU(4) ~ so(6):")

# Cartan of so(6): H12, H34, H56
H12_8 = B(0,1)[:8,:8]
H34_8 = B(2,3)[:8,:8]
H56_8 = B(4,5)[:8,:8]

# Find common eigenbasis
ev0, ev0v = np.linalg.eigh(H12_8)
print("Eigenvalues of (H12, H34, H56):")
for v0 in sorted(set(round(x.real, 6) for x in ev0)):
    m = [abs(ev0[i].real - v0) < 1e-6 for i in range(8)]
    sp = ev0v[:, m]
    if sp.shape[1] == 0: continue
    # Diagonalize H34 in this subspace
    h34p = sp.conj().T @ H34_8 @ sp
    e34 = np.linalg.eigvalsh(h34p)
    for v34 in sorted(set(round(x.real, 6) for x in e34)):
        # Then H56
        m2 = [abs(e34[i].real - v34) < 1e-6 for i in range(sp.shape[1])]
        sp2 = sp @ (np.linalg.eigh(h34p)[1])[:, m2]
        if sp2.shape[1] == 0: continue
        if sp2.shape[1] > 1:
            h56p = sp2.conj().T @ H56_8 @ sp2
            for v56 in sorted(set(round(x.real, 6) for x in np.linalg.eigvalsh(h56p))):
                print(f"  ({round(v0,3)}, {round(v34,3)}, {round(v56,3)})")
        else:
            v56 = round((sp2.conj().T @ H56_8 @ sp2)[0,0].real, 3)
            print(f"  ({round(v0,3)}, {round(v34,3)}, {v56})")

# Under SU(4), the 8C spinor decomposes as 4 + 4*
# Under SU(4) -> SU(3) x U(1): 4 -> 3_1 + 1_{-3}, 4* -> 3*_{-1} + 1_{3}
# The 3 is color triplet, the 1 is lepton (4th color)

# ═══════════════════════════════════════════════════════════════════
# 6. Summary
# ═══════════════════════════════════════════════════════════════════

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if all_comm or all_comm_8:
    print(f"""
  Pati-Salam SU(4) x SU(2)_L x SU(2)_R verified in Cl(8,0).
  Dimensions: 15 (SU(4)) + 3 (SU(2)_L) + 3 (SU(2)_R) = 21 of 28 so(8).
  Unbroken: 7 bivectors are coset (broken at GUT scale).
  SM emerges via: SU(4) -> SU(3)xU(1)_(B-L) and SU(2)_R -> U(1)_R.
""")
else:
    print(f"""
  Pati-Salam does NOT embed in this Cl(8,0) basis.
  The sigma_z factor couples SU(4) and SU(2)^2.

  Possible fix: rebuild Cl(8,0) = Cl(6) x Cl(2) as separate factors.
  G1..G6 act on Cl(6) only (no sigma_z).
  G7, G8 act on Cl(2) only.
  Then [SU(4), SU(2)^2] = 0 automatically.
  Trade-off: different signature for the gauge generators.
""")
