# How often does the truly strongest team (by expected goal diff) win a 22-game season?
import random, math
def pois(l):
    L,k,p=math.exp(-l),0,1.0
    while True:
        p*=random.random()
        if p<=L: return k
        k+=1
random.seed(3); N=2000; best_wins=0; top3=0
for _ in range(N):
    atk=[random.gauss(1.2,.25) for _ in range(12)]; dfn=[random.gauss(1,.2) for _ in range(12)]
    strength=sorted(range(12),key=lambda i:-(atk[i]/dfn[i]))
    pts=[0]*12; gd=[0]*12
    for h in range(12):
        for a in range(12):
            if h==a: continue
            gh,ga=pois(atk[h]*dfn[a]*1.15),pois(atk[a]*dfn[h]/1.15)
            gd[h]+=gh-ga; gd[a]+=ga-gh
            if gh>ga: pts[h]+=3
            elif gh<ga: pts[a]+=3
            else: pts[h]+=1; pts[a]+=1
    order=sorted(range(12),key=lambda i:(-pts[i],-gd[i]))
    best_wins+= order[0]==strength[0]
    top3+= strength[0] in order[:3]
print(f"strongest team champion: {best_wins/N:.0%}; finishes top 3: {top3/N:.0%}")
