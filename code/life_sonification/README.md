# Game of Life Sonification

A density-based sonification of Conway's Game of Life — making emergence audible.

## Conway's Game of Life

The rules are simple:
1. A live cell with 2 or 3 neighbors survives.
2. A dead cell with exactly 3 neighbors becomes alive.
3. All other cells die or stay dead.

From these three rules emerge gliders (moving patterns), blinkers (oscillators), still lifes, and complex interactions. The structure arises entirely from local rules applied uniformly.

## Sonification Strategy

The 128 × 128 grid is divided into **5 vertical bands**, each mapping to a note in the pentatonic scale (C3, D3, E3, G3, A3).

For each generation:
1. Compute the population density of each band (column range)
2. If density > 2%, include that note in the output
3. Amplitude = 0.1 + 0.5 × density (louder if more populated)
4. Combine all active notes into a chord

As the Game evolves, births, deaths, collisions, and gliders produce changes in the population structure, which manifests as chord changes and harmonic shifts in the sonification.

## What You Hear

- **Silence or sparse notes:** Early in evolution as patterns stabilize
- **Chord changes:** When gliders collide or patterns interact
- **Sustained notes:** Stable regions with oscillating patterns
- **Complex harmony:** Multiple regions with different densities

The sonification reveals the dynamics without explicit event tracking — population structure drives the sound entirely.

## Files

- **sonify.py** — Main script. Runs 240 generations of 128×128 Life, computes band densities, synthesizes pentatonic chords
- **out/life.wav** — 22.05 kHz mono, 24 seconds (240 generations)
- **out/evolution.png** — Heatmap showing grid state over time
- **out/spectrogram.png** — STFT showing frequency content
- **out/panel.png** — Combined visualization

## Key Insight

Sonifying emergence reveals something about its nature: emergence is not visible in individual rules, and not easy to perceive in static grid images. But when mapped to evolving sound, the structure of emergence becomes perceptible — the rise and fall of populations, the periods of stability and disruption, the creation of patterns that persist.

The sonification demonstrates that structure can be perceived across multiple modalities: visual (the grid), sonic (this sonification), and conceptual (the three simple rules).
