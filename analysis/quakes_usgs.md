# A year of M5+ earthquakes (USGS, 2025-10-01 to 2026-10-01)
Data: USGS FDSN event API, 1,994 events. Script: quakes_usgs.py.

- Gutenberg-Richter b-value (Aki-Utsu, Mc=5): 1.21 ± 0.03, a bit above the textbook ~1.0. Possibly a bin-correction/Mc effect; I didn't test it.
- Daily counts are clustered: variance/mean = 2.59 (Poisson would be 1). Busiest day 2026-06-08 had 27, the day after a M7.8 in the Philippines.
- Time of day is consistent with uniform (chi2 23.3, df 23).
- 83% shallow (<70 km), 14% intermediate, 3% deep. Indonesia, Philippines, Russia, Japan lead the counts.

## Follow-up: the b-value vs completeness threshold
Raising Mc: 5.0→1.21, 5.2→1.13, 5.4→1.07, 5.6→1.07, 5.8→1.03, 6.0→1.01 (±0.09). So b converges to ~1.0 above M6; the excess at M5 looks like a catalogue artefact (41% of events use mb, the rest mww, so the low end mixes magnitude scales). I didn't verify that cause directly. See quakes_bvalue_mc.py.

## Follow-up 2: splitting by magnitude type
mww only: b=0.87 at Mc 5.0, 1.03 at Mc 5.5. mb only: b=2.62 at Mc 5.0 (n=821). Neither scale is complete over the full range: small events get mb, larger get mww, so each sub-catalogue is a truncated slice of the whole. This supports the mixed-scale explanation for the inflated pooled b (script: quakes_bvalue_magtype.py). It's consistent with the hypothesis rather than proof; mww being incomplete at M5.0 fits its low b.
