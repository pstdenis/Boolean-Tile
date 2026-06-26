"""hypercharge_from_so10.py
Compute SM hypercharge Y from SO(10) Cartan eigenvalues on the 16C spinor.
The 5 Cartan generators hi of so(10) give eigenvalues +/- 1 on the 16C.
I3 = 0.5 * sum(ai*hi)  for half-integer ai
Y  = sum(bi*hi) / 6    for integer bi
Q = I3 + Y/2

We search over (ai, bi) to match the 16 SM fermion charges.
"""

import numpy as np, math

sx=np.array([[0,1],[1,0]],dtype=complex)
sy=np.array([[0,-1j],[1j,0]],dtype=complex)
sz=np.array([[1,0],[0,-1]],dtype=complex)
I2=np.eye(2,dtype=complex)

def kron(*m):
    r=m[0]
    for x in m[1:]: r=np.kron(r,x)
    return r

# Cl(10,0)
G=[kron(sx,I2,I2,I2,I2),kron(sy,I2,I2,I2,I2),kron(sz,sx,I2,I2,I2),kron(sz,sy,I2,I2,I2),
   kron(sz,sz,sx,I2,I2),kron(sz,sz,sy,I2,I2),kron(sz,sz,sz,sx,I2),kron(sz,sz,sz,sy,I2),
   kron(sz,sz,sz,sz,sx),kron(sz,sz,sz,sz,sy)]

# 16C spinor
G_all=G[0]
for i in range(1,10): G_all=G_all@G[i]
gamma=1j*G_all
_,evecs_g=np.linalg.eigh(gamma)
P=evecs_g[:,[i for i,v in enumerate(np.linalg.eigh(gamma)[0]) if abs(v.real-1)<0.1]]
print(f"16C spinor: {P.shape[1]} dim")

# 5 Cartan generators on 16C
H_16c = {}
for i,idx in enumerate([(0,1),(2,3),(4,5),(6,7),(8,9)]):
    H=0.5j*(G[idx[0]]@G[idx[1]]-G[idx[1]]@G[idx[0]])
    H_16c[i+1]=P.conj().T @ H @ P

# Simultaneous eigenbasis via random sum
rng=np.random.RandomState(42)
coeffs=[rng.randn() for _ in range(5)]
H_sum=sum(coeffs[i]*H_16c[i+1] for i in range(5))
_,evecs_s=np.linalg.eigh(H_sum)

# Cartan eigenvalues for each state
spinor_data=[]
for idx in range(16):
    vec=evecs_s[:,idx]
    h=tuple(int(round((vec.conj().T@H_16c[i+1]@vec).real,0)) for i in range(5))
    spinor_data.append((h,vec))

patterns=set(sd[0] for sd in spinor_data)
print(f"Distinct Cartan patterns: {len(patterns)}/16")
for p in sorted(patterns):
    print(f"  {[f'{v:+d}' for v in p]}")
print()

# SM charges expected for 16 SO(10) states
sm_exp = [
    ("u_L",+0.5,1/6,+2/3),("d_L",-0.5,1/6,-1/3),
    ("u_R",0.0,2/3,+2/3),("d_R",0.0,-1/3,-1/3),
    ("nu_L",+0.5,-0.5,0.0),("e_L",-0.5,-0.5,-1.0),
    ("e_R",0.0,-1.0,-1.0),("nu_R",0.0,0.0,0.0),
    ("ub_L",-0.5,-1/6,-2/3),("db_L",+0.5,-1/6,+1/3),
    ("ub_R",0.0,-2/3,-2/3),("db_R",0.0,+1/3,+1/3),
    ("nub_L",-0.5,+0.5,0.0),("eb_L",+0.5,+0.5,+1.0),
    ("eb_R",0.0,+1.0,+1.0),("nub_R",0.0,0.0,0.0),
]

# Search I3: a_i in {-2,-1,0,1,2} -> I3 = 0.5 * sum a_i*h_i
best_I3, best_I3s = None, 0
for a1 in range(-2,3):
 for a2 in range(-2,3):
  for a3 in range(-2,3):
   for a4 in range(-2,3):
    for a5 in range(-2,3):
     s=sum(1 for (h,_),(_,i,_,_) in zip(spinor_data,sm_exp)
           if abs(0.5*sum(a*h for a,h in zip([a1,a2,a3,a4,a5],h))-i)<0.01)
     if s>best_I3s: best_I3s,best_I3=s,(a1,a2,a3,a4,a5)

# Search Y: y_i in {-12..12} -> Y = sum(y_i*h_i)/6
best_Y, best_Ys = None, 0
if best_I3:
    for y1 in range(-12,13):
     for y2 in range(-12,13):
      for y3 in range(-12,13):
       for y4 in range(-12,13):
        for y5 in range(-12,13):
         if all(v==0 for v in [y1,y2,y3,y4,y5]): continue
         s=sum(1 for (h,_),(_,i,y,q) in zip(spinor_data,sm_exp)
               if abs(0.5*sum(a*h for a,h in zip(best_I3,h))-i)<0.01
               and abs(0.5*sum(a*h for a,h in zip(best_I3,h))
                       +sum(yi*hi for yi,hi in zip([y1,y2,y3,y4,y5],h))/12.0-q)<0.01)
         if s>best_Ys: best_Ys,best_Y=s,(y1,y2,y3,y4,y5)

print(f"I3 = 0.5 x {best_I3}: {best_I3s}/16")
print(f"Y  = {best_Y}/6: {best_Ys}/16")
print()

# Display
if best_Y is not None:
    a=best_I3; y=best_Y
    print(f"  {'Particle':>12} | {'h1 h2 h3 h4 h5':>18} | I3   Y    Q  ")
    print(f"  {'-'*12}-+-{'-'*18}-+-----------------")
    for (h,_),(name,i3,_,q) in zip(spinor_data,sm_exp):
        ci=0.5*sum(ai*hi for ai,hi in zip(a,h))
        cy=sum(yi*hi for yi,hi in zip(y,h))/6.0
        cq=ci+cy/2
        ok=abs(ci-i3)<0.01 and abs(cq-q)<0.01
        hs=" ".join(f"{hx:+d}" for hx in h)
        print(f"  {name:>12} | {hs:>18} | {ci:+.2f} {cy:+.2f} {cq:+.2f} {'✓' if ok else '✗'}")
    print(f"\nTotal: {best_Ys}/16 matches")

print(f"\n"+"="*70)
print("SUMMARY")
print("="*70)
if best_Ys==16:
    print(f"\nSM hypercharge VERIFIED: Y = ({best_Y})/6 * hi")
else:
    print(f"\nSM charges not fully matched ({best_Ys}/16).")
    print("Possible fixes:")
    print("1. Permute the SM particle ordering")
    print("2. Try different gauge group embedding")
    print("3. The 1/6 factor comes from a different normalization")
