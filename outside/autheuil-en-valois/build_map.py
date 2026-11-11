import json,sys,html
D=json.load(open(sys.argv[1])); T=open(sys.argv[2]).read(); E=open(sys.argv[3]).read()
top,bottom=E.split('<!--MAP-->')
allp={p['n']:p for g in D['pts'] for p in D['pts'][g]}
ann=[]
def label(name,text,dx,dy,anchor='start',ring=True):
    p=allp.get(name) or (dict(x=D['aut'][0],y=D['aut'][1]) if name=='AUT' else None)
    if not p: print('missing',name); return
    s=''
    if ring: s+=f'<circle cx="{p["x"]}" cy="{p["y"]}" r="5.5" fill="none" style="stroke:var(--ink);stroke-width:1.2"/>'
    s+=f'<line x1="{p["x"]}" y1="{p["y"]}" x2="{p["x"]+dx*0.8}" y2="{p["y"]+dy*0.8}" style="stroke:var(--ink2);stroke-width:.8"/>'
    s+=f'<text class="lab" x="{p["x"]+dx}" y="{p["y"]+dy}" text-anchor="{anchor}">{html.escape(text)}</text>'
    ann.append(s)
for spec in json.loads(sys.argv[5]): label(*spec)
annjs="out+=`"+''.join(ann).replace('`','')+"`;"
lst=lambda g:'<br>'.join(html.escape(f"{p['n']} ({p['d']})") for p in D['pts'][g])
out=(T.replace('{{ESSAY_TOP}}',top).replace('{{ESSAY_BOTTOM}}',bottom).replace('{{ANNOT}}',annjs)
 .replace('{{N_OIL}}',str(D['counts']['oil'])).replace('{{N_OCC}}',str(D['counts']['occ'])).replace('{{N_ALL}}',f"{D['n']:,}")
 .replace('{{LIST_OIL}}',lst('oil')).replace('{{LIST_OCC}}',lst('occ'))
 .replace('{{DATA}}',json.dumps(D,ensure_ascii=False,separators=(',',':'))))
open(sys.argv[4],'w').write(out); print('ok')
