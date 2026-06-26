#!/usr/bin/env python3
"""
Measure convergence test: IFS branching measure -> Bures volume measure.
Tests if the dyadic IFS pushforward measure converges to Bures volume measure.
"""

import numpy as np
import math

# 16 tiles in Convention A
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


def bures_volume_element(r_vec):
    """Bures volume element at point with Bloch vector r."""
    r_sq = np.dot(r_vec, r_vec)
    if r_sq >= 1: return 0
    return 1.0 / (8 * math.sqrt(1 - r_sq))


def bloch_vector_from_sphere_area(radius=1):
    return 4 * math.pi * radius * radius


def measure_convergence_test():
    """Test measure convergence at various depths."""
    print("=== Measure Convergence Test ===\n")
    
    # Test tile: AND (entangling)
    tile_idx = 1
    phi = 0.0
    
    for depth in [1, 2, 3, 4, 5, 6]:
        N = 2 ** depth
        total_bures_vol = 0
        total_uniform_vol = 0
        total_mass = 0
        
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                
                vec = bloch_vector(tile_idx, A, B, 0.0)
                r_vec = np.array(vec)
                r_norm = np.linalg.norm(r_vec)
                
                if r_norm < 1.0:
                    bures_vol_elem = bures_volume_element(r_vec)
                    # Pushforward measure: weight by Bures volume element
                    total_bures_vol += bures_vol_elem
                else:
                    bures_vol_elem = 0
                
                # Uniform weight for comparison
                total_uniform_vol += 1.0
                total_mass += 1.0
        
        avg_bures = total_bures_vol / total_mass if total_mass > 0 else 0
        print(f"Depth {depth} (N={N}): avg Bures vol element = {avg_bures:.6f} over {total_mass} points")
    
    print()


def phase_sweep():
    """Test how measure changes with phase."""
    print("=== Phase Sweep (AND at depth 5) ===\n")
    tile_idx = 1
    N = 32
    
    for phi in [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]:
        total_bures = 0
        count = 0
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                vec = bloch_vector(1, A, B, phi)
                r_vec = np.array(vec)
                r_norm = np.linalg.norm(r_vec)
                if r_norm < 1.0:
                    total_bures += bures_volume_element(r_vec)
                    count += 1
        avg = total_bures / count if count > 0 else 0
        print(f"  phi={phi:.3f}: avg Bures vol = {avg:.6f} (count={count})")
    print()


def tile_comparison():
    """Compare measure across all tiles at one depth."""
    print("=== Tile Comparison at depth 5 ===\n")
    N = 32
    phi = 0.0
    
    for idx in range(16):
        total_bures = 0
        count = 0
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                vec = bloch_vector(idx, A, B, phi)
                r_vec = np.array(vec)
                r_norm = np.linalg.norm(r_vec)
                if r_norm < 1.0:
                    total_bures += bures_volume_element(r_vec)
                    count += 1
        avg = total_bures / count if count > 0 else 0
        print(f"  {TILES[idx]:12s}: avg Bures vol = {avg:.6f} (interior points={count}/{N*N})")
    print()


def bures_volume_of_ball():
    """Compute Bures volume of entire Bloch ball analytically."""
    # Integral of dV = d^3r / (8*sqrt(1-r^2)) over r<=1
    # In spherical coords: integral_0^1 r^2 dr * integral dOmega / (8*sqrt(1-r^2))
    # = 4*pi * integral_0^1 r^2 / (8*sqrt(1-r^2)) dr
    # = pi/2 * integral_0^1 r^2/sqrt(1-r^2) dr
    # = pi/2 * (pi/4) = pi^2/8
    return math.pi * math.pi / 8


def depth_scaling():
    """How does the discrete measure scale with depth?"""
    print("=== Depth Scaling Analysis ===\n")
    
    tile_idx = 1  # AND
    phi = 0.0
    total_volume = bures_volume_of_ball()
    print(f"Analytic Bures volume of Bloch ball: {total_volume:.6f}\n")
    
    for depth in range(1, 8):
        N = 2 ** depth
        total_bures = 0
        total_points = 0
        
        for ri in range(N):
            for ci in range(N):
                A = (ri + 0.5) / N
                B = (ci + 0.5) / N
                vec = bloch_vector(1, A, B, 0.0)
                r_vec = np.array(vec)
                r_norm = np.linalg.norm(r_vec)
                if r_norm < 1.0:
                    total_bures += bures_volume_element(r_vec)
        
        # The sum of volume elements over grid approximates integral
        # Each grid cell has area (1/N)^2 in parameter space
        # But we need the Jacobian of the map (A,B) -> r
        # For now, just show the sum
        print(f"Depth {depth} (N={N}): sum Bures vol elem = {total_bures:.6f}")
    
    print()


if __name__ == "__main__":
    print("Bures volume of Bloch ball (analytic):", bures_volume_of_ball())
    print()
    measure_convergence_test()
    phase_sweep()
    tile_comparison()
    depth_scaling()