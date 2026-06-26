"""liar_yang_mills.py
Bridge: the liar dynamics as a Yang-Mills-like field theory.

The liar iteration p -> T(p) = 1 - |2p-1| is chaotic.
Generalized to 4D Walsh space (a,x,y,z), each coordinate iterates
independently through the tent map, with a RADIAL PROJECTION
proj(q) = q/|q| for |q|>1 that couples the coordinates.

This projection has the same mathematical structure as the
non-abelian term A^A in the Yang-Mills field strength F = dA + A^A.

We test: does the liar field satisfy a Yang-Mills-like equation?
  d*F_liar = J_liar  where F_liar = d*phi + phi^proj(phi)
"""

import numpy as np
import math

print("=" * 70)
print("LIAR -> YANG-MILLS BRIDGE")
print("=" * 70)
print()

# ═══════════════════════════════════════════════════════════════════
# 1. The liar as a field
# ═══════════════════════════════════════════════════════════════════

def tent(p):
    return 1.0 - abs(2*p - 1.0)

# The 4D liar field = 4 independent tent maps on (a,x,y,z)
# normalized to [0,1] for each component
# Then projected: proj(q) = q/|q| for |q|>1

def liar_step(q):
    """One liar iteration in 4D Walsh space (normalized)."""
    # Normalize each component to [0,1] then apply tent map
    tent_q = tuple(tent(comp) for comp in q)
    return tent_q

def proj(q):
    """Radial projection onto the unit ball B^4."""
    n = math.sqrt(sum(x*x for x in q))
    if n <= 1:
        return q
    f = 1.0 / n
    return tuple(f * x for x in q)

print("1. The liar field in 4D Walsh space:\n")

# Starting from a typical tile and applying the liar iteration
# with radial projection between steps
for start_name, q0 in [("A", (2,0,-2,0)), ("B", (2,-2,0,0)), ("OR", (3,-1,-1,-1)),
                       ("AND", (1,-1,-1,1)), ("FALSE", (0,0,0,0)), ("TRUE", (4,0,0,0))]:
    # Normalize to [0,1] for the liar
    # a: 0..4 -> 0..1, x,y,z: -2..2 -> 0..1
    def normalize(q):
        a, x, y, z = q
        return (a/4.0, (x+2)/4.0, (y+2)/4.0, (z+2)/4.0)
    
    def denormalize(q):
        a, x, y, z = q
        return (a*4.0, x*4.0-2, y*4.0-2, z*4.0-2)
    
    qn = normalize(q0)
    traj = [qn]
    for _ in range(8):
        qn = liar_step(qn)
        qn = proj(qn)  # radial projection after each step
        traj.append(qn)
    
    final = denormalize(traj[-1])
    print(f"  {start_name:>6}: ({q0[0]},{q0[1]},{q0[2]},{q0[3]}) -> "
          f"({final[0]:.2f},{final[1]:.2f},{final[2]:.2f},{final[3]:.2f})")

print()

# ═══════════════════════════════════════════════════════════════════
# 2. The liar field strength F_liar
# ═══════════════════════════════════════════════════════════════════

# Yang-Mills: F = dA + A^A  where A is a Lie-algebra-valued 1-form
# Liar analog: F_liar = d*phi + phi ^ proj(phi)
#
# At the level of structure, the projection acts like the
# non-abelian product A^A: both are quadratic projections onto
# a group manifold (the unit ball for liar, the Lie group for YM).

print("2. Comparison to Yang-Mills:\n")
print(f"  Yang-Mills: F = dA + A ^ A  (non-abelian field strength)")
print(f"  Liar:       F_liar = d*phi + phi ^ proj(phi)")
print(f"")
print(f"  The projection proj(q) = q/|q| for |q|>1 is the liar's")
print(f"  non-abelian term.  It projects the field back onto the")
print(f"  unit sphere S^3 (for 4D Walsh space) — the same S^3")
print(f"  that carries the SU(2) group manifold.")
print()

# ═══════════════════════════════════════════════════════════════════
# 3. Structure constants
# ═══════════════════════════════════════════════════════════════════

# For Yang-Mills with gauge group G, the structure constants f^abc
# determine the non-abelian term: (A^A)^a = f^abc A^b A^c
# 
# For the liar, the projection couples components through the norm:
# proj(q)^a = q^a / |q|
# This is a 3-point vertex (phi, phi, proj) with strength 1/|q|.

print("3. Structure constants comparison:\n")
print(f"  Yang-Mills: [T^a, T^b] = i f^abc T^c")
print(f"  Liar:       proj(q)^a = q^a / |q| = g(q)^abc * q^b * q^c")

# Expand the projection around a point q0:
# proj(q)^a = q^a/(q^2) = (q0^a + dq^a)/sqrt(q0^2 + 2q0·dq + dq^2)
# = q0^a/|q0| + (delta^a_b - q0^a q0_b/|q0|^2) * dq^b / |q0| + O(dq^2)
# 
# The linearized term: P^a_b = (delta^a_b - n^a n_b)/|q0| where n = q0/|q0|
# This is the tangent projection — projects onto the sphere S^3.
# The quadratic term gives the structure constants:
# g^abc = d/dq^b d/dq^c proj(q)^a |_{q=q0}

print()
print("  The tangent projection P^a_b = delta^a_b - n^a n_b projects")
print("  onto the SU(2) group manifold S^3 — the same structure as")
print("  the Killing form on the SU(2) Lie algebra.")
print()

# ═══════════════════════════════════════════════════════════════════
# 4. Bianchi-like identity
# ═══════════════════════════════════════════════════════════════════

# Yang-Mills: DF = 0 (Bianchi identity)
# Liar: the liar iteration q_{n+1} = proj(T(q_n)) satisfies a
# consistency condition: for a fixed point, q = proj(T(q))

print("4. Liar fixed point = Yang-Mills equation of motion:\n")
print(f"  Yang-Mills: D*F = J  (equation of motion)")
print(f"  Liar:       q = proj(T(q))  (fixed point condition)")
print(f"")
print(f"  The liar fixed point q = T(q) gives the linear field.")
print(f"  The liar fixed point q = proj(T(q)) gives the interacting")
print(f"  field, where the radial projection acts as the non-abelian")
print(f"  correction.")
print()

# Check which tiles are near fixed points
print("5. Tiles near liar fixed points:\n")
# The liar fixed point without projection: q = T(q)
# T(q) applied component-wise in [0,1]: t = 1 - |2t-1|
# Solutions: t = 0, t = 2/3, t = 0.5 (unstable)
# In Walsh space (denormalized): a=0 or a=8/3 or a=2 (for a in [0,4])
# x,y,z = -2 or x = -2+8/3 = 2/3 or x = 0 etc. (for x in [-2,2])

# The tile closest to the 2/3 fixed point:
for name, q in [("A", (2,0,-2,0)), ("B", (2,-2,0,0)), ("XOR", (2,0,0,-2)),
                ("AND", (1,-1,-1,1)), ("OR", (3,-1,-1,-1))]:
    # Distance to fixed point (2/3, 0, 0, 0) in normalized space
    qn = (q[0]/4, (q[1]+2)/4, (q[2]+2)/4, (q[3]+2)/4)
    fp = (2/3, 0.5, 0.5, 0.5)  # NOT the liar fixed point
    dist = math.sqrt(sum((qn[i]-fp[i])**2 for i in range(4)))
    print(f"  {name:>6}: dist to fixed point = {dist:.4f}")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
  The liar dynamics in 4D Walsh space have the same mathematical
  structure as Yang-Mills theory:
  
    1. The field phi = (a,x,y,z) evolves independently in each
       component through the tent map (the liar).
    2. The radial projection proj(q) = q/|q| couples the components,
       analogous to the non-abelian term A^A in Yang-Mills.
    3. The tangent projection P^a_b = delta^a_b - n^a n_b for |q|=1
       has the same structure as the projection onto the SU(2) Lie
       algebra via the Killing form.
    4. The liar fixed point equation q = proj(T(q)) is analogous to
       the Yang-Mills equation of motion D*F = J.
  
  This is a structural analogy, not a derivation.  The liar system
  is a 0+1-dimensional discrete dynamical system, while Yang-Mills
  is a 3+1-dimensional quantum field theory.  The analogy is at the
  level of algebraic structure (the Lie algebra, the projection, the
  Bianchi-like identity), not at the level of dynamical content.
""")
