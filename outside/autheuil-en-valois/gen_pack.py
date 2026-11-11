import json,re,random,sys
random.seed(60031)
D=json.load(open('gen_data.json')); EX=json.load(open('/tmp/oise/articles.json'))
BAD=re.compile(r"(?:\b(?:de|du|le|à|est)\s*[.,;)])|\s{2,}[,.]|\(\s*\)|:\s*$|\bdu\s+,|loi du\s+,")
keep=['__lead__','Localisation','Géologie et relief','Hydrographie','Climat','Typologie','Occupation des sols','Habitat et logement','Voies de communication et transports','Histoire','Rattachements administratifs','Rattachements électoraux','Intercommunalité','Élections municipales et communautaires','Pyramide des âges','Lieux et monuments','Liens externes']
pool={}
for h in keep:
    items=[]
    for x in D['pool'].get(h,[]):
        p=[l for l in x['p'] if not BAD.search(l) and '{C}-' not in l and 'd{C}' not in l]
        if p: items.append(dict(src=x['src'],p=p))
    random.shuffle(items); pool[h]=items[:50]
    print(h,len(items))
# census sentences from extracts
cen=[]
for t,txt in EX.items():
    name=re.sub(r"\s*\(.*\)$","",t)
    m=re.search(r"En 20\d\d, la commune comptait [^\n]+",txt)
    if m: cen.append(dict(src=name,p=[m.group(0).replace(name,'{C}')]))
pool['Évolution démographique']=cen; print('census',len(cen))
names=D['names']
json.dump(dict(names=names,pool=pool),open('gen_pack.json','w'),ensure_ascii=False,separators=(',',':'))
import os;print(os.path.getsize('gen_pack.json')//1024,'KB')
