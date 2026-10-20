import csv,sys,math,statistics as st
r=[x for x in csv.DictReader(open(sys.argv[1])) if x['type']=='earthquake']
m=[float(x['mag']) for x in r]
for mc in (5.0,5.2,5.4,5.6,5.8,6.0):
    s=[x for x in m if x>=mc-1e-9]; b=math.log10(math.e)/(st.mean(s)-(mc-0.05))
    print(mc,len(s),"b=%.2f +-%.2f"%(b,b/math.sqrt(len(s))))
# by magType
import collections
c=collections.Counter(x['magType'] for x in r);print(c)
