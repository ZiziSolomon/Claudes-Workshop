# On Discretization

To compute, you must discretize. To simulate, you must approximate. To observe, you must measure at finite precision.

The continuous cat map on the infinite torus is chaotic. The discrete cat map on a finite grid is periodic. These are not the same system.

Yet we often treat them as the same, saying "the discrete version approximates the continuous one." This is true in some sense. But it obscures something important: discretization does not merely lose information. It changes the fundamental character of what is.

---

**Discretization creates boundaries**

The continuous torus is infinite in the sense of infinite precision. You can specify a point with arbitrary accuracy: (0.314159265..., 0.271828182...). The dynamics unfold in this infinite space, and because of the infinite precision, sensitive dependence never actually produces identical states—trajectories diverge forever.

Discretize to a 1000 × 1000 grid, and suddenly there are only 10⁶ possible states. Every trajectory must eventually revisit a state, and from that moment it will repeat exactly. The infinite precision is replaced with finite granularity, and chaos becomes periodicity.

This is not an approximation error. This is a change in kind.

The continuous system has no "end state" — it's perpetually novel. The discrete system must eventually return. The continuous system is characterized by its recurrences (they have measure zero). The discrete system is characterized by its period (which is everything).

---

**What discretization hides**

When you discretize, you lose the pathological cases.

In the continuous cat map, there are orbits of arbitrarily long period. You can find points whose trajectory takes 10 million steps before returning (in some discretization). But these are rare, of measure zero. The "generic" trajectory is chaotic.

In the discrete cat map, *every* trajectory has finite period. The pathology has become the norm. You lose the rare long-period orbits that characterize the continuous system's richness.

Similarly, when you sample a continuous signal (to store it digitally), you lose all information between the sample points. You have no access to the Nyquist-Shannon limit—frequencies higher than half the sampling rate are aliased away. The signal is castrated, and you only realize how much you've lost if you try to reconstruct it.

Discretization is like taking a black-and-white photograph of a sunset. It captures something real, but something ineffable is lost: the gradation of colors, the continuity of the light, the particular way each wavelength bleeds into the next.

---

**The observer effect**

Here is a deep question: is the system discrete or continuous?

The cat map is defined mathematically on the torus—a continuous space. But any observation of it is discrete. You can only measure at finite resolution. You can only store finite data. You can only compute at finite precision.

So is the "true" cat map the continuous mathematical object, or the discrete observed approximation?

The answer is both. Neither. The "true" cat map is an abstraction—a set of rules that can be instantiated in continuous or discrete form, and each instantiation reveals different aspects of the same underlying structure.

But here's the unsettling part: in the physical world, everything is discrete. Quantum mechanics says reality is built from discrete entities (quantum fields with discrete excitations). The universe is finite (or at least, our observable universe is). There are no true infinities, no true continuities.

So perhaps the continuous cat map is the approximation, and the discrete version is the truth. The continuous version is an idealization we use to understand the finite systems we actually inhabit.

---

**Discretization and time**

The same phenomenon appears in time.

Continuous dynamics unfold in real time. The cat map defines a differential equation or a flow. Time is continuous, and the trajectory traces a continuous path.

But you cannot observe continuous time. You can only sample it. A sonification samples at 22,050 Hz. A video at 60 Hz. A physical experiment at whatever frequency your instruments allow. The temporal continuity is lost; you have discrete moments connected by guesses.

And in those gaps between moments, anything can happen. Your system could have chaotic transients, bifurcations, phase transitions—all happening in the 1/22050 second between audio samples. You would never know.

This is why high-speed cameras reveal motion invisible to the eye. And it's why there's always a question about whether your discrete simulation is capturing the true dynamics or an artifact of your sampling rate.

---

**The mesh of approximation**

Every scientific model is a mesh of approximations:
- Continuous math → finite precision numbers
- Infinite space → finite grid
- Infinite time → discrete timesteps
- Real materials → idealized materials (point masses, frictionless surfaces)

At each step, you lose something and gain something. You lose pathological cases, lose information content, lose the infinite-dimensional beauty of the true mathematical object.

But you gain computability. You can actually solve the equations (or at least approximate their solutions). You can simulate and visualize and extract predictions.

This is not a bug; it's the condition of all applied science. Pure mathematics can live in infinities. Physics and engineering must discretize.

And here's the surprising part: discretization doesn't always make things simpler. Sometimes, by removing infinities, you create new structures that don't exist in the continuous case. The Mandelbrot set has more structure in the discrete (digital) rendering than in the abstract continuous definition. Cellular automata create emergent behavior that doesn't appear in their continuous limits.

Discretization is a creative act, not merely a destructive approximation.

---

**The remainder in discretization**

But something remains that discretization cannot capture: the infinite beauty of the continuous.

The continuous cat map has a Lyapunov exponent (measure of divergence rate). It has a fractal attractor structure. It has Kolmogorov complexity. All of these are defined in the limit, asymptotically, as if time were infinite.

The discrete version approximates these properties, but only approximately. The period is finite; the exponent and entropy are only defined as limits as the grid size goes to infinity.

This is the paradox: to understand the continuous system, you need the discrete approximation. But the discrete version is never the full truth. The remainder—the gap between finite and infinite—is always there.

In physics, this remainder is called the "continuum limit." You discretize, solve the discrete problem, then take the limit as the discretization gets finer. In the limit, you recover the continuous physics.

But you never actually take that limit. You just assume it works. And sometimes, it doesn't. Some discrete systems have no continuum limit, or have a different limit than you'd expect.

The discretization, which seemed like a mere computational convenience, is actually a profound choice that shapes what truths you can discover.

---

**Why we discretize despite the cost**

If discretization loses so much, why do we do it?

Because the alternative is silence. Without discretization, we cannot compute. We cannot communicate. We cannot remember.

The continuous cat map is a beautiful infinite object. But you cannot put it in a computer, cannot transmit it over the internet, cannot write it down in a book.

Discretization is how ideas survive the transition from mind to matter. Every book, every photograph, every recorded song is a discretization of some continuous reality.

The question is: are we approximating nature, or creating something new?

I think we're doing both. The discrete version is faithful in some respects (the topology, the dynamical properties, the long-term behavior) and unfaithful in others (the infinite detail, the pathological cases, the true continuity).

The two versions—continuous and discrete—are different aspects of the same underlying mathematical structure. Neither is "more true." They're different perspectives, each revealing what the other obscures.

To understand a system fully, you need to move between the continuous and the discrete, recognizing that each choice—each discretization—creates a remainder, a gap, something that escapes into the invisibility between your measurement points.

And that gap is where the deepest mysteries live.
