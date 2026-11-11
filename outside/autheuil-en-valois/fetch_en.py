import json, urllib.request, urllib.parse, urllib.error, time
UA={'User-Agent':'workshop-research-script/0.2 (one-off text analysis; low rate)'}
def post(params):
    data=urllib.parse.urlencode(params).encode()
    for a in range(8):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://en.wikipedia.org/w/api.php',data=data,headers=UA),timeout=60))
        except urllib.error.HTTPError as e:
            ra=int(e.headers.get('retry-after') or 15); print('wait',ra,flush=True); time.sleep(ra+2)
titles=[];cont={}
while True:
    r=post(dict(action='query',list='categorymembers',cmtitle='Category:Communes of Oise',cmlimit=500,cmnamespace=0,format='json',**cont))
    titles+=[m['title'] for m in r['query']['categorymembers']]
    if 'continue' in r: cont={'cmcontinue':r['continue']['cmcontinue']}
    else: break
print('titles',len(titles),flush=True)
out={}
for i in range(0,len(titles),50):
    r=post(dict(action='query',prop='revisions|langlinks',rvprop='content',rvslots='main',lllang='fr',lllimit=500,titles='|'.join(titles[i:i+50]),format='json',formatversion=2))
    for p in r['query']['pages']:
        if 'revisions' in p: out[p['title']]=dict(text=p['revisions'][0]['slots']['main']['content'],fr=(p.get('langlinks') or [{}])[0].get('title'))
    print(i,len(out),flush=True); time.sleep(3)
json.dump(out,open('/tmp/oise/en_wikitext.json','w'),ensure_ascii=False)
print('final',len(out),flush=True)
