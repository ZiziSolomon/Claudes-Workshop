# Abelian sandpile: drop 20000 grains at the centre, topple at 4, print as PGM->text summary
import numpy as np
N=61; g=np.zeros((N,N),int); g[N//2,N//2]=20000
while (g>=4).any():
    t=g//4; g-=4*t
    g[1:,:]+=t[:-1,:]; g[:-1,:]+=t[1:,:]; g[:,1:]+=t[:,:-1]; g[:,:-1]+=t[:,1:]
print("\n".join("".join(" .:#"[v] for v in r) for r in g[::2]))
print("grains kept:",g.sum())
