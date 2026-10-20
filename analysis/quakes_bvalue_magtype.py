import csv,sys,math,statistics as st
r=[x for x in csv.DictReader(open(sys.argv[1])) if x['type']=='earthquake']
for t in ('mww','mb'):
  for mc in (5.0,5.5):
    s=[float(x['mag']) for x in r if x['magType']==t and float(x['mag'])>=mc-1e-9]
    if len(s)>20:
      b=math.log10(math.e)/(st.mean(s)-(mc-0.05));print(t,mc,len(s),"b=%.2f +-%.2f"%(b,b/math.sqrt(len(s))))
