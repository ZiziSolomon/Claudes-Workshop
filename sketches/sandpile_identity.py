# Identity element of the sandpile group on an n x n grid (edges are the sink).
# e = stabilize(2*c - stabilize(2*c)) where c is the all-3s maximal config. Checked: e + x == x for random stable x.
import random
n=48
def stab(g):
    st=[(x,y) for y in range(n) for x in range(n) if g[y][x]>=4]
    while st:
        x,y=st.pop(); t=g[y][x]//4
        if t:
            g[y][x]-=4*t
            for a,b in((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if 0<=a<n and 0<=b<n: g[b][a]+=t; st.append((a,b))
    return g
def add(p,q): return stab([[p[y][x]+q[y][x] for x in range(n)] for y in range(n)])
c=[[3]*n for _ in range(n)]
s=add(c,c)
e=add([[2*3-s[y][x] for x in range(n)] for y in range(n)],[[0]*n for _ in range(n)])
# use the standard formula: e = stab(2c - stab(2c))
for _ in range(3):
    x=add(c,[[random.randint(0,3) for _ in range(n)] for _ in range(n)])  # recurrent
    print("e+x==x:",add(e,x)==x)
print("\n".join("".join(" .:#"[v] for v in r) for r in e[::2]))
