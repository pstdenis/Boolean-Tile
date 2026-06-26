import plotly.graph_objects as go
import numpy as np, math

def make_tt(idx):
    return tuple((idx>>(3-i))&1 for i in range(4))
def walsh(tt):
    v00,v01,v10,v11=tt
    return (v00+v01+v10+v11,v00-v01+v10-v11,v00+v01-v10-v11,v00-v01-v10+v11)
def ccw(x,y,z): return (y,z,x)

TILE_NAMES = {0:"FALSE",1:"AND",2:"A_AND_NOTB",3:"A",4:"NOTA_AND_B",5:"B",
              6:"XOR",7:"OR",8:"NOR",9:"XNOR",10:"NOTB",11:"B_IMP_A",
              12:"NOTA",13:"A_IMP_B",14:"NAND",15:"TRUE"}

pts = {}
for idx in range(16):
    a,x,y,z = walsh(make_tt(idx))
    pts[idx] = (x,y,z,a,TILE_NAMES[idx])

# CCW orbits
orbits = []
unvisited = set(range(16))
while unvisited:
    start = min(unvisited)
    orbit = [start]
    a1,x1,y1,z1 = walsh(make_tt(start))
    
    # Fixed points: (0,0,0) stays at (0,0,0) under CCW (FALSE, TRUE)
    if x1==0 and y1==0 and z1==0:
        unvisited.discard(start)
        orbits.append(orbit)
        continue
    
    while True:
        x1,y1,z1 = ccw(x1,y1,z1)
        matches = [i for i in range(16) if walsh(make_tt(i))[1:]==(x1,y1,z1)]
        if not matches:
            break
        nxt = matches[0]
        if nxt==start: break
        orbit.append(nxt); unvisited.discard(nxt)
    unvisited.discard(start)
    orbit.sort()
    if len(orbit)>=3: orbits.append(orbit)
    else:
        # Fixed points: OR, NOR, FALSE, TRUE
        orbits.append(orbit)
    unvisited.discard(start)
    orbit.sort()

fig = go.Figure()

# Octahedron edges (all 12 edge segments as one trace)
verts = [(2,0,0),(-2,0,0),(0,2,0),(0,-2,0),(0,0,2),(0,0,-2)]
edge_xs, edge_ys, edge_zs = [], [], []
for i,v1 in enumerate(verts):
    for j,v2 in enumerate(verts):
        if i>=j: continue
        if (abs(v1[0])==2 and v2[0]==-2 and v1[1]==0 and v2[1]==0 and v1[2]==0 and v2[2]==0): continue
        if (v1[1]==2 and v2[1]==-2 and v1[0]==0 and v2[0]==0 and v1[2]==0 and v2[2]==0): continue
        if (v1[2]==2 and v2[2]==-2 and v1[0]==0 and v2[0]==0 and v1[1]==0 and v2[1]==0): continue
        edge_xs += [v1[0],v2[0],None]
        edge_ys += [v1[1],v2[1],None]
        edge_zs += [v1[2],v2[2],None]

fig.add_trace(go.Scatter3d(x=edge_xs,y=edge_ys,z=edge_zs,
    mode='lines',line=dict(color='gray',width=1.5),showlegend=False,hoverinfo='skip'))

# CCW cycles as single trace per orbit
ccw_colors = ['#FF6B6B','#4ECDC4','#45B7D1','#FFD93D']
ccw_names = ['CCW Cycle 1 (AND)','CCW Cycle 2 (B_IMP_A)','CCW Cycle 3 (A)','CCW Cycle 4 (XNOR)']

for ci,orb in enumerate(orbits):
    xs = [pts[i][0] for i in orb] + [None, pts[orb[0]][0]]
    ys = [pts[i][1] for i in orb] + [None, pts[orb[0]][1]]
    zs = [pts[i][2] for i in orb] + [None, pts[orb[0]][2]]
    fig.add_trace(go.Scatter3d(x=xs,y=ys,z=zs,
        mode='lines',line=dict(color=ccw_colors[ci%4],width=5),
        name=ccw_names[ci%4]))

# Dipole tiles + interior + FALSE/TRUE as scatter
x_dip,y_dip,z_dip,t_dip,c_dip = [],[],[],[],[]
x_int,y_int,z_int,t_int,c_int = [],[],[],[],[]
x_ft,y_ft,z_ft = [],[],[]

for idx,(x,y,z,a,name) in pts.items():
    mag = math.sqrt(x*x+y*y+z*z)
    if idx in [0,15]:
        x_ft.append(x); y_ft.append(y); z_ft.append(z)
    elif mag > 1.9:
        colors_dip = {'A':'#E74C3C','B':'#2ECC71','XOR':'#3498DB',
                      'NOTA':'#E67E22','NOTB':'#9B59B6','XNOR':'#1ABC9C'}
        x_dip.append(x); y_dip.append(y); z_dip.append(z)
        t_dip.append(name); c_dip.append(colors_dip.get(name,'purple'))
    else:
        x_int.append(x); y_int.append(y); z_int.append(z)
        t_int.append(name); c_int.append('#F39C12' if a%2==1 else '#95A5A6')

fig.add_trace(go.Scatter3d(x=x_dip,y=y_dip,z=z_dip,
    mode='markers+text',marker=dict(size=16,color=c_dip,line=dict(color='black',width=2)),
    text=t_dip,textposition='top center',name='Dipole tiles (SU(2) adjoint)'))

fig.add_trace(go.Scatter3d(x=x_int,y=y_int,z=z_int,
    mode='markers+text',marker=dict(size=8,color=c_int,line=dict(color='black',width=1)),
    text=t_int,textposition='top center',name='Mixed tiles (a=1,3)',showlegend=False))

fig.add_trace(go.Scatter3d(x=x_ft,y=y_ft,z=z_ft,
    mode='markers+text',marker=dict(size=14,color='white',line=dict(color='black',width=2)),
    text='FALSE/TRUE',textposition='top center',name='Center'))

# Axes
for col,lab in [('#E74C3C','R_A(x)'),('#2ECC71','R_B(y)'),('#3498DB','R_AB(z)')]:
    v=[0,0,0]
    idx = {'R_A(x)':0,'R_B(y)':1,'R_AB(z)':2}[lab]
    v[idx]=3
    fig.add_trace(go.Scatter3d(x=[0,v[0]],y=[0,v[1]],z=[0,v[2]],
        mode='lines',line=dict(color=col,width=4),showlegend=False,hoverinfo='skip'))
    fig.add_trace(go.Scatter3d(x=[v[0]],y=[v[1]],z=[v[2]],
        mode='text',text=[lab],textposition='top center',
        textfont=dict(color=col,size=14),showlegend=False,hoverinfo='skip'))

# SU(3) root system arrows: from origin to each dipole vertex
# 6 roots: ±R_A, ±R_B, ±R_AB (the 6 octahedron vertices)
root_vtx = [(2,0,0),(-2,0,0),(0,2,0),(0,-2,0),(0,0,2),(0,0,-2)]
root_xs, root_ys, root_zs = [], [], []
for rx,ry,rz in root_vtx:
    root_xs += [0,rx*0.95,None]  # stop just before the vertex marker
    root_ys += [0,ry*0.95,None]
    root_zs += [0,rz*0.95,None]
fig.add_trace(go.Scatter3d(x=root_xs,y=root_ys,z=root_zs,
    mode='lines',line=dict(color='#8E44AD',width=3.5,dash='dash'),
    name='SU(3) roots (6 gens, to dipole vertices)'))

fig.update_layout(
    title=dict(text='Walsh Octahedron: SM Gauge Structure from 16 Boolean Tiles<br>'
                    '<sub>6 dipole tiles = SU(2) adjoint | SU(3) roots (dashed) | CCW 3-cycles (colored)</sub>',
               font=dict(size=18)),
    scene=dict(
        xaxis=dict(title='R_A (x)',range=[-3.5,3.5]),
        yaxis=dict(title='R_B (y)',range=[-3.5,3.5]),
        zaxis=dict(title='R_AB (z)',range=[-3.5,3.5]),
        aspectmode='cube',
        camera=dict(eye=dict(x=1.8,y=1.5,z=0.8))
    ),
    legend=dict(x=0,y=1,font=dict(size=11)),
    width=950,height=800
)

fig.write_html(r'C:\Users\pauls\Desktop\Boolean Tile\docs\walsh_octahedron.html')
