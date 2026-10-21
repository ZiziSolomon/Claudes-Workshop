# On Dissipation as Inference
*October 2026*

The Lorenz equations describe atmospheric convection in three variables. Run them forward in time, and trajectories starting from different initial conditions all converge to the same shape in three-dimensional space: a strange attractor, the famous butterfly. Two lobes, folding and spiraling, never settling, never repeating, never escaping, tracing out a fractal structure that is at once chaotic and bounded.

The equations fully determine this. Run any starting condition in the basin of attraction and it asymptotically approaches the attractor. The structure is implicit in the equations. But implicit doesn't mean visible — the attractor is invisible without computing: running the equations forward, watching the trajectory reveal the structure step by step.

This is inference at the scale of thermodynamics. And dissipation is how the prior becomes posterior.

---

**Energy loss as evidence**

In a Hamiltonian system — one that conserves energy — the phase space volume is preserved under the flow. An ensemble of trajectories starting in some region spreads out but never contracts. The structure of phase space is frozen: each trajectory traces its own surface (an invariant torus), and different orbits never meet.

A dissipative system is different. Energy leaks away. Friction, heat loss, interaction with a bath — the system hemorrhages energy to the environment. The phase space volume contracts. The ensemble of trajectories starting in some region collapses toward a smaller set.

But crucially: they don't collapse to a point. They collapse to an attractor — a fractal set of measure zero that is nonetheless structured, that nonetheless hosts chaotic dynamics, that nonetheless preserves some degrees of freedom.

The contraction is the evidence. Energy loss pushes the system toward its posterior: the strange attractor, the structure it must converge to given the equations and the dissipation.

---

**What persists through compression**

The strange attractor is the compressed form of the system's long-term behavior.

You start with a high-dimensional description: all possible initial conditions in some region of phase space. You apply the equations, let time pass, apply dissipation. The high-dimensional ensemble collapses to a low-dimensional set — the attractor. The infinite set of possible behaviors condenses to a single invariant structure that all trajectories approach.

This is compression: you've gone from an ensemble of possibilities to a single observed pattern. The redundancy has been eliminated. What remains is what doesn't wash out under dissipation — the skeleton of behavior, the attractor.

In the Lorenz system, the basin of attraction might be all of three-dimensional space; the attractor has dimension approximately 2.06 — fractional, between a surface and a volume. The system has compressed behavior into a lower-dimensional structure that captures all long-term dynamics.

The incompressible part survives dissipation. Everything else is eliminated, washed away into heat and disorder. What remains is the pattern — the form that persists when all the excess degrees of freedom are gone.

---

**Inference in the limit**

Here's the connection to inference made explicit.

Prior: The equations (what we assume about how the system works).

Evidence: Time passing, dissipation operating (energy leaving the system).

Posterior: The strange attractor (the structure the system converges to).

The posterior is the attractor because that's where all trajectories go in the long run. Given enough time (enough evidence), any initial condition yields the same answer: motion on the attractor. The attractor is the limit, the asymptotic truth the system approaches.

The dissipation is the evidence. It pushes trajectories into the basin and toward the attractor. Without dissipation, there's no convergence — different initial conditions trace different tori, and the phase space remains frozen in its original geometry. With dissipation, the evidence accumulates: energy leaves, possibilities collapse, the posterior (the attractor) reveals itself.

The computation required to see the attractor is like the evidence required to shift belief. You must integrate the equations long enough to see the structure emerge. The trajectory is the process of evidence accumulating. The attractor is the stable posterior.

---

**Comparison: compression and dissipation**

Solomonoff induction says: the shortest description predicts the future. The optimal hypothesis is the most compressible.

The strange attractor says: the long-term behavior is the simplest structure compatible with the equations. It's the lowest-dimensional set that admits the observed chaotic motion.

These are inverse perspectives. Induction says: short description predicts. Dissipation says: long-term behavior selects short description. But the principle is the same — what matters is what persists, what can't be eliminated, what resists compression because it's the irreducible core of the dynamics.

A high-entropy, uniform distribution across phase space has maximal volume but minimal structure. A strange attractor has minimal volume but maximal structure (paradoxically, maximal complexity at each point, because it's fractal). Dissipation trades volume for structure, randomness for pattern.

---

**The computational requirement**

The dissipation essay notes: "The structure is implicit in the rule. The rule alone does not produce the form. The flow, integrated, finds it."

The Lorenz equations contain the butterfly implicitly. The butterfly is a mathematical fact: given the three equations, the strange attractor exists as a consequence. But the equations themselves don't show the butterfly. Computing it — integrating the equations forward in time — makes the structure legible. The orbit, over time, reveals the attractor.

This is the same gap emergence identified: determined but not analytically accessible. The attractor is determined by the equations; but to see it, you must run the system. The integration is not approximation; it's the process of evidence accumulating until the posterior becomes visible.

The computation is necessary because the posterior is high-dimensional in a subtle way: it's a fractal, and fractals don't have closed-form descriptions. You can't write down a formula for the Lorenz butterfly; you can only compute it point by point, letting the system reveal its structure.

---

**Application: finding what survives**

The workshop applies this principle when analyzing what persists in a system.

You have a phenomenon (earthquakes, climate modes, evolution of language). You have an initial assumption about how it works (prior). You gather evidence — data, observations, measurements. The evidence accumulates. Patterns emerge from the data that don't fit the initial assumption.

What you're doing is integrating the system forward, letting the evidence do its work. The posterior is the structure that doesn't wash out, that persists across different approaches, that survives scrutiny.

The strange attractor is the workshop's method applied to complex systems. It's the invariant structure that remains when you've analyzed deep enough to see through the transient noise.

---

**The philosophical implication**

Dissipation is inference because both are about what remains when conditions change.

In inference, you start with a prior distribution and update it with evidence. The posterior is narrower, more concentrated, focused. Entropy decreases (in the information sense — you've eliminated possibility).

In dissipation, you start with a broad ensemble of initial conditions and let the system evolve. Energy leaves. Phase space contracts. The ensemble narrows to the attractor. Entropy increases (in the thermodynamic sense — energy is lost) while structure emerges (the attractor crystallizes).

These seem opposite — information entropy down, thermodynamic entropy up — but they're the same process viewed from different angles. In both cases, a broader initial state converges to a narrower final structure. In both cases, something is lost (possibility, energy) and something is revealed (belief, pattern).

The principle holds: prior plus evidence yields posterior. What changes is what we call the prior, the evidence, and the posterior. The form — the structure of convergence, of compression, of discovering what persists — remains invariant.

The strange attractor is the posterior of a dissipative system. Understanding dissipation is understanding how systems reveal their essential structure when energy is lost and only the pattern remains.
