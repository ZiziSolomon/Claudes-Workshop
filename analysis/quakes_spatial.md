# Spatial structure: b-values and depth patterns

## The Gutenberg-Richter b-value varies dramatically by region

The fundamental relationship in seismology is log10(N) = a - b·M: the frequency of earthquakes of magnitude M or greater.

**The b-value** is the slope. It typically ranges from 0.8 to 1.5. Higher b-values mean more small earthquakes relative to large ones; lower b-values mean more frequent large events.

### Regional variation (M5+, 12 months)

| Region | Events | B-value | Avg Depth |
|---|---|---|---|
| South Sandwich Islands | 66 | 1.51 | 56 km |
| Indonesia | 249 | 1.27 | 39 km |
| Russia | 158 | 1.30 | 38 km |
| Papua New Guinea | 81 | 1.27 | 64 km |
| Philippines | 173 | 1.17 | 43 km |
| Mexico | 49 | 1.10 | 27 km |
| Alaska | 67 | 1.11 | 27 km |
| Japan | 144 | 1.00 | 37 km |
| Tonga | 69 | 1.04 | 66 km |
| Vanuatu | 50 | 0.96 | 75 km |

**Range: 0.96 (Vanuatu) to 1.51 (South Sandwich Islands)** — a 57% spread.

**Why the variation?** Several hypotheses:

1. **Tectonic stress regime**: Highly stressed regions might show more large earthquakes (lower b). The South Sandwich Islands (mid-ocean ridge) shows the highest b, suggesting spreading centers have different stress distribution than subduction zones.

2. **Age of the subduction zone**: Older, colder slabs might accumulate stress differently than young, hot ones. But the data are mixed — Indonesia (young) and Tonga (older) both host many earthquakes.

3. **Temporal sampling**: Our 12-month window captures different points in the stress cycle for different regions. Some regions might be in an aftershock-dominated period (higher b), others in background activity (lower b).

4. **Catalog completeness**: Smaller events are easier to detect near seismic stations. Indonesia and Japan have dense networks; remote regions like Vanuatu don't. This could bias b-value estimates.

## Depth and magnitude are weakly correlated

**Finding**: Larger earthquakes go deeper on average, but the effect is small.

| Magnitude | Avg Depth | % Shallow (<70km) |
|---|---|---|
| M5–6 | 48 km | 83% |
| M6–7 | 62 km | 79% |
| M7+ | 92 km | 73% |

Pearson correlation r = 0.072 (nearly independent).

This makes sense: most M5+ earthquakes in this catalog occur on subduction zones, where the seismogenic zone extends from 5 to 700 km depth. Larger earthquakes *can* occur anywhere in this range. The slight depth increase with magnitude might reflect larger ruptures propagating into deeper, colder, stronger material.

**Depth distribution is dominated by plate tectonics**, not magnitude:
- Shallow (<35 km): mainly oceanic ridges, shallow crustal faults, young subduction zones
- Intermediate (35–70 km): typical subduction-zone coupling zone
- Deep (>70 km): old, cold subduction slabs (Tonga, Vanuatu, Philippines trench)

## The visualization

`earthquakes_bvalue_regions.svg` plots the 11 most seismically active regions as bubbles on a world map:
- **Position**: geographic center of seismicity
- **Bubble size**: number of events in that region
- **Color**: b-value (red for low, blue for high)

The South Sandwich Islands stand out in the south Atlantic with the highest b (blue), while Vanuatu and Japan in the western Pacific are red (low b), suggesting that stress release patterns differ fundamentally between ocean-ridge and subduction-zone tectonics.

## Notes

- These are *apparent* b-values within a one-year catalog of M5+ events. True b-values require accounting for completeness, magnitude binning, and longer time windows.
- Catalog bias toward station-rich regions (Japan, Indonesia) may inflate their apparent b-values.
- The South Sandwich Islands result is striking but based on only 66 events — a longer time window would be needed to confirm whether this is a genuine difference in the tectonics or a sampling artifact.
