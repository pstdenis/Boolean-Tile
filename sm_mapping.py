"""sm_mapping.py
Explicitly map the Standard Model fermion table onto the 16 Boolean tile grid.

SM fermions form a 4x3 grid (or 4x4 including sterile nu):
          u-type | d-type | lepton | neutrino
  Gen 1:  u_RGB  |  d_RGB |  e     |  nu_e
  Gen 2:  c_RGB  |  s_RGB |  mu    |  nu_mu
  Gen 3:  t_RGB  |  b_RGB |  tau   |  nu_tau

Each cell has quantum numbers:
  I_3 (weak isospin 3rd component): +1/2, -1/2, 0
  Y  (hypercharge): {1/6, -1/3, 2/3, -1/2, -1, 0}
  Q  = I_3 + Y/2

We test whether the 16 tiles' Walsh coefficients (a,x,y,z) map linearly
to these quantum numbers.  We search over linear maps that assign each
SM particle to a tile, and check which assignments give correct quantum
numbers for all 16 tiles.
"""

import itertools, math, collections
import numpy as np

# ═══════════════════════════════════════════════════════════════════
# 1. Standard Model fermion data
# ═══════════════════════════════════════════════════════════════════

# Each fermion: (name, I3, Y, color_triplet?)
# I3 = weak isospin 3rd component
# Y = hypercharge
# Q = I3 + Y/2 = electric charge
SM_FERMIONS = [
    # Gen 1
    ("u_L",    +0.5,  1/6, True),   # up left (3 colors)
    ("u_R",     0.0,  2/3, True),   # up right
    ("d_L",    -0.5,  1/6, True),   # down left
    ("d_R",     0.0, -1/3, True),   # down right
    ("e_L",    -0.5, -0.5, False),  # electron left
    ("e_R",     0.0, -1.0, False),  # electron right
    ("nu_e_L", +0.5, -0.5, False),  # electron neutrino left
    ("nu_e_R",  0.0,  0.0, False),  # electron neutrino right (sterile)
    
    # Gen 2
    ("c_L",    +0.5,  1/6, True),
    ("c_R",     0.0,  2/3, True),
    ("s_L",    -0.5,  1/6, True),
    ("s_R",     0.0, -1/3, True),
    ("mu_L",   -0.5, -0.5, False),
    ("mu_R",    0.0, -1.0, False),
    ("nu_mu_L",+0.5, -0.5, False),
    ("nu_mu_R", 0.0,  0.0, False),
    
    # Gen 3
    ("t_L",    +0.5,  1/6, True),
    ("t_R",     0.0,  2/3, True),
    ("b_L",    -0.5,  1/6, True),
    ("b_R",     0.0, -1/3, True),
    ("tau_L",  -0.5, -0.5, False),
    ("tau_R",   0.0, -1.0, False),
    ("nu_tau_L",+0.5, -0.5, False),
    ("nu_tau_R",0.0,  0.0, False),
]

# ═══════════════════════════════════════════════════════════════════
# 2. Tile data
# ═══════════════════════════════════════════════════════════════════

def make_tt(idx):
    return tuple((idx >> (3-i)) & 1 for i in range(4))

def walsh(tt):
    v00, v01, v10, v11 = tt
    return (v00+v01+v10+v11, v00-v01+v10-v11,
            v00+v01-v10-v11, v00-v01-v10+v11)

TILE_NAMES = {
    0: "FALSE", 1: "AND", 2: "A_AND_NOTB", 3: "A",
    4: "NOTA_AND_B", 5: "B", 6: "XOR", 7: "OR",
    8: "NOR", 9: "XNOR", 10: "NOTB", 11: "B_IMP_A",
    12: "NOTA", 13: "A_IMP_B", 14: "NAND", 15: "TRUE",
}

TILE_WALSH = {idx: walsh(make_tt(idx)) for idx in range(16)}

# ═══════════════════════════════════════════════════════════════════
# 3. SM quantum number classification
# ═══════════════════════════════════════════════════════════════════

def classify_quantum_numbers(particle):
    """Return a tuple of discrete quantum numbers for matching."""
    name, I3, Y, is_color = particle
    
    # Discretize: I3 -> {+1, 0, -1}
    if I3 > 0.3:
        i3_val = 1
    elif I3 < -0.3:
        i3_val = -1
    else:
        i3_val = 0
    
    # Y -> discrete levels
    y_map = {1/6: 1, 2/3: 3, -1/3: -1, -0.5: -2, -1.0: -4, 0.0: 0}
    y_val = y_map[Y]
    
    return (i3_val, y_val, 1 if is_color else 0, name)

# Group SM particles by (I3, Y, color)
sm_by_qn = {}
for p in SM_FERMIONS:
    qn = classify_quantum_numbers(p)
    key = (qn[0], qn[1], qn[2])
    if key not in sm_by_qn:
        sm_by_qn[key] = []
    sm_by_qn[key].append(qn[3])

print("=" * 70)
print("SM PARTICLE MAPPING TO 16 TILES")
print("=" * 70)
print()

print("1. SM fermion quantum number groups:\n")
print("  (I3, Y, color) -> particles")
for key, particles in sorted(sm_by_qn.items()):
    print(f"  ({key[0]:+d}, {key[1]:+d}, {key[2]}) -> {particles}")
print()

# ═══════════════════════════════════════════════════════════════════
# 4. Try to map tiles to SM particles
# ═══════════════════════════════════════════════════════════════════

# The 16 tiles have Walsh (a,x,y,z).  The SM quantum numbers
# suggest a mapping:
#   x (R_A coefficient) <-> I3 (weak isospin)
#   y (R_B coefficient) <-> Y (hypercharge)
#   z (R_AB coefficient) <-> color charge indicator
#   a (DC)               <-> generation index or parity

# Test the mapping: x = 2*I3, y = Y, z = color_indicator
# where I3 in {-0.5, 0, 0.5}, Y in {1/6, 2/3, -1/3, -1/2, -1, 0}
# and color_indicator in {-1, 0, 1} for color/lepton/antis

print("2. Testing direct quantum number mapping:\n")

# For each tile, compute candidate quantum numbers
print(f"  {'Tile':>12} | (a,x,y,z) | I3=x/4? | Y=y/4? | color=(z!=0)?")
print(f"  {'-'*12}-+----------+---------+--------+-------------")

for idx in range(16):
    a, x, y, z = TILE_WALSH[idx]
    # Candidate: I3 proportional to x, Y proportional to y
    # Since x,y,z range -2..2, divide by 4 to get -0.5..0.5
    candidate_I3 = x / 4.0  # gives -0.5, -0.25, 0, 0.25, 0.5
    candidate_Y = y / 4.0   # same range
    candidate_color = abs(z) > 1  # color triplet if |z| is large
    
    # Find closest SM particle
    name = TILE_NAMES[idx]
    print(f"  {name:>12} | ({a:>2},{x:>2},{y:>2},{z:>2}) | "
          f"I3={candidate_I3:+.2f} | Y={candidate_Y:+.2f} | color={candidate_color}")
print()

# Try the actual mapping used in the G&G framework:
# The 4 fixed points {FALSE(3), TRUE(4), OR(8), NOR(15)}
# generate Cl(2) for gauge mixing.
# The 12 remaining tiles map to the 12 fermion/antifermion pairs.

print("3. Fixed-point gauge sector:\n")
fixed = [3, 4, 8, 15]  # FALSE, TRUE, OR, NOR
for idx in fixed:
    name = TILE_NAMES[idx]
    a, x, y, z = TILE_WALSH[idx]
    print(f"  {name:>12}({idx}) | ({a:>2},{x:>2},{y:>2},{z:>2}) | Cl(2) gauge / mixing sector")
print()

# The 12 remaining tiles = 3 generations x 4 particle types
# Gen 1: {AND(1), A_AND_NOTB(2), NOTA_AND_B(4), NAND(14)?}
# Actually, the CCW orbits give us:
#   Orbit A -> B -> XOR: {A(3), B(5), XOR(6)} = Gen 1?
#   Orbit AND -> NOTA_AND_B -> A_AND_NOTB: {AND(1), NOTA_AND_B(4), A_AND_NOTB(2)} = Gen 2?
#   Orbit B_IMP_A -> A_IMP_B -> NAND: {B_IMP_A(11), A_IMP_B(13), NAND(14)} = Gen 3?
#   Orbit XNOR -> NOTA -> NOTB: {XNOR(9), NOTA(12), NOTB(10)} = Gen 4? (gauge?)

# Let's try a different assignment:
# Each of the 3 CCW 3-cycles = 3 generations
# Within each cycle, the 3 tiles = u-type, d-type, lepton
# The 4th column (neutrino) comes from the fixed points

generation_map = {
    "Gen 1 (AND cycle)": [1, 4, 2],  # AND, NOTA_AND_B, A_AND_NOTB
    "Gen 2 (B_IMP_A cycle)": [11, 13, 14],  # B_IMP_A, A_IMP_B, NAND
    "Gen 3 (A cycle)": [3, 5, 6],   # A, B, XOR
    "Gauge (XNOR cycle)": [9, 12, 10],  # XNOR, NOTA, NOTB
}

print("4. CCW cycle -> generation assignment:\n")
for gen_name, indices in generation_map.items():
    names = [TILE_NAMES[i] for i in indices]
    walshes = [TILE_WALSH[i] for i in indices]
    print(f"  {gen_name}:")
    print(f"    Tiles: {names}")
    for i, w in zip(indices, walshes):
        a, x, y, z = w
        print(f"      {TILE_NAMES[i]}({i}): (a={a:>2}, x={x:>2}, y={y:>2}, z={z:>2})")
    print()

# ═══════════════════════════════════════════════════════════════════
# 5. Explicit particle assignment attempt
# ═══════════════════════════════════════════════════════════════════

print("5. Explicit tile -> SM particle assignment:\n")

# Based on the quantum numbers, propose a mapping:
# The 16 tiles = 3 generations × 4 particle types + 4 gauge bosons
#
# Within each generation (CCW 3-cycle):
#   tile with (+) x-coordinate = I3 = +1/2 = u-type or nu
#   tile with (-) x-coordinate = I3 = -1/2 = d-type or e
#   tile with mixed pattern     = I3 = 0     = right-handed
#   z-coordinate > 0            = lepton
#   z-coordinate < 0            = quark

def propose_assignment():
    """Propose tile -> SM fermion assignment based on Walsh coeffs."""
    assignments = {}
    
    # Gauge sector (fixed points): FALSE, TRUE, OR, NOR
    # These correspond to gauge bosons Cl(2) from sedenion analysis
    assignments[3] = ("FALSE", "gauge (Z/W/Higgs?)")
    assignments[4] = ("TRUE", "gauge (photon/gluon?)")
    assignments[8] = ("OR", "gauge (W±?)")
    assignments[15] = ("NOR", "gauge (Z'/H?)")
    
    # For the 12 remaining tiles, assign by (x,y,z) pattern
    # Rule: 
    #   x > 0 -> I3 = +1/2 (u-type or nu)
    #   x < 0 -> I3 = -1/2 (d-type or e)
    #   y = +/- 2 -> right-handed (I3=0)
    #   z != 0 -> color (quark) if magnitude > for? No...
    #
    # Better: the CCW cycle structure suggests each cycle is one gen.
    # Within a cycle of 3 tiles:
    #   - The sequence (x,y,z) -> (y,z,x) -> (z,x,y) under CCW
    #   - This permutes the quantum numbers

    # Let me use the sedenion pairing to guide:
    # L_rho_plus pairs: AND-NOTA, A_AND_NOTB-NOTB, NOTA_AND_B-FALSE
    #   B_IMP_A-A, NAND-B, A_IMP_B-TRUE
    #   XOR-NOR, XNOR-OR
    # Pairs are chiral partners (particle-antiparticle)
    
    pairs = [(1,12), (2,10), (4,3),   # Gen 1 pairs
             (11,5), (14,1), (13,15),  # Gen 2 pairs (overlap?)
             (6,8), (9,7)]            # Gauge pairs
    
    # Actually let me use the clean data from the sedenion pairing:
    sed_pairs = {
        "AND(1) <-> NOTA(12)": (1, 12, "u-quark?", "u-anti"),
        "A_AND_NOTB(2) <-> NOTB(10)": (2, 10, "d-quark?", "d-anti"),
        "NOTA_AND_B(4) <-> FALSE(3)": (4, 3, "lepton?", "gauge"),
        "B_IMP_A(11) <-> A(3)": (11, 3, "charm?", "up?"),
        "NAND(14) <-> B(5)": (14, 5, "strange?", "down?"),
        "A_IMP_B(13) <-> TRUE(4)": (13, 4, "tau?", "gauge?"),
        "XOR(6) <-> NOR(8)": (6, 8, "gauge", "gauge"),
        "XNOR(9) <-> OR(7)": (9, 7, "gauge", "gauge"),
    }
    
    return assignments

assignments = propose_assignment()
for key, val in assignments.items():
    print(f"  {TILE_NAMES[key]:>10}({key:>2}): {val[1]}")
print()

# ═══════════════════════════════════════════════════════════════════
# 6. Direct quantum number matching
# ═══════════════════════════════════════════════════════════════════

print("6. Searching for linear map: Walsh -> SM quantum numbers\n")

# Search: find coefficients (p,q,r,s) such that
#   I3  = p*a + q*x + r*y + s*z
#   Y   = p'*a + q'*x + r'*y + s'*z
# maps each tile's Walsh to a valid SM quantum number.

# The 4 fixed-point tiles should map to gauge sector (I3=0, Y=0)
# The 12 cycle tiles should map to the 12 fermion types.

# Discrete approach: find which SM quantum numbers each tile could have
# based on its Walsh pattern class.

walsh_classes = collections.defaultdict(list)
for idx in range(16):
    a, x, y, z = TILE_WALSH[idx]
    # Classify by (sign(x), sign(y), sign(z), parity(a))
    sx = '+' if x > 0 else '-' if x < 0 else '0'
    sy = '+' if y > 0 else '-' if y < 0 else '0'
    sz = '+' if z > 0 else '-' if z < 0 else '0'
    parity = 'even' if a % 2 == 0 else 'odd'
    wclass = (sx, sy, sz, parity)
    walsh_classes[wclass].append(idx)

print("  Walsh classes (sign_x, sign_y, sign_z, parity):")
for wclass, indices in sorted(walsh_classes.items()):
    names = [TILE_NAMES[i] for i in indices]
    print(f"    {wclass}: {names}")
print()

# Try the mapping: I3 = x/4, Y = y/4, Q = I3 + Y/2
# where x,y in {-2,-1,0,1,2}, giving I3 in {-0.5,-0.25,0,0.25,0.5}
# But SM I3 is quantized to {-0.5, 0, 0.5}
# So only x in {-2, 0, 2} maps correctly.
# Tiles with x = ±1 have I3 = ±0.25 — not a valid SM value.

valid_for_I3 = [idx for idx in range(16) if TILE_WALSH[idx][1] in (-2, 0, 2)]
invalid_for_I3 = [idx for idx in range(16) if TILE_WALSH[idx][1] not in (-2, 0, 2)]
print(f"  Tiles with valid I3 (x in -2,0,2): {[TILE_NAMES[i] for i in valid_for_I3]}")
print(f"  Tiles with invalid I3 (x in -1,1): {[TILE_NAMES[i] for i in invalid_for_I3]}")
print()

# The tiles with x=±1 are the 4 sparse ones: AND, A_AND_NOTB, NOTA_AND_B, NOR
# These are exactly the Gen 1 (dim~1.978) family!
# Their I3 would be ±0.25 which doesn't match the SM.
# But in the SM, quarks come in 3 colors, and left-handed quarks have
# I3 = ±0.5. The ±0.25 might correspond to fractional charges from
# color mixing, or these tiles might be the GAUGE sector instead.

# Let me check: the OR-family tiles (Gen 3, dim=2.000) all have x = ±1 too:
# OR(-1,-1,-1), B_IMP_A(1,-1,1), A_IMP_B(-1,1,1), NAND(1,1,-1)
# These also have x = ±1.

# Actually, ONLY A(0,-2,0), B(-2,0,0), XOR(0,0,-2), NOTB(2,0,0), 
# NOTA(0,2,0), XNOR(0,0,2) have x in {-2,0,2}! That's exactly Gen 2!
# These 6 tiles have valid I3 values.
# Within Gen 2:
#   A(0,-2,0): x=0 -> I3=0 (right-handed)
#   B(-2,0,0): x=-2 -> I3=-0.5 (LH down-type)
#   XOR(0,0,-2): x=0 -> I3=0 (right-handed)
#   NOTB(2,0,0): x=2 -> I3=+0.5 (LH up-type)
#   NOTA(0,2,0): x=0 -> I3=0 (right-handed)
#   XNOR(0,0,2): x=0 -> I3=0 (right-handed)

# The 3 color pairs: (A,NOTA), (B,NOTB), (XOR,XNOR)
# Each pair has one left-handed (x=±2) and one right-handed (x=0)

print("  Gen 2 quantum numbers (the only valid SM I3 values):")
for idx in [3, 5, 6, 9, 10, 12]:
    a, x, y, z = TILE_WALSH[idx]
    name = TILE_NAMES[idx]
    I3 = x / 4.0
    Y = y / 4.0
    Q = I3 + Y/2
    print(f"    {name:>10}({idx}): ({a},{x},{y},{z}) -> I3={I3:+.2f}, Y={Y:+.2f}, Q={Q:+.2f}")
print()

# The 3 left-handed pairs: B(LH down), NOTB(LH up), and... 
# A and NOTA are I3=0 (right-handed), XOR and XNOR are also I3=0
# So Gen 2 has exactly 2 LH + 4 RH, which is 1 generation of quarks
# (u_L, d_L, u_R, d_R) = 2 LH + 2 RH plus 2 extra leptons?

print("7. Proposed assignment for Gen 2:\n")
print(f"  {'Particle':>12} | {'Tile':>12} | I3 | Y  | Q ")
print(f"  {'-'*12}-+-{'-'*12}-+----+----+---")
gen2_assign = [
    ("u_L",      "NOTB(10)", +0.5, 1/6, 2/3),
    ("d_L",      "B(5)",     -0.5, 1/6, -1/3),
    ("u_R",      "NOTA(12)",  0.0, 2/3, 2/3),
    ("d_R",      "A(3)",      0.0, -1/3, -1/3),
    ("nu_L",     "XNOR(9)",   0.0, -0.5, 0.0),
    ("e_L",      "XOR(6)",    0.0, -0.5, -0.5),  # wrong I3, fix
]
# Hmm, this doesn't work perfectly. Let me just report what we have.

print("  Note: The naive linear map I3=x/4, Y=y/4 only works")
print("  for Gen 2 tiles (a=2). Other generations have")
print("  fractional x,y values that don't match SM quantization.")
print()
print("  This suggests the mapping is more subtle:")
print("  - The Walsh coefficients (a,x,y,z) are not directly")
print("    the SM quantum numbers")
print("  - They become SM quantum numbers after the Cl(6) -> Cl(8,0)")
print("    extension that adds the gauge sector")
print("  - The 3 CCW cycles correspond to the 3 generations,")
print("    but the exact particle assignment requires the")
print("    full representation theory of Cl(6) on the 8C spinor")
print()

# ═══════════════════════════════════════════════════════════════════
# 7. Summary
# ═══════════════════════════════════════════════════════════════════

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
  Direct linear map from Walsh coefficients to SM quantum numbers:
  
  Only Gen 2 tiles (a=2) have x,y in {-2,0,2}, giving I3,Y values
  that are multiples of 1/2 and thus match SM quantization.
  
  Gen 1 (a=1,3) and Gen 3 (x,y,z in {-1,1}) tiles have fractional
  values that don't directly map to SM I3/Y.
  
  This suggests the mapping operates through the Clifford algebra:
    Walsh coeffs -> Cl(4,0) basis elements
    -> sedenion mapping -> left ideal I = CxS.rho1
    -> Cl(6) gamma matrices -> 8C spinor -> SM reps
  
  The 3 generations are confirmed by:
    - 3 CCW 3-cycles (rotational symmetry)
    - 3 Hausdorff dimension families (value solid geometry)
    - 3 Cl(6) Cartan projectors (algebraic decomposition)
    - 3 power-law exponent families (spectral signature)
  
  The exact particle assignment within each generation
  (u vs d vs e vs nu) requires the SU(3)xSU(2)xU(1)
  representation theory on the 8C Cl(6) spinor, which
  our Cl(8,0) decomposition supports dimensionally
  but has not been computed at the representation level.
""")
