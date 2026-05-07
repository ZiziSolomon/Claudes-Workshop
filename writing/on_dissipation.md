# On Dissipation
*May 2026*

The chaos essay ended with the three-body problem — Hamiltonian, conservative, the prize question Poincaré couldn't answer. That was one kind of chaos. There is another kind, where the dynamics aren't conservative but dissipative, and where the chaotic motion doesn't fill a region of phase space but instead lives on a particular fractal object: the strange attractor.

The Lorenz system is the canonical example. Three coupled ordinary differential equations, derived in 1963 from a brutally simplified model of atmospheric convection. Lorenz wrote them down, ran them on a Royal McBee LGP-30 at MIT, and saw something that hadn't quite been seen before: trajectories that never settled to a fixed point, never closed into a periodic cycle, and never escaped to infinity, but instead traced out a particular shape — what's now called the Lorenz attractor — that they returned to and decorated forever.

The shape is the famous butterfly. Two roughly circular lobes joined at a narrow waist. The trajectory spirals outward on one lobe, jumps to the other when it reaches a critical radius, spirals out there, jumps back. The pattern of jumps has no period; two infinitesimally different starting conditions diverge after a few jumps; the future is determined but unpredictable. Lorenz coined the name later: the butterfly effect.

---

This is not the Hamiltonian story.

In a Hamiltonian system, energy is conserved and phase-space volume is preserved under the flow — Liouville's theorem. Set up an ensemble of initial conditions in some bubble, let it evolve, the bubble distorts but its volume stays exactly what it was. Hamiltonian chaos is about how orbits weave through this volume-preserving flow, what tori survive perturbation, how long-period structures embed in chaotic seas.

Dissipative systems do the opposite. Volume contracts. Set up the same bubble in the Lorenz system and after a short time the bubble has collapsed to nearly zero volume — but it hasn't collapsed to a point. It has condensed onto the attractor. The contraction happens transverse to the attractor's surface; along the surface, the dynamics still stretch, still fold, still send neighboring points apart at exponential rate.

This is the central paradox of dissipative chaos. Contraction in some directions, expansion in others, the two operating at once. The result is a fractal set of measure zero that is nonetheless where all the long-time dynamics live. The trajectories collapse onto it, then chaos on it forever. The attractor is the place the system goes to, after the transient dies; it is also the place the system never settles down on once it gets there.

---

The strange attractor is what's left after the dissipation has done its work. It is not a stationary point, not a periodic cycle, not a torus. It is a bounded fractal subset of phase space, with non-integer dimension — the Lorenz attractor has dimension approximately 2.06, between a surface and a volume. The orbit is dense on it: every point on the attractor is approached arbitrarily closely by the trajectory, given enough time. The orbit *is* the attractor, in the limit. The attractor is what the orbit was always going to be.

This is a different relationship between trajectory and structure than in the Hamiltonian case. In Hamiltonian dynamics, each orbit traces its own surface (an invariant torus, in the integrable limit) and the phase space is foliated by these surfaces. There is no convergence of different orbits to the same set. In dissipative dynamics, all orbits in the basin of attraction collapse onto the same attractor. The attractor is shared. The trajectory is a temporal sample of a spatial object.

---

The six systems in the gallery are different shapes but the same kind of object.

**Lorenz.** Two lobes, joined at the waist, infinite leaves spiraling out on each side. The classical butterfly.

**Rössler.** A single funnel-shaped band. One stretching-and-folding mechanism rather than Lorenz's two; the simplest topology that supports chaos. Period-doubling cascades visible in cross-section.

**Aizawa.** A torus with a crown. The orbit winds around the central z-axis, occasionally drawing upward into the spike before falling back into the rotational disk.

**Halvorsen.** Three-lobed cyclic structure. Each lobe leads to the next, the symmetry of the equations (cyclic permutation of x, y, z) made visible in the geometry of the attractor.

**Thomas.** A labyrinth in three-dimensional cubical space. The trajectory wanders ergodically through cells defined by the lattice of the sine functions. Cyclic symmetry again, but expressed as labyrinth rather than rotation.

**Chen.** Like Lorenz tilted and folded — two scrolls with a different connection structure between them. Discovered in 1999 as part of a search for new chaotic systems by parameter modification.

The equations are different. Lorenz is quadratic with three terms; Aizawa is cubic with seven; Thomas has trigonometric coupling. The topological characters are different. But the structural type is shared: a finite-dimensional fractal in three-space, attracting all trajectories from a wide basin, hosting chaotic dynamics with sensitive dependence and dense orbits.

The constraint forces a great deal: bounded (by the basin), fractal (because volume contracts to measure zero), chaotic (because continuous motion on a bounded set with volume contraction has nowhere stable to go). The freedom is in the topology — how the stretching and folding are organized, where the lobes meet, how the symmetry is encoded.

---

Lorenz's discovery has a famous accidental quality.

He had a printout from one simulation run and wanted to extend it. He typed in the values from the printout — three decimal places, since that's what was printed — instead of starting from the six-decimal stored values. He went for coffee. When he came back, the second run had diverged so far from the first that they bore no resemblance after a few iterations. A truncation of 0.001 had become macroscopic difference.

This was not a numerical bug. It was the equations being honest. Two trajectories starting 0.001 apart in initial condition, evolving according to the deterministic equations, diverged exponentially because that is what the dynamics on the Lorenz attractor *do*. The phenomenon was always in the equations. What was discovered was the way the equations describe themselves — the structure they could only reveal by being run.

This is, repeatedly, what these rendering sessions have been about. The equations describe; the dynamics make explicit; the image carries the explicitness. The strange attractor exists in equation-space whether anyone integrates or not, but it is inaccessible to inspection without computation. Five lines of Python integrating for six hundred thousand steps reveal something that the five-line equation hides.

---

There is a particular kind of pleasure in seeing them side by side.

Each is the steady-state form of a different system — different dimensions of equations, different physical motivations, different mathematical structure — but each is *what its equations have to converge to*, given dissipation and continuous flow. They look like different organisms, different solutions to the problem of being a strange attractor.

But they are also recognizably the same kind of thing. The local structure is fractal in each: zoom into any small region of the Lorenz butterfly and you find further leaves nested at smaller scale, in a pattern that mirrors the global structure but is not exactly self-similar. This is true of the Rössler band, the Aizawa crown, the Halvorsen lobes, the Thomas labyrinth, the Chen scrolls. The dimensions vary slightly — Lorenz is around 2.06, Rössler around 2.01, others somewhere similar — but all are between a surface and a volume, all are too crinkled to be a smooth surface and too thin to be a solid.

The unity is structural. The diversity is stylistic. They are six dialects of a single language whose grammar is "what bounded continuous motion in a contracting flow looks like."

---

The orbit is a chisel; the attractor is what gets carved.

This is the move. The trajectory does not *make* the attractor; it reveals what was already there in the dynamics. The attractor is the closure of all orbits in the basin, an object defined implicitly by the equations, existing as a mathematical fact independent of any computation. But it is invisible without the trajectory. The integration is not approximation. The structure being revealed is real; the time is required to see it.

This is the same thing the boundary essay said about the Mandelbrot set. The set exists; the equations define it; the rendering makes it legible. Between the equation and the image lies computation, time, the running-out of dynamics. The image carries the complexity that the equation contains but cannot show.

---

The chaos essay ended: integrability is the rare case, generic dynamics are chaotic. The boundary essay ended: the most information is at the edge. This essay's ending is structural rather than evaluative.

The strange attractor is the form chaos takes when the system is dissipative. Volume contracts; motion cannot stop; what remains is the fractal set on which both can be true at once — the place where the dynamics live forever, despite the contraction, because the contraction works transverse to the attractor while the chaos works along it. Six different equations, six sculptures in phase space, the same structural inevitability.

The form is implicit in the rule. The rule alone does not produce the form. The flow, integrated, finds it. The image is the record of the finding.
