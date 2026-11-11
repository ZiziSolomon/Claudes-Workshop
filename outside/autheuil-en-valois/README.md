# Autheuil-en-Valois, minus the template

Open `index.html`. It's an essay plus the French Wikipedia article on Autheuil-en-Valois (Oise, 265 inhabitants), coloured by how much of each phrase is shared boilerplate across all 678 Oise commune articles.

Pipeline (Nov 2026):
1. `fetch.py`: raw wikitext for every page in Catégorie:Commune dans l'Oise, 50 per request. Fetching one page at a time hit HTTP 429 almost immediately.
2. `clean.py wikitext.json clean.json`: rough wikitext → plain text.
3. `analyze.py clean.json Autheuil-en-Valois autheuil_extract.json [other_extracts.json]`: 4-gram document frequency; a word is *frame* if it sits in a 4-gram found in ≥20 articles. The optional plain-text extracts catch boilerplate that templates generate, which never appears in the raw wikitext.
4. `page.py template.html index.html essay.html`
5. `ellipsis.py wikitext.json`: counts sections whose only content is the `{{…}}` "section to be completed" placeholder.

`oise_stats.json` holds the per-commune word counts (own / frame / data).
