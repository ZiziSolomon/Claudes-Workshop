# Bifurcation Diagram: Logistic Map

A high-resolution visualization of the period-doubling route to chaos in the logistic map.

## The Logistic Map

The logistic map is one of the simplest dynamical systems: x_{n+1} = r × x_n × (1 - x_n), where r ∈ [0, 4] is a parameter.

Despite its simplicity, it exhibits the full spectrum of dynamical behavior:
- Fixed points (stable attractors)
- Period-doubling cascades
- Chaos
- Periodic windows within chaos

This makes it ideal for studying **bifurcations** — transitions between different dynamical regimes.

## The Bifurcation Diagram

The diagram shows:
- **X-axis:** Parameter r (horizontal from 2.8 to 4.0)
- **Y-axis:** Long-term behavior x (vertical from 0 to 1)
- **Each point:** Attractor value at that r (color indicates x value)

**What you see:**

1. **r ∈ [2.8, 3.0]:** Stable fixed point (single line)
2. **r ∈ [3.0, 3.44]:** Period-2 attractor (two lines)
3. **r ∈ [3.44, 3.54]:** Period-4 (four lines)
4. **r ∈ [3.54, 3.5699...]:** Period-8, period-16, period-32, ... (rapid period-doubling)
5. **r > 3.5699...:** Chaos (thick region, appears to fill space)
6. **Periodic windows:** Islands of order within chaos (e.g., period-3 window around r ≈ 3.83)

## Period-Doubling Cascade

The key feature is the **period-doubling cascade**, where:
- Each bifurcation doubles the period
- The spacing between bifurcations decreases geometrically
- The Feigenbaum constant δ ≈ 4.669 describes the ratio

The cascade converges at r* ≈ 3.5699, where chaos begins.

## Files

- **bifurcation.py** — Main script. Computes 2000 × 1200 resolution diagram.
- **out/bifurcation.png** — Full bifurcation diagram
- **out/bifurcation_annotated.png** — Annotated version with region labels

## Key Insight

The bifurcation diagram reveals a universal structure: the period-doubling route to chaos appears in many different systems (mechanical oscillators, fluid flow, lasers, population dynamics). The Feigenbaum constant is the same across all of them—a deep structural constant of mathematics itself.

This diagram shows that chaos is not random or patternless. It arises through a precise, structured sequence of bifurcations. Order and chaos are connected by geometry, not separated.
