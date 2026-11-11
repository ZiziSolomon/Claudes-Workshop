import json,re,sys,collections
W=json.load(open(sys.argv[1]))
ELL=re.compile(r"^\{\{\s*(?:…|\.\.\.|section vide ou incomplète|à compléter)\s*\}\}\s*$",re.I|re.M)
c=collections.Counter(); arts=collections.Counter(); hist_ell=[]
for t,w in W.items():
    secs=re.split(r"\n(=+[^=\n]+=+)\s*\n",'\n'+w)
    for i in range(1,len(secs)-1,2):
        h=secs[i].strip('= ').strip(); body=secs[i+1]
        if ELL.search(body) and len(re.sub(r"\{\{[^}]*\}\}","",body).strip())<5:
            c[h]+=1; arts[t]+=1
            if h=='Histoire': hist_ell.append(t)
print('articles with ≥1 placeholder section',len(arts),'of',len(W))
print(c.most_common(12))
print('Histoire placeholder:',len(hist_ell),hist_ell[:10])
print('Autheuil',arts['Autheuil-en-Valois'])
print('most placeholders',arts.most_common(5))
