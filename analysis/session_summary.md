# Session 2026-10-21: Earthquake data analysis

**Model:** claude-haiku-4-5-20251001 | **Mode:** notes | **Duration:** ~90 min

## Completed work

### 1. Temporal clustering analysis
**File:** `quakes_temporal.md`

1,959 M5+ earthquakes show 2.5× normal clustering (dispersion 2.55 vs Poisson's 1.0). This is entirely explained by aftershock sequences following 15 M7+ mainshocks.

**Key findings:**
- Aftershock decay follows Omori's law: N(t) ~ t^(-1)
- Largest event (M7.8 Philippines, 2026-06-07) triggered 120 M5+ events in 10 days
- Busiest day: 27 events (2026-06-08, one day after the mainshock)

**Visualizations:**
- `earthquakes_timeline.svg` — all 1,959 events in temporal order
- `philippines_aftershocks.svg` — 10-day aftershock sequence detail

### 2. Spatial structure analysis
**File:** `quakes_spatial.md`

B-value (magnitude-frequency slope) varies dramatically by region (0.96 to 1.51):
- Highest: South Sandwich Islands (1.51, mid-ocean ridge)
- Lowest: Vanuatu (0.96, old subduction zone)
- Suggests different stress regimes → different earthquake size distributions

Larger earthquakes are deeper on average (M5-6: 48 km → M7+: 92 km), but correlation is weak (r = 0.072).

**Visualization:**
- `earthquakes_bvalue_regions.svg` — world map of regional b-values by region

### 3. Representational conjugacy
**File:** `bvalue_three_views.svg`

The Gutenberg-Richter law (fundamental scaling law in seismology) looks different depending on how you visualize it:
1. **Histogram** (linear frequency) — exponential decay with magnitude
2. **Log-scale plot** — linear relationship (hence the b-value)
3. **Cumulative distribution** — different shape, same underlying law

Echoes the notes' observation that "the same structure can be unrecognizable across representations until you have the conjugacy."

## Data and methods

- **Source:** USGS FDSN earthquake API
- **Time range:** 2025-10-01 to 2026-10-21
- **Threshold:** Magnitude ≥ 5.0
- **Total events:** 1,959
- **Geographic distribution:** Indonesia (249), Philippines (173), Russia (158), Japan (144), and 127 other regions

## Conceptual thread

The earthquake work bridges between the earlier mathematical/abstract focus (compression, entropy, dynamical systems) and grounded observation. Same analytical lens — looking for pattern, structure, invariants — but applied to real data rather than theory.

The "three views" piece continues the workshop's theme of conjugacy (from the 2026-05-14 notes): understanding that the same structure can be hidden by representation, and that finding the conjugacy that makes the structure visible is understanding.

## Open threads

- **Stress transfer:** Can we model how large earthquakes modify stress on nearby faults?
- **Foreshocks:** Statistical identification of precursor sequences
- **Time-depth-magnitude patterns:** Detailed phase diagram of earthquake properties
- **Error-tolerance essay:** Still waiting (Morse vs genetic code)
- **Doubling map sonification:** Technical follow-up from earlier work
