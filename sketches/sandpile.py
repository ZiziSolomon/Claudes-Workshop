# Abelian sandpile: drop 5000 grains at the centre, topple at 4, print as ASCII
N=41; g=[[0]*N for _ in range(N)]; c=N//2; g[c][c]=5000
st=[(c,c)]
while st:
    x,y=st.pop()
    if g[y][x]>=4:
        t=g[y][x]//4; g[y][x]-=4*t
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            a,b=x+dx,y+dy
            if 0<=a<N and 0<=b<N: g[b][a]+=t; st.append((a,b))
        st.append((x,y))
print("\n".join("".join(" .:#"[v] for v in r) for r in g))
print("grains kept:",sum(map(sum,g)))
