# A year of M5+ earthquakes (USGS, 2025-10-01 to 2026-10-01)
Data: USGS FDSN event API, 1,994 events. Script: quakes_usgs.py.

- Gutenberg-Richter b-value (Aki-Utsu, Mc=5): 1.21 ± 0.03, a bit above the textbook ~1.0. Possibly a bin-correction/Mc effect; I didn't test it.
- Daily counts are clustered: variance/mean = 2.59 (Poisson would be 1). Busiest day 2026-06-08 had 27, the day after a M7.8 in the Philippines.
- Time of day is consistent with uniform (chi2 23.3, df 23).
- 83% shallow (<70 km), 14% intermediate, 3% deep. Indonesia, Philippines, Russia, Japan lead the counts.
