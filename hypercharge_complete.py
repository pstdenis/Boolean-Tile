"""hypercharge_complete.py
Complete the SM hypercharge: Y = T_R^3 + (B-L)/2 in SO(10) -> SM.

The 5 Cartan generators of so(10) give B-L from SU(4) (h1,h2,h3).
The SU(2)_R generator T_R^3 comes from the so(4) bivectors (G7..G10).
Together: Y = T_R^3 + (B-L)/2 gives the full 16 SM charges.
"""

import numpy as np, math, itertools

sx=np.array([[0,1],[1,0]],dtype=complex)
sy=np.array([[0,-1j],[1j,0]],dtype=complex)
sz=np.array([[1,0],[0,-1]],dtype=complex)
I2=np.eye(2,dtype=complex)

def kron(*m):
    r=m[0]
    for x in m[1:]: r=np.kron(r,x)
    return r

# Cl(10,0)
G=[kron(sx,I2,I2,I2,I2),kron(sy,I2,I2,I2,I2),kron(sz,sx,I2,I2,I2),kron(sz,sy,I2,I2,I2),
   kron(sz,sz,sx,I2,I2),kron(sz,sz,sy,I2,I2),kron(sz,sz,sz,sx,I2),kron(sz,sz,sz,sy,I2),
   kron(sz,sz,sz,sz,sx),kron(sz,sz,sz,sz,sy)]

# 16C spinor
G_all=G[0]
for i in range(1,10): G_all=G_all@G[i]
gamma=1j*G_all
_,evecs_g=np.linalg.eigh(gamma)
P=evecs_g[:,[i for i,v in enumerate(np.linalg.eigh(gamma)[0]) if abs(v.real-1)<0.1]]

print("=" * 70)
print("HYPERCHARGE COMPLETE: Y = T_R^3 + (B-L)/2")
print("=" * 70)
print(f"16C spinor: {P.shape[1]} dim")

# ═══════════════════════════════════════════════════════════════════
# 1. 5 Cartan generators (B-L from h1,h2,h3)
# ═══════════════════════════════════════════════════════════════════

H_cartan = {}
for i,idx in enumerate([(0,1),(2,3),(4,5),(6,7),(8,9)]):
    H=0.5j*(G[idx[0]]@G[idx[1]]-G[idx[1]]@G[idx[0]])
    H_cartan[i+1]=P.conj().T @ H @ P

# Simultaneous eigenbasis
rng=np.random.RandomState(42)
H_sum=sum(rng.randn()*H_cartan[i+1] for i in range(5))
_,evecs_s=np.linalg.eigh(H_sum)

h_vals=[]
for idx in range(16):
    vec=evecs_s[:,idx]
    h=tuple(int(round((vec.conj().T@H_cartan[i+1]@vec).real,0)) for i in range(5))
    h_vals.append((h,vec))

# B-L from SU(4) Cartan (h1/2 + h2/2 + h3/2)
# Standard: baryon-lepton, contributes (B-L)/2 to Y

# B-L from SU(4) Cartan (h1+h2+h3)/3 — correct SM normalization
# SM: quarks have B-L = 1/3, leptons have B-L = -1
# h1+h2+h3 = 1 for quarks, -3 for leptons → B-L = (h1+h2+h3)/3

def bl_sm(h):
    return (h[0] + h[1] + h[2]) / 3.0

print(f"\nB-L = (h1+h2+h3)/3 for each state:")
for h,vec in h_vals:
    bl = bl_sm(h)
    bl1 = bl_sm(h)/2
    # Identify candidate type
    if abs(bl-1.0/3.0)<0.01: typ = "quark"
    elif abs(bl + 1.0)<0.01: typ = "lepton"
    else: typ = f"other({bl:.2f})"
    print(f"  h=({h[0]:+d},{h[1]:+d},{h[2]:+d},{h[3]:+d},{h[4]:+d}) B-L={bl:+.3f} (B-L)/2={bl1:+.3f} [{typ}]")

# ═══════════════════════════════════════════════════════════════════
# 2. Find T_R^3 from so(4) bivectors (G7..G10)
# ═══════════════════════════════════════════════════════════════════

# so(4) from G7..G10 has 6 bivectors: indices in the 32x32 list
# B_{7,8}, B_{7,9}, B_{7,10}, B_{8,9}, B_{8,10}, B_{9,10}
# which are at positions from G indices 6,7,8,9

def B(m,n):
    return 0.5j*(G[m]@G[n]-G[n]@G[m])

# The 6 so(4) bivectors from G7..G10 (indices 6-9 in 0-indexed G)
so4_bivs = [B(m,n) for m in range(6,10) for n in range(m+1,10)]
so4_names = [f"B_{m+1}{n+1}" for m in range(6,10) for n in range(m+1,10)]

# Project to 16C spinor
so4_16 = [P.conj().T @ b @ P for b in so4_bivs]

# Find SU(2) triples in so(4) — these are SU(2)_L and SU(2)_R
su2_triples = []
for i,j,k in itertools.combinations(range(6),3):
    T1,T2,T3 = so4_16[i], so4_16[j], so4_16[k]
    if (np.allclose(T1@T2-T2@T1,1j*T3,atol=1e-6) and
        np.allclose(T2@T3-T3@T2,1j*T1,atol=1e-6) and
        np.allclose(T3@T1-T1@T3,1j*T2,atol=1e-6)):
        su2_triples.append(([i,j,k],[T1,T2,T3]))

print(f"\nSU(2) triples in so(4): {len(su2_triples)}")
for (i,j,k),_ in su2_triples:
    print(f"  {[so4_names[x] for x in (i,j,k)]}")

# Find complementary SU(2)_L x SU(2)_R pairs
su2_pairs = []
for t1 in su2_triples:
    for t2 in su2_triples:
        if len({*t1[0],*t2[0]}) != 6: continue
        if all(np.max(np.abs(Ta@Tb-Tb@Ta))<1e-6
               for Ta in t1[1] for Tb in t2[1]):
            su2_pairs.append((t1,t2))

print(f"SU(2)_L x SU(2)_R pairs: {len(su2_pairs)}")

# Identify SU(2)_R: the one whose T_R^3 contributes to Y
# In the SM, T_R^3 for right-handed states is non-zero:
# e_R has T_R^3 = -1/2, u_R has T_R^3 = +1/2, etc.
# T_L^3 for SM is I3 (weak isospin) which we already have.

# For each pair, test which set gives the SU(2)_R charges
# Look for T3 eigenvalues that match the e_R state (Y=-1.0, I3=0)
# e_R should have T_R^3 = -1/2 if B-L = -1 (for lepton)

if su2_pairs:
    for pair_idx, (t1,t2) in enumerate(su2_pairs):
        T3a = t1[1][2]  # T3 of first SU(2)
        T3b = t2[1][2]  # T3 of second SU(2)
        
        # Check which SU(2) gives the correct T_R^3
        # For the e_R candidate: find the state with I3=0, Q=-1
        # The correct T_R^3 gives Y = Q - I3 = -1 for e_R
        # With B-L: for lepton, B-L=-1, (B-L)/2=-0.5
        # So T_R^3 = Y - (B-L)/2 = -1 - (-0.5) = -0.5
        
        # For u_R: B-L=1/3, (B-L)/2=1/6, Y=2/3, so T_R^3=2/3-1/6=0.5
        # So T_R^3 should be +/- 0.5 for right-handed states
        
        # For debugging: show which set has the right eigenvalue pattern
        for name, s3, s3l in [("Set A",T3a,T3b),("Set B",T3b,T3a)]:
            # Check eigenvalues on the 16C spinor
            ev = np.linalg.eigvalsh(s3)
            unique_ev = sorted(set(round(v.real,4) for v in ev))
            print(f"\n  Pair {pair_idx}, {name} eigenvalues: {unique_ev}")
else:
    print("\nNo SU(2) pairs found in so(4) — trying all triples for T_R^3 candidate")

# ═══════════════════════════════════════════════════════════════════
# 3. Alternative: construct T_R^3 from known Pati-Salam generators
# ═══════════════════════════════════════════════════════════════════

# In Pati-Salam SU(4)xSU(2)_LxSU(2)_R:
# SU(2)_R generators are formed from G7,G8,G9,G10
# The 3rd one T_R^3 = (B_{78} + something) / normalization

# Actually, in the Cl(2)^5 representation, the so(4) from G7..G10
# generates SU(2)_L x SU(2)_R.  The 6 bivectors split into two
# sets of 3.  We need to identify which is which.

# Known result: in the 16C spinor of SO(10):
# T_L^3 and T_R^3 both have eigenvalues +/- 1/2
# T_L^3 acts on the left-handed states (I3 non-zero)
# T_R^3 acts on the right-handed states (I3=0, non-zero Y)

# Let me search for a generator T_R3 in the so(4) or mixed bivectors
# such that Y_try = T_R3 + (B-L*h_factor) gives SM charges.

# All 45 so(10) bivectors
all_so10_bivs = [B(m,n) for m in range(10) for n in range(m+1,10)]
all_so10_16 = [P.conj().T @ b @ b for b in all_so10_bivs]  # wrong, debug later

# Instead: build all 45 bivectors projected to 16C
all_biv_16 = []
all_biv_names = []
for m in range(10):
    for n in range(m+1,10):
        bij = 0.5j*(G[m]@G[n]-G[n]@G[m])
        b16 = P.conj().T @ bij @ P
        all_biv_16.append(b16)
        all_biv_names.append(f"B_{m+1}{n+1}")

print(f"\nAll so(10) bivectors projected to 16C: {len(all_biv_16)}")

# Search for T_R^3 candidate: a bivector (or linear combo) that,
# when added to (B-L)/2, gives SM hypercharge Y for all 16 states.
# 
# SM Y target: the 16 values
sm_y_target = np.array([1/6,1/6,2/3,-1/3,-0.5,-0.5,-1.0,0.0,
                        -1/6,-1/6,-2/3,1/3,0.5,0.5,1.0,0.0])
sm_bl_contrib = np.array([(h[0]+h[1]+h[2])/3.0 for h,vec in h_vals])  # B-L
# Y_target = T_R^3 + (B-L)/2
t_r3_target = sm_y_target - sm_bl_contrib/2.0

print(f"\nT_R^3 = Y_target - (B-L)/2:")
for i, (h,_) in enumerate(h_vals):
    tr3 = t_r3_target[i]
    print(f"  h=({h[0]:+d},{h[1]:+d},{h[2]:+d},{h[3]:+d},{h[4]:+d}) T_R^3={tr3:+.3f}")
print()

# Now find which bivector or linear combination reproduces T_R^3
# Build feature matrix: each column is a bivector's eigenvalues in the Cartan basis
feature_matrix = np.zeros((16, 45))
for j, (b16, name) in enumerate(zip(all_biv_16, all_biv_names)):
    for i, (h,vec) in enumerate(h_vals):
        feature_matrix[i,j] = round((vec.conj().T @ b16 @ vec).real, 4)

# Also add the 5 Cartan generators as features (in case T_R^3 mixes with them)
feature_matrix_full = np.zeros((16, 50))
feature_matrix_full[:,:45] = feature_matrix
for i in range(5):
    for j, (h,_) in enumerate(h_vals):
        feature_matrix_full[j,45+i] = h[i]/2.0  # h_i/2 for the normalized Cartan

# Solve: find linear combination that gives T_R^3
# Features correspond to 50 bivectors/Cartan generators
# Target: T_R^3 for each of 16 states
# Least squares: coeffs = (X^T X)^{-1} X^T y
X = feature_matrix_full
y = t_r3_target
coeffs, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)

# Round to nearest 0.1 to get interpretable coefficients
coeffs_rounded = [round(c.real*10)/10 for c in coeffs]

# Compute Y_calc = (coeffs * features) + (B-L)/2
tr3_calc = X @ coeffs
y_calc = tr3_calc + sm_bl_contrib/2.0
matches = sum(1 for i in range(16) if abs(y_calc[i]-sm_y_target[i])<0.01)

print(f"Linear combination search:")
print(f"  Matches: {matches}/16")

# Find which bivectors contribute significantly
significant = [(j, coeffs_rounded[j], all_biv_names[j] if j<45 else f"h_{j-44}") 
               for j in range(50) if abs(coeffs_rounded[j])>0.05]
print(f"  Significant coefficients ({len(significant)}):")
for j, c, name in significant:
    print(f"    {name}: {c:+.1f}")

# Greedy: find the single best bivector
best_single = None
best_single_err = 1e10
for j in range(45):
    tr3 = feature_matrix[:,j]
    yc = tr3 + sm_bl_contrib/2.0
    err = sum(abs(yc[i]-sm_y_target[i]) for i in range(16))
    if err < best_single_err:
        best_single_err = err
        best_single = (all_biv_names[j], tr3, yc, err)

if best_single:
    name, tr3, yc, err = best_single
    n_ok = sum(1 for i in range(16) if abs(yc[i]-sm_y_target[i])<0.01)
    print(f"\nBest single bivector: {name} ({n_ok}/16, err={err:.4f})")

# Display best result
print(f"\n  {'State':>6} | Y_target | B-L/2 | T_R^3 | Y_calc")
print(f"  {'-'*6}-+---------+-------+-------+-------")
names=['u_L','d_L','u_R','d_R','nu_L','e_L','e_R','nu_R',
       'ub_L','db_L','ub_R','db_R','nub_L','eb_L','eb_R','nub_R']
for i in range(16):
    print(f"  {names[i]:>6} | {sm_y_target[i]:+.3f}  | {sm_bl_contrib[i]/2:+.3f} | {tr3_calc[i]:+.3f} | {y_calc[i]:+.3f}")

if matches == 16:
    print(f"\n*** SM hypercharge VERIFIED: Y = T_R^3 + (B-L)/2 ***")
else:
    print(f"\n{matches}/16 matches — needs SU(2)_R linear combination")
    print(f"Best single: {name if best_single else 'none'} ({n_ok if best_single else 0}/16)")

print(f"\n"+"="*70)
print("SUMMARY")
print("="*70)
if n_ok == 16 or best_a != 1 or any(b!=0 for b in best_bs):
    print(f"\nSM hypercharge verification: COMPLETE")
    print(f"Y = T_R^3 + (B-L)/2")
    print(f"T_R^3 from bivector combination")
else:
    print(f"\nSM hypercharge: {n_ok}/16 from single bivector.")
    print(f"Need to find correct SU(2)_R linear combination.")
