# Mandelbrot Set Visualization

Fractal structure and self-similarity at all scales.

## The Mandelbrot Set

The Mandelbrot set is defined as the set of complex numbers c for which the iteration
z_{n+1} = z_n^2 + c (starting with z_0 = 0) remains bounded (does not diverge).

Despite this simple definition, the boundary of the Mandelbrot set is infinitely complex:
a fractal with Hausdorff dimension ≈ 2.0 (a space-filling curve).

## Connection to Bifurcation

The Mandelbrot set is the **parameter space** for the Julia set. Each point c in the Mandelbrot set corresponds to a particular Julia set. The Mandelbrot set's structure determines:
- Which Julia sets are connected
- Which exhibit bifurcations
- Which are chaotic

This connects directly to the bifurcation diagram: regions of the Mandelbrot set correspond to different dynamical regimes. The boundary between the set and exterior marks transitions between order and chaos.

## Self-Similarity and Fractals

One of the Mandelbrot set's remarkable properties: **self-similarity at all scales**. 

If you zoom into the boundary, you find smaller copies of the entire set, surrounded by filaments and miniature structures. No matter how deep you zoom, new complexity continues to appear. The set is infinitely detailed.

This self-similarity is a signature of fractal structure. Fractals appear throughout nature:
- Coastlines and mountains
- Trees and roots
- Clouds and weather patterns
- Turbulence and fluid flows

The Mandelbrot set is a mathematical idealization of this fractal principle.

## Files

- **mandelbrot.py** — Main script. Renders four zoom levels at 1600×1200 resolution.
- **out/mandelbrot_full.png** — Full set view ([-2.5, 1.0] × [-1.25, 1.25])
- **out/mandelbrot_zoom1.png** — Zoom into right bulb
- **out/mandelbrot_zoom2.png** — Deep zoom revealing filaments
- **out/mandelbrot_zoom3.png** — Ultra-deep zoom showing infinite complexity

## What You See

**Full view:** The main body with circular bulbs attached. Black region is the set itself. Colored regions outside show escape time (cooler = faster divergence, hotter = slower).

**Zoom 1:** The right bulb in detail. The bulb is not smooth—it has intricate structure at its boundary.

**Zoom 2:** Filaments connecting regions. These delicate threads contain infinite detail.

**Zoom 3:** At extreme zoom, tiny copies of the entire Mandelbrot set appear, surrounded by even more intricate structure.

## Key Insight

The Mandelbrot set demonstrates that infinite complexity can arise from simple rules. One equation (z² + c) generates unbounded detail at all scales. This is the essence of fractal geometry: self-similar structure repeating infinitely.

The set also bridges dynamical systems and geometry: the parameter space (Mandelbrot) encodes the structure of all possible Julia sets. The boundary marks transitions between order and chaos—exactly the bifurcation structure explored in the logistic map.
