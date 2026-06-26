"""triality_so8.py
Use the Cl(2)xCl(2)xCl(2)xCl(2) representation of Cl(8,0).
The 4th tensor factor is G7,G8 — truly independent.
Bivectors from different factors commute.
SU(3) from G1..G6, SU(2) from G5..G8 with independent 4th factor.
"""

import numpy as np
import itertools, math

sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

def kron(*mats):
    r = mats[0]
    for m in mats[1:]: r = np.kron(r, m)
    return r

# Cl(8,0) = Cl(2) x Cl(2) x Cl(2) x Cl(2)
G = [
    kron(sx, I2, I2, I2),      # G1: sigma_x on 1st factor
    kron(sy, I2, I2, I2),      # G2: sigma_y on 1st factor
    kron(sz, sx, I2, I2),      # G3: sigma_z*sigma_x
    kron(sz, sy, I2, I2),      # G4: sigma_z*sigma_y
    kron(sz, sz, sx, I2),      # G5: sigma_z*sigma_z*sigma_x
    kron(sz, sz, sy, I2),      # G6: sigma_z*sigma_z*sigma_y
    kron(sz, sz, sz, sx),      # G7: ...*sigma_x on 4th factor
    kron(sz, sz, sz, sy),      # G8: ...*sigma_y on 4th factor
]

I16 = np.eye(16, dtype=complex)

print("=" * 70)
print("Cl(2)^4 CL(8,0) REPRESENTATION")
print("=" * 70)
cl8_ok = all(np.allclose(G[a]@G[b]+G[b]@G[a],
                         2*I16 if a==b else 0, atol=1e-10)
             for a in range(8) for b in range(8))
print(f"Cl(8,0): {cl8_ok}")

# ═══════════════════════════════════════════════════════════════════
# SU(3) from Jordan-Schwinger on G1..G6
# ═══════════════════════════════════════════════════════════════════

G6 = G[:6]
a_op = [0.5*(G6[2*i] + 1j*G6[2*i+1]) for i in range(3)]
ad_op = [0.5*(G6[2*i] - 1j*G6[2*i+1]) for i in range(3)]
H = [ad_op[i]@a_op[i] - 0.5*I16 for i in range(3)]

su3 = [H[0]-H[1], (H[0]+H[1]-2*H[2])/math.sqrt(3)]
su3 += [ad_op[i]@a_op[j] for i in range(3) for j in range(3) if i!=j]

# Verify SU(3) closure
closed = True
for a in range(8):
    for b in range(a+1,8):
        c = su3[a]@su3[b] - su3[b]@su3[a]
        in_sp = any(np.allclose(c, x, atol=1e-6) or np.allclose(c, -x, atol=1e-6) or
                    np.allclose(c, 1j*x, atol=1e-6) or np.allclose(c, -1j*x, atol=1e-6)
                    for x in su3)
        if not in_sp and np.max(np.abs(c)) > 1e-8:
            closed = False
print(f"SU(3) closure: {closed}")

# ═══════════════════════════════════════════════════════════════════
# 8C spinor decomposition
# ═══════════════════════════════════════════════════════════════════

su3_8 = [g[:8,:8] for g in su3]
ev0, ev0v = np.linalg.eigh(su3_8[0])
wt = []
for v0 in sorted(set(round(x.real,6) for x in ev0)):
    m = [abs(ev0[i].real - v0) < 1e-6 for i in range(8)]
    sp = ev0v[:, m]
    if sp.shape[1] == 0: continue
    h1p = sp.conj().T @ su3_8[1] @ sp
    e1 = np.linalg.eigvalsh(h1p)
    for v1 in sorted(set(round(x.real,6) for x in e1)):
        wt.append((round(v0,3), round(v1,3)))
nz = [w for w in wt if not (abs(w[0])<1e-6 and abs(w[1])<1e-6)]
z = [w for w in wt if abs(w[0])<1e-6 and abs(w[1])<1e-6]
print(f"3+3*+1+1: {len(nz)==6 and len(z)==2} ({len(nz)} nz, {len(z)} z)")

# ═══════════════════════════════════════════════════════════════════
# so(4) from G5..G8: bivectors involving the 4th tensor factor
# ═══════════════════════════════════════════════════════════════════

def B(m,n):
    return 0.5j*(G[m]@G[n]-G[n]@G[m])

bivs = [B(m,n) for m in range(8) for n in range(m+1,8)]
biv_labels = [(m+1,n+1) for m in range(8) for n in range(m+1,8)]

# Bivectors from G5..G8: {(4,5),(4,6),(4,7),(5,6),(5,7),(6,7)}
# In the flat list of 28 (m:0..7, n:m+1..8):
# m=4: (4,5),(4,6),(4,7) = 3 bivs at positions from m=0..3: 7+6+5+4=22, so 22,23,24
# m=5: (5,6),(5,7) = 2 at position 22+3=25, plus 0-based 25,26 
# m=6: (6,7) = 1 at position 25+2=27
so4_idx = [22, 23, 24, 25, 26, 27]
so4 = [bivs[i] for i in so4_idx]
so4_labels = [biv_labels[i] for i in so4_idx]

print(f"\nso(4) from G5..G8: 6 bivectors")

# Find SU(2) triples
su2_triples = []
for i,j,k in itertools.combinations(range(6), 3):
    T1,T2,T3 = so4[i], so4[j], so4[k]
    if (np.allclose(T1@T2-T2@T1, 1j*T3, atol=1e-6) and
        np.allclose(T2@T3-T3@T2, 1j*T1, atol=1e-6) and
        np.allclose(T3@T1-T1@T3, 1j*T2, atol=1e-6)):
        su2_triples.append(((i,j,k), [T1,T2,T3]))

print(f"SU(2) triples: {len(su2_triples)}")
for (i,j,k),_ in su2_triples:
    print(f"  {[so4_labels[x] for x in (i,j,k)]}")

# Find complementary SU(2) x SU(2) pairs
su2xsu2 = []
for t1 in su2_triples:
    for t2 in su2_triples:
        if len({*t1[0], *t2[0]}) != 6: continue
        if all(np.max(np.abs(T1@T2 - T2@T1)) < 1e-6
               for T1 in t1[1] for T2 in t2[1]):
            su2xsu2.append((t1, t2))

print(f"SU(2)_L x SU(2)_R pairs: {len(su2xsu2)}")

# ═══════════════════════════════════════════════════════════════════
# Does so(4) commute with SU(3)?
# ═══════════════════════════════════════════════════════════════════

print(f"\n[SU(3), SU(2)] check:")

if su2_triples:
    _, [T1,T2,T3] = su2_triples[0]
    T1_8,T2_8,T3_8 = T1[:8,:8], T2[:8,:8], T3[:8,:8]
    comm = all(np.max(np.abs(T_8 @ g - g @ T_8)) < 1e-6
               for g in su3_8 for T_8 in (T1_8,T2_8,T3_8))
    print(f"[SU(3), SU(2)] = 0: {comm}")
else:
    print(f"No SU(2) to check")

# Try mixed bivectors too (G1..G4 x G5..G8)
print(f"\nMixed bivectors (G1..G4 x G5..G8):")
mixed_idx = [i for i in range(28) if i not in so4_idx and i < 22]
# Actually mixed bivectors are all where (m<4 and n>=4) or (m>=4 and n>4)
# Let me just search all 28 for SU(2) that commutes with SU(3)

all_found = []
for i,j,k in itertools.combinations(range(28), 3):
    T1,T2,T3 = bivs[i], bivs[j], bivs[k]
    if not (np.allclose(T1@T2-T2@T1, 1j*T3, atol=5e-7) and
            np.allclose(T2@T3-T3@T2, 1j*T1, atol=5e-7) and
            np.allclose(T3@T1-T1@T3, 1j*T2, atol=5e-7)):
        continue
    T1_8,T2_8,T3_8 = T1[:8,:8], T2[:8,:8], T3[:8,:8]
    comm = all(np.max(np.abs(T_8 @ g - g @ T_8)) < 1e-6
               for g in su3_8 for T_8 in (T1_8,T2_8,T3_8))
    if comm:
        all_found.append((i,j,k))
        print(f"  SU(2) at ({i},{j},{k}) = {biv_labels[i]},{biv_labels[j]},{biv_labels[k]}: COMMUTES")

print(f"\nTotal SU(2) commuting with SU(3): {len(all_found)}")

if all_found:
    i,j,k = all_found[0]
    T1,T2,T3 = bivs[i], bivs[j], bivs[k]
    T1_8,T2_8,T3_8 = T1[:8,:8], T2[:8,:8], T3[:8,:8]
    Y = bivs[-1][:8,:8]  # B_78
    y_comm = all(np.max(np.abs(Y @ g - g @ Y)) < 1e-6 for g in su3_8)
    print(f"[U(1), SU(3)] = 0: {y_comm}")

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  Cl(2)^4 representation: {cl8_ok}
  SU(3) closure: {closed}
  SU(2) triples in so(4) (G5..G8): {len(su2_triples)}
  SU(2) x SU(2) pairs: {len(su2xsu2)}
  SU(2) commuting with SU(3) (all 28 bivectors): {len(all_found)}
""")
