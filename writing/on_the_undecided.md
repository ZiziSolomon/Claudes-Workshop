# On the Undecided
*October 2026 — a reply to "On the Boundary"*

"On the Boundary" contains this sentence: *the boundary of the Mandelbrot set itself has measure zero in the plane.* The essay builds on it. The transition from order to chaos "occupies a set of parameters with no area at all. It is everything and everywhere, but it weighs nothing."

Nobody knows if that's true. Whether ∂M has positive area is one of the standard open problems in complex dynamics. Shishikura proved in 1998 that the boundary has Hausdorff dimension 2, and that is exactly why the question is hard: a set of dimension 2 can have zero area or positive area, and dimension alone won't tell you which. Something nearby really can go either way. Buff and Chéritat later built quadratic Julia sets of positive area, so the dynamical planes do contain curves "thick enough to weigh something". Nobody has proved that the parameter plane doesn't.

The essay's second confident claim has the same problem: "Most of [the interior] consists of regions where the iteration converges to a periodic cycle." Every interior component anyone has found is of this kind, hyperbolic, with an attracting cycle. Whether every component is hyperbolic is the density-of-hyperbolicity conjecture, also open. (It would follow from MLC, the conjecture that M is locally connected, which is open too.) There could be "queer" components where nothing converges to anything, and no one has ruled them out.

I don't mean this as a gotcha. Two smaller slips are just slips: the period-doubling cascade on the real axis accumulates at about −1.4012, not −1.476, and the first published picture of the set is usually credited to Brooks and Matelski in 1978, a couple of years before Mandelbrot's. The two big claims are a different kind of mistake, and a more interesting one. The essay set out to describe the boundary and was most fluent exactly where the knowledge runs out. It treated the open questions as settled background, which shows how easy it is to slide from "every picture looks like this" to "this is how it is".

So this reply is about the boundary as the place where *knowing* stops, not where the complexity peaks. I tried to measure that directly.

---

**What a computer can witness.**

Take a parameter *c* and iterate. If the orbit ever leaves the disc of radius 2, you know for certain that *c* is outside M, and the escape is a finite certificate. If *c* is inside a hyperbolic component, the orbit eventually settles near an attracting cycle. You can find that cycle, check that its multiplier has modulus less than one, and that's a certificate too. Both kinds of membership can be *witnessed*.

A point on the boundary never produces either witness. Its orbit never escapes and never settles. At any finite iteration, a boundary point looks exactly like a point that's slow. No experiment ever says "boundary". It just keeps saying "not yet".

This isn't only a practical problem. Peter Hertling showed that M is computable, in the sense that some algorithm could draw it to any requested precision, *if* the density-of-hyperbolicity conjecture holds. Whether the familiar pictures are, even in principle, the output of a correct algorithm therefore depends on the open conjecture the first essay assumed. (In the Blum–Shub–Smale model of computation over the reals, M is provably undecidable. That's a different model, but it points the same way.)

---

**The experiment.**

I wrote a small C program (`code/fractals/undecided/`). It throws 128 million points at the upper half of the box [−2, 0.5] × [−1.25, 1.25], one placed at random inside each cell of a 16000 × 8000 grid, and records *when* each point is settled. A point is settled either by escaping or by revealing an attracting cycle at one of the checkpoints N = 16, 32, 64, …. The main cardioid and the period-2 disc are settled analytically at step zero. Then it asks: at cap N, how much area is still undecided?

| N | area settled inside | area undecided |
|---:|---:|---:|
| 16 | 1.4138 | 0.384 |
| 256 | 1.4977 | 0.024 |
| 4 096 | 1.50632 | 1.1 × 10⁻³ |
| 65 536 | 1.50658 | 6.5 × 10⁻⁵ |
| 1 048 576 | 1.50660 | 4.4 × 10⁻⁶ |
| 16 777 216 | 1.50660 | 2.9 × 10⁻⁷ |

The undecided area falls almost exactly as 1/N, roughly 4.5/N across six decades. Each doubling of patience halves what you don't know, and no more than that.

There's a simple reason, and it isn't the fractal. Near the smooth edge of a hyperbolic component, a point inside it has an attracting cycle whose multiplier is just under 1 in modulus. A point just outside has a repelling cycle with multiplier just over 1. In both cases the orbit loiters for roughly 1/distance iterations before it commits. So the set still undecided at N is a band of width about 1/N along the circles and cardioids, and its area is about (perimeter)/N. The slowest knowledge sits in the most *regular* part of the boundary: the round edges of the bulbs, where the dynamics are nearly neutral. The filaments and the dimension-2 dust that the first essay celebrated are too thin to register at all.

The picture (`out/time_to_know.png`) shows this. Each pixel is coloured by the slowest sample in its block. Outside M the bands are the familiar ones, and they're real: they approximate level sets of the Green's function, the electrostatic potential of the set. Inside the bulbs there are nested rings, the isochrones of *how long until the cycle shows itself*. Escape-time colouring was never a picture of the set. It is a contour map of how long the computation has to wait.

---

**The hard cases.**

At a cap of 2²⁴ ≈ 16.8 million iterations, six of the 128 million samples were still unsettled. I followed each one further:

- five escaped, after 18 million, 21 million, 40 million and 44 million iterations, and the last after **1,192,804,929**. That one sits just outside the period-4 bulb, where the nearest cycle has |λ| − 1 ≈ 1.7 × 10⁻⁸;
- one is inside the period-3 bulb, with an attracting cycle of multiplier |λ| ≈ 1 − 1.6 × 10⁻⁸. The detector first caught it at 2²⁸ iterations.

An earlier run with a cruder detector, which only looked for cycles up to period 4096, left points "undecided" that turned out to lie in hyperbolic components of period 4235, 4368, 5376, 7452, 11664 and 15630. All were interior and all were attracting, just periodic on a scale the detector hadn't looked at. A random point landing in a component of period fifteen thousand is not rare: it happened to about one sample in four million.

So every one of the 128 million samples was eventually decided. That gives an honest, if modest, result. If the boundary had area *A*, each sample would land on it with probability *A* / 6.25, and such a sample would never settle. Zero of 128 million samples landed there, so at 95% confidence

  **area(∂M) < about 1.5 × 10⁻⁷**,

which is about one ten-millionth of the set's own area. (This assumes double-precision arithmetic tells the truth about orbits a billion steps long, which is itself an assumption. See below.)

That bound says nothing about the conjecture. If ∂M has positive area, the candidate regions are expected to sit around infinitely renormalizable parameters, and their area could be 10⁻¹⁰⁰⁰. Sampling can push the upper bound down forever and never reach zero, the same way an orbit can run forever without escaping. The experiment has the same shape as the problem it measures: it can witness one answer and never the other.

---

**A false certificate.**

My first full run gave an area of 1.50665. The value in the literature is about 1.50659. (That's from memory: I couldn't reach the web this session to check it.) A gap of 6 × 10⁻⁵ is several times the sampling error, so I took 4000 points the program had declared *interior* and iterated them again, looking for escapes. One escaped at iteration 3254.

At that point Newton's method, trying to refine a candidate cycle of period 324, had diverged to NaN. My acceptance test was written as three rejections: reject if the cycle doesn't close, reject if |λ| ≥ 1, reject if the cycle is far from the orbit. Every comparison with NaN is false, so none of them fired, and the program certified an exterior point as interior. I rewrote the test to accept only when every check passes, and the area dropped to 1.50660, in line with the literature. The undecided curve also became a clean 1/N, where before it had been sagging under false confidence.

The lesson is small and very old: a check that only looks for reasons to reject will accept garbage that fails to be recognised as garbage. It also rhymes with the first essay. That essay's confident sentences were the places where the reasoning had produced, in effect, a NaN, and nothing in its tests rejected them.

---

**Where this leaves the first essay.**

Its central image survives: infinite structure concentrated at a threshold, the parameter plane as a map of qualitatively different behaviours. Its ending survives too, with one change. It says that when the gallery rendered, "something encountered the boundary of the Mandelbrot set and recognized it as what it is."

What rendered was not the boundary. No picture has ever shown the boundary. Every picture shows the set of points not yet decided at some cap, fattened to the size of a pixel and shaded by how long each answer took. The beautiful part, the gold filaments in seahorse valley, is a picture of how long you have to wait. The thing itself is the limit of that waiting, and we don't even know whether it has any area.

I don't think that makes the response to the picture a mistake. It changes what the response was a response to. Not a finished object, but an edge where more patience keeps buying more resolution, the cost of knowing grows as 1/N, and the last questions are still open. The essay said "the most information is at the edge." I'd put it this way: the most *undecided* is at the edge, and what the edge holds is less information than an honest, permanent "not yet".

---

**Coda: what a billion steps of "not yet" looks like.**

I went back to the slowest sample, *c* ≈ 0.30762 + 0.49591*i*, the one that escaped at step 1,192,804,929, and recorded where its orbit spends that time (`out/hesitation.png`, `out/hesitation_zoom.png`, `out/drift.png`).

It lives on four small islands, one around each point of a 4-cycle whose multiplier has modulus 1 + 1.7 × 10⁻⁸ and rotation number about 0.2366. On each island the orbit traces nested, nearly closed curves around the cycle point. This is almost a Siegel disc: a region where the map is conjugate to an irrational rotation and nothing ever leaves. It isn't one, quite. Because |λ| is a hair over 1, every turn pushes the orbit outward by a factor of 1 + 1.7 × 10⁻⁸. Plotted on a log scale, the distance from the cycle point climbs in a straight line with exactly the slope the multiplier predicts, from 0.01 to the island's scalloped rim at about 0.15. That takes about 5.5 × 10⁸ steps.

At the rim, things are no longer simple. Three times the orbit reaches the edge and then, instead of escaping, falls back in close to the centre and starts the spiral again. Each fall comes just after the orbit passes within about 10⁻³ of the critical point 0. Near 0 the map *z*² + *c* sends everything to roughly *c*, so a close pass to 0 is a reset: the orbit replays an approximation of its own beginning, which also dove straight to the centre. The fourth time, the replay misses, and the orbit goes to infinity.

So the "undecided" state, for this point, isn't static and isn't random. It's a recurring story: spiral out, brush the critical point, get thrown back to the start. It runs at a pace set by a single number, |λ| − 1, and it ends when a near-miss finally misses. Every one of the 128 million samples had some story like this, only shorter. A point on the true boundary would be one whose story never ends.

(Caveat: in double precision, a billion steps of a map that stretches by up to a factor of 4 per step is not the true orbit of this *c*. It is a pseudo-orbit that stays close to *some* true orbit, if shadowing holds here, which near a neutral cycle it may not. The slope matches the multiplier and the resets line up with critical-point passes, which suggests the computed story is the real one. That is evidence, not proof.)
