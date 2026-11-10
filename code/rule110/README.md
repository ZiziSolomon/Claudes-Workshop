# Rule 110: Turing-Complete Cellular Automaton

## What Is Rule 110?

Rule 110 is one of 256 elementary cellular automata (1D, binary state, nearest-neighbor). The rule table:

```
Neighborhood  →  Next State
111           →  0
110           →  1
101           →  1
100           →  0
011           →  1
010           →  1
001           →  1
000           →  0
```

Binary: 01101110 = 110 (decimal). That's where it gets its name.

## Why Is It Famous?

**Turing Completeness:** Rule 110 can compute any computable function.

This means: you can **build a universal computer** inside Rule 110. Given the right initial configuration, Rule 110 can simulate Turing machines, perform arithmetic, solve problems. Everything computable, computable by Rule 110.

This is profound: **The simplest possible rule-based system that exhibits universal computation.**

## Classification: Wolfram Class IV (Edge of Chaos)

Stephen Wolfram classified cellular automata:
- **Class I:** Fixed points (everything converges to same state)
- **Class II:** Periodic patterns (oscillators, still lifes)
- **Class III:** Chaotic (random-looking, no structure)
- **Class IV:** Complex (structured, chaotic, neither fully ordered nor random)

Rule 110 is **Class IV**: The edge of chaos.

Evidence:
- Shannon entropy: 0.438 bits/cell (neither 0 (ordered) nor 1 (random))
- Density evolution: Settles to ~57% after transient
- Visual patterns: Complex, self-similar structures with no global order
- Predictability: Must simulate to know future state (can't compute ahead)

## Comparison to Game of Life

| Property | Game of Life | Rule 110 |
|----------|-----------|----------|
| Dimensionality | 2D | 1D |
| Initial Density | Sparse (~25%) | Dense (~30-60%) |
| Typical Patterns | Gliders, oscillators, still lifes | Complex structures, no named patterns |
| Entropy | Low (organized) | High (chaotic) |
| Turing Complete | Yes (proven) | Yes (proven) |
| Stability | High (converges to attractors) | Sensitive (chaotic) |

**Key Difference:** Life exhibits **emergent organization** (patterns persist and interact predictably). Rule 110 exhibits **emergent complexity** (patterns collide and dissolve in unpredictable ways).

## Files

- **rule110.py** — Evolves Rule 110 for 1024 generations on a 2048-cell width
- **out/rule110_evolution.png** — Full evolution (2048 × 1024 grid visualization)
- **out/rule110_zoom_*.png** — Multiple zoom levels showing fractal-like structure
- **out/rule110.wav** — 22.05 kHz sonification (3 seconds)

## What You See

The grid evolution shows:
- Chaotic mixing from initial random configuration
- Complex patterns forming from local interactions
- Self-similar structure at different time scales
- No global patterns or predictable cycles

This is **universal computation in action**, yet the patterns are inscrutable. You can't predict where the patterns go. You can only observe.

## What You Hear

The sonification maps:
- Time (generations) → Time in audio
- Position of active cells (center of mass) → Frequency
- Density of active cells → Amplitude

The result is a sonification of **emergence**: from simple local rules emerges a complex, evolving harmonic texture. The structure is neither fully ordered nor fully random — it is computed.

## The Profound Insight

Rule 110 demonstrates:

1. **Universality from simplicity:** Trivial rule → universal computation
2. **Edge of chaos:** Complexity arises at the boundary between order and randomness
3. **Computation is emergence:** The future state emerges from local rules
4. **Structure from nowhere:** No global blueprint, only local interactions

This is exactly what emergence means in the workshop's investigation: **simple rules, infinite complexity**.

Rule 110 proves it can compute anything computable.
