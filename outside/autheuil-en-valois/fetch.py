import json, urllib.request, urllib.parse, urllib.error, time
UA={'User-Agent':'workshop-research-script/0.2 (one-off text analysis; low rate)'}
titles=[t for t in json.load(open('/tmp/oise/titles.json')) if not t.startswith(('Liste','Armorial'))]
out={}
for i in range(0,len(titles),50):
    batch=titles[i:i+50]
    data=urllib.parse.urlencode(dict(action='query',prop='revisions',rvprop='content',rvslots='main',titles='|'.join(batch),format='json',formatversion=2,redirects=1)).encode()
    for attempt in range(8):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request('https://fr.wikipedia.org/w/api.php',data=data,headers=UA),timeout=60))
            for p in r['query']['pages']:
                if 'revisions' in p: out[p['title']]=p['revisions'][0]['slots']['main']['content']
            break
        except urllib.error.HTTPError as e:
            ra=int(e.headers.get('retry-after') or 15); print('wait',e.code,ra,flush=True); time.sleep(ra+2)
    print(i,len(out),flush=True)
    time.sleep(3)
json.dump(out,open('/tmp/oise/wikitext.json','w'),ensure_ascii=False)
print('final',len(out),flush=True)
