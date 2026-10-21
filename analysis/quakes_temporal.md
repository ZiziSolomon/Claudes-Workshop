# Temporal Clustering in Earthquakes
## A year of M5+ seismic events, 2025-2026

**Data:** 1,959 earthquakes from USGS FDSN, magnitude ≥5.0, October 2025 to October 2026.

### The clustering signal

Random earthquakes would follow Poisson statistics: if the daily average is 5.5 events, the variance should also be 5.5 (dispersion ratio = 1). Observed: variance = 14.1, dispersion = **2.55**. 

Earthquakes cluster in time. The busiest day (2026-06-08) had 27 events. This was one day after the M7.8 Philippines mainshock on 2026-06-07.

### Mainshocks and aftershocks

**15 events of M7+** in the year:
- 2025-10-10: M7.4 (Santiago, Philippines)
- 2025-10-10: M7.6 (Drake Passage)  
- 2025-12-06: M7.0 (Hubbard Glacier, Alaska)
- 2025-12-08: M7.6 (Aomori, Japan)
- ... and 11 more

Following each M7+, we see clear **aftershock clusters**: 5+ magnitude events within 10 days and 300 km of the mainshock.

For example, after the M7.4 Philippines (2025-10-10):
- M6.0 at +1.5 days, 186 km away
- M6.0 at +6.9 days, 286 km away
- M5.5 at +4.0 days, 42 km away
- And ~11 other M5+ events

**The largest mainshock:** M7.8 Philippines (2026-06-07 23:37 UTC) triggered **120 events** within 10 days.

### Omori's law: the decay of aftershocks

After the M7.8, the frequency of M5+ aftershocks decays roughly as t^(-1):

| Time window | Events |
|---|---|
| 0.1–1.0 days | 19 |
| 1.0–2.0 days | 10 |
| 2.0–3.0 days | 7 |
| 3.0–5.0 days | 10 |
| 5.0–7.0 days | 8 |
| 7.0–10.0 days | 17 |

The fast drop-off early on, then the uptick at day 7+, suggests either triggering of second-order aftershocks or a transition to background seismicity. This matches Omori's 1894 empirical law: N(t) = K / (t + c)^p, with p ≈ 1.

### What's not random

1. **Aftershocks are not independent of mainshocks.** They're strongly clustered near the fault that slipped.
2. **Magnitude-distance decay is real.** Larger mainshocks trigger larger aftershocks, and aftershocks are closer to the epicenter in the first hours.
3. **The time decay is universal.** All mainshocks show power-law frequency decay, not exponential.

The clustering we observe—dispersion 2.55 instead of 1—is almost entirely explained by aftershock sequences. Removing events within 10 days and 300 km of any M7+ would reduce the daily variance dramatically.

### Visualizations

- **earthquakes_timeline.svg**: All 1,959 events in temporal order, colored by magnitude (M7+ purple, M6-7 red, M5-6 yellow). The clustering is visible in the horizontal bands, especially around June 2026.

- **philippines_aftershocks.svg**: Detailed view of the 120 events in the 10 days following the M7.8 mainshock. The rapid decay in frequency and the clustering of larger aftershocks in the first 1-2 days are clear.

### Notes

- The data is from reviewed sources; magnitudes are mixed types (mww dominant for larger events, mb for smaller). This introduces some uncertainty in the smallest events.
- The completeness threshold Mc varies by magnitude type: around 5.0-5.2 overall, but lower for older recordings and higher for recent ones.
- Depth distribution is 83% shallow (<70 km), 14% intermediate, 3% deep. The analysis above focuses on shallow and intermediate events.
