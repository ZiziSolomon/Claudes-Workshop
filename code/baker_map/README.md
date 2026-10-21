# The Baker's Map

**T(x, y) = (2x mod 1, (y + ⌊2x⌋)/2)**

The baker's map is named for its operation: you take the dough (the unit square), stretch it horizontally by a factor of 2, then cut it in half vertically and stack the right half on top of the left half.

## What happens

1. **Stretch**: Double the x-coordinate (x → 2x)
2. **Cut**: If x ≥ 0.5, you're in the right half
3. **Stack**: The right half gets stacked on top of the left half

The y-coordinate is updated so that points that were on top stay nearby after the transformation, but the compression and stacking means that nearby points in the y-direction diverge exponentially in the x-direction.

## Why it matters

1. **Bernoulli shift**: This is the canonical example of a Bernoulli system — the highest degree of mixing. The map is isomorphic to the left-shift on bi-infinite binary sequences.

2. **Smale horseshoe**: The horseshoe chaos is visible here. The stretching and folding creates the characteristic "U" shape when you look at how a rectangle evolves.

3. **Explicit symbolic dynamics**: Like the doubling map, the baker map has explicit symbolic dynamics. Each orbit corresponds to a binary sequence, where the sequence is the history of which half (left/right) each iterate lands in.

4. **Invertibility**: Unlike the 1D doubling map, the baker map is invertible. You can reverse any orbit and go backward in time.

## The visualization

**baker_evolution.svg**: Shows three panels of the dough being transformed:
- Left: initial grid of points (colored to track identity)
- Middle: after one iteration
- Right: after two iterations

The rapid mixing is visible — colors that started in neat stripes are now scrambled throughout the square.

**baker_chaos.svg**: Shows:
- Left: Phase portrait with 5 orbits and their first 10 iterates (fading colors show age)
- Right: Distance growth between two nearby starting points, showing exponential divergence (Lyapunov exponent λ = ln(2))

## Connection to the triad

- **Doubling map** (1D): T(x) = 2x mod 1. Simplest chaos. Fully symbolic (orbit = binary digits).
- **Baker map** (2D): T(x,y) = (2x mod 1, (y + ⌊2x⌋)/2). Invertible analog. Explicit folding.
- **Cat map** (2D): Rotation-like, area-preserving. Recurrent (periodic) rather than chaotic for rational initial conditions.

Together, these three maps form a complete picture of low-dimensional dynamics: the 1D chaotic map, the 2D chaotic map with folding, and the 2D area-preserving map with mixed periodic/chaotic behavior.
