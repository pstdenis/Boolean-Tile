"""chaotic_liar_report.py
Synthesis: The Standard Model gauge groups are the symmetry groups
of the chaotic liar attractor at various dimensionalities.

The liar biconditional p <-> ~p in Lukasiewicz logic = 1 - |2p-1| = the tent map.
The tent map is chaotic (Lyapunov = log 2) and generates the IFS.
At n variables, n independent tent maps generate the nD IFS.
The symmetry groups of these attractors are:
  n=1: Cantor dust -> Z2
  n=2: Sierpinski carpet -> S_3 (SU(3) Weyl) 
  n=3: 3D Sierpinski sponge -> SO(3) (SU(2) adjoint)
  Phase: U(1) fiber
"""

print("=" * 70)
print("CHAOTIC LIAR -> SM GAUGE GROUPS")
print("=" * 70)
print()

print("""
The liar biconditional:
  p <-> ~p  =  1 - |p - (1-p)|  =  1 - |2p-1|
  
  This IS the tent map T(p).  Iterating T(p) generates the
  dyadic IFS: at each step, one bit of p's binary expansion
  determines the next function in the IFS tree.
  
  The tent map has Lyapunov exponent lambda = log 2 > 0 -> CHAOS.
  
  The chaotic liar IS the engine that drives the IFS.
""")

print("The hierarchy:\n")
print(f"  {'n':>2} | {'Variables':>12} | {'Tent map':>18} | {'Attractor':>25} | {'Symmetry':>18} | {'Gauge group':>18}")
print(f"  {'-'*2}-+-{'-'*12}-+-{'-'*18}-+-{'-'*25}-+-{'-'*18}-+-{'-'*18}")
print(f"  {'1':>2} | {'p':>12} | {'T(p) = 1-|2p-1|':>18} | {'Cantor dust (dim=0.63)':>25} | {'Z2':>18} | {'(trivial)':>18}")
print(f"  {'2':>2} | {'p,q':>12} | {'T_2 = (Tp,Tq)':>18} | {'Sierpinski carpet (dim~1.89)':>25} | {'S_3':>18} | {'SU(3) Weyl':>18}")
print(f"  {'3':>2} | {'p,q,r':>12} | {'T_3 = (Tp,Tq,Tr)':>18} | {'3D Sierpinski sponge (dim~2)':>25} | {'SO(3)':>18} | {'SU(2)/Z2':>18}")
print(f"  {'Phase':>2} | {'arg(p)':>12} | {'U(1) fiber':>18} | {'Circle S^1':>25} | {'U(1)':>18} | {'U(1)':>18}")
print()

print("The Lyapunov exponents are additive:\n")
print(f"  n=1: lambda = log(2)") 
print(f"  n=2: lambda_1 + lambda_2 = 2*log(2)")
print(f"  n=3: lambda_1 + lambda_2 + lambda_3 = 3*log(2)")
print(f"  The IFS is a product of independent chaotic maps.")
print()

print("The connection to the 16 Boolean tiles:\n")
print(f"  The 16 tiles = IFS at depth 2 for n=2 liar attractor.")
print(f"  The Walsh coefficients (a,x,y,z) are Fourier modes of")
print(f"  the liar attractor on the 2D truth table grid.")
print(f"  The CCW rotation on (x,y,z) is the S_3 symmetry.")
print(f"  S_3 is the Weyl group of SU(3).")
print(f"")
print(f"  The (x,y,z) directions span S^2, which has SO(3)=SU(2)/Z2")
print(f"  rotational symmetry from the 3D liar attractor.")
print(f"")
print(f"  The U(1) exchange phase theta = exp(i*z*pi/4) is the")
print(f"  circle fiber that gives the U(1) gauge group.")

print()
print("=" * 70)
print("FULL CHAIN")
print("=" * 70)
print("""
  Liar paradox (logic)
    |
    | Lukasiewicz biconditional: p <-> ~p = 1 - |2p-1|
    v
  Tent map (dynamics, chaotic, Lyapunov = log 2)
    |
    | Iteration of the tent map = dyadic IFS
    v
  IFS attractor (Cantor dust / Sierpinski / 3D sponge)
    |
    | Walsh transform on the IFS truth tables
    v
  Walsh coefficients (a,x,y,z,...)
    |
    | Clifford algebra of the Walsh basis functions
    v
  Cl(2n,0) for n Boolean variables
    |
    | Symmetry groups of the liar attractor at each n
    v
  SU(3) x SU(2) x U(1)
    (Standard Model gauge groups)
""")
