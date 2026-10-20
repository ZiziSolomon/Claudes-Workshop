import csv,sys,math,collections,statistics as st
from datetime import datetime
r=[x for x in csv.DictReader(open(sys.argv[1])) if x['type']=='earthquake']
m=[float(x['mag']) for x in r]; print(len(r),"quakes M>=5, 12 months")
# b-value (Aki-Utsu, Mc=5.0, bin 0.1)
mean=st.mean(m); b=math.log10(math.e)/(mean-(5.0-0.05)); print("mean mag %.3f  b=%.3f +- %.3f"%(mean,b,b/math.sqrt(len(m))))
for t in (5,6,7,8): print("M>=%d: %d"%(t,sum(x>=t for x in m)))
# daily counts vs Poisson
d=collections.Counter(x['time'][:10] for x in r)
days=365; c=[d.get(k,0) for k in {(datetime(2025,10,1).toordinal()+i) for i in range(0)}]
import datetime as D
c=[d.get((D.date(2025,10,1)+D.timedelta(i)).isoformat(),0) for i in range(365)]
mu=st.mean(c);v=st.variance(c);print("daily mean %.2f var %.2f dispersion %.2f (Poisson=1)"%(mu,v,v/mu))
print("busiest days:",d.most_common(4))
# by hour, test uniformity chi2
h=collections.Counter(int(x['time'][11:13]) for x in r);e=len(r)/24
print("hour chi2 %.1f (df23, 5%% crit 35.2)"%sum((h[i]-e)**2/e for i in range(24)))
# depth classes
dp=[float(x['depth']) for x in r if x['depth']]
for lo,hi,n in((0,70,'shallow'),(70,300,'inter'),(300,800,'deep')):print(n,sum(lo<=z<hi for z in dp))
# biggest
for x in sorted(r,key=lambda x:-float(x['mag']))[:5]:print(x['mag'],x['time'][:10],x['place'])
# countries
cc=collections.Counter(x['place'].split(',')[-1].strip() for x in r);print(cc.most_common(10))
# largest-event aftershock: M5+ within 10 days & 300km of top quakes
