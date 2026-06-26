#!/usr/bin/env python3
"""
Measure convergence test v2: Proper pushforward measure vs Bures volume.
"""

import numpy as np
import math

TILES = {
    0:  "FALSE", 1:  "AND",   2:  "A and notB", 3:  "A",
    4:  "notA and B", 5:  "B",   6:  "XOR",   7:  "OR",
    8:  "NOR",   9:  "XNOR", 10: "notB",   11: "B implies A",
    12: "notA",   13: "A implies B", 14: "NAND", 15: "TRUE"
}

H2 = np.array([[1, 1, 1, 1],
               [1, -1, 1, -1],
               [1, 1, -1, -1],
               [1, -1, -1, 1]], dtype=float)

def truth_table(idx):
    return [(1 if ((idx >> (3 - i)) & 1) else -1) for i in range(4)]

def bloch_vector(tile_idx, A, B, phi=0.0):
    sA, cA = math.sqrt(1 - A), math.sqrt(A)
    sB, cB = math.sqrt(1 - B), math.sqrt(B)
    eip = complex(math.cos(phi), math.sin(phi))
    eip2 = eip * eip

    psi0 = np.array([
        sA * sB,
        sA * cB * eip,
        cA * sB * eip,
        cA * cB * eip2
    ], dtype=complex)

    tt = np.array([(1 if ((tile_idx >> (3 - i)) & 1) else -1) for i in range(4)])
    v = H2 @ psi0
    v = v * tt * 0.5
    psi = H2 @ v * 0.5

    rho = np.outer(psi, psi.conj())

    rho1_00 = rho[0, 0] + rho[1, 1]
    rho1_01 = rho[0, 2] + rho[1, 3]
    rho1_11 = rho[2, 2] + rho[3, 3]

    X = 2 * rho1_01.real
    Y = 2 * rho1_01.imag
    Z = (rho1_00 - rho1_11).real

    return np.array([X, Y, Z], dtype=float)


def bures_distance(r1, r2):
    r1 = np.array(r1, dtype=float)
    r2 = np.array(r2, dtype=float)
    dot = np.dot(r1, r2)
    r1_sq = np.dot(r1, r1)
    r2_sq = np.dot(r2, r2)
    term = (1 - r1_sq) * (1 - r2_sq)
    if term < 0: term = 0
    F = 0.5 * (1 + dot + math.sqrt(max(0, term)))
    F = max(0, min(1, F))
    return math.sqrt(2 - 2 * math.sqrt(F))


def bloch_vector_derivatives(tile_idx, A, B, phi=0.0, eps=1e-6):
    """Numerical derivatives of Bloch vector wrt A and B."""
    v = bloch_vector(idx, A, B, phi)
    v_A = bloch_vector(idx, A + eps, B, phi)
    v_B = bloch_vector(idx, A, B + eps, phi)
    dA = (v_A - v) / eps
    dB = (v_B - v) / eps
    return dA, dB


def jacobian_det(tile_idx, A, B, phi=0.0):
    """Jacobian determinant of map (A,B) -> (X,Y,Z)."""
    eps = 1e-6
    v = bloch_vector(tile_idx, A, B, phi)
    v_A = bloch_vector(tile_idx, A + eps, B, phi)
    v_B = bloch_vector(tile_idx, A, B + eps, phi)
    dA = (v_A - v) / eps
    dB = (v_B - v) / eps
    
    # For 2D -> 3D map, we use the area element sqrt(det(J^T J))
    # where J is 3x2 Jacobian
    J = np.column_stack([dA, dB])  # 3x2
    area_elem = math.sqrt(max(0, np.linalg.det(J.T @ J)))
    return area_elem


def bures_volume_element(r_vec):
    r_sq = np.dot(r_vec, r_vec)
    if r_sq >= 1: return 0
    return 1.0 / (8 * math.sqrt(1 - r_sq))


def test_measure_convergence():
    """Test if pushforward measure converges to Bures volume measure."""
    print("=== Measure Convergence: Pushforward vs Bures ===\n")
    
    # Sample random points in Bloch ball for Bures volume
    np.random.seed(42)
    M = 50000
    bures_vol_sum = 0
    for _ in range(M):
        # Sample uniformly in Bloch ball using rejection
        while True:
            r = np.random.uniform(-1, 1, 3)
            if np.dot(r, r) <= 1:
                break
        bures_vol_sum += 1.0 / (8 * math.sqrt(1 - np.dot(r, r)))
    bures_avg = bures_vol_sum / M
    print(f"Monte Carlo Bures volume avg: {bures_avg:.6f}")
    
    # Compare with analytic
    print(f"Analytic Bures volume: {math.pi**2/8:.6f}")
    print()
    
    # Test different tiles at depth 6
    depth = 6
    N = 2 ** depth
    tile_idx = 1  # AND
    
    total_weight = 0
    bures_sum = 0
    uniform_sum = 0
    
    for ri in range(N):
        for ci in range(N):
            A = (ri + 0.5) / N
            B = (ci + 0.5) / N
            vec = bloch_vector(1, A, B, 0.0)
            r_vec = np.array(vec)
            r_norm = np.linalg.norm(r_vec)
            
            if r_norm < 1.0:
                # Jacobian of (A,B) -> r
                J_det = jacobian_det(1, A, B, 0.0)
                # Pushforward weight: 1/N^2 * 1/Jacobian
                weight = 1.0 / (N * N)
                bures_vol = bures_volume_element(vec)
                total_weight += weight * J_det
                bures_sum += weight * J_det * bures_volume_element(vec)
                uniform_sum += weight
    
    print(f"Depth {depth}: total pushforward weight = {total_weight:.6f}")
    print(f"  Weighted Bures avg = {bures_sum/total_weight if total_weight>0 else 0:.6f}")
    print(f"  Uniform avg = {uniform_sum/total_weight if total_weight>0 else 0:.6f}")
    
    # Compare with analytic Bures volume
    print(f"Analytic Bures volume: {math.pi**2/8:.6f}")
    

def histogram_test():
    """Compare distribution of radial coordinate r."""
    print("\n=== Radial Distribution Comparison ===\n")
    
    # Bures radial distribution: p(r) ~ r^2 / sqrt(1-r^2)
    # Sample from this analytically
    bins = 20
    bures_hist = np.zeros(bins)
    M = 100000
    for _ in range(M):
        # Sample r from p(r) ~ r^2/sqrt(1-r^2)
        u = np.random.random()
        # CDF: F(r) = (1/2)*(arcsin(r) - r*sqrt(1-r^2)) + 1/2
        # Inverse not simple, use rejection
        while True:
            r = np.random.random()
            if np.random.random() < r / math.sqrt(1 - r*r):
                break
        bures_hist[int(r * bins)] += 1
    bures_hist = bures_hist / M
    
    # IFS distribution for AND at depth 6
    depth = 6
    N = 2**6
    ifs_hist = np.zeros(bins)
    count = 0
    for ri in range(N):
        for ci in range(N):
            A = (ri + 0.5) / N
            B = (ci + 0.5) / N
            vec = bloch_vector(1, A, B, 0.0)
            r = np.linalg.norm(vec)
            if r < 1:
                ifs_hist[int(r * bins)] += 1
                count += 1
    ifs_hist = ifs_hist / count if count > 0 else ifs_hist
    
    print("Radial distribution (bin -> fraction):")
    for i in range(bins):
        r_center = (i + 0.5) / bins
        if bures_hist[i] > 0 or ifs_hist[i] > 0:
            print(f"  r={r_center:.2f}: Bures={bures_hist[i]:.6f}, IFS={ifs_hist[i]:.6f}, ratio={ifs_hist[i]/bures_hist[i] if bures_hist[i]>0 else 'inf':.3f}")


def depth_convergence_of_histogram():
    """Check how IFS radial histogram converges with depth."""
    print("\n=== Depth Convergence of Radial Histogram ===\n")
    
    bins = 15
    
    for depth in [2, 3, 4, 5, 6]:
        N = 2**depth
        hist = np.zeros(bins)
        count = 0
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                vec = bloch_vector(1, A, B, 0.0)
                r = np.linalg.norm(vec)
                if r < 1:
                    hist[int(r * bins)] += 1
                    count += 1
        hist = hist / count if count > 0 else hist
        print(f"Depth {depth} (N={N}):")
        for i in range(bins):
            r_center = (i + 0.5) / bins
            if hist[i] > 0.001:
                print(f"  r={r_center:.2f}: {hist[i]:.6f}")
        print()


def tile_comparison_histogram():
    """Compare radial distributions across all tiles at depth 5."""
    print("\n=== Tile Radial Histograms (depth 5) ===\n")
    
    bins = 10
    depth = 5
    N = 2**depth
    
    for idx in range(16):
        hist = np.zeros(bins)
        count = 0
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                vec = bloch_vector(idx, A, B, 0.0)
                r = np.linalg.norm(vec)
                if r < 1:
                    hist[int(r * bins)] += 1
                    count += 1
        hist = hist / count if count > 0 else hist
        mean_r = sum((i+0.5)/bins * hist[i] for i in range(bins))
        print(f"  {TILES[idx]:12s}: mean r = {mean_r:.4f}, interior pts = {count}")


if __name__ == "__main__":
    test_measure_convergence()
    histogram_test()
    depth_convergence_of_histogram()
    tile_comparison_histogram()