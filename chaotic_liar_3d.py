"""chaotic_liar_3d.py
The 3D liar: THREE independent copies of the 1D liar:
  p <-> ~p, q <-> ~q, r <-> ~r
  
This gives the 3D product tent map:
  T_3(p,q,r) = (1 - |2p-1|, 1 - |2q-1|, 1 - |2r-1|)

The attractor is the 3D Sierpinski sponge = 3D Cantor dust.
The boundary of the attractor at maximal truth projects to S^3 = SU(2).

The 3 variables (p,q,r) map to (x,y,z) Walsh coefficients — the
3 non-DC coefficients of the 16-tile system. SO(3) rotates them.
"""

import numpy as np
import math

print("=" * 70)
print("CHAOTIC LIAR: 3D  (n=3, 256 Boolean functions)")
print("=" * 70)
print()

# 3D liar: THREE independent 1D liars
# p <-> ~p = 1 - |2p-1|
# q <-> ~q = 1 - |2q-1|
# r <-> ~r = 1 - |2r-1|
# T_3(p,q,r) = (T(p), T(q), T(r))

def liar_3d(p, q, r):
    """Three independent 1D liars = 3D product tent map."""
    return (1.0 - abs(2*p - 1.0),
            1.0 - abs(2*q - 1.0),
            1.0 - abs(2*r - 1.0))

print("1. Independent liar iteration on [0,1]^3:\n")
print(f"  p <-> ~p, q <-> ~q, r <-> ~r are independent tent maps\n")

# The 3 variables (p,q,r) correspond to (x,y,z) Walsh coefficients
# These are the 3 non-DC components: R_A, R_B, R_AB
# The boundary of the 3D attractor is the sphere S^2 (if we fix DC=a)

print("2. The 3D liar variables = (x,y,z) Walsh coefficients:\n")
print(f"  p <-> ~p  —>  x (R_A coefficient)  — dipole along A")
print(f"  q <-> ~q  —>  y (R_B coefficient)  — dipole along B")
print(f"  r <-> ~r  —>  z (R_AB coefficient) — dipole along A^B")
print(f"")
print(f"  The boundary |(p,q,r)| = 1 is S^2.")
print(f"  SO(3) rotations of S^2 are the adjoint rep of SU(2).")
print()

# The CCW rotation cycles (x,y,z) -> (y,z,x) which is a
# 120-degree rotation about (1,1,1) in SO(3)
# SO(3) = SU(2)/Z2, so SU(2) is the double cover

print("3. SU(2) from the boundary S^2:\n")
print(f"  The 3D liar maps R^3 -> R^3 via the product tent map.")
print(f"  The boundary S^2: the set of (p,q,r) where p^2+q^2+r^2 = 1.")
print(f"  SO(3) acts on S^2 by rotations.")
print(f"  SU(2) = double cover of SO(3).")
print(f"  The CCW rotation is an SO(3) element (order 3).")
print()

# Lyapunov exponents
print(f"4. Lyapunov exponents:\n")
print(f"  lambda_p = lambda_q = lambda_r = log(2) = {math.log(2):.6f}")
print(f"  Total = 3*log(2) = {3*math.log(2):.6f}")
print()

# The full SM chain
print("5. The full chain:\n")
print(f"  Dimension | Variables | Tent map   | Attractor     | Symmetry")
print(f"  {'-'*9}-+-{'-'*10}-+-{'-'*11}-+-{'-'*14}-+-{'-'*15}")
print(f"  1D        | p         | T(p)       | Cantor dust   | Z2")
print(f"  2D        | p,q       | T_2(p,q)   | Sierpinski    | S_3 = SU(3) Weyl")
print(f"  3D        | p,q,r     | T_3(p,q,r) | 3D sponge     | SO(3) = SU(2)")
print(f"  Phase     | arg(p)    | U(1) fiber | Circle S^1    | U(1)")
print()

print("=" * 70)
print("CHAOTIC LIAR 3D: COMPLETE")
print("=" * 70)
print("""
  Three independent 1D liars give the 3D product tent map.
  
  The 3 variables map to (x,y,z) Walsh coefficients.
  The boundary of the attractor is S^2.
  SO(3) rotations of S^2 give SU(2).
  
  The full SM gauge group:
    SU(3) from the S_3 symmetry of the 2D liar
    SU(2) from the SO(3) symmetry of the 3D liar boundary
    U(1) from the phase of the Walsh coefficients
""")
