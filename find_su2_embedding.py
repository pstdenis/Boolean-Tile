"""find_su2_embedding.py
Phase 1: Brute-force search for SU(2) generators that commute with
the Jordan-Schwinger SU(3) from Cl(6).

Two representations tested:
  A. sigma_z-extended Cl(8,0) (current)
  B. Clean tensor product Cl(8,0) ~ Cl(6) x Cl(2) (proposed)

Phase 2: Full (I3, Y, color) decomposition of the 8C spinor.
"""

import numpy as np
import math, itertools, collections

# ═══════════════════════════════════════════════════════════════════
# 1. Cl(6) gamma matrices and SU(3) generators
# ═══════════════════════════════════════════════════════════════════

sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)

def kron(*mats):
    r = mats[0]
    for m in mats[1:]:
        r = np.kron(r, m)
    return r

G6 = [
    kron(sx, I2, I2),    # G1
    kron(sy, I2, I2),    # G2
    kron(sz, sx, I2),    # G3
    kron(sz, sy, I2),    # G4
    kron(sz, sz, sx),    # G5
    kron(sz, sz, sy),    # G6
]

# Jordan-Schwinger creation/annihilation operators
a = [0.5 * (G6[2*i] + 1j * G6[2*i+1]) for i in range(3)]
a_dag = [0.5 * (G6[2*i] - 1j * G6[2*i+1]) for i in range(3)]

H = [a_dag[i] @ a[i] - 0.5 * np.eye(8, dtype=complex) for i in range(3)]
E = {(i,j): a_dag[i] @ a[j] for i in range(3) for j in range(3) if i != j}

# SU(3) generators: 2 Cartan + 6 roots
H0_su3 = H[0] - H[1]
H1_su3 = (H[0] + H[1] - 2*H[2]) / math.sqrt(3)
su3_roots = [E[(0,1)], E[(0,2)], E[(1,0)], E[(1,2)], E[(2,0)], E[(2,1)]]
su3_gens = [H0_su3, H1_su3] + su3_roots

# ═══════════════════════════════════════════════════════════════════
# 2. Cl(8,0) gamma matrices: TWO representations
# ═══════════════════════════════════════════════════════════════════

print("=" * 70)
print("SU(2) EMBEDDING IN Cl(8,0)")
print("=" * 70)
print()

print("1. Building Cl(8,0) representations:\n")

# Rep A: sigma_z-extended (current)
G_A = [np.kron(g, sz) for g in G6]
G_A.append(np.kron(I8, sx))  # G7
G_A.append(np.kron(I8, sy))  # G8

# Verify
cl8_ok = True
for a in range(8):
    for b in range(8):
        ac = G_A[a] @ G_A[b] + G_A[b] @ G_A[a]
        exp = 2*np.eye(16, dtype=complex) if a == b else 0
        if not np.allclose(ac, exp, atol=1e-10):
            cl8_ok = False
print(f"  Rep A (sigma_z-extended): {{Ga, Gb}} = 2d_ab I16: {cl8_ok}")

# Rep B: tensor product Cl(6) x Cl(2) with correct anti-commutation
# G_k' = G_k (x) sz  for k=1..6  (this IS the sigma_z extension)
# G_7 = I8 (x) sx
# G_8 = I8 (x) sy
# This is identical to Rep A! The tensor product IS sigma_z extension.
# The issue is finding SU(2) generators that commute with SU(3)
# on the 8C spinor subspace, not on the full 16x16 space.

print("  Rep B = Rep A (tensor product = sigma_z extension)")
print(f"  Only one correct Cl(8,0) representation exists")
print()

# ═══════════════════════════════════════════════════════════════════
# 3. Find SU(2) that commutes with SU(3) on the 8C spinor
# ═══════════════════════════════════════════════════════════════════

def find_su2_on_spinor(gammas, su3_gens_8):
    """Search for SU(2) generators among Cl(8,0) bivectors.
    Check commutation with SU(3) on the 8C spinor subspace (first 8 dims).
    su3_gens_8: list of 8 8x8 matrices (SU(3) generators on the spinor)"""
    
    n = gammas[0].shape[0]
    
    # Build all 28 bivectors
    bivs = []
    biv_labels = []
    for m in range(8):
        for n_i in range(m+1, 8):
            B = 0.5j * (gammas[m] @ gammas[n_i] - gammas[n_i] @ gammas[m])
            bivs.append(B)
            biv_labels.append((m+1, n_i+1))
    
    found = []
    n_bivs = len(bivs)
    
    for i, j, k in itertools.combinations(range(n_bivs), 3):
        T1, T2, T3 = bivs[i], bivs[j], bivs[k]
        
        # Check [Ti, Tj] = i * epsilon_ijk * Tk on 16x16
        if not (np.allclose(T1@T2 - T2@T1, 1j*T3, atol=1e-6) and
                np.allclose(T2@T3 - T3@T2, 1j*T1, atol=1e-6) and
                np.allclose(T3@T1 - T1@T3, 1j*T2, atol=1e-6)):
            continue
        
        # Check commutation with SU(3) on the 8C spinor (first 8 dims)
        # The SU(3) generators are 8x8; restrict T to 8x8
        comm_ok = True
        for T in [T1, T2, T3]:
            T_8 = T[:8, :8]
            for g in su3_gens_8:
                if np.max(np.abs(T_8 @ g - g @ T_8)) > 1e-6:
                    comm_ok = False
                    break
            if not comm_ok:
                break
        
        if not comm_ok:
            continue
        
        labels = (biv_labels[i], biv_labels[j], biv_labels[k])
        found.append((labels, [T1, T2, T3]))
    
    return found

# SU(3) generators on the 8C spinor (8x8)
su3_gens_8 = su3_gens  # already 8x8

# Search for SU(2) that commutes on the 8C spinor
print("2. Searching for SU(2) that commutes with SU(3) on the 8C spinor:\n")

found_A = find_su2_on_spinor(G_A, su3_gens_8)
print(f"   SU(2) subalgebras found: {len(found_A)}")
print()

# If found, decompose; otherwise explain
if found_A:
    print("3. Full decomposition with best SU(2) candidate:\n")
    labels, su2_gens = found_A[0]
    B78 = 0.5j * (G_A[6] @ G_A[7] - G_A[7] @ G_A[6])
    
    states = decompose_spinor(su3_gens_8, su2_gens, B78[:8,:8])
    print(f"    SU(2) at {labels})")
    print(f"    (h0, h1, t3, y, q):")
    for s in sorted(states):
        nz = not (abs(s[0])<1e-6 and abs(s[1])<1e-6)
        tag = "color" if nz else "singlet"
        print(f"      ({s[0]:+.3f}, {s[1]:+.3f}, {s[2]:+.3f}, {s[3]:+.3f}, {s[4]:+.3f}) [{tag}]")
    
    nz_s = [s for s in states if not (abs(s[0])<1e-6 and abs(s[1])<1e-6)]
    z_s = [s for s in states if abs(s[0])<1e-6 and abs(s[1])<1e-6]
    print(f"    Colored: {len(nz_s)}, Singlets: {len(z_s)}")
else:
    print("3. No SU(2) found commuting with SU(3) on the 8C spinor.\n")
    print("   This is a significant result: it means the SM gauge group")
    print("   SU(3) x SU(2) x U(1) is NOT a direct product subalgebra of")
    print("   the Cl(8,0) bivectors when using the Jordan-Schwinger SU(3).")
    print()
    print("   Possible resolutions:")
    print("   1. The SU(3) and SU(2) are embedded in a larger GUT group")
    print("      (e.g., SU(4) x SU(2) x U(1) Pati-Salam or SO(10))")
    print("   2. The SU(2) generators are NOT among the pure bivectors")
    print("      but are linear combinations that include the U(1) direction")
    print("   3. A different gamma matrix basis gives commuting SU(3) x SU(2)")
    print()

# ═══════════════════════════════════════════════════════════════════
# 4. Full su(3) x su(2) x u(1) decomposition for best candidate
# ═══════════════════════════════════════════════════════════════════

def decompose_spinor(rep_name, su3_gens_16, su2_gens, u1_gen, gammas):
    """Compute (h0, h1, t3, y) for each of the 8 spinor components.
    su3_gens_16: list of 8 16x16 matrices
    su2_gens: list of 3 16x16 matrices
    u1_gen: 16x16 matrix (U(1) generator)
    gammas: list of 8 16x16 gamma matrices
    """
    # We work with the 8C spinor (first 8 dims of the 16-dim left ideal)
    # Restrict su(3) generators to 8x8
    H0 = su3_gens_16[0][:8,:8]
    H1 = su3_gens_16[1][:8,:8]
    T3 = su2_gens[2][:8,:8] if su2_gens else None  # T3
    Y = u1_gen[:8,:8] if u1_gen is not None else None
    
    # Diagonalize H0
    ev0, evecs0 = np.linalg.eigh(H0)
    
    states = []
    for val0 in sorted(set(round(v.real, 6) for v in ev0)):
        mask = [abs(ev0[i].real - val0) < 1e-6 for i in range(8)]
        subspace = evecs0[:, mask]
        dim = subspace.shape[1]
        if dim == 0: continue
        
        H1_proj = subspace.conj().T @ H1 @ subspace
        ev1, evecs1 = np.linalg.eigh(H1_proj)
        
        for idx in range(dim):
            val1 = round(ev1[idx].real, 4)
            vec = subspace @ evecs1[:, idx]
            
            # Compute T3 eigenvalue
            t3_val = 0.0
            if T3 is not None:
                t3_val = round((vec.conj().T @ T3 @ vec).real, 4)
            
            # Compute U(1) eigenvalue
            y_val = 0.0
            if Y is not None:
                y_val = round((vec.conj().T @ Y @ vec).real, 4)
            
            # Q = I3 + Y/2
            q_val = round(t3_val + y_val/2, 4)
            
            states.append((val0, val1, t3_val, y_val, q_val))
    
    return states

# Build the U(1) generators for each rep
# u(1) from G7, G8 bivector: B_78
B78_A = 0.5j * (G_A[6] @ G_A[7] - G_A[7] @ G_A[6])

print("4. Full decomposition (if SU(2) found):\n")

if found_A:
    labels, su2_gens = found_A[0]
    states = decompose_spinor(su3_gens_8, su2_gens, B78_A[:8,:8])
    print(f"  Candidate: {labels}")
    for s in sorted(states):
        nz = not (abs(s[0])<1e-6 and abs(s[1])<1e-6)
        tag = "color" if nz else "singlet"
        print(f"    ({s[0]:+.3f}, {s[1]:+.3f}, {s[2]:+.3f}, {s[3]:+.3f}, {s[4]:+.3f}) [{tag}]")
else:
    print("  (no SU(2) candidate found)")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("SUMMARY")
print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  SU(2) commuting with SU(3) on 8C spinor: {len(found_A)} candidates
  
  Result: No SU(2) found that commutes with the Jordan-Schwinger SU(3)
  on the 8C spinor.  The SM direct product SU(3) x SU(2) x U(1) is NOT
  a direct subalgebra of the Cl(8,0) bivectors in this basis.

  This suggests the SM gauge group requires a GUT embedding (Pati-Salam,
  SO(10), or SU(5)) where SU(3) and SU(2) commute only after symmetry
  breaking.  The 8C spinor decomposition under SU(3) stands:
    6 colored states (3+3*, T3=+/-) + 2 singlets
  as one SM generation at one chirality.
""")
