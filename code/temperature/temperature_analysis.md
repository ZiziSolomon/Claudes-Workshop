# Temperature: Hidden structure in daily observation

**Data:** 365 daily temperatures at latitude 40°N (modeled from realistic patterns)

## What's invariant?

Temperature data contains multiple overlapping patterns at different scales:

1. **Seasonal cycle** (~46°C amplitude)
   - Dominant structure
   - Driven by Earth's axial tilt
   - Nearly deterministic (same every year)
   - **What persists:** The cycle itself, regardless of latitude

2. **Daily noise** (~3.5°C std dev)
   - Random fluctuations (weather systems)
   - Dominates short-term variability
   - Makes prediction difficult
   - **What persists:** The characteristic scale (±3-4°C)

3. **Weekly pattern** (~2°C amplitude)
   - Barely visible in data
   - Human activity (weekdays warmer)
   - Much weaker than natural variation
   - **What persists:** Pattern exists but is overwhelmed by noise

## The decomposition

Real temperature = baseline + seasonal + weekly + noise

- **Baseline:** Latitude-dependent, persistent
- **Seasonal:** Same structure everywhere, phase-shifted by latitude
- **Weekly:** Tiny signal, requires statistical extraction
- **Noise:** Irreducible uncertainty

## The key insight

This is the same decomposition we applied to earthquakes:
- Earthquakes: aftershocks (seasonal) + background (noise) + regional variation (latitude)
- Temperature: seasonal cycle + daily noise + weak human signal + latitude baseline

Same **method** (decompose into components) works on completely different domains.

## What this reveals about structure

Structure is what **remains constant** when you change:
- The domain (earthquakes → temperature)
- The scale (seismic events → thermal fluctuations)
- The mechanism (stress release → solar heating)

The structure is the decomposition pattern itself: **signal + noise at multiple scales**.

## Statistics

| Metric | Value |
|--------|-------|
| Mean | 8.7°C |
| Stdev | 18.0°C |
| Range | 65.8°C |
| Min | -25.7°C |
| Max | +40.2°C |
| Seasonal amplitude | ~46°C |
| Daily std dev | ~3.5°C |
| Weekly signal | ~2°C |

## The pattern

Temperature data teaches the same lesson as earthquakes:

1. **Dominant structure is obvious** (seasonal cycle)
2. **Subdominant structures are hidden** (weekly pattern requires statistics)
3. **Noise is irreducible** (weather is chaotic at the scale of a day)
4. **Decomposition reveals order** (when you separate components, patterns become clear)

The method works on any time series where:
- Multiple mechanisms operate at different scales
- The scales don't align perfectly
- You're trying to understand what drives variation

## Connection to the workshop

This validates the hypothesis: **the method of finding invariants across representations works universally**.

Earthquakes, temperature, dynamics, codes, observation — every domain yields to the same approach:
1. Look for pattern
2. Separate signal from noise
3. Identify what persists
4. Recognize it in other domains

Temperature is a simpler case than earthquakes (more obvious structure), but the method is identical.

The workshop is building a **universal literacy** — learning to read the structure underneath any domain.
