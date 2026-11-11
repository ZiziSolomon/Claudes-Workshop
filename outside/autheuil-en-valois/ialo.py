import csv,glob,re,json,math,sys,collections,unicodedata,html
rows={}
for f in sorted(glob.glob(sys.argv[1]+'/c_*.csv')):
    for r in csv.reader(open(f,errors='ignore')):
        if len(r)!=4 or not r[2].startswith('Point'): continue
        insee,label,coord,end=r
        if insee[:2] in ('97','98','99') or not re.match(r"^\d[\dAB]\d{3}$",insee): continue
        m=re.match(r"Point\(([-\d.]+) ([-\d.]+)\)",coord); lon,lat=float(m.group(1)),float(m.group(2))
        if not (-5.5<lon<10 and 41<lat<51.5): continue
        cur=not end
        if insee not in rows or (cur and not rows[insee]['cur']): rows[insee]=dict(name=label,lon=lon,lat=lat,cur=cur)
cur={k:v for k,v in rows.items() if v['cur']}
print('communes',len(rows),'current',len(cur),'depts',len({k[:2] for k in cur}))
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
OIL=re.compile(r"(?:euil|ueil)$"); OCC=re.compile(r"(?:jols|jouls|jol|joul)$")
groups={'oil':[],'occ':[]}
for k,v in cur.items():
    words=re.split(r"[-\s’']",strip(v['name']))
    words=[w for w in words if not re.match(r"^(?:breuil|brueil|montreuil|pujols?|puyols?)$",w)]
    if any(OIL.search(w) for w in words): groups['oil'].append(k)
    elif any(OCC.search(w) for w in words): groups['occ'].append(k)
print({g:len(x) for g,x in groups.items()})
print('occ sample',[cur[k]['name'] for k in groups['occ']][:40])
aut=[cur[k]['name'] for k in cur if re.match(r"^(aut|alt|aud|ault|out)[h]?(euil|ueil|eu?il|ouil)",strip(cur[k]['name']))]
print('autheuils',aut)
# projection
lon0=2.5; kx=math.cos(math.radians(46.5))
xs=[(v['lon']-lon0)*kx for v in cur.values()]; ys=[-v['lat'] for v in cur.values()]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
W=760; s=W/(maxx-minx); H=round((maxy-miny)*s)
def P(v): return round(((v['lon']-lon0)*kx-minx)*s,1), round((-v['lat']-miny)*s,1)
bg=[]
for v in cur.values():
    x,y=P(v); bg+= [int(x*10),int(y*10)]
pts={g:[dict(n=cur[k]['name'],d=k[:2],x=P(cur[k])[0],y=P(cur[k])[1]) for k in sorted(groups[g],key=lambda k:cur[k]['name'])] for g in groups}
A=[k for k in cur if cur[k]['name']=='Autheuil-en-Valois']
autp=P(cur[A[0]]) if A else None
# latitude stats
def medlat(g): import statistics; return statistics.median(cur[k]['lat'] for k in groups[g])
print('median lat oil',medlat('oil'),'occ',medlat('occ'))
south=sum(1 for k in groups['oil'] if cur[k]['lat']<45.5); print('oil south of 45.5',south)
json.dump(dict(W=W,H=H,bg=bg,pts=pts,aut=autp,n=len(cur),counts={g:len(x) for g,x in groups.items()}),open(sys.argv[2],'w'),ensure_ascii=False,separators=(',',':'))
