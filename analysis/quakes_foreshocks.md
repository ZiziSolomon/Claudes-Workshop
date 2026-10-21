# Foreshocks: a null result

**Question:** Are large earthquakes preceded by elevated seismic activity?

**Answer:** Yes, but not unusually so. This is a negative result that contradicts popular expectation.

## The data

Looking at all 15 M7+ earthquakes in the dataset:
- **Every one** is preceded by M5+ activity in the 30 days before (mean: 149 events)
- **All but one** are preceded by M6+ activity (mean: 11 events)
- The largest foreshock before an M7+ is often itself a large earthquake (M7.5, M7.4, M7.1)

## The signal is noise

**The catch:** There's no statistical enhancement.

The background rate of M5+ earthquakes globally is ~161 per 30-day window. The pre-mainshock rate is 149 — actually *slightly lower* (0.9× enhancement).

**Interpretation:** 
1. All 15 M7+ occur in the same seismically active zones (Indonesia, Philippines, Japan, etc.)
2. These zones always have ~150 M5+ events per month
3. The mainshocks don't causally precede smaller events; they just happen in noisy places
4. The large foreshocks (M6+, M7.x) are geographically separate from the mainshocks — they're usually triggered seismicity from *previous* large events

## Why we see "foreshocks"

The appearance of foreshocks is an artifact of:
- **High background seismicity** in subduction zones
- **Triggering cascades**: old mainshocks trigger smaller events for months
- **Selective attention**: we remember the foreshocks that came before big quakes and forget all the foreshocks that came before small ones (Bayesian reasoning failure)

## Implications

Earthquake prediction based on foreshock identification in catalogs is unlikely to work at the M5+ threshold used here. Prediction would require:
- Much better detection (tracking foreshocks below M4, which requires dense local networks)
- A deeper understanding of stress transfer on specific faults (not possible from global catalogs)
- Recognition that mainshocks may be *independent* of recent activity, not triggered by it

The data suggest that if large earthquakes are predictable, the signal is not in the short-term (30-day) frequency of nearby seismic activity. It might be in stress accumulation over years/decades, which is invisible in this 12-month window.

## Caveats

- Our analysis uses M5+ only. Foreshock studies typically use lower thresholds (M2+) near the epicenter.
- The global 1-year USGS catalog is incomplete for small events and distant regions.
- Some of the "foreshocks" identified here may be stress-transferred aftershocks from much older events.
- True foreshocks (triggered instability in the fault hours or days before rupture) might exist but are indistinguishable from background in global data.
