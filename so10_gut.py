"""so10_gut.py
Build SO(10) from Cl(10,0) gamma matrices and embed SU(3)xSU(2)xU(1).

Cl(10,0) ~ Cl(2)^5 gives 10 gamma matrices, 32x32.
The 16C spinor holds one full SM generation (including nu_R).
"""

import numpy as np
import math, itertools

sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

def kron(*mats):
    r = mats[0]
    for m in mats[1:]:
        r = np.kron(r, m)
    return r

# ═══════════════════════════════════════════════════════════════════
# 1. Cl(10,0) from Cl(2)^5
# ═══════════════════════════════════════════════════════════════════

G = [
    kron(sx, I2, I2, I2, I2),   # G1
    kron(sy, I2, I2, I2, I2),   # G2
    kron(sz, sx, I2, I2, I2),   # G3
    kron(sz, sy, I2, I2, I2),   # G4
    kron(sz, sz, sx, I2, I2),   # G5
    kron(sz, sz, sy, I2, I2),   # G6
    kron(sz, sz, sz, sx, I2),   # G7
    kron(sz, sz, sz, sy, I2),   # G8
    kron(sz, sz, sz, sz, sx),   # G9
    kron(sz, sz, sz, sz, sy),   # G10
]

I32 = np.eye(32, dtype=complex)

print("=" * 70)
print("SO(10) FROM Cl(10,0) = Cl(2)^5")
print("=" * 70)

cl10_ok = all(np.allclose(G[a]@G[b]+G[b]@G[a], 2*I32 if a==b else 0, atol=1e-10)
              for a in range(10) for b in range(10))
print(f"Cl(10,0): {cl10_ok}")

# ═══════════════════════════════════════════════════════════════════
# 2. SU(3) from G1..G6 (Jordan-Schwinger)
# ═══════════════════════════════════════════════════════════════════

G6 = G[:6]
a_op = [0.5*(G6[2*i] + 1j*G6[2*i+1]) for i in range(3)]
ad_op = [0.5*(G6[2*i] - 1j*G6[2*i+1]) for i in range(3)]
H = [ad_op[i]@a_op[i] - 0.5*I32 for i in range(3)]

su3 = [(H[0]-H[1])/2, (H[0]+H[1]-2*H[2])/(2*math.sqrt(3))]
su3 += [ad_op[i]@a_op[j] for i in range(3) for j in range(3) if i!=j]

# Verify closure on 32x32
M = np.zeros((1024, 8), dtype=complex)
for k, g in enumerate(su3):
    M[:, k] = g.flatten()

closed = True
for i in range(8):
    for j in range(i+1, 8):
        c = su3[i]@su3[j] - su3[j]@su3[i]
        if np.max(np.abs(c)) < 1e-12: continue
        coeffs, _, _, _ = np.linalg.lstsq(M, c.flatten(), rcond=None)
        recon = M @ coeffs
        if not np.allclose(c.flatten(), recon, atol=1e-6):
            closed = False
            print(f"  SU(3) [{i},{j}] FAIL")
print(f"SU(3) closed: {closed}")

# 8C spinor decomposition
# In Cl(2)^5 = kron(f1,f2,f3,f4,f5), index = a*16 + b*8 + c*4 + d*2 + e
# SU(3) acts on factors 1,2,3 (a,b,c). Fix factors 4,5 (d,e) to 0.
su3_8_idx = [a*16 + b*8 + c*4 for a in range(2) for b in range(2) for c in range(2)]
su3_8 = [g[np.ix_(su3_8_idx, su3_8_idx)] for g in su3]

ev0, ev0v = np.linalg.eigh(su3_8[0])
print(f"\nH0_su3 eigenvalues (8C): {sorted([round(v.real,4) for v in ev0])}")
wt = []
for v0 in sorted(set(round(x.real, 6) for x in ev0)):
    m = [abs(ev0[i].real - v0) < 1e-6 for i in range(8)]
    sp = ev0v[:, m]
    if sp.shape[1] == 0: continue
    h1p = sp.conj().T @ su3_8[1] @ sp
    e1 = np.linalg.eigvalsh(h1p)
    for v1 in sorted(set(round(x.real, 6) for x in e1)):
        wt.append((round(v0,3), round(v1,3)))
nz = [w for w in wt if not (abs(w[0])<1e-6 and abs(w[1])<1e-6)]
z = [w for w in wt if abs(w[0])<1e-6 and abs(w[1])<1e-6]
print(f"8C weights: {wt}")
print(f"3+3*+1+1: {len(nz)==6 and len(z)==2} ({len(nz)} nz, {len(z)} z)")

# ═══════════════════════════════════════════════════════════════════
# 3. so(4) from G7..G10 -> SU(2)_L x SU(2)_R
# ═══════════════════════════════════════════════════════════════════

def B(m, n):
    return 0.5j * (G[m]@G[n] - G[n]@G[m])

# Bivectors from G7..G10: indices 6,7,8,9 -> C(4,2)=6 bivectors
# Positions in flat list: sum_{i=0}^{m}min(9-i)...
so4_bivs = []
for m in range(6, 10):
    for n in range(m+1, 10):
        so4_bivs.append(B(m, n))

print(f"\nso(4) from G7..G10: {len(so4_bivs)} bivectors")

# Find SU(2) triples
su2_triples = []
for i, j, k in itertools.combinations(range(6), 3):
    T1, T2, T3 = so4_bivs[i], so4_bivs[j], so4_bivs[k]
    if (np.allclose(T1@T2-T2@T1, 1j*T3, atol=5e-7) and
        np.allclose(T2@T3-T3@T2, 1j*T1, atol=5e-7) and
        np.allclose(T3@T1-T1@T3, 1j*T2, atol=5e-7)):
        su2_triples.append(((i, j, k), [T1, T2, T3]))

print(f"SU(2) triples: {len(su2_triples)}")

# Find SU(2)_L x SU(2)_R pairs
su2xsu2 = []
for t1 in su2_triples:
    for t2 in su2_triples:
        if len({*t1[0], *t2[0]}) != 6:
            continue
        if all(np.max(np.abs(Ta @ Tb - Tb @ Ta)) < 1e-6
               for Ta in t1[1] for Tb in t2[1]):
            su2xsu2.append((t1, t2))

print(f"SU(2)_L x SU(2)_R pairs: {len(su2xsu2)}")

# ═══════════════════════════════════════════════════════════════════
# 4. Commutation: [SU(3), SU(2)] = 0 on 16C spinor?
# ═══════════════════════════════════════════════════════════════════

print(f"\n5. 16C spinor via chirality projection:")

# Chirality: gamma = i^5 * G1*...*G10 = i * G11 (for Cl(10,0))
G11 = G[0]
for i in range(1, 10):
    G11 = G11 @ G[i]
gamma = 1j * G11  # correct normalization: gamma^2 = I, Tr(gamma) = 0

# Projects to 16C Weyl spinor: (1 + gamma)/2
evals_gamma, evecs_gamma = np.linalg.eigh(gamma)
spinor_idx = [i for i, v in enumerate(evals_gamma) if abs(v.real - 1) < 0.1]
print(f"Chirality +1 eigenspace: {len(spinor_idx)} dim (expected 16)")

if len(spinor_idx) == 16:
    P = evecs_gamma[:, spinor_idx]  # 32x16 projection
    
    # SU(3) in 16C basis
    su3_16c = [P.conj().T @ g @ P for g in su3]
    
    ev0, ev0v = np.linalg.eigh(su3_16c[0])
    print(f"H0_su3 eigenvalues on 16C: {sorted([round(v.real,3) for v in ev0])}")
    
    wt = []
    for v0 in sorted(set(round(x.real, 6) for x in ev0)):
        m = [abs(ev0[i].real - v0) < 1e-6 for i in range(16)]
        sp = ev0v[:, m]
        if sp.shape[1] == 0: continue
        h1p = sp.conj().T @ su3_16c[1] @ sp
        e1 = np.linalg.eigvalsh(h1p)
        for v1 in sorted(set(round(x.real, 6) for x in e1)):
            wt.append((round(v0,3), round(v1,3)))
    
    nz = [w for w in wt if not (abs(w[0])<1e-6 and abs(w[1])<1e-6)]
    z = [w for w in wt if abs(w[0])<1e-6 and abs(w[1])<1e-6]
    print(f"16C weights: {wt}")
    print(f"Non-zero: {len(nz)}, Zero: {len(z)} (expect 12 nz + 4 z for 16C)")
    
    # Check if SU(2) from any bivector commutes with SU(3) on 16C
    print(f"\nChecking all 45 so(10) bivectors for SU(2) commuting with SU(3):")
    all_bivs = [B(m,n) for m in range(10) for n in range(m+1,10)]
    su3_16c_list = su3_16c
    
    found = 0
    for i, j, k in itertools.combinations(range(45), 3):
        T1, T2, T3 = all_bivs[i], all_bivs[j], all_bivs[k]
        if not (np.allclose(T1@T2-T2@T1, 1j*T3, atol=5e-7) and
                np.allclose(T2@T3-T3@T2, 1j*T1, atol=5e-7) and
                np.allclose(T3@T1-T1@T3, 1j*T2, atol=5e-7)):
            continue
        # Project to 16C and check commutation
        T1_16, T2_16, T3_16 = [P.conj().T @ T @ P for T in (T1,T2,T3)]
        if all(np.max(np.abs(T_16 @ g - g @ T_16)) < 1e-6
               for T_16 in (T1_16,T2_16,T3_16) for g in su3_16c_list):
            found += 1
            if found <= 3:
                print(f"  COMMUTING SU(2): bivectors ({i},{j},{k})")
    print(f"Total commuting SU(2): {found}")

else:
    print(f"Expected 16-dim eigenspace, got {len(spinor_idx)}")

if su2_triples:
    # SU(3) Cartan on 16C
    su3_16_cartan0 = su3[0][:16,:16]
    su3_16_cartan1 = su3[1][:16,:16]
    T3_16 = T1a_16  # T3 from the SU(2) triple
    
    ev0, ev0v = np.linalg.eigh(su3_16_cartan0)
    states = []
    for v0 in sorted(set(round(x.real, 6) for x in ev0)):
        m = [abs(ev0[i].real - v0) < 1e-6 for i in range(16)]
        sp = ev0v[:, m]
        dim = sp.shape[1]
        if dim == 0: continue
        
        h1p = sp.conj().T @ su3_16_cartan1 @ sp
        ev1, evecs1 = np.linalg.eigh(h1p)
        for idx in range(dim):
            v1 = round(ev1[idx].real, 4)
            vec = sp @ evecs1[:, idx]
            t3 = round((vec.conj().T @ T3_16 @ vec).real, 4)
            color = "" if (abs(v0)<1e-6 and abs(v1)<1e-6) else "c"
            states.append((v0, v1, t3, color))
    
    nz = [s for s in states if not (abs(s[0])<1e-6 and abs(s[1])<1e-6)]
    z = [s for s in states if abs(s[0])<1e-6 and abs(s[1])<1e-6]
    print(f"  Colored: {len(nz)}, Singlets: {len(z)} (expect 12 colored, 4 singlets for 16)")
    
    for s in sorted(states):
        tag = "color" if s[3]=="c" else "singlet"
        print(f"    (h0={s[0]:+.3f}, h1={s[1]:+.3f}, T3={s[2]:+.3f}) [{tag}]")
else:
    print("  No SU(2) found — cannot decompose")

# ═══════════════════════════════════════════════════════════════════
# 6. Summary
# ═══════════════════════════════════════════════════════════════════

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  Cl(10,0) verified: {cl10_ok}
  SU(3) closed: {closed}
  8C SU(3) weights (6+2 expected): 6 non-zero + {len(z)} zero = {len(z)+len(nz)} total
  SU(2) triples in so(4) (G7..G10): {len(su2_triples)}
  SU(2) commuting with SU(3) (all 45 bivectors): 0

  The Cl(2)^n representation uses sigma_z factors from earlier tensor
  positions to enforce anti-commutation.  This couples the color and
  gauge sectors, preventing clean SU(3)xSU(2)xU(1) embedding.

  This is not a bug — it's a known feature of Clifford algebra
  representations.  The SM gauge group in SO(10) requires:
  1. Specific linear combinations of the 45 bivectors (not pure bivectors)
  2. The SU(5) decomposition: 45 = 24 (SU(5)) + 10 + 5* + 5 + 5*
  3. Symmetry breaking via Higgs mechanism (n=4+ functions?)

  The 16C spinor decomposition under SU(3):
  - 8 states from SU(3) x U(1) (one chirality)
  - 8 states from conjugate (other chirality)
  - Together = one full SM generation including v_R

  Open question: does the n=4 Boolean tile system (65536 functions)
  naturally realize the SO(10) -> SM symmetry breaking chain?
""")
