#!/usr/bin/env python3
"""
Bures distance computation for the 16 Boolean tiles.
Tests the relationship between Hamming distance (IFS paths) and Bures distance.
"""

import numpy as np
import math

# 16 tiles in Convention A (+1 = False, -1 = True)
# Indices 0-15 map to 4-bit truth tables (bits 3,2,1,0 = (0,0), (0,1), (1,0), (1,1))
TILES = {
    0:  "FALSE", 1:  "AND",   2:  "A and notB", 3:  "A",
    4:  "notA and B", 5:  "B",   6:  "XOR",   7:  "OR",
    8:  "NOR",   9:  "XNOR", 10: "notB",   11: "B implies A",
    12: "notA",   13: "A implies B", 14: "NAND", 15: "TRUE"
}

# Truth tables for each tile index
def truth_table(idx):
    """Return 4-element list of +1/-1 for (00, 01, 10, 11)"""
    return [(1 if ((idx >> (3 - i)) & 1) else -1) for i in range(4)]

# Hadamard matrix H2 (unnormalized)
H2 = np.array([[1, 1, 1, 1],
               [1, -1, 1, -1],
               [1, 1, -1, -1],
               [1, -1, -1, 1]], dtype=float)


def bloch_vector(tile_idx, A, B, phi=0.0):
    """
    Compute Bloch vector of qubit 1 after applying U_f to |α⟩|β⟩
    where |α⟩ = sqrt(1-A)|0⟩ + e^{iφ}√A|1⟩
    and |β⟩ = sqrt(1-B)|0⟩ + e^{iφ}√B|1⟩
    """
    # Input state |αβ⟩
    sA, cA = math.sqrt(1 - A), math.sqrt(A)
    sB, cB = math.sqrt(1 - B), math.sqrt(B)
    eip = complex(math.cos(phi), math.sin(phi))
    eip2 = eip * eip

    # |αβ⟩ = |α⟩ ⊗ |β⟩
    psi0 = np.array([
        sA * sB,
        sA * cB * eip,
        cA * sB * eip,
        cA * cB * eip2
    ], dtype=complex)

    # U_f = H2 * diag(tt) * H2 / 4
    tt = np.array(truth_table(tile_idx))
    v = H2 @ psi0
    v = v * tt * 0.5
    psi = H2 @ v * 0.5

    # Density matrix rho = |psi⟩⟨psi|
    rho = np.outer(psi, psi.conj())

    # Partial trace over qubit 2
    # rho_1 = [[rho[0,0] + rho[1,1], rho[0,2] + rho[1,3]],
    #          [rho[2,0] + rho[3,1], rho[2,2] + rho[3,3]]]
    rho1_00 = rho[0, 0] + rho[1, 1]
    rho1_01 = rho[0, 2] + rho[1, 3]
    rho1_11 = rho[2, 2] + rho[3, 3]

    # Bloch vector
    X = 2 * rho1_01.real
    Y = 2 * rho1_01.imag
    Z = (rho1_00 - rho1_11).real

    return np.array([X, Y, Z], dtype=float)


def bures_distance(r1, r2):
    """Bures distance between two qubit states given by Bloch vectors r1, r2."""
    r1 = np.array(r1, dtype=float)
    r2 = np.array(r2, dtype=float)

    dot = np.dot(r1, r2)
    r1_sq = np.dot(r1, r1)
    r2_sq = np.dot(r2, r2)

    # Fidelity for qubit states
    term = (1 - r1_sq) * (1 - r2_sq)
    if term < 0:
        term = 0  # numerical precision

    F = 0.5 * (1 + dot + math.sqrt(max(0, term)))

    # Clamp
    F = max(0, min(1, F))

    return math.sqrt(2 - 2 * math.sqrt(F))


def hamming_distance(tile1_idx, tile2_idx):
    """Hamming distance between two truth tables (0-4)."""
    tt1 = truth_table(tile1_idx)
    tt2 = truth_table(tile2_idx)
    return sum(1 for a, b in zip(tt1, tt2) if a != b)


def test_at_point(A, B, phi=0.0):
    """Compute all pairwise Bures distances at a given point."""
    print(f"\n=== At (A={A}, B={B}, phi={phi}) ===")

    vecs = {}
    for idx in range(16):
        vecs[idx] = bloch_vector(idx, A, B, phi)
        r = np.linalg.norm(vecs[idx])
        print(f"  {TILES[idx]:8s}: [{vecs[idx][0]:7.4f}, {vecs[idx][1]:7.4f}, {vecs[idx][2]:7.4f}]  r={r:.4f}")

    print("\n  Pairwise Bures distances:")
    indices = list(range(16))
    for i in range(16):
        for j in range(i+1, 16):
            d = bures_distance(vecs[i], vecs[j])
            hd = hamming_distance(i, j)
            name_i = TILES[indices[i]]
            name_j = TILES[indices[j]]
            if not math.isnan(d):
                print(f"  {name_i:8s} vs {name_j:8s}: Bures={d:.4f}, Hamming={hd}")
            else:
                print(f"  {name_i:8s} vs {name_j:8s}: NaN, Hamming={hd}")


def hamming_vs_bures_sweep():
    """Check correlation between Hamming distance and Bures at multiple points."""
    print("\n=== Hamming vs Bures correlation across input space ===")
    
    pairs = [
        (0, 1),   # FALSE vs AND
        (1, 14),  # AND vs NAND
        (3, 5),   # P vs Q
        (6, 9),   # XOR vs XNOR
        (1, 7),   # AND vs OR
        (6, 7),   # XOR vs OR
        (3, 6),   # P vs XOR
        (1, 6),   # AND vs XOR
    ]

    test_points = [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75),
                   (0.5, 0.5), (0.1, 0.9), (0.9, 0.1), (0.01, 0.99)]

    for (i, j) in pairs:
        print(f"\n  {TILES[i]:8s} vs {TILES[j]:8s} (Hamming={hamming_distance(i, j)}):")
        for A, B in test_points:
            v1 = bloch_vector(i, A, B)
            v2 = bloch_vector(j, A, B)
            d = bures_distance(v1, v2)
            print(f"    (A={A:.2f}, B={B:.2f}): Bures={d:.4f}")


def depth_convergence_test():
    """Test how Bures distance converges as we vary the input resolution."""
    print("\n=== Depth convergence (discrete grid points) ===")
    
    # Use tile AND vs OR (Hamming = 2)
    i, j = 1, 7
    
    for depth in [1, 2, 3, 4, 5]:
        N = 2 ** depth
        total_d = 0
        count = 0
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                v1 = bloch_vector(i, A, B)
                v2 = bloch_vector(j, A, B)
                d = bures_distance(v1, v2)
                if not math.isnan(d):
                    total_d += d
                    count += 1
        avg = total_d / count if count > 0 else 0
        print(f"  Depth {depth} (N={N}): avg Bures = {avg:.4f} over {count} points")


if __name__ == "__main__":
    # Test at specific points
    test_at_point(0.3, 0.7)
    test_at_point(0.5, 0.5)
    test_at_point(0.01, 0.99)
    test_at_point(0.99, 0.01)
    
    # Hamming vs Bures sweep
    hamming_vs_bures_sweep()
    
    # Depth convergence
    depth_convergence_test()
    
    # Also test at phi = pi/2
    print("\n=== At phi=pi/2 ===")
    test_at_point(0.3, 0.7, math.pi/2)