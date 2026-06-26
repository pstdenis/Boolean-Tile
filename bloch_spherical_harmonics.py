"""bloch_spherical_harmonics.py
Verify that the Three.js Bloch sphere visualization of the 16 tiles
is exactly the spherical harmonic decomposition we analyzed.

Each tile's radial surface at (theta, phi) = IFS accumulator mapped to S^2.
The radial deformation decomposes into spherical harmonics Y_l^m.
The decomposition coefficients ARE the Walsh coefficients (a,x,y,z).
"""

import numpy as np, math, itertools, collections

# ═══════════════════════════════════════════════════════════════════
# 1. Tile data and IFS accumulator (matching Bloch.html code)
# ═══════════════════════════════════════════════════════════════════

def make_tt(idx):
    return tuple((idx >> (3-i)) & 1 for i in range(4))

def walsh(tt):
    v00,v01,v10,v11 = tt
    return (v00+v01+v10+v11, v00-v01+v10-v11,
            v00+v01-v10-v11, v00-v01-v10+v11)

TILE_NAMES = {
    0:"FALSE",1:"AND",2:"A_AND_NOTB",3:"A",
    4:"NOTA_AND_B",5:"B",6:"XOR",7:"OR",
    8:"NOR",9:"XNOR",10:"NOTB",11:"B_IMP_A",
    12:"NOTA",13:"A_IMP_B",14:"NAND",15:"TRUE",
}
TILE_WALSH = {idx: walsh(make_tt(idx)) for idx in range(16)}

def ifs_accumulator(tile_idx, row, col, depth):
    """Match Bloch.html: reads truth table bits at each IFS level."""
    tt = make_tt(tile_idx)
    acc = 0
    for i in range(depth):
        rb = (row >> (depth - 1 - i)) & 1
        cb = (col >> (depth - 1 - i)) & 1
        acc += ((tt[rb * 2 + cb])) << (depth - 1 - i)
    return acc

# ═══════════════════════════════════════════════════════════════════
# 2. Sample the radial surface at S^2 grid points (like Bloch.html)
# ═══════════════════════════════════════════════════════════════════

RES = 64  # sampling resolution (Bloch.html uses 128, but 64 is fine for verification)
DEPTH = 4  # IFS depth
N = 1 << DEPTH
MAX_VAL = N - 1
MAX_RADIUS = 1.6  # matches Bloch.html

print("=" * 70)
print("BLOCH SPHERE SPHERICAL HARMONIC DECOMPOSITION")
print("=" * 70)
print()

for tile_idx in range(16):
    # Sample the radial function R(theta, phi) on the S^2 grid
    radial_samples = np.zeros((RES, RES))
    for tr in range(RES):
        theta = (tr / RES) * math.pi
        ri = int(math.floor((tr / RES) * N))
        for tc in range(RES):
            ci = int(math.floor((tc / RES) * N))
            acc = ifs_accumulator(tile_idx, ri, ci, DEPTH)
            ratio = acc / MAX_VAL
            
            # Bloch.html: R = acc===0 ? zeroRadius*MAX_RADIUS : ratio*MAX_RADIUS
            # But zeroRadius = 1/(1<<depth) is very small
            if acc == 0:
                R = (1.0 / N) * MAX_RADIUS
            else:
                R = ratio * MAX_RADIUS
            
            radial_samples[tr, tc] = R
    
    # Decompose into spherical harmonics
    # Y_0^0 = 1/sqrt(4*pi)
    # Y_1^0 = sqrt(3/(4*pi)) * cos(theta)
    # Y_1^1 = -sqrt(3/(4*pi)) * sin(theta) * exp(i*phi)
    # 
    # The radial function R(theta,phi) should be:
    # R = sum_{l,m} c_{l,m} * Y_l^m(theta,phi)
    # We compute c_{l,m} by integrating R * conj(Y_l^m) over S^2
    
    # Discretized spherical harmonic basis functions
    Y00 = np.zeros((RES, RES))
    Y10 = np.zeros((RES, RES))
    Y11_re = np.zeros((RES, RES))  # real part of Y_1^1
    Y11_im = np.zeros((RES, RES))  # imag part of Y_1^{-1}
    
    for tr in range(RES):
        theta = (tr / RES) * math.pi
        for tc in range(RES):
            phi = (tc / RES) * 2 * math.pi
            
            Y00[tr,tc] = 1.0 / math.sqrt(4*math.pi)
            Y10[tr,tc] = math.sqrt(3.0/(4*math.pi)) * math.cos(theta)
            # Real Y1^1 = -sqrt(3/(4pi)) * sin(theta) * cos(phi)
            # Imag Y1^1 = -sqrt(3/(4pi)) * sin(theta) * sin(phi)
            Y11_re[tr,tc] = -math.sqrt(3.0/(4*math.pi)) * math.sin(theta) * math.cos(phi)
            Y11_im[tr,tc] = -math.sqrt(3.0/(4*math.pi)) * math.sin(theta) * math.sin(phi)
    
    # Compute coefficients by integration over S^2
    # c_{l,m} = int R * conj(Y_l^m) * dOmega
    # dOmega = sin(theta) * dtheta * dphi
    d_theta = math.pi / RES
    d_phi = 2 * math.pi / RES
    
    c00 = 0
    c10 = 0
    c11_re = 0
    c11_im = 0
    
    for tr in range(RES):
        theta = (tr + 0.5) / RES * math.pi  # mid-point
        sin_t = math.sin(theta)
        weight = sin_t * d_theta * d_phi
        
        for tc in range(RES):
            R = radial_samples[tr, tc]
            
            c00 += R * Y00[tr,tc] * weight
            c10 += R * Y10[tr,tc] * weight
            c11_re += R * Y11_re[tr,tc] * weight
            c11_im += R * Y11_im[tr,tc] * weight
    
    # The Walsh coefficients of the tile:
    a, x, y, z = TILE_WALSH[tile_idx]
    
    # Scale the Walsh coefficients to match the spherical harmonic expansion
    # In the Bloch sphere visualization, the radius at each point is:
    # R = R_base + k*(x*sin(theta)*cos(phi) + y*sin(theta)*sin(phi) + z*cos(theta))
    # where R_base is the l=0 monopole (DC component)
    # The Walsh coefficients are related to the spherical harmonic coefficients via:
    # c00 ~ a  (monopole)
    # c10 ~ z  (coefficient of cos(theta) = Y_1^0)
    # c11_re ~ x  (coefficient of sin(theta)*cos(phi))
    # c11_im ~ y  (coefficient of sin(theta)*sin(phi))
    # (up to normalization factors)
    
    print(f"  {TILE_NAMES[tile_idx]:>10} (idx={tile_idx:>2}):")
    print(f"    Walsh=(a={a:>2}, x={x:>2}, y={y:>2}, z={z:>2})")
    print(f"    SH coeffs:  c00={c00:.4f}  c10={c10:.4f}  c11_re={c11_re:.4f}  c11_im={c11_im:.4f}")
    
    # The Walsh coefficients (a,x,y,z) should be proportional to (c00, c11_re, c11_im, c10)
    # up to a constant factor. Let's check the ratios.
    if abs(x) > 0.01:
        print(f"    Ratio c11_re/x = {c11_re/x:.4f}")
    if abs(y) > 0.01:
        print(f"    Ratio c11_im/y = {c11_im/y:.4f}")
    if abs(z) > 0.01:
        print(f"    Ratio c10/z = {c10/z:.4f}")
    if abs(a) > 0.01:
        print(f"    Ratio c00/a = {c00/a:.4f}")
    
    # Check if the ratios are consistent
    ratios = []
    for c, w in [(c11_re, x), (c11_im, y), (c10, z), (c00, a)]:
        if abs(w) > 0.01:
            ratios.append(c/w)
    if ratios:
        mean_r = np.mean(ratios)
        std_r = np.std(ratios)
        print(f"    Ratio consistency: mean={mean_r:.4f}, std={std_r:.4f} [{len(ratios)} measurements]")
    
    print()

# ═══════════════════════════════════════════════════════════════════
# 3. Summary
# ═══════════════════════════════════════════════════════════════════

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
  The Bloch sphere visualization renders each tile as a surface on S^2.
  The radial deformation at each (theta, phi) is the IFS accumulator.
  
  The spherical harmonic decomposition of this surface gives:
    c00 = coefficient of Y_0^0 (monopole) -> proportional to Walsh 'a' (DC)
    c10 = coefficient of Y_1^0 (z-dipole) -> proportional to Walsh 'z'
    c11_re = coefficient of Re(Y_1^1) (x-dipole) -> proportional to Walsh 'x'
    c11_im = coefficient of Im(Y_1^1) (y-dipole) -> proportional to Walsh 'y'
  
  If the ratios c/x, c/y, c/z, c/a are consistent, the visualization
  IS the spherical harmonic decomposition of the Walsh coefficients.
""")
