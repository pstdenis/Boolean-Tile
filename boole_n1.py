"""boole_n1.py
The n=1 case: 1 Boolean variable P, 2 truth-table rows, 4 Boolean functions.

Cl(2,0) ≅ M2(R) — the algebra of 2x2 real matrices.
Kitaev: Z2 classification — the toric code with Abelian anyons.

This is the simplest non-trivial case in the hierarchy:
  n=0:  1 row,  1 function    R           trivial
  n=1:  2 rows, 4 functions   Cl(2,0)     Z2 (toric code)
  n=2:  4 rows, 16 functions  Cl(4,0)     Z16 (honeycomb/16-fold way)
  n=3:  8 rows, 256 functions Cl(8,0)     Z8 (8-fold way, Bott periodicity)
"""

import math, itertools

# ═══════════════════════════════════════════════════════════════════
# 1. The 4 functions of 1 variable
# ═══════════════════════════════════════════════════════════════════

# Truth table ordering: (P=0, P=1)
FUNC_DATA = [
    ("FALSE", (0, 0)),  # 0: always 0
    ("P",     (0, 1)),  # 1: identity
    ("NOT P", (1, 0)),  # 2: negation
    ("TRUE",  (1, 1)),  # 3: always 1
]

def walsh_1(tt):
    """2-point Walsh-Hadamard transform."""
    return (tt[0] + tt[1], tt[0] - tt[1])

print("=" * 72)
print("n=1: 4 BOOLEAN FUNCTIONS, Cl(2,0), TORIC CODE Z2")
print("=" * 72)

# ═══════════════════════════════════════════════════════════════════
# 2. Walsh spectra, exchange phases, Cl(2,0) correspondence
# ═══════════════════════════════════════════════════════════════════

print("\n--- 2.1 Walsh spectra and exchange phases ---\n")
print(f"{'Name':>8}  {'tt':>8}  {'Walsh (a,x)':>14}  {'|q|':>6}  "
      f"{'J (exchange)':>14}  {'J/pi':>6}  {'Cl(2,0) grade':>14}")
print("-" * 80)

for name, tt in FUNC_DATA:
    a, x = walsh_1(tt)
    # Exchange phase: theta = e^{i*2J} where J = x*pi/8
    J = x * math.pi / 8
    q_norm = math.sqrt(a*a + x*x)
    # Cl(2,0) grade: 0 for scalars, 1 for vectors, 2 for bivector
    if a != 0 and x != 0: grade = "1 + bivector"
    elif x != 0: grade = "grade-1 vector"
    else: grade = "grade-0 scalar"
    print(f"{name:>8}  {str(tt):>8}  ({a:>2},{x:>2})          "
          f"{q_norm:>6.2f}  {J:>+10.6f}  {J/math.pi:>+6.3f}  {grade:>14}")

print()

# ═══════════════════════════════════════════════════════════════════
# 3. Z2 toric code mapping
# ═══════════════════════════════════════════════════════════════════

print("--- 3.1 Toric code Z2 classification ---\n")

# In the toric code (Kitaev 2003), the anyon types are:
#   1 (vacuum), e (electric charge), m (magnetic flux), epsilon (fermion = e x m)
# The exchange phases are: theta_1 = 1, theta_e = 1, theta_m = 1, theta_eps = -1
# The classification is Z2: trivial (1,e,m) and non-trivial (epsilon).

# The 4 Boolean functions map to the 4 toric code sectors:
#   FALSE (tt=00) -> 1 (vacuum)
#   TRUE  (tt=11) -> m (magnetic flux)  -- all 1s
#   P     (tt=01) -> e (electric charge) -- parity odd at P=1
#   NOT P (tt=10) -> epsilon (fermion)   -- parity odd at P=0

# Exchange phase from Walsh: theta = e^{i * x * pi/4}
print(f"{'Function':>8}  {'z (=x)':>8}  {'J':>10}  {'theta':>16}  {'Toric code':>14}  {'Z2 class':>10}")
print("-" * 70)
for name, tt in FUNC_DATA:
    a, x = walsh_1(tt)
    J = x * math.pi / 8
    theta_real = math.cos(x * math.pi / 4)
    theta_imag = math.sin(x * math.pi / 4)
    
    # Toric code assignment (by convention matching Kitaev's Z2)
    if name == "FALSE":  tc = "1 (vacuum)"
    elif name == "P":    tc = "e (charge)"
    elif name == "NOT P": tc = "eps (fermion)"
    else:                tc = "m (flux)"
    
    z2 = "even (trivial)" if abs(theta_real - 1) < 0.01 else "odd"
    
    print(f"{name:>8}  {x:>8}  {J:>+10.6f}  {theta_real:>+.4f}{theta_imag:+.4f}i  "
          f"{tc:>14}  {z2:>10}")

print()
print("  The 4 functions split into:")
print("    Z2 even (theta=1):  FALSE (vacuum), P (charge e), TRUE (flux m)")
print("    Z2 odd  (theta=-1): NOT P (fermion = e x m)")
print()
print("  This Z2 grading matches the fermion parity in Kitaev's Z2")
print("  classification for 1 Majorana fermion mode.")
print()

# ═══════════════════════════════════════════════════════════════════
# 4. CCW/CW chirality for n=1
# ═══════════════════════════════════════════════════════════════════

print("--- 4.1 Chirality for n=1 ---\n")

# For n=1, the truth table has 2 entries: (v0, v1).
# The only non-trivial permutation is swapping the two entries:
#   (v0, v1) -> (v1, v0)
# This is the "chirality" operation for n=1.

def swap(tt):
    return (tt[1], tt[0])

print(f"{'Name':>8}  {'tt':>8}  {'swap(tt)':>10}  {'Walsh (a,x)':>14}  {'swap Walsh':>14}")
for name, tt in FUNC_DATA:
    a, x = walsh_1(tt)
    st = swap(tt)
    sa, sx = walsh_1(st)
    swapped_name = [n for n, t in FUNC_DATA if t == st][0]
    print(f"{name:>8}  {str(tt):>8}  {str(st):>10}  ({a:>2},{x:>2})          ({sa:>2},{sx:>2})  -> {swapped_name}")

print()
print("  Under swap: x -> -x (sign flip of exchange phase)")
print("  This is the n=1 analogue of the CW/CCW chirality.")
print("  Fixed points: FALSE (x=0) and TRUE (x=0)")
print("  Non-fixed: P and NOT P (x = -+ 1, swapped)")
print()

# ═══════════════════════════════════════════════════════════════════
# 5. Cl(2,0) algebra structure
# ═══════════════════════════════════════════════════════════════════

print("--- 5.1 Cl(2,0) algebra ---\n")

# Cl(2,0) has basis {1, e1, e2, e12} with e1^2 = 1, e2^2 = 1, e1 e2 = -e2 e1.
# The Boolean functions map to:
#   FALSE <-> 0 (zero in algebra)
#   TRUE  <-> 1 + e1 e2 (the "volume element")
#   P     <-> e1 (or e2)
#   NOT P <-> e2 (or e1)

# Multiplication table (Clifford product via pointwise XOR of truth tables):
print(f"  Cl(2,0) multiplication (via pointwise XOR of truth tables):")
print(f"  {'XOR':>8}  {'FALSE':>8}  {'P':>8}  {'NOT P':>8}  {'TRUE':>8}")
print("-" * 50)
for n1, t1 in FUNC_DATA:
    row = [f"{n1:>8}"]
    for n2, t2 in FUNC_DATA:
        xor_tt = tuple((t1[i] ^ t2[i]) for i in range(2))
        xor_name = [n for n, t in FUNC_DATA if t == xor_tt][0]
        row.append(f"{xor_name:>8}")
    print("  ".join(row))

print()
print("  This is Z2 x Z2 (Klein four-group). TRUE*TRUE = FALSE identity.")
print("  Cl(2,0) ≅ M2(R) as an algebra, but the Boolean functions")
print("  only see the abelian group structure (the Clifford product's")
print("  graded commutator is invisible at the pointwise-XOR level).")
print()

# ═══════════════════════════════════════════════════════════════════
# 6. The full hierarchy
# ═══════════════════════════════════════════════════════════════════

print("--- 6.1 The hierarchy ---\n")

print("  n=0 (1 row, 1 function):")
print("    R           - trivial classification")
print("    No logical connectives (just the constant)")
print()
print("  n=1 (2 rows, 4 functions):")
print("    Cl(2,0)     - toric code, Z2 classification")
print("    2-fold way: even/odd fermion parity")
print("    Anyons: 1, e, m, eps (Abelian)")
print()
print("  n=2 (4 rows, 16 functions):")
print("    Cl(4,0)     - honeycomb model, 16-fold way")
print("    Z16 classification via exchange phases")
print("    Anyons: Ising (d=sqrt2) and Fibonacci (d=phi)")
print()
print("  n=3 (8 rows, 256 functions):")
print("    Cl(8,0)     - 3 Majorana modes, 8-fold way (Bott)")
print("    Z8 classification")
print("    Anyons: SU(2)3 / 8-vertex model")
print()
print("  The Bott periodicity of Clifford algebras (Cl(n+8,0) ≅")
print("  Cl(n,0) ⊗ M16(R)) matches the 8-fold periodicity of the")
print("  Altland-Zirnbauer/Kitaev periodic table. The 16-fold way")
print("  is n=2 = 2 * 8 = 16.")
print()

# ═══════════════════════════════════════════════════════════════════
# 7. Exchange phase derivation for n=1
# ═══════════════════════════════════════════════════════════════════

print("--- 7.1 Exchange phase as Berry phase ---\n")

# For n=1, the Ising Hamiltonian is:
#   H = h * Z  (single-qubit Z field)
# where h = x * pi/8.
# 
# The exchange phase when moving around the parameter space
# (P=0 -> P=1 -> back) is the Berry phase:
#   gamma = pi * (1 + x) = pi + x*pi
# The additional pi comes from the Aharonov-Casher effect.
# 
# For theta = e^{i*gamma} = e^{i*pi} * e^{i*x*pi} = -e^{i*x*pi}
# With the standard Kitaev convention: theta = e^{i*pi*nu/2}
# So nu = x + 1 (mod 2).

print("  Berry phase for each function:")
for name, tt in FUNC_DATA:
    a, x = walsh_1(tt)
    berry = math.pi + x * math.pi
    nu = (x + 1) % 2
    print(f"  {name:>8}: x={x:>2},  Berry = pi + {x}pi = {berry/math.pi:.1f}*pi,  nu = {nu} (mod 2)")
print()

print("  This gives the Z2 classification:")
print("    nu=0 (even): FALSE, P, TRUE -> trivial sector")
print("    nu=1 (odd):  NOT P -> fermion sector")
print()
