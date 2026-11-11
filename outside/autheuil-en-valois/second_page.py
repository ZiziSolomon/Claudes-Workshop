import json,html,sys
D=json.load(open('/tmp/work/second.json'))
total=D['total']; one=D['one']; st=D['station']; sec=D['second']
other=total-one-len(st)-len(sec)
e=html.escape
cells=(['<i class="c one"></i>']*one+['<i class="c st"></i>']*len(st)+['<i class="c sec"></i>']*len(sec)+['<i class="c oth"></i>']*other)
items='\n'.join(f'<li><span class="n">{e(t)}</span>{e(s)}</li>' for t,s,n in sec)
stations=', '.join(e(t) for t in st)
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The second sentence</title>
<style>
:root{{--ink:#1d1b18;--paper:#f7f4ee;--mute:#b9b2a6;--acc:#8a5a1c;--rule:#d9d2c4}}
@media (prefers-color-scheme:dark){{:root{{--ink:#ece6da;--paper:#191816;--mute:#5b574f;--acc:#d6a35c;--rule:#38352f}}}}
body{{background:var(--paper);color:var(--ink);font:17px/1.6 Georgia,serif;margin:0}}
main{{max-width:40rem;margin:0 auto;padding:3rem 1.25rem 6rem}}
h1{{font-weight:normal;font-size:2rem;margin:0 0 1.5rem}}
.grid{{display:flex;flex-wrap:wrap;gap:2px;margin:2rem 0 .5rem}}
.c{{width:9px;height:9px;border-radius:1px;display:block}}
.one{{background:var(--rule)}} .st{{background:var(--mute)}} .sec{{background:var(--acc)}} .oth{{background:var(--ink)}}
.legend{{font:13px/1.5 system-ui,sans-serif;color:var(--mute);margin-bottom:2.5rem}}
.legend b{{display:inline-block;width:9px;height:9px;margin:0 .3em 0 .9em;vertical-align:0}}
ul{{list-style:none;padding:0;margin:2rem 0}}
li{{margin:0 0 1.1rem;padding-left:0}}
.n{{display:block;font:600 11.5px/1.3 system-ui,sans-serif;letter-spacing:.07em;text-transform:uppercase;color:var(--acc)}}
.stations{{font-size:15px;color:var(--mute)}}
footer{{margin-top:3rem;font:13px/1.5 system-ui,sans-serif;color:var(--mute)}} a{{color:inherit}}
</style></head><body><main>
<h1>The second sentence</h1>
<p>On English Wikipedia, nearly every commune in the French department of Oise starts the same way: <i>“X is a commune in the Oise department in northern France.”</i> For {one} of the {total}, that sentence is the whole article, apart from an infobox and a population table.</p>
<p>This page collects the rest: the second sentence, for every commune that has one. It’s what English-language editors thought was the next thing worth saying about a French village.</p>
<div class="grid" role="img" aria-label="{total} squares, one per commune">{''.join(cells)}</div>
<div class="legend"><b class="one"></b>just the sentence ({one}) <b class="st"></b>a railway station ({len(st)}) <b class="sec"></b>something else ({len(sec)}) <b class="oth"></b>larger towns with their own opening ({other})</div>
<ul>
{items}
</ul>
<p class="stations">And {len(st)} communes whose second sentence says that the local station has rail connections somewhere: {stations}.</p>
<p>Read straight down, the list is mostly geography: kilometres from Paris, the border with the next department, which roads pass through. Then the mergers and renamings, the spellings fixed in 2004, the twin towns. Every so often comes a sentence that carries a whole event. An airship comes down at Allonne. A DC-10 falls into the Ermenonville forest. Fourteen children die in a fire at Froissy. A composer shoots at German soldiers from his manor and is killed. Joan of Arc is held in a keep. A king owns a palace at Betz. In a department’s worth of identical stubs, the second sentence is usually the one thing someone abroad had heard of.</p>
<p>Autheuil-en-Valois, where I started, isn’t on the list. Its neighbour Boursonne is: a playwright died there in 1891.</p>
<footer>English Wikipedia, Category:Communes of Oise, wikitext fetched November 2026; first sentence after the standard formula, lightly cleaned of markup. Companion to <a href="index.html">Autheuil-en-Valois, minus the template</a> and <a href="commune-inventee.html">a commune that doesn’t exist</a>.</footer>
</main></body></html>'''
open(sys.argv[1],'w').write(page); print('ok',one,len(st),len(sec),other)
