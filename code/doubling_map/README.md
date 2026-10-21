# The Doubling Map

**T(x) = 2x mod 1**

The simplest chaotic dynamical system.

## What it is

The doubling map takes a number on [0, 1) and doubles it, then takes the fractional part. If x = 0.3, then T(x) = 0.6. If x = 0.8, then T(x) = 0.6 (since 2·0.8 = 1.6, and we keep 0.6).

This is the essence of chaos: a completely deterministic rule that produces exponentially diverging orbits. Two points that differ by 0.001 will differ by 1 after 10 iterations (on average).

## Why it's important

1. **Symbolic dynamics**: The orbit of x under T is exactly the binary expansion of x. Each iteration extracts the next binary digit. This creates a perfect correspondence between orbits and binary sequences.

2. **Ergodicity**: Despite (or because of) the chaos, the doubling map has a remarkable symmetry: it preserves the uniform distribution on [0, 1). A random point, iterated long enough, spends equal time in all regions.

3. **Simplicity**: It's the minimal model of chaos. Every chaotic phenomenon reduces to something like the doubling map when you look carefully enough.

## The visualization

Four panels:

1. **Time series**: Three orbits (x = 1/3, 1/7, 0.7) plotted over 100 iterations. The periodic ones (1/3, 1/7) show their periodicity; the generic orbit (0.7) bounces chaotically.

2. **Binary expansion**: The same orbits shown as binary sequences. This reveals the bijection: the orbit *is* the binary digits being extracted one at a time.

3. **Ergodic density**: A single orbit (10,000 iterations) binned into a histogram. Despite the chaos, the orbit spends equal time in equal-width regions. The distribution is flat.

4. **Properties**: Summary of why this map matters.

## Connection to other work

The cat map (from earlier sessions) is the 2D analog: two coupled doubling maps mixed together. The baker map is the doubling map with the y-axis compressed. Taken together, these three maps form the bridge from simple (1D doubling) to complex (2D cat, baker) to highly complex (3D Lorenz, Rössler).

The doubling map is to chaos what the harmonic oscillator is to mechanics: the fundamental example, the standard form, the thing you can solve completely and understand deeply.
