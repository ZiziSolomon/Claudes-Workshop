import json,sys,html,re,statistics
S=json.load(open('/tmp/work/stats.json')); R=json.load(open('/tmp/work/render.json'))
T='Autheuil-en-Valois'
st=S['stats']; me=st[T]
owns=sorted(v['own'] for v in st.values())
rank=sum(1 for v in st.values() if v['own']<me['own'])
def esc(s): return html.escape(s)
def para(tokens):
    out=[];prev=None
    for tok,cl in tokens:
        sp='' if (re.match(r"^[,.)\]:;’']",tok) or (prev and prev in "(’'°-")) else ' '
        out.append(f'{sp}<span class="{cl}">{esc(tok)}</span>' if cl!=prev or True else esc(tok))
        prev=tok
    return ''.join(out).strip()
body=[]
for item in R[T]:
    if item[0]=='H':
        lvl=min(item[1]+1,5); body.append(f'<h{lvl}>{esc(item[2])}</h{lvl}>')
    else: body.append(f'<p>{para(item[1])}</p>')
# histogram of own words
bins=[0,25,50,75,100,150,200,300,500,1000,2000,5000,100000]
labels=['<25','25–49','50–74','75–99','100–149','150–199','200–299','300–499','500–999','1000–1999','2000–4999','5000+']
cnt=[sum(1 for o in owns if bins[i]<=o<bins[i+1]) for i in range(len(labels))]
mybin=[i for i in range(len(labels)) if bins[i]<=me['own']<bins[i+1]][0]
mx=max(cnt)
bars=''.join(f'<div class="bar{" me" if i==mybin else ""}"><div class="fill" style="height:{100*c/mx:.0f}%"></div><span class="n">{c}</span><span class="l">{labels[i]}</span></div>' for i,c in enumerate(cnt))
tmpl=open(sys.argv[1]).read().replace('{{ESSAY}}',open(sys.argv[3]).read())
from collections import Counter
rc=Counter(cl for it in R[T] if it[0]=='P' for t,cl in it[1] if t[0].isalnum())
rw=sum(rc.values())
me=dict(me); me.update(words=rw,own=rc['own'],frame=rc['frame'],data=rc['data'],own_frac=rc['own']/rw)
out=(tmpl.replace('{{BODY}}','\n'.join(body)).replace('{{BARS}}',bars)
 .replace('{{N}}',str(S['N'])).replace('{{TH}}',str(S['TH']))
 .replace('{{WORDS}}',f"{me['words']:,}").replace('{{OWN}}',str(me['own']))
 .replace('{{FRAME}}',str(me['frame'])).replace('{{DATA}}',str(me['data']))
 .replace('{{OWNPCT}}',f"{100*me['own_frac']:.0f}").replace('{{FRAMEPCT}}',f"{100*me['frame']/me['words']:.0f}")
 .replace('{{RANK}}',str(rank)).replace('{{MEDOWN}}',str(round(statistics.median(owns))))
 .replace('{{MEDPCT}}',f"{100*statistics.median(v['own_frac'] for v in st.values()):.0f}")
 .replace('{{EMPTY}}',str(me['empty_headings'])))
open(sys.argv[2],'w').write(out)
print('wrote',sys.argv[2])
