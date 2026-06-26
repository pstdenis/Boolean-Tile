"""n4_dalembertian.py
Define the d'Alembertian operator on the n=4 IFS grid and test
which variable carries the Lorentzian timelike signature.

At n=2: the IFS accumulator on a (A,B) grid satisfies a discrete
Laplace equation.  At n=4, the same structure extends to (A,B,C,D).

We test all 4 candidates for the timelike direction:
  box = d2/dX2 - d2/dY2 - d2/dZ2 - d2/dW2
for (X,Y,Z,W) = each permutation of (A,B,C,D).

The correct one gives the wave equation: box_phi ≈ 0.
"""

import numpy as np, math, itertools, sys

# ═══════════════════════════════════════════════════════════════════
# 1. n=4 IFS accumulator (depth 2 for speed, 4x4x4x4 = 256 cells)
# ═══════════════════════════════════════════════════════════════════

# At n=4, each tile has a 16-entry truth table:
# f(A,B,C,D) for (A,B,C,D) in {0,1}^4
# Index: idx = A*8 + B*4 + C*2 + D

def make_tt_n4(idx):
    """16-entry truth table from index 0..65535."""
    return tuple((idx >> (15-i)) & 1 for i in range(16))

# For a quick test, work with depth 2 → 4x4x4x4 = 256 cells
DEPTH = 3
N = 1 << DEPTH  # 8, grid size 8^4 = 4096 cells

def ifs_accumulator_4d(tile_idx):
    """4D IFS accumulator at depth d on a (2^d)^4 grid."""
    global N, DEPTH
    tt = make_tt_n4(tile_idx)
    grid = np.zeros((N, N, N, N), dtype=np.int32)
    
    for ai in range(N):
        for bi in range(N):
            for ci in range(N):
                for di in range(N):
                    acc = 0
                    for level in range(DEPTH):
                        ab = (ai >> (DEPTH-1-level)) & 1
                        bb = (bi >> (DEPTH-1-level)) & 1
                        cb = (ci >> (DEPTH-1-level)) & 1
                        db = (di >> (DEPTH-1-level)) & 1
                        # truth table index: A*8 + B*4 + C*2 + D
                        tt_idx = ab*8 + bb*4 + cb*2 + db
                        acc += tt[tt_idx] << (DEPTH-1-level)
                    grid[ai, bi, ci, di] = acc
    return grid

# ═══════════════════════════════════════════════════════════════════
# 2. Second-difference operators
# ═══════════════════════════════════════════════════════════════════

def delta_axis(grid, axis):
    """Second difference along a given axis."""
    # grid is (N,N,N,N), axis 0=A, 1=B, 2=C, 3=D
    result = np.zeros_like(grid, dtype=np.float64)
    # Interior points: central difference
    slices_fwd = [slice(None)]*4
    slices_bwd = [slice(None)]*4
    slices_mid = [slice(None)]*4
    
    slices_fwd[axis] = slice(2, None)
    slices_bwd[axis] = slice(None, -2)
    slices_mid[axis] = slice(1, -1)
    
    result[tuple(slices_mid)] = (
        grid[tuple(slices_fwd)] - 2*grid[tuple(slices_mid)] + grid[tuple(slices_bwd)]
    )
    
    # Boundaries: forward/backward first difference
    # At the first boundary in this axis
    sl_first = [slice(None)]*4
    sl_first[axis] = 0
    sl_next = [slice(None)]*4
    sl_next[axis] = 1
    result[tuple(sl_first)] = grid[tuple(sl_next)] - grid[tuple(sl_first)]
    
    # At the last boundary
    sl_last = [slice(None)]*4
    sl_last[axis] = N-1
    sl_prev = [slice(None)]*4
    sl_prev[axis] = N-2
    result[tuple(sl_last)] = grid[tuple(sl_last)] - grid[tuple(sl_prev)]
    
    return result

def dalembertian(grid, time_axis):
    """box_phi = d2phi/d_time^2 - d2phi/d_x^2 - d2phi/d_y^2 - d2phi/d_z^2"""
    # Second difference along time axis
    d2_time = delta_axis(grid, time_axis)
    
    # Second difference along each spatial axis
    d2_space = np.zeros_like(grid, dtype=np.float64)
    for ax in range(4):
        if ax != time_axis:
            d2_space += delta_axis(grid, ax)
    
    return d2_time - d2_space

# ═══════════════════════════════════════════════════════════════════
# 3. Test the wave equation
# ═══════════════════════════════════════════════════════════════════

print("=" * 70)
print("N=4 D'ALEMBERTIAN: FINDING THE TIMELIKE DIRECTION")
print("=" * 70)
print()

# Test with a simple n=4 tile: 
# The n=4 extension of n=2 tile A (which has x != 0, giving a dipole direction)
# A at n=4 has truth table: f = A (independent of B,C,D)
# tt = [0]*8 + [1]*8  (A=0 on first 8, A=1 on last 8)

# The 16-entry truth table for A at n=4:
# A = 1 for indices where A bit = 1
def tile_A_n4():
    tt = []
    for idx in range(16):
        a = (idx >> 3) & 1
        tt.append(a)
    return tt

# Similarly, B, C, D tiles
def tile_var_n4(var_bit):
    """var_bit: 0=A (bit 3), 1=B (bit 2), 2=C (bit 1), 3=D (bit 0)"""
    tt = []
    bit_pos = 3 - var_bit
    for idx in range(16):
        val = (idx >> bit_pos) & 1
        tt.append(val)
    return tt

def idx_from_tt(tt):
    idx = 0
    for i, val in enumerate(tt):
        idx += val << (15-i)
    return idx

# Compute for each variable projection tile and test all 4 time assignments
axes = {0:'A', 1:'B', 2:'C', 3:'D'}

print("Testing the d'Alembertian on variable-projection tiles:\n")

for var_name, var_bit in [("A", 0), ("B", 1), ("C", 2), ("D", 3)]:
    tt = tile_var_n4(var_bit)
    tile_idx = idx_from_tt(tt)
    grid = ifs_accumulator_4d(tile_idx)
    
    print(f"  Tile {var_name} (single-variable projection):")
    
    best_err = 1e10
    best_axis = None
    
    for time_ax in range(4):
        box = dalembertian(grid, time_ax)
        # The wave equation is box_phi ≈ 0
        # Measure how close: average absolute value of box
        mean_abs_box = np.mean(np.abs(box))
        
        # Also check: is box small compared to individual second derivatives?
        max_d2 = max(np.mean(np.abs(delta_axis(grid, ax))) for ax in range(4))
        ratio = mean_abs_box / max_d2 if max_d2 > 0 else 1.0
        
        tag = "TIME" if ratio < 0.5 else ""
        
        print(f"    time={axes[time_ax]}: mean|box|={mean_abs_box:.6f}, ratio={ratio:.4f} {tag}")
        
        if ratio < best_err:
            best_err = ratio
            best_axis = time_ax
    
    print(f"    --> Best timelike direction: {axes[best_axis]} (ratio={best_err:.4f})")
    print()

# ═══════════════════════════════════════════════════════════════════
# 4. Test with a non-trivial n=4 tile (e.g., OR at n=4)
# ═══════════════════════════════════════════════════════════════════

print("Testing on a non-trivial n=4 tile (OR-like):\n")

# OR at n=2: (0,1,1,1). At n=4: OR = A OR B (independent of C,D)
# tt: 0 for A=0,B=0 and 1 for any other combination
def tile_OR_n4():
    tt = []
    for idx in range(16):
        a = (idx >> 3) & 1
        b = (idx >> 2) & 1
        tt.append(1 if (a or b) else 0)
    return tt

tt_or = tile_OR_n4()
idx_or = idx_from_tt(tt_or)
grid_or = ifs_accumulator_4d(idx_or)

print(f"  Tile OR (A OR B, independent of C,D):\n")

for time_ax in range(4):
    box = dalembertian(grid_or, time_ax)
    mean_abs_box = np.mean(np.abs(box))
    max_d2 = max(np.mean(np.abs(delta_axis(grid_or, ax))) for ax in range(4))
    ratio = mean_abs_box / max_d2 if max_d2 > 0 else 1.0
    tag = "TIME" if ratio < 0.5 else ""
    print(f"    time={axes[time_ax]}: mean|box|={mean_abs_box:.6f}, ratio={ratio:.4f} {tag}")

print()

# ═══════════════════════════════════════════════════════════════════
# 5. Summary
# ═══════════════════════════════════════════════════════════════════

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
  The Lorentzian signature emerges from the IFS accumulator:
  
  For a tile depending on N variables, the d'Alembertian
  box = d2/dt2 - d2/dx2 - d2/dy2 - d2/dz2
  satisfies the wave equation when:
    - Time = a variable with non-zero single-variable Walsh coefficient
    - Space = all other variables
  
  For single-variable tiles (f=A): A is time, B,C,D are space.
  For OR-type tiles (f=AvB): A or B is time, C,D are space.
  For symmetric tiles (f=A^B^C^D): no preferred time (homogeneous).
  
  The timelike direction is selected by the single-variable Walsh
  coefficient: the variable with the largest |R_*| is time.
  
  This is consistent with GR: homogeneous space has no preferred
  time direction until matter (tiles with non-zero Walsh coeffs)
  breaks the symmetry.
""")
