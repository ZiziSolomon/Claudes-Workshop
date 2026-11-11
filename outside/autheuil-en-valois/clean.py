import re, json, sys
def strip_nested(s, open_, close, repl):
    out=[];i=0;depth=0;start=0
    res=[];buf=''
    # iterative innermost replacement
    pat=re.compile(re.escape(open_)+r"((?:(?!"+re.escape(open_)+r"|"+re.escape(close)+r").)*)"+re.escape(close),re.S)
    prev=None
    while prev!=s:
        prev=s; s=pat.sub(lambda m: repl(m.group(1)), s)
    return s
ORD={'I':'Ier'}
def tmpl(inner):
    parts=[p.strip() for p in inner.split('|')]
    name=parts[0].lower().strip()
    args=[p for p in parts[1:] if '=' not in p.split(' ')[0] or not re.match(r"^\w[\w ]*=",p)]
    if name in ('unité','unite','nobr','tmp','nombre','formatnum:','date','lang','japonais','nb','nombre'):
        return ' '.join(a.replace('.',',') if re.match(r"^\d+\.\d+$",a) else a for a in args)
    if name in ('convert','cvt'):
        a=[x for x in parts[1:] if '=' not in x]
        return (a[0]+' '+a[1]) if len(a)>=2 else ''
    if name in ('lang','lang-fr','nowrap','small'): return args[-1] if args else ''
    if name.startswith('formatnum'): return inner.split(':',1)[1]
    if name in ('s-','s','sp-','s2-'): return (args[0]+'e siècle') if args else ''
    if name in ('-s-',): return (args[0]+'e siècle av. J.-C.') if args else ''
    if name in (',',): return ''
    if name in ('etc.','etc'): return ', etc.'
    if name in ('er','e','re','ers','es','res'): return name
    if name in ('1er','1re'): return name
    if name in ('nobr','citation','guil','«'): return ' '.join(args)
    if name in ('mh','classé mh','classé mh.','inscrit mh'): return name.upper()
    return ''
def clean(w):
    w=re.sub(r"<!--.*?-->","",w,flags=re.S)
    w=re.sub(r"<ref[^>/]*/>","",w)
    w=re.sub(r"<ref[^>]*>.*?</ref>","",w,flags=re.S)
    w=re.sub(r"<gallery.*?</gallery>","",w,flags=re.S|re.I)
    w=strip_nested(w,'{{','}}',tmpl)
    w=strip_nested(w,'{|','|}',lambda x:'')
    w=re.sub(r"\[\[(?:Fichier|Image|File|Catégorie|Category):[^\[\]]*(?:\[\[[^\]]*\]\][^\[\]]*)*\]\]","",w,flags=re.I)
    w=re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]",r"\1",w)
    w=re.sub(r"\[\[([^\]]*)\]\]",r"\1",w)
    w=re.sub(r"\[https?://\S+ ([^\]]*)\]",r"\1",w)
    w=re.sub(r"'{2,}","",w)
    w=re.sub(r"<[^>]+>","",w)
    w=w.replace('&nbsp;',' ')
    lines=[]
    for l in w.split('\n'):
        l=l.strip()
        if not l or l.startswith(('|','!','{','}','__')): continue
        if l.startswith(('*','#',':',';')): l=l.lstrip('*#:; ')
        m=re.match(r"^(=+)\s*(.*?)\s*=+$",l)
        if m: lines.append(m.group(1)+' '+m.group(2)+' '+m.group(1)); continue
        lines.append(l)
    return '\n'.join(lines)
if __name__=='__main__':
    src=json.load(open(sys.argv[1])); out={t:clean(w) for t,w in src.items()}
    json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
