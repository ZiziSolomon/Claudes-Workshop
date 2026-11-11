import json,re,sys
sys.path.insert(0,'/tmp/work')
from clean import clean
EN=json.load(open(sys.argv[1]))
out=[];station=[];one=0
for t,v in sorted(EN.items()):
    w=re.split(r"\n==\s*(?:See also|References|External links|Notes|Population)",v['text'])[0]
    c=clean(w)
    prose=' '.join(l for l in c.split('\n') if not l.startswith('=')).strip()
    prose=re.sub(r"\s+"," ",prose)
    m=re.search(r"is an? commune in the Oise department in (?:northern|the Hauts-de-France region of northern) France\.?\s*",prose)
    if not m: continue
    rest=prose[m.end():].strip()
    if rest.startswith(','):
        parts=re.split(r"(?<=[a-z0-9\)])\.\s+(?=[A-Z])",rest,maxsplit=1)
        rest=parts[1].strip() if len(parts)>1 else ''
    if not rest: one+=1; continue
    sents=re.split(r"(?<=[a-z0-9\)])\.\s+(?=[A-Z])",rest)
    s=sents[0].rstrip('.')+'.'
    if 'station has rail connections' in s or re.search(r"station is served by",s): station.append(t); continue
    if len(s.split())<4: continue
    out.append((t,s,len(sents)))
print(one,len(station),len(out))
json.dump(dict(one=one,station=station,second=out,total=len(EN)),open('/tmp/work/second.json','w'),ensure_ascii=False,indent=0)
for t,s,n in out: print('-',t,'|',s[:230])
