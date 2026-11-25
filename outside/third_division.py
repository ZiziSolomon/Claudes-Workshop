# A small-club season simulator: 12 teams, double round robin, Poisson goals.
# Team names are generic Baghdad-area-style placeholders (Junoob = "south").
import random, math, sys
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
random.seed(seed)
names = ["Junoob","Shamal","Sharq","Gharb","Latifiya","Mahmudiya","Yusufiya","Madain","Abu Ghraib","Taji","Karkh","Rusafa"]
atk = {n: random.gauss(1.2,0.25) for n in names}
dfn = {n: random.gauss(1.0,0.2) for n in names}
def pois(l):
    L, k, p = math.exp(-l), 0, 1.0
    while True:
        p *= random.random()
        if p <= L: return k
        k += 1
T = {n:[0,0,0,0,0,0] for n in names}  # P W D L GF GA
for h in names:
    for a in names:
        if h==a: continue
        gh, ga = pois(atk[h]*dfn[a]*1.15), pois(atk[a]*dfn[h]/1.15)
        for t,f,c in ((h,gh,ga),(a,ga,gh)):
            r=T[t]; r[0]+=1; r[4]+=f; r[5]+=c
            r[1 if f>c else 3 if f<c else 2]+=1
rows = sorted(names, key=lambda n:(-(3*T[n][1]+T[n][2]), -(T[n][4]-T[n][5]), -T[n][4]))
print(f"seed {seed}\n{'':3}{'team':<12}{'P':>3}{'W':>3}{'D':>3}{'L':>3}{'GF':>4}{'GA':>4}{'Pts':>4}")
for i,n in enumerate(rows,1):
    r=T[n]; print(f"{i:<3}{n:<12}{r[0]:>3}{r[1]:>3}{r[2]:>3}{r[3]:>3}{r[4]:>4}{r[5]:>4}{3*r[1]+r[2]:>4}")
