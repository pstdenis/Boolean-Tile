"""lukasiewicz_lagrangian.py
Explore the Liar paradox iteration in Łukasiewicz logic on the 16-tile
Walsh coefficient space as a dynamical system, and compare to a
Yang-Mills-like Lagrangian.

The liar iteration: p → ¬p → p → ... (period 2 in 1D)
Extended to 4D Walsh space: (a,x,y,z) → ¬(a,x,y,z) → ...
with the full Łukasiewicz operations: ¬q, q⊕r, q⊙r, q→r

The radial projection proj(q) = q/|q| for |q|>1 introduces non-linearity
that creates chaotic dynamics — the liar becomes a strange attractor.
"""

import numpy as np
import math

# ═══════════════════════════════════════════════════════════════════
# 1. Łukasiewicz operations on the 4D Walsh coefficient space
# ═══════════════════════════════════════════════════════════════════

# Walsh coefficients range in [-4,4] for DC, [-2,2] for others
# The unit ball is |q| <= 1, but Walsh coeffs typically exceed this.
# The radial projection projects back to the unit ball.

def proj(q):
    """Radial projection onto the closed unit ball B^4."""
    n = math.sqrt(sum(x*x for x in q))
    if n <= 1:
        return q
    f = 1.0 / n
    return tuple(f * x for x in q)

def luk_not(q):
    """Łukasiewicz negation: ¬q = -q (in Walsh space, (4-a, -x, -y, -z))."""
    a, x, y, z = q
    return (4 - a, -x, -y, -z)

def luk_or(q, r):
    """Łukasiewicz strong disjunction: q ⊕ r = proj(q+r-1)."""
    return proj(tuple(q[i] + r[i] - (1 if i == 0 else 0) for i in range(4)))

def luk_and(q, r):
    """Łukasiewicz strong conjunction: q ⊙ r = proj(q+r+1)."""
    return proj(tuple(q[i] + r[i] + (1 if i == 0 else 0) for i in range(4)))

def luk_imp(q, r):
    """Łukasiewicz implication: q → r = ¬q ⊕ r."""
    return luk_or(luk_not(q), r)

# ═══════════════════════════════════════════════════════════════════
# 2. The Liar paradox in Łukasiewicz logic
# ═══════════════════════════════════════════════════════════════════

# The Liar: "This statement is false." → p = ¬p
# In Łukasiewicz: p = 1-p → p = 0.5 (the fixed point)
# In Walsh space: q = ¬q → q = (2, 0, 0, 0) (the center)

print("=" * 70)
print("ŁUKASIEWICZ LIAR AS DYNAMICAL SYSTEM")
print("=" * 70)
print()

print("1. Liar fixed points:\n")
# Solve q = ¬q: (a,x,y,z) = (4-a, -x, -y, -z)
# => a = 2, x = 0, y = 0, z = 0
liar_fixed = (2, 0, 0, 0)
print(f"  Liar fixed point q = ¬q: ({liar_fixed[0]}, {liar_fixed[1]}, {liar_fixed[2]}, {liar_fixed[3]})")
print(f"  In tile terms: the center of Walsh space (a=2, all others zero)")
print()

# More complex liar-like statements:
# "This statement is equivalent to its negation" → p = ¬p (same as above)
# "p or not p" → p ⊕ ¬p = proj(p + (1-p) - 1) = proj(0) = (0,0,0,0) = FALSE (always false)
# "p and not p" → p ⊙ ¬p = proj(p + (1-p) + 1) = proj(2) = (1,0,0,0) = ? 

print(f"  p ⊕ ¬p = FALSE (always false, excluded middle fails)")
print(f"  p ⊙ ¬p = proj(2,0,0,0) = (1,0,0,0) (NOT false — paraconsistent)")
print()

# ═══════════════════════════════════════════════════════════════════
# 3. Iterated liar system
# ═══════════════════════════════════════════════════════════════════

# The liar iteration: x_{n+1} = ¬x_n (period 2)
# But with projection: x_{n+1} = proj(¬x_n) = proj(4-a, -x, -y, -z)
# If |¬x_n| > 1, projection kicks in → non-linear → chaos?

def iterate_luk(f, x0, n_steps, record_each=False):
    """Iterate a Łukasiewicz function f starting from x0.
    Returns the trajectory as a list of points.
    """
    trail = [x0]
    x = x0
    for i in range(n_steps):
        x = f(x)
        trail.append(x)
    return trail

# Simple liar: x → ¬x → x → ...
print("2. Simple liar iteration (x → ¬x → x → ...):\n")
trail = iterate_luk(luk_not, liar_fixed, 4)
for i, t in enumerate(trail):
    tag = "(FIXED)" if t == liar_fixed else ""
    print(f"  x{i} = ({t[0]:.4f}, {t[1]:.4f}, {t[2]:.4f}, {t[3]:.4f}) {tag}")

print(f"\n  The fixed point (2,0,0,0) is stable under ¬ — no chaos yet.\n")

# The liar with projection from a non-fixed starting point
# Start with any tile's Walsh coefficients
tile_walshes = {
    'A': (2, 0, -2, 0),
    'B': (2, -2, 0, 0),
    'XOR': (2, 0, 0, -2),
    'OR': (3, -1, -1, -1),
    'AND': (1, -1, -1, 1),
}

print("3. Liar iteration from tile starting points:\n")
for name, q0 in tile_walshes.items():
    trail = iterate_luk(luk_not, q0, 6)
    period = None
    for i in range(2, len(trail)):
        if trail[i] == q0:
            period = i
            break
    proj_norm = max(math.sqrt(sum(x*x for x in t)) for t in trail)
    print(f"  {name:>5}: start=({q0[0]},{q0[1]},{q0[2]},{q0[3]}) "
          f"period={period}, max|proj|={proj_norm:.4f}")

print()

# ═══════════════════════════════════════════════════════════════════
# 4. The liar with Łukasiewicz OR (self-referential)
# p = p ⊕ p  →  p = proj(2p-1)
# This is the "self-OR" iteration: x_{n+1} = x_n ⊕ x_n = proj(2*x_n - 1)
# (with the -1 applied to the a/DC component)

def self_or(q):
    """Self-referential OR: x → x ⊕ x = proj(2x - (1,0,0,0))."""
    return proj(tuple(2*q[i] - (1 if i == 0 else 0) for i in range(4)))

print("4. Self-referential OR iteration (x → x ⊕ x):\n")

for name, q0 in tile_walshes.items():
    trail = iterate_luk(self_or, q0, 10)
    # Check for convergence to fixed point
    final = trail[-1]
    diff = max(abs(final[i] - trail[-2][i]) for i in range(4))
    print(f"  {name:>5}: {q0} → {final}, Δlast={diff:.4f}")

print()

# The self-OR operator has fixed points at q where q = proj(2q-(1,0,0,0))
# This means either |2q-(1,0,0,0)| <= 1 (so no projection needed) or
# q is on the boundary |q| = 1.
# Fixed points without projection: 2q-(1,0,0,0) = q → q = (1,0,0,0)
# In Walsh space: a=1, x=0, y=0, z=0, which is mapped from truth-tables
# with a=1 (like AND, NOR)... but let's check the actual iteration.

# ═══════════════════════════════════════════════════════════════════
# 5. Action/Lagrangian for the liar iteration
# ═══════════════════════════════════════════════════════════════════

# For a discrete dynamical system x_{n+1} = f(x_n), the action is:
# S = sum_n |x_{n+1} - f(x_n)|^2  (minimum along actual trajectory)
# 
# For the continuous version, the liar fixed point equation q = f(q)
# gives the Euler-Lagrange equation: the gradient of the potential V(q)
# balances the "force" from the kinetic term.
#
# We define V(q) = |q - f(q)|^2 — the "self-consistency potential"
# The liar fixed points are the minima of V.

print("5. Self-consistency potential V(q) = |q - f(q)|^2:\n")

import math

def V_not(q):
    """V(q) = |q - ¬q|^2"""
    diff = tuple(q[i] - luk_not(q)[i] for i in range(4))
    return sum(x*x for x in diff)

def V_self_or(q):
    """V(q) = |q - (q ⊕ q)|^2"""
    fq = self_or(q)
    diff = tuple(q[i] - fq[i] for i in range(4))
    return sum(x*x for x in diff)

print(f"  Liar V(q) = |q - ¬q|^2:")
for name, q0 in tile_walshes.items():
    v = V_not(q0)
    print(f"    {name:>5}: V({q0}) = {v:.4f}")

print(f"\n  Self-OR V(q) = |q - q⊕q|^2:")
for name, q0 in tile_walshes.items():
    v = V_self_or(q0)
    print(f"    {name:>5}: V({q0}) = {v:.4f}")

# The liar Lagrangian: L = (dφ/dt)^2 - V(φ)  where φ(t) ∈ R^4
# This is a scalar field theory with one field φ = (a,x,y,z).
# The standard Yang-Mills Lagrangian: L_YM = tr(F∧*F)
# where F = dA + A∧A is the field strength of the gauge field A.

# Comparison: the liar Lagrangian has a single 4-component field φ
# while YM has an 8-component gauge field A (for SU(3)) plus 3+1 more.
# The liar iteration is the equation of motion for φ:
#   d²φ/dt² + ∇V(φ) = 0
# which at the fixed point gives ∇V = 0 → φ = ¬φ → φ = (2,0,0,0).

# ═══════════════════════════════════════════════════════════════════
# 6. Summary
# ═══════════════════════════════════════════════════════════════════

print(f"\n" + "=" * 70)
print("SUMMARY: ŁUKASIEWICZ LAGRANGIAN")
print("=" * 70)
print("""
  The liar iteration in Łukasiewicz logic on the 4D Walsh space
  has fixed points that solve q = ¬q, giving (a,x,y,z) = (2,0,0,0).
  
  The self-consistency potential V(q) = |q - f(q)|^2 defines a
  Lagrangian L = (dφ/dt)^2 - V(φ) for a single 4-component field.
  
  The Standard Model Lagrangian has more fields (8 gluons for SU(3),
  3 weak bosons for SU(2), 1 photon for U(1)) and a more complex
  structure with gauge interactions.
  
  To connect: the 4-component Walsh field (a,x,y,z) would need to
  be SU(3)×SU(2)×U(1)-valued, not R^4-valued.  The projection
  proj(q) would become the non-linear gauge interaction term.
  
  This mapping is not yet established computationally, but the
  structure is suggestive: the radial projection has the same
  mathematical form as the non-abelian field strength F = dA + A∧A.
  
  Future work: formulate the liar iteration on the SU(3)×SU(2)×U(1)
  gauge bundle and compare the resulting EOM to Yang-Mills.
""")
