import json,re,sys,collections,random
C=json.load(open(sys.argv[1]))  # cleaned wikitext per commune
TOK=re.compile(r"\d[\d   ]*(?:[.,]\d+)?|[\w’'\-]+|[^\w\s]",re.U)
def base(t): return re.sub(r"\s*\(.*\)$","",t)
STOP={'','le','la','les','de','du','des','en','sur','sous','et','Saint','Sainte','lès','aux','au'}
def norm(tok,np):
    if re.match(r"^\d",tok): return '⟨N⟩'
    if tok in np: return '⟨C⟩'
    return tok.lower()
docs={}
for t,txt in C.items():
    np=set(re.split(r"[\s\-’']",base(t)))-STOP
    secs=[];cur=None
    for line in txt.split('\n'):
        m=re.match(r"^(=+) (.*?) =+$",line)
        if m: cur=m.group(2); secs.append([cur,[]]); continue
        if cur is None: cur='__lead__'; secs.append([cur,[]])
        tk=TOK.findall(line); secs[-1][1].append((line,[norm(x,np) for x in tk]))
    docs[t]=secs
K=4;df=collections.Counter()
for t,secs in docs.items():
    s=set()
    for h,ps in secs:
        for line,n in ps:
            for i in range(len(n)-K+1): s.add(tuple(n[i:i+K]))
    df.update(s)
TH=20
def ownfrac(n):
    cls=[0]*len(n)
    for i in range(len(n)-K+1):
        if df[tuple(n[i:i+K])]>=TH:
            for j in range(i,i+K): cls[j]=1
    words=[c for x,c in zip(n,cls) if re.match(r"[\w⟨]",x) and x!='⟨N⟩']
    return 1-sum(words)/max(1,len(words)), len(words)
# collect frame paragraphs per heading
pool=collections.defaultdict(list)
for t,secs in docs.items():
    name=base(t)
    for h,ps in secs:
        good=[]
        for line,n in ps:
            of,nw=ownfrac(n)
            if nw>=6 and of<=0.12: good.append(line.replace(name,'{C}'))
        if good: pool[h].append(dict(src=name,p=good))
# names
names=sorted(set(base(t) for t in C))
order=[h for h,_ in docs['Autheuil-en-Valois']]
out=dict(names=names,order=order,pool={h:pool[h] for h in set(order) if h in pool})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
for h in order: print(h, len(pool.get(h,[])))
print(len(json.dumps(out,ensure_ascii=False))//1024,'KB')
