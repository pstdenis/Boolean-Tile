"""alt_su3_embedding.py
Find SU(3) from the so(6) bivectors via root system decomposition,
then search for commuting SU(2) among Cl(8,0) bivectors.
"""

import numpy as np
import math, itertools, collections

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
    kron(sx, I2, I2), kron(sy, I2, I2),
    kron(sz, sx, I2), kron(sz, sy, I2),
    kron(sz, sz, sx), kron(sz, sz, sy),
]

def biv(m, n):
    return 0.5j * (G6[m] @ G6[n] - G6[n] @ G6[m])

# 15 so(6) bivectors
bivs = []
biv_map = {}
for m in range(6):
    for n in range(m+1, 6):
        idx = len(bivs)
        bivs.append(biv(m, n))
        biv_map[(m, n)] = idx

print("=" * 70)
print("ALT SU(3) FROM so(6) ROOT SYSTEM")
print("=" * 70)

# Cartan: H12(0), H34(2), H56(4)
H_idx = [0, 2, 4]
H = [bivs[i] for i in H_idx]
non_cartan = [i for i in range(15) if i not in H_idx]

# Compute root vectors by diagonalizing ad_H on the 12-dim non-Cartan space
# Build 12x12 matrices representing ad_H1, ad_H2, ad_H3 on the non-Cartan bivectors

def adjoint_matrix(H_element, basis):
    """Matrix of ad_H in the given basis: M[a,b] = coeff of B_a in [H, B_b]"""
    n = len(basis)
    M = np.zeros((n, n), dtype=complex)
    for b in range(n):
        comm = H_element @ basis[b] - basis[b] @ H_element
        for a in range(n):
            M[a,b] = np.trace(comm @ basis[a].conj().T) / np.trace(basis[a] @ basis[a].conj().T)
    return M

non_cartan_bivs = [bivs[i] for i in non_cartan]
n_nc = len(non_cartan_bivs)

M1 = adjoint_matrix(H[0], non_cartan_bivs)
M2 = adjoint_matrix(H[1], non_cartan_bivs)
M3 = adjoint_matrix(H[2], non_cartan_bivs)

# Check commutativity
print(f"[M1, M2] = 0: {np.allclose(M1@M2, M2@M1, atol=1e-10)}")
print(f"[M2, M3] = 0: {np.allclose(M2@M3, M3@M2, atol=1e-10)}")
print(f"[M1, M3] = 0: {np.allclose(M1@M3, M3@M1, atol=1e-10)}")

# Simultaneously diagonalize: they commute, so find common eigenvectors
# Diagonalize M1, then M2 in each eigenspace
evals1, evecs1 = np.linalg.eig(M1)

roots = {}
for val1_idx in range(n_nc):
    val1 = evals1[val1_idx]
    vec = evecs1[:, val1_idx]
    
    # The corresponding linear combination of bivectors is:
    # E = sum_a vec[a] * B_{non_cartan[a]}
    # Its eigenvalue under M1 is val1
    
    # Find the eigenvalue under M2 by projecting M2 onto this eigenvector
    # E is simultaneously an eigenvector of M2 if M1 and M2 commute
    # val2 = (E^dag . M2 . E) / (E^dag . E)
    e_vec = np.array([vec[i].real + 1j*vec[i].imag for i in range(n_nc)])
    m2_proj = e_vec.conj().T @ M2 @ e_vec / (e_vec.conj().T @ e_vec)
    val2 = m2_proj
    
    # Same for M3
    m3_proj = e_vec.conj().T @ M3 @ e_vec / (e_vec.conj().T @ e_vec)
    val3 = m3_proj
    
    key = (round(val1.real, 6), round(val2.real, 6), round(val3.real, 6))
    if key not in roots:
        roots[key] = []
    roots[key].append(val1_idx)

print(f"\n{len(roots)} distinct roots (need 6 non-zero pairs for su(3)):")
for a, inds in sorted(roots.items(), key=lambda x: sum(abs(v) for v in x[0])):
    if sum(abs(v) for v in a) < 1e-10:
        print(f"  alpha={a} (zero root): {len(inds)} vectors")
    else:
        print(f"  alpha={a}: {len(inds)} vectors")

# Pair roots into +- pairs (for real eigenvalues)
# su(3) roots come in ± pairs; the Cartan subalgebra has 2 independent directions
# We need to find 3 non-zero root pairs (6 generators) + 2 Cartan = 8 total
non_zero_roots = [(a, inds) for a, inds in roots.items() if sum(abs(v) for v in a) > 1e-10]

pairs = []
used = set()
for alpha, inds in sorted(non_zero_roots, key=lambda x: sum(abs(v) for v in x[0])):
    neg_alpha = tuple(-v for v in alpha)
    if neg_alpha in roots:
        # Use the first eigenvector from each eigenspace
        i, j = inds[0], roots[neg_alpha][0]
        if i not in used and j not in used:
            pairs.append((alpha, i, j))
            used.update([i, j])

# Reconstruct the full so(6) generators from the eigenvectors
# For each root pair, we construct: E_alpha = sum coeff * B_k
# The 8 su(3) generators are: 2 Cartan (H12, H34) + 6 root generators
# from the 3 root pairs.

print(f"\nRoot pairs: {len(pairs)} (need 3)")
print()

if len(pairs) < 3:
    print("Not enough root pairs for su(3).")
else:
    pairs = pairs[:3]
    
    # Build the 6 root generators from eigenvector linear combinations
    root_gen = []
    for alpha, i, j in pairs:
        vec_i = evecs1[:, i]
        vec_j = evecs1[:, j]
        E_a = sum(vec_i[k] * non_cartan_bivs[k] for k in range(n_nc))
        E_na = sum(vec_j[k] * non_cartan_bivs[k] for k in range(n_nc))
        root_gen.extend([E_a, E_na])
    
    # Cartan generators: use H12 and H34  
    H_cartan = [bivs[H_idx[0]], bivs[H_idx[1]]]
    su3_gen = H_cartan + root_gen
    
    print(f"su(3): {len(su3_gen)} generators ({len(pairs)} root pairs)")
    
    # Verify closure
    closed = True
    for a in range(8):
        for b in range(a+1, 8):
            c = su3_gen[a] @ su3_gen[b] - su3_gen[b] @ su3_gen[a]
            in_sp = any(np.allclose(c, x, atol=1e-6) or np.allclose(c, -x, atol=1e-6) or
                        np.allclose(c, 1j*x, atol=1e-6) or np.allclose(c, -1j*x, atol=1e-6)
                        for x in su3_gen)
            if not in_sp and np.max(np.abs(c)) > 1e-8:
                closed = False
    print(f"closure: {closed}")
    
    # 8C spinor decomposition
    ev0, ev0v = np.linalg.eigh(bivs[H_idx[0]])
    wt = []
    for v0 in sorted(set(round(x.real, 6) for x in ev0)):
        m = [abs(ev0[i].real - v0) < 1e-6 for i in range(8)]
        sp = ev0v[:, m]
        if sp.shape[1] == 0: continue
        h1p = sp.conj().T @ bivs[H_idx[1]] @ sp
        e1 = np.linalg.eigvalsh(h1p)
        for v1 in sorted(set(round(x.real, 6) for x in e1)):
            wt.append((round(v0, 4), round(v1, 4)))
    
    nz = [w for w in wt if not (abs(w[0])<1e-6 and abs(w[1])<1e-6)]
    z = [w for w in wt if abs(w[0])<1e-6 and abs(w[1])<1e-6]
    pattern_ok = len(nz) == 6 and len(z) == 2
    print(f"3+3*+1+1: {pattern_ok} ({len(nz)} nz, {len(z)} z)")
    for w in sorted(wt):
        tag = " [singlet]" if (abs(w[0])<1e-6 and abs(w[1])<1e-6) else ""
        print(f"  ({w[0]:+.4f}, {w[1]:+.4f}){tag}")
    print()
    
    # Cl(8,0) and SU(2) search
    G8 = [np.kron(g, sz) for g in G6]
    G8.append(np.kron(I8, sx))
    G8.append(np.kron(I8, sy))
    
    so8_bivs = [0.5j * (G8[m] @ G8[n] - G8[n] @ G8[m])
                for m in range(8) for n in range(m+1, 8)]
    so8_labels = [(m+1,n+1) for m in range(8) for n in range(m+1, 8)]
    
    su3_16 = [np.kron(g, sz) for g in su3_gen]
    su3_8 = [g[:8,:8] for g in su3_16]
    
    # Mark bivectors used by su(3)
    used_16 = set()
    for i, B in enumerate(so8_bivs):
        for g in su3_16:
            if np.allclose(B, g, atol=1e-6) or np.allclose(B, -g, atol=1e-6):
                used_16.add(i)
                break
    
    rem = [i for i in range(28) if i not in used_16]
    print(f"so(8): {len(so8_bivs)}, su(3) uses {len(used_16)}, {len(rem)} remaining")
    
    found_su2 = []
    for i, j, k in itertools.combinations(rem, 3):
        T1, T2, T3 = so8_bivs[i], so8_bivs[j], so8_bivs[k]
        if not (np.allclose(T1@T2-T2@T1, 1j*T3, atol=1e-6) and
                np.allclose(T2@T3-T3@T2, 1j*T1, atol=1e-6) and
                np.allclose(T3@T1-T1@T3, 1j*T2, atol=1e-6)):
            continue
        for T in [T1, T2, T3]:
            T8 = T[:8,:8]
            if any(np.max(np.abs(T8 @ g - g @ T8)) > 1e-6 for g in su3_8):
                break
        else:
            found_su2.append(((i,j,k), [T1, T2, T3]))
    
    print(f"SU(2) commuting with SU(3): {len(found_su2)}")
    
    if found_su2:
        labels, gens = found_su2[0]
        names = [so8_labels[l] for l in labels]
        T3 = gens[2][:8,:8]
        Y = so8_bivs[-1][:8,:8]  # B_78
        
        print(f"Candidate: {names}")
        print(f"[U(1), SU(3)] = 0: {all(np.max(np.abs(Y @ g - g @ Y)) < 1e-6 for g in su3_8)}")
        print()
        print("(h0, h1, T3, Y, Q):")
        ev0, ev0v = np.linalg.eigh(su3_8[0])
        for v0 in sorted(set(round(x.real, 6) for x in ev0)):
            m = [abs(ev0[i].real - v0) < 1e-6 for i in range(8)]
            sp = ev0v[:, m]
            if sp.shape[1] == 0: continue
            h1p = sp.conj().T @ su3_8[1] @ sp
            e1, e1v = np.linalg.eigh(h1p)
            for jdx in range(sp.shape[1]):
                v1 = round(e1[jdx].real, 4)
                vec = sp @ e1v[:, jdx]
                t3 = round((vec.conj().T @ T3 @ vec).real, 4)
                y = round((vec.conj().T @ Y @ vec).real, 4)
                q = round(t3 + y/2, 4)
                tag = "" if (abs(v0)<1e-6 and abs(v1)<1e-6) else " [color]"
                print(f"  ({v0:+.3f}, {v1:+.3f}, T3={t3:+.3f}, Y={y:+.3f}, Q={q:+.3f}){tag}")

print(f"\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
Result: SU(2) commuting with alternative SU(3): {len(found_su2) if 'found_su2' in dir() else 'N/A'}

If 0: Same negative result as Jordan-Schwinger SU(3).
      The issue is structural: su(3) x su(2) x u(1) does NOT embed
      as a direct product in the so(8) bivectors.

If > 0: A different SU(3) basis allowed room for SU(2).
      The previous negative result was basis-dependent.
""")
