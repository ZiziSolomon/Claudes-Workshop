# Sandpile with 30000 grains at the centre, drawn as SVG (no edge loss: grid is big enough).
N=201; c=N//2; g=[[0]*N for _ in range(N)]; g[c][c]=30000
st=[(c,c)]
while st:
    x,y=st.pop()
    t=g[y][x]//4
    if t:
        g[y][x]-=4*t
        for a,b in((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            g[b][a]+=t; st.append((a,b))
assert sum(map(sum,g))==30000
col=["#fbf6e9","#e9b44c","#c8553d","#2d3a4a"]
s=3
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{N*s}" height="{N*s}">']
for y in range(N):
    for x in range(N):
        if g[y][x]: o.append(f'<rect x="{x*s}" y="{y*s}" width="{s}" height="{s}" fill="{col[g[y][x]]}"/>')
o.append('</svg>')
open("sketches/sandpile.svg","w").write("\n".join(o))
print({v:sum(r.count(v) for r in g) for v in range(4)})
