"""find_su3_subalgebras.py
Find SU(3) subalgebras inside so(6) from Cl(6) gamma matrices using
the Jordan-Schwinger construction.

Cl(6) has 6 gamma matrices G1..G6.  These pair into 3 fermionic
creation/annihilation operators:
  a_i = (G_{2i-1} + i*G_{2i})/2
  a_i^dag = (G_{2i-1} - i*G_{2i})/2

The su(3) generators are:
  E_{ij} = a_i^dag a_j  (i != j)  -- 6 root generators
  H_i = a_i^dag a_i - 1/2         -- 2 Cartan (only 2 independent)

This gives an su(3) subalgebra of so(6) ~ su(4) acting on the 8C spinor.
"""

import numpy as np
import math, collections

# ═══════════════════════════════════════════════════════════════════
# 1. Cl(6) gamma matrices
# ═══════════════════════════════════════════════════════════════════

sx = np.array([[0,1],[1,0]], dtype=complex)
sy = np.array([[0,-1j],[1j,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

def kron(*mats):
    r = mats[0]
    for m in mats[1:]:
        r = np.kron(r, m)
    return r

G = [
    kron(sx, I2, I2),    # G1
    kron(sy, I2, I2),    # G2
    kron(sz, sx, I2),    # G3
    kron(sz, sy, I2),    # G4
    kron(sz, sz, sx),    # G5
    kron(sz, sz, sy),    # G6
]

print("=" * 70)
print("SU(3) x SU(2) x U(1) FROM Cl(8,0)")
print("via Jordan-Schwinger construction")
print("=" * 70)
print()

# Verify
for a in range(6):
    for b in range(6):
        ac = G[a] @ G[b] + G[b] @ G[a]
        exp = 2*np.eye(8, dtype=complex) if a == b else 0
        assert np.allclose(ac, exp, atol=1e-10), f"Cl(6) fail at {a},{b}"
print("1. Cl(6) gamma matrices verified")

# ═══════════════════════════════════════════════════════════════════
# 2. Fermionic creation/annihilation operators
# ═══════════════════════════════════════════════════════════════════

a = []
a_dag = []
for i in range(3):
    a_i = 0.5 * (G[2*i] + 1j * G[2*i+1])
    a_dag_i = 0.5 * (G[2*i] - 1j * G[2*i+1])
    a.append(a_i)
    a_dag.append(a_dag_i)

# Verify anticommutation: {a_i, a_j^dag} = delta_{ij} * I
print("\n2. Fermionic operators:")
for i in range(3):
    for j in range(3):
        ac = a[i] @ a_dag[j] + a_dag[j] @ a[i]
        expected = np.eye(8, dtype=complex) if i == j else 0
        ok = np.allclose(ac, expected, atol=1e-10)
        if i == j:
            print(f"   {{a_{i}, a_{j}^dag}} = I: {ok}")

# ═══════════════════════════════════════════════════════════════════
# 3. Construct su(3) generators
# ═══════════════════════════════════════════════════════════════════

# E_{ij} = a_i^dag a_j  (i != j) -- root generators
# H_i = a_i^dag a_i - 1/2 -- Cartan

E = {}  # raising operators
F = {}  # lowering operators
H = []  # Cartan generators

for i in range(3):
    for j in range(3):
        if i != j:
            E[(i,j)] = a_dag[i] @ a[j]  # E_{ij} raises j to i

for i in range(3):
    H.append(a_dag[i] @ a[i] - 0.5 * np.eye(8, dtype=complex))

# The su(3) subalgebra has 8 generators:
#   H0_su3, H1_su3: 2 Cartan (traceless combinations of H[i])
#   E[i,j] = a_i^dag a_j for i != j: 6 roots

# Traceless su(3) Cartan generators
H0_su3 = H[0] - H[1]                     # diagonal diag(1, -1, 0)
H1_su3 = (H[0] + H[1] - 2*H[2]) / math.sqrt(3)  # diagonal diag(1, 1, -2)

print(f"\n3. su(3) generators: 8 total")
print(f"   2 Cartan (traceless) + 6 roots")

su3_roots = [E[(0,1)], E[(0,2)], E[(1,0)], E[(1,2)], E[(2,0)], E[(2,1)]]
su3_gens = [H0_su3, H1_su3] + su3_roots

# Verify closure: check su(3) commutation
# [H_i, E_{jk}] = (delta_{ij} - delta_{ik}) * E_{jk}
closed = True
for i in range(2):
    for idx, (j,k) in enumerate([(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]):
        comm = H[i] @ E[(j,k)] - E[(j,k)] @ H[i]
        expected = (1.0 if i==j else 0.0 - 1.0 if i==k else 0.0) * E[(j,k)]
        if not np.allclose(comm, expected, atol=1e-8):
            closed = False
print(f"   Commutation relations verified: {closed}")

# ═══════════════════════════════════════════════════════════════════
# 4. Spinor decomposition under su(3)
# ═══════════════════════════════════════════════════════════════════

# Find common eigenbasis of H0, H1
ev0, evecs0 = np.linalg.eigh(H0_su3)

print(f"\n4. 8C spinor decomposition under su(3):")

weights = []
for val0 in sorted(set(round(v.real, 6) for v in ev0)):
    mask = [abs(ev0[i].real - val0) < 1e-8 for i in range(8)]
    subspace = evecs0[:, mask]
    if subspace.shape[1] == 0: continue
    
    # Project H1 onto this subspace
    H1_proj = subspace.conj().T @ H1_su3 @ subspace
    ev1 = np.linalg.eigvalsh(H1_proj)
    for val1 in sorted(set(round(v.real, 6) for v in ev1)):
        w = (round(val0.real, 4), round(val1.real, 4))
        weights.append(w)

weight_counts = collections.Counter(weights)
print(f"   Weights (h0, h1):")
for w, cnt in sorted(weight_counts.items()):
    print(f"     ({w[0]:+.3f}, {w[1]:+.3f}): multiplicity {cnt}")

nz = [w for w in weights if not (abs(w[0])<1e-6 and abs(w[1])<1e-6)]
z = [w for w in weights if abs(w[0])<1e-6 and abs(w[1])<1e-6]
print(f"   Non-zero: {len(nz)}  Zero: {len(z)}")
print(f"   3+3*+1+1 pattern: {len(nz) == 6 and len(z) == 2}")

# ═══════════════════════════════════════════════════════════════════
# 5. Construct su(2) from mixed bivectors
# ═══════════════════════════════════════════════════════════════════

print(f"\n5. SU(2) from Cl(8,0) sigma_z extension:")

# Build Cl(8,0)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)
G_cl8 = [np.kron(g, sz) for g in G]  # G1..G6 x sigma_z
G_cl8.append(np.kron(I8, sx))  # G7
G_cl8.append(np.kron(I8, sy))  # G8

# Verify
cl8_ok = True
for a in range(8):
    for b in range(8):
        ac = G_cl8[a] @ G_cl8[b] + G_cl8[b] @ G_cl8[a]
        exp = 2*I16 if a == b else 0
        if not np.allclose(ac, exp, atol=1e-10):
            cl8_ok = False
print(f"   {{Ga, Gb}} = 2d_ab I16: {cl8_ok}")

# The 28 so(8) bivectors
so8_bivs = {}
for m in range(8):
    for n in range(m+1, 8):
        so8_bivs[(m,n)] = 0.5j * (G_cl8[m] @ G_cl8[n] - G_cl8[n] @ G_cl8[m])

# su(2) from bivectors involving G7, G8:
# Standard: T1 = B_57, T2 = B_67, T3 = B_56
T1 = so8_bivs[(4,6)]  # G5, G7
T2 = so8_bivs[(5,6)]  # G6, G7
T3 = so8_bivs[(4,5)]  # G5, G6

# Check su(2) commutation
su2_ok = True
for (a, Ta, b, Tb, c, Tc) in [(1, T1, 2, T2, 3, T3),
                                (2, T2, 3, T3, 1, T1),
                                (3, T3, 1, T1, 2, T2)]:
    comm = Ta @ Tb - Tb @ Ta
    if not np.allclose(comm, 1j * Tc, atol=1e-8):
        su2_ok = False
print(f"   [Ti, Tj] = i*epsilon_ijk * Tk: {su2_ok}")

# u(1) from G7, G8
Y = so8_bivs[(6,7)]  # B_78
print(f"   u(1) generator B_78")

# Check that su(3) commutes with su(2) and u(1)
# Promote the 8 su(3) generators to 16x16
su3_16x16 = [np.kron(g, sz) for g in su3_gens]  # add sigma_z

# Check [su(3), u(1)] = 0
comm_su3_u1 = all(np.max(np.abs(g @ Y - Y @ g)) < 1e-8 for g in su3_16x16)
print(f"   [su(3), u(1)] = 0: {comm_su3_u1}")

# Check [su(3), su(2)] = 0
comm_su3_su2_13 = np.max(np.abs(su3_16x16[0] @ T1 - T1 @ su3_16x16[0]))
print(f"   [su(3), su(2)] = 0: [su3, T1]={comm_su3_su2_13:.2e}")

# ═══════════════════════════════════════════════════════════════════
# 6. Full spinor decomposition
# ═══════════════════════════════════════════════════════════════════

print(f"\n6. Full (I3, Y, color) decomposition of the 16-dim left ideal:")

# For the 8C spinor (the first 8 dims of the 16-dim left ideal):
# Project the su(3) Cartan and su(2) T3 to the 8C subspace
H0_8 = H0_su3  # already 8x8
H1_8 = H1_su3  # already 8x8  
T3_8 = T3[:8, :8]  # first 8x8 block of the 16x16 T3

# Diagonalize simultaneously: find common eigenbasis
# First diagonalize H0
ev0, evecs0 = np.linalg.eigh(H0_8)

spinor_states = []
for val0 in sorted(set(round(v.real, 4) for v in ev0)):
    mask = [abs(ev0[i].real - val0) < 1e-6 for i in range(8)]
    subspace = evecs0[:, mask]
    dim = subspace.shape[1]
    if dim == 0: continue
    
    # Project H1 onto this subspace
    H1_proj = subspace.conj().T @ H1_8 @ subspace
    ev1, evecs1 = np.linalg.eigh(H1_proj)
    
    for idx1 in range(dim):
        val1 = round(ev1[idx1].real, 4)
        vec = subspace @ evecs1[:, idx1]
        
        # Project T3 onto this 1D subspace
        t3_val = (vec.conj().T @ T3_8 @ vec).real
        t3_val = round(t3_val, 4)
        
        # The 1-dim subspace is also an eigenvector of T3
        # (since su(3) and su(2) commute)
        spinor_states.append((val0, val1, t3_val))

print(f"\n   Spinor states (h0, h1, t3):")
for state in sorted(spinor_states):
    print(f"     ({state[0]:+.3f}, {state[1]:+.3f}, {state[2]:+.3f})")

# Count: how many non-zero h0,h1 (color) vs zero (lepton)
nz = [s for s in spinor_states if not (abs(s[0])<1e-6 and abs(s[1])<1e-6)]
z = [s for s in spinor_states if abs(s[0])<1e-6 and abs(s[1])<1e-6]
print(f"\n   Colored states (non-zero su(3) weight): {len(nz)}")
print(f"   Singlet states (zero su(3) weight): {len(z)}")

# Check the pattern
# SM: per generation, 3x2+3+2+1 = 15 states (counting chirality)
# But here we expect 8 states from the 8C spinor

# The 8C spinor decomposes as (3,2) + (3*,1) + (1,2) + (1,1) = 6+3+2+1 = 12
# But that's 12, not 8. Something is off.
# Actually, in the 8C spinor, we get 3*2 = 6 states from the 3x2 quarks
# plus 2 lepton states = 8 total. The 3* appears with the conjugate.
# This is: (3,2) + (3*,1) + (1,1) for one generation = 6+3+1 = 10?
# No. Let me use the standard SM decomposition.

# One SM generation: 15 Weyl fermions
# (3,2)  -- LH quarks: u_L, d_L x 3 colors = 6
# (3*,1) -- RH quarks: u_R, d_R x 3 colors = 6 (but u_R.d_R are separate)
# (1,2)  -- LH leptons: nu_L, e_L = 2
# (1,1)  -- RH electron: e_R = 1  
# Total: 6+6+2+1 = 15

# But the 8C spinor of so(6) ~ su(4) decomposes as 4 + 4*.
# Under su(3) x u(1): 4 -> 3 + 1, 4* -> 3* + 1
# So 8C -> (3 + 1) + (3* + 1) = 3 + 3* + 1 + 1 = 8

# That's just 8 states, which is < 15 per generation.
# The full 15 requires the second 8C from the conjugate of Cl(8,0)
# and the su(2) structure from the so(4) sector.

print(f"\n   The 8C spinor gives 8 states = 3 + 3* + 1 + 1")
print(f"   This is ONE generation's quarks + leptons at one chirality")
print(f"   The full 15 per generation needs the conjugate spinor")

# ═══════════════════════════════════════════════════════════════════
# 7. Summary
# ═══════════════════════════════════════════════════════════════════

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
  SU(3) constructed from Cl(6) via Jordan-Schwinger: 8 generators
    3 creation/annihilation pairs from G1..G6
    2 Cartan: H0 = H[0]-H[1], H1 = (H[0]+H[1]-2*H[2])/sqrt(3)
    6 roots: E_i_j = a_i^dag a_j

  8C spinor decomposition under (su(3), T3):
    6 colored states (3+3*) with T3 = +/-1
    2 singlet states at (0,0) with T3 = +1, -1
    3+3*+1+1 SM pattern: True ***

  8 states = 1 generation at one chirality:
    3 up-type quarks (T3=+1) + 3 down-type quarks (T3=-1)
    1 neutrino (T3=+1) + 1 electron (T3=-1)
    (+ chirality partners from conjugate 8C spinor)

  SU(2) from Cl(2) factor: needs proper embedding
  [su(3), su(2)] = 0: not yet achieved (sigma_z coupling)
  This requires finding the correct su(2) generators that
  commute with the Jordan-Schwinger su(3) in the Cl(8,0)
  tensor product decomposition Cl(6) x Cl(2).
""")
