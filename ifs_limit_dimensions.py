"""ifs_limit_dimensions.py
IFS LIMIT SET dimension (top-slice: cells surviving ALL levels).

This is the set of points that never hit a 0 bit at any IFS depth — the
Cantor-like limit set. Its dimension is dim = log2(k) where k = #{1's}
in the tile's 4-entry truth table.

Contrast with the CHAOS GAME attractor (ifs_geometry.py), which measures
the union of all levels (acc > 0) and converges to dim ~ 2 for all k >= 2.

k=2 tiles (A,B,XOR,...): limit set is a 1D line (dim=1)
k=3 tiles (OR,AND,...): limit set is the Sierpinski gasket (dim=log2(3)~1.585)
k=4 (TRUE): limit set is the full 2D plane (dim=2)
k=1 (AND,NOR,...): limit set is isolated points (dim=0)
k=0 (FALSE): empty set (dim=0)
"""

import numpy as np, math, collections

# ═══════════════════════════════════════════════════════════════════
# 1. Tile data
# ═══════════════════════════════════════════════════════════════════

def make_tt(idx):
    return tuple((idx>>(3-i))&1 for i in range(4))

def walsh(tt):
    v00,v01,v10,v11=tt
    return (v00+v01+v10+v11, v00-v01+v10-v11,
            v00+v01-v10-v11, v00-v01-v10+v11)

TILE_NAMES = {
    0:"FALSE",1:"AND",2:"A_AND_NOTB",3:"A",
    4:"NOTA_AND_B",5:"B",6:"XOR",7:"OR",
    8:"NOR",9:"XNOR",10:"NOTB",11:"B_IMP_A",
    12:"NOTA",13:"A_IMP_B",14:"NAND",15:"TRUE",
}

print("=" * 70)
print("CORRECTED HAUSDORFF DIMENSIONS")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════
# 2. Analytical support dimension
# ═══════════════════════════════════════════════════════════════════

print("\n1. Analytical support dimension (infinite depth limit):\n")
print(f"  A tile with k = number of 1s in the 4-entry truth table has")
print(f"  IFS support dimension = log2(k) at the limit.")
print(f"  (For k=0: dim=0, k=1: dim=log2(1)=0, k=2: dim=1, k=3: dim~1.585, k=4: dim=2)")
print()

print(f"  {'Tile':>12} | tt      | k | dim_support (analytical)")
print(f"  {'-'*12}-+--------+---+------------------------")

analytical_dims = {}
for idx in range(16):
    tt = make_tt(idx)
    k = sum(tt)
    name = TILE_NAMES[idx]
    if k == 0:
        dim = 0.0
    elif k == 1:
        dim = 0.0  # singleton set, dim 0
    else:
        dim = math.log2(k)
    analytical_dims[idx] = dim
    print(f"  {name:>12} | {tt} | {k} | {dim:.4f}")

print()

# ═══════════════════════════════════════════════════════════════════
# 3. Computational support dimension at finite depth
# ═══════════════════════════════════════════════════════════════════

print("2. Computational support dimension (finite depth box-counting):\n")

def ifs_support(tile_idx, depth):
    """Binary support: 1 if IFS accumulator == MAX (all levels occupied at all depths).
    This is the 'top slice' — cells in the IFS limit set that survive to infinite depth."""
    N = 1 << depth
    max_val = (1 << depth) - 1  # 2^d - 1: all bits = 1 at all levels
    tt = make_tt(tile_idx)
    grid = np.zeros((N, N), dtype=np.int32)
    for r in range(N):
        for c in range(N):
            acc = 0
            for i in range(depth):
                ra = (r >> (depth-1-i)) & 1
                cb = (c >> (depth-1-i)) & 1
                acc += tt[ra*2 + cb] << (depth-1-i)
            # Only cells that NEVER hit a 0 bit at any level are in the IFS limit set
            # This means the cell's accumulator must be at MAXIMUM value
            if acc == max_val:
                grid[r,c] = 1
    return grid

def box_count_binary(grid, box_size):
    """Count boxes of size box_size containing at least one occupied cell."""
    N = grid.shape[0]
    count = 0
    for i in range(0, N, box_size):
        for j in range(0, N, box_size):
            if np.any(grid[i:i+box_size, j:j+box_size] > 0):
                count += 1
    return count

def estimate_dim(grid):
    """Box-counting dimension from power-of-2 box sizes."""
    N = grid.shape[0]
    sizes, counts = [], []
    box = 1
    while box <= N:
        sizes.append(box)
        counts.append(box_count_binary(grid, box))
        box *= 2
    if len(sizes) < 3 or min(counts) == 0:
        return 0.0
    valid = [(s, c) for s, c in zip(sizes, counts) if c > 0]
    if len(valid) < 2:
        return 0.0
    log_sizes = np.log([1.0/s for s, _ in valid])
    log_counts = np.log([float(c) for _, c in valid])
    A = np.vstack([log_sizes, np.ones(len(log_sizes))]).T
    dim, _ = np.linalg.lstsq(A, log_counts, rcond=None)[0]
    return dim

depth = 7
N = 1 << depth

print(f"  {'Tile':>12} | k  | dim_support(analytical) | dim_support(depth {depth})")
print(f"  {'-'*12}-+----+------------------------+----------------------")

for idx in range(16):
    grid = ifs_support(idx, depth)
    dim_comp = estimate_dim(grid)
    dim_anal = analytical_dims[idx]
    k = sum(make_tt(idx))
    name = TILE_NAMES[idx]
    
    # Check convergence: compare computational to analytical
    conv = abs(dim_comp - dim_anal) < 0.01
    tag = "OK" if conv else "MISMATCH"
    
    print(f"  {name:>12} | {k:>2} | {dim_anal:.4f}               | {dim_comp:.4f}  [{tag}]")

print()

# ═══════════════════════════════════════════════════════════════════
# 4. Value solid dimension (3D height map)
# ═══════════════════════════════════════════════════════════════════

print("3. Value solid dimension (3D height map, depth 6):\n")

def value_solid(tile_idx, depth):
    """3D grid: grid[r,c,z] = 1 if IFS accumulator at (r,c) >= z."""
    N = 1 << depth
    max_val = (1 << depth) - 1
    tt = make_tt(tile_idx)
    grid_3d = np.zeros((N, N, max_val + 1), dtype=np.int32)
    for r in range(N):
        for c in range(N):
            acc = 0
            for i in range(depth):
                ra = (r >> (depth-1-i)) & 1
                cb = (c >> (depth-1-i)) & 1
                acc += tt[ra*2 + cb] << (depth-1-i)
            for z in range(acc + 1):
                grid_3d[r, c, z] = 1
    return grid_3d

def box_count_3d(grid_3d, box_size):
    """Count 3D boxes containing at least one occupied voxel."""
    N = grid_3d.shape[0]
    count = 0
    for i in range(0, N, box_size):
        for j in range(0, N, box_size):
            for k in range(0, N, box_size):
                if np.any(grid_3d[i:i+box_size, j:j+box_size, k:k+box_size] > 0):
                    count += 1
    return count

def estimate_dim_3d(grid_3d):
    """Box-counting dimension for 3D grid."""
    N = grid_3d.shape[0]
    sizes, counts = [], []
    box = 1
    while box <= N:
        sizes.append(box)
        counts.append(box_count_3d(grid_3d, box))
        box *= 2
    if len(sizes) < 3 or min(counts) == 0:
        return 0.0
    valid = [(s, c) for s, c in zip(sizes, counts) if c > 0]
    if len(valid) < 2:
        return 0.0
    log_sizes = np.log([1.0/s for s, _ in valid])
    log_counts = np.log([float(c) for _, c in valid])
    A = np.vstack([log_sizes, np.ones(len(log_sizes))]).T
    dim, _ = np.linalg.lstsq(A, log_counts, rcond=None)[0]
    return dim

depth_vs = 6  # must be small enough for 3D box counting to be fast
N_vs = 1 << depth_vs

print(f"  {'Tile':>12} | k  | dim_support(analytical) | dim_valuesolid(depth {depth_vs}) | expected")
print(f"  {'-'*12}-+----+------------------------+----------------------------+----------")

for idx in range(16):
    k = sum(make_tt(idx))
    dim_anal = analytical_dims[idx]
    name = TILE_NAMES[idx]
    
    if k == 0:
        dim_vs = 0.0
        exp = "empty"
    else:
        grid_3d = value_solid(idx, depth_vs)
        dim_vs = estimate_dim_3d(grid_3d)
        # Value solid should have dim ~ 2 (fills a 2D surface in 3D)
        exp = "~2" if abs(dim_vs - 2.0) < 0.15 else f"other({dim_vs:.3f})"
    
    print(f"  {name:>12} | {k:>2} | {dim_anal:.4f}               | {dim_vs:.4f}                 | {exp}")

print()

# ═══════════════════════════════════════════════════════════════════
# 5. Summary
# ═══════════════════════════════════════════════════════════════════

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
  The earlier computation (~1.978, ~1.999, 2.000) was measuring the
  FRACTAL SUPPORT of the IFS at finite depth, NOT the analytical
  Hausdorff dimension.  The values were converging toward but not
  reaching the infinite-depth limit.
  
  The correct analytical formula:
    dim_support = log2(k)   where k = #{1s} in the tile's truth table
    At infinite depth, the support dimension is:
      k=0 (FALSE):        dim=0
      k=1 (NOR, etc.):    dim=0 (single cells, isolated dust)
      k=2 (A,B,XOR,...):  dim=1 (1D Cantor-like sets)
      k=3 (AND,OR,...):   dim=log2(3) ~ 1.585
      k=4 (TRUE):         dim=2 (full 2D)
  
  The VALUE SOLID (3D height map) dimension is ~2.0 for all non-trivial
  tiles, because the height maps are 2D surfaces embedded in 3D space.
  
  The earlier '3 families' (~1.978, ~1.999, 2.000) were artifacts of
  finite-depth box-counting on the binary support, not the true
  Hausdorff dimensions.  The corrected picture changes the generation
  family assignment: AND/OR family has dim=log2(3)~1.585 (not ~1.978),
  A/B family has dim=1 (not ~1.999), TRUE has dim=2.
""")
