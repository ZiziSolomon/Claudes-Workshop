from math import *
def d(a,b):
    la1,lo1,la2,lo2=map(radians,(*a,*b))
    h=sin((la2-la1)/2)**2+cos(la1)*cos(la2)*sin((lo2-lo1)/2)**2
    return 2*3958.8*asin(sqrt(h))
fkl=(41.3778,-79.8603)
for n,c in {"PIT":(40.4915,-80.2329),"ERI":(42.0831,-80.1739),"CLE":(41.4117,-81.8498),"BUF":(42.9405,-78.7322)}.items():
    print(n,round(d(fkl,c)),"mi straight-line")
# threshold is from memory, unverified
T=90
print("within",T,"mi:",[n for n,c in {"PIT":(40.4915,-80.2329),"ERI":(42.0831,-80.1739)}.items() if d(fkl,c)<T])
