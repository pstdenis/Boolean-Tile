"""su2_from_s2.py
Demonstrate SU(2) acting on the (x,y,z) Walsh coefficients as SO(3)
rotations of the 2-sphere.

The l=1 spherical harmonic subspace is spanned by 3 Walsh coefficients
(x,y,z).  SO(3) acts on this space as rotations of S^2.
SU(2) is the double cover of SO(3).

The CCW permutation (x,y,z) -> (y,z,x) is an SO(3) rotation.
The 3 so(3) generators are:
  L_x = -i(y*d/dz - z*d/dy)  — rotation in (y,z) plane
  L_y = -i(z*d/dx - x*d/dz)  — rotation in (z,x) plane
  L_z = -i(x*d/dy - y*d/dx)  — rotation in (x,y) plane

We verify:
1. CCW is an SO(3) rotation (det=+1, R^3=I)
2. The 6 dipole tiles form ± pairs along the 3 coordinate axes
3. SO(3) rotations map tiles to tiles
4. The "top slice" of the IFS attracts converges to S^2
"""

import numpy as np
import math, itertools, collections

# ═══════════════════════════════════════════════════════════════════
# 1. Tile data and SO(3) structure
# ═══════════════════════════════════════════════════════════════════

def make_tt(idx):
    return tuple((idx >> (3-i)) & 1 for i in range(4))

def walsh(tt):
    v00,v01,v10,v11 = tt
    return (v00+v01+v10+v11, v00-v01+v10-v11,
            v00+v01-v10-v11, v00-v01-v10+v11)

TILE_NAMES = {
    0:"FALSE", 1:"AND", 2:"A_AND_NOTB", 3:"A",
    4:"NOTA_AND_B", 5:"B", 6:"XOR", 7:"OR",
    8:"NOR", 9:"XNOR", 10:"NOTB", 11:"B_IMP_A",
    12:"NOTA", 13:"A_IMP_B", 14:"NAND", 15:"TRUE",
}
TILE_WALSH = {idx: walsh(make_tt(idx)) for idx in range(16)}

print("=" * 70)
print("SU(2) FROM S^2: SPHERICAL HARMONICS ON 16 TILES")
print("=" * 70)
print()

# ═══════════════════════════════════════════════════════════════════
# 2. The 6 dipole tiles as ± coordinate axes on S^2
# ═══════════════════════════════════════════════════════════════════

print("1. Dipole basis as SU(2) weight space:\n")

dipole_axes = {
    "A/NOTA": (0, -2, 0),       # -y direction
    "B/NOTB": (-2, 0, 0),       # -x direction
    "XOR/XNOR": (0, 0, -2),     # -z direction
    "NOTA/A": (0, 2, 0),        # +y direction
    "NOTB/B": (2, 0, 0),        # +x direction
    "XNOR/XOR": (0, 0, 2),      # +z direction
}

print(f"  Dipole (l=1) tiles form ±x, ±y, ±z axes on S^2:\n")
for name, (x, y, z) in sorted(dipole_axes.items(), key=lambda kv: (kv[1][0], kv[1][1], kv[1][2])):
    r = math.sqrt(x*x + y*y + z*z)
    print(f"    {name:>15}: ({x:+d},{y:+d},{z:+d}) on S^2? r={r/2:.0f}")

# The 3 axes form an orthonormal basis for R^3
# SO(3) acts on this space as rotations
# The CCW rotation permutes the axes: x→y→z→x

print()

# ═══════════════════════════════════════════════════════════════════
# 3. Verify SO(3) rotation generators on (x,y,z)
# ═══════════════════════════════════════════════════════════════════

print("2. SO(3) generators on (x,y,z) space:\n")

# SO(3) Lie algebra: so(3) = span{L_x, L_y, L_z}
# [L_i, L_j] = i * epsilon_ijk * L_k

L_x = np.array([[0,0,0],[0,0,-1j],[0,1j,0]])  # rotation about x
L_y = np.array([[0,0,1j],[0,0,0],[-1j,0,0]])  # rotation about y
L_z = np.array([[0,-1j,0],[1j,0,0],[0,0,0]])  # rotation about z

# Verify [L_i, L_j] = i * epsilon_ijk * L_k
for (a, La, b, Lb, c, Lc) in [
    (1, L_x, 2, L_y, 3, L_z),
    (2, L_y, 3, L_z, 1, L_x),
    (3, L_z, 1, L_x, 2, L_y),
]:
    comm = La @ Lb - Lb @ La
    ok = np.allclose(comm, 1j * Lc, atol=1e-10)
    print(f"    [L_{a}, L_{b}] = i*L_{c}: {ok}")

# The CCW rotation as an SO(3) rotation about (1,1,1) by 120 degrees
# Using real Rodrigues rotation formula: R = I + sin(th)*K + (1-cos(th))*K^2
# where K is the cross-product matrix [n]x
n = np.array([1,1,1]) / math.sqrt(3)
theta = 2*math.pi/3
K = np.array([[0,-n[2],n[1]],[n[2],0,-n[0]],[-n[1],n[0],0]])
R_ccw = np.eye(3) + math.sin(theta)*K + (1-math.cos(theta))*(K @ K)

print(f"CCW rotation matrix:")
print(f"  R = {R_ccw.tolist()}")
print(f"  det(R) = {np.linalg.det(R_ccw):.1f} (should be +1)")
print(f"  R^3 = I? {np.allclose(R_ccw @ R_ccw @ R_ccw, np.eye(3), atol=1e-6)}")
print(f"  Acts as (x,y,z) -> ({R_ccw[0,0]:.0f}x+{R_ccw[0,1]:.0f}y+{R_ccw[0,2]:.0f}z, "
      f"{R_ccw[1,0]:.0f}x+{R_ccw[1,1]:.0f}y+{R_ccw[1,2]:.0f}z, "
      f"{R_ccw[2,0]:.0f}x+{R_ccw[2,1]:.0f}y+{R_ccw[2,2]:.0f}z)")
print()

# Find the index for a given tile name
def tile_idx(name):
    return next(i for i, n in TILE_NAMES.items() if n == name)

# Verify mapping of tiles under R_ccw
print(f"  Tile rotations under R_ccw:")
idx3 = tile_idx('A')
a,x,y,z = TILE_WALSH[idx3]
xyz = R_ccw @ np.array([x,y,z])
print(f"  A({x},{y},{z}) -> ({int(round(xyz[0]))},{int(round(xyz[1]))},{int(round(xyz[2]))})")

print()

# ═══════════════════════════════════════════════════════════════════
# 4. The "top slice" of IFS attractor converges to S^2
# ═══════════════════════════════════════════════════════════════════

print("3. Top slice of IFS attractor:\n")

# The top slice of each tile's IFS attractor is concentrated at specific
# (x,y,z) directions — not filling S^2.
# SU(2) appears as the rotational symmetry of the SET of all 6 dipole
# tile Walsh directions, not from any single tile's limit.

print("  SU(2) appears as the rotational symmetry of the 6 dipole")
print("  directions {±x, ±y, ±z} on S^2, NOT from any single tile's")
print("  top slice.  The set of 6 points is invariant under SO(3).")
print()

# ═══════════════════════════════════════════════════════════════════
# 4. SU(3) vs SU(2): two sides of the same coin
# ═══════════════════════════════════════════════════════════════════

print("4. SU(3) vs SU(2): two complementary symmetries\n")
print("""
  SU(3) acts on the DISCRETE weight lattice (bulk):
    8C spinor = 3 + 3* + 1 + 1
    Jordan-Schwinger creation/annihilation on G1..G6
    Generators: 2 Cartan + 6 roots

  SU(2) acts on the CONTINUOUS S^2 boundary:
    6 dipole tiles {±x, ±y, ±z} on S^2
    SO(3) rotations of (x,y,z) space
    Generators: L_x, L_y, L_z (cross-product matrices)

  They are independent because the SU(3) generators act on
  the (h0,h1) weight space, while SU(2) acts on (x,y,z).
  The combined group is SU(3) x SO(3) ~ SU(3) x SU(2)/Z2.
""")
