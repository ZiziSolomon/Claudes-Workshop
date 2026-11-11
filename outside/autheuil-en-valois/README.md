# Autheuil-en-Valois, minus the template

Open `index.html`. It's an essay plus the French Wikipedia article on Autheuil-en-Valois (Oise, 265 inhabitants), coloured by how much of each phrase is shared boilerplate across all 678 Oise commune articles.

Pipeline (Nov 2026):
1. `fetch.py`: raw wikitext for every page in Catégorie:Commune dans l'Oise, 50 per request. Fetching one page at a time hit HTTP 429 almost immediately.
2. `clean.py wikitext.json clean.json`: rough wikitext → plain text.
3. `analyze.py clean.json Autheuil-en-Valois autheuil_extract.json [other_extracts.json]`: 4-gram document frequency; a word is *frame* if it sits in a 4-gram found in ≥20 articles. The optional plain-text extracts catch boilerplate that templates generate, which never appears in the raw wikitext.
4. `page.py template.html index.html essay.html`
5. `ellipsis.py wikitext.json`: counts sections whose only content is the `{{…}}` "section to be completed" placeholder.

`oise_stats.json` holds the per-commune word counts (own / frame / data).

## Companion: `second-sentence.html`

`fetch_en.py` pulls English Wikipedia's Category:Communes of Oise (682 pages). `second.py en_wikitext.json` takes the sentence after "X is a commune in the Oise department in northern France." 539 articles have nothing after it, and 28 add only a railway station. `second_page.py out.html` renders the other 79 as a list.

## Companion: `commune-inventee.html`

Writes a fake Oise commune each time you load it. The name comes from an order-3 character Markov model over the 678 real names. Each section is filled with a frame paragraph (≤12% own words) lifted from a randomly chosen real commune, with that commune's name swapped out. History, economy, toponymy, mayors and notable people get the "section vide" banner. Very occasionally, History instead gets the one paragraph the template does know: Croix de guerre 1914–1918. `gen_data.py clean.json gen_data.json` → `gen_pack.py` → the JSON is inlined into `gen_template.html`.

## Companion: `high-clearing.html`

A map of every current French commune whose name ends in -euil/-ueil (northern reflex of Gaulish *ialo-*, "clearing") or -jols/-jouls/-joul (Occitan reflex). Data comes from Wikidata (P374 INSEE + P625), fetched in ten INSEE-prefix chunks by `fetch_wikidata.sh` (example query in `wikidata_query_example.rq`). `ialo.py <dir-with-c_*.csv> map.json`, then `build_map.py map.json map_template.html map_essay.html out.html '<labels json>'`. Map text is in `map_essay.html`.
