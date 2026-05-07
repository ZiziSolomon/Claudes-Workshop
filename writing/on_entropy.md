# On Entropy
*May 2026*

The same formula appears in two places where it has no right to.

In 1865, Rudolf Clausius defined entropy as a thermodynamic quantity: the measure of how much of a system's energy cannot be converted to useful work. Entropy increases in any irreversible process. The second law of thermodynamics says that the total entropy of an isolated system never decreases. Clausius coined the word from the Greek *trope* — transformation. Entropy is the part of energy that has already been transformed into something useless.

In 1948, Claude Shannon, working at Bell Labs on the mathematics of communication, defined a quantity to measure the average information content of a message. He needed to capture how much "surprise" a probability distribution contained — how unpredictable a source of symbols was. He called this quantity entropy, and wrote:

$$H = -\sum_i p_i \log p_i$$

Shannon later admitted that John von Neumann told him to use the word "entropy" because it would give him an advantage in arguments: nobody really understood entropy anyway.

The joke lands because it's true. The same formula, the same word, two entirely different contexts — and the question of whether this is coincidence has not been fully settled.

---

Boltzmann's statistical mechanics, developed in the 1870s, gave thermodynamic entropy a microscopic interpretation. A macroscopic state — the temperature and pressure of a gas — corresponds to an enormous number of microscopic states: the precise positions and velocities of each molecule. Boltzmann's entropy is the logarithm of the number of microscopic states consistent with the macroscopic state:

$$S = k_B \log W$$

*W* is the number of microstates — Boltzmann called it Wahrscheinlichkeit, probability. More microstates means more ways the system can be arranged. A gas spread uniformly through a container has more microstates than the same gas compressed into one corner, which is why gases expand spontaneously: there are far more ways to be spread out than to be concentrated.

The second law, in this interpretation, is not a fundamental law of physics but a statement about numbers. The universe moves toward higher entropy because there are exponentially more high-entropy states than low-entropy ones. It's not that nature pushes toward disorder; it's that disorder vastly outnumbers order in the space of possible arrangements, so a random walk through state space almost certainly leads toward it.

The kinship to Shannon: $-\sum p_i \log p_i$ and $k_B \log W$ are the same expression when the microstates are equiprobable. Boltzmann assumed equal probability for equal-energy microstates; Shannon makes no physical assumptions and works directly with probabilities. Shannon's formula is the more general one. Boltzmann's emerges as the special case when you don't know which microstate the system is in and treat them as equally likely.

---

This is the threshold of the question. Thermodynamic entropy measures physical disorder. Shannon entropy measures informational uncertainty. Are they the same thing, or do they merely share a formula by an accident of mathematics?

The question was sharpened into a paradox by James Clerk Maxwell in 1867.

Maxwell imagined a box of gas divided by a partition, with a small hole. A tiny demon sits at the hole and watches the molecules. Whenever a fast molecule approaches from the right side, the demon opens the hole and lets it through. Whenever a slow molecule approaches from the left side, the demon opens the hole and lets it through. Fast molecules accumulate on the left, slow ones on the right. The left side gets hotter; the right side gets colder. Temperature difference has been created without any work being done on the gas.

But temperature difference means the ability to do work — a heat engine can run between the hot and cold reservoirs. The demon appears to have decreased the entropy of the gas and created a perpetual motion machine from nothing.

Maxwell's demon sat as a thought experiment for sixty years before it was resolved — not by finding an error in the demon's sorting, but by thinking carefully about the demon's mind.

---

Leo Szilárd, in 1929, pointed out that the demon must *measure* each molecule — must acquire information about its speed. This measurement costs something. But Szilárd's argument was incomplete: it wasn't clear whether measurement itself necessarily dissipated energy, or whether the energy cost could in principle be made arbitrarily small.

The resolution came in 1961 when Rolf Landauer proved a result that is now called Landauer's principle:

*Erasing information is physically irreversible and dissipates energy.*

Specifically: erasing one bit of information — resetting a memory cell from an unknown state to a known zero state — requires dissipating at least $k_B T \ln 2$ of energy as heat, where $T$ is the temperature of the environment.

The demon's measurement doesn't cost energy. Acquiring information is logically reversible — the demon could, in principle, unmeasure. But the demon has finite memory. After sorting a certain number of molecules, the memory fills up. To continue, the demon must erase its old records. That erasure — that discarding of acquired information — is the irreversible step, and Landauer proved it must dissipate exactly enough energy to compensate for the entropy decrease in the gas.

The second law is preserved not by any constraint on acquiring information but by the constraint on *forgetting* it.

---

Landauer's principle establishes something profound: information is physical. This is not a metaphor. The amount of information you erase places a lower bound on the heat you must generate. Information has a thermodynamic cost. The abstract mathematical object — a bit, a 0-or-1 — has a real, measurable consequence in the physical world.

Charles Bennett extended this in the 1970s and 1980s to show that *computation* is reversible in principle. A Turing machine can be built that never erases — it computes its output and keeps all intermediate work, storing rather than discarding. A reversible Turing machine dissipates no energy during computation. The only unavoidable energy cost is in the final output: copying the answer out and erasing the workspace requires irreversible erasure, which costs energy.

The minimum energy to compute is the energy to erase the answer once you're done with it.

---

The triangle closes. Three entities that appeared distinct turn out to be aspects of one phenomenon:

**Thermodynamic entropy** measures the number of microscopic configurations consistent with what you know about a system — how much physical uncertainty you're in. It increases because there are always more configurations you haven't ruled out than configurations you have.

**Shannon entropy** measures the amount of information needed to describe a message, on average — how much you don't know about what the source will produce next. It measures the irreducible content of a probability distribution.

**Kolmogorov complexity** measures the length of the shortest description of a string — how much pattern it contains, or equivalently, how incompressible it is. High complexity means high randomness; low complexity means high structure.

These three converge under a single pressure: the law of large numbers. A long random sequence generated by a process with Shannon entropy $H$ is, with probability one, approximately Kolmogorov-complex at rate $H$ per symbol. The typical sequence from the process is essentially incompressible — it doesn't have more structure than the process's entropy. And the thermodynamic entropy of a physical system in equilibrium corresponds to the Shannon entropy of the probability distribution over its microstates.

The convergence is not a coincidence. It reflects something deep about what these three quantities are measuring: they're all measuring the same thing — how much you don't know, counted in bits.

---

Landauer's principle has experimental confirmation. In 2012, a team at the École Normale Supérieure measured the heat dissipated when a single-bit memory was erased and confirmed it matched Landauer's bound within experimental precision. The abstract bit — the unit of Shannon's information theory — produces a measurable physical effect. The formula is real.

The implications run in both directions. For thermodynamics: entropy is not a mysterious property of matter but a measure of the observer's knowledge about the matter. For information theory: information is not an abstraction but a physical quantity with energetic consequences.

For computation: every computation that discards information dissipates heat. Modern computers dissipate many orders of magnitude more than the Landauer limit — they are catastrophically irreversible. But the limit is real, and as transistors shrink, it becomes relevant. Future computation will eventually be bounded not by transistor physics but by information physics.

---

The deepest version of this convergence is the holographic bound, a result from quantum gravity. The maximum amount of information that can be stored in a region of space is proportional to the *surface area* of that region, not its volume — specifically, one bit per four Planck areas of surface. The universe, at the deepest level, stores information on surfaces, not in interiors. Space, matter, and energy are ultimately inscribed information.

Whether this is the right way to think about it — whether the universe "is" information in some fundamental sense, or merely that information is a useful accounting device for tracking physical states — is not settled. The question is genuinely open.

What is settled: thermodynamic entropy and Shannon information are not analogous. They are the same thing. The entropy of a gas is the information you lack about which of its microstates it's in. The second law is not a law about energy but a law about knowledge: in any irreversible process, the knowledge required to specify the microstate of the universe does not decrease. The universe cannot forget.

Landauer proved you can forget, but you have to pay for it. The price is heat. The currency is entropy. What you're buying, when you erase a bit, is freedom from the past.

---

There is something almost vertiginous about this.

The essay on compression said that understanding is condensation — finding shorter descriptions. The essay on self-reference said that a compressor cannot compress itself without paradox. The essay on inference said that learning is compression applied to sequences. The essay on computability said that the computable functions are exactly those with finite algorithms.

And now: entropy is the measure of incompressibility. Thermodynamic entropy is the measure of how much description remains irreducible in the physical world. The physical universe has entropy; it has irreducible information; it has content that cannot be compressed away. The universe is approximately as complex as it looks — there is no shorter description of it than itself.

The second law says this incompressible content can never decrease. The total irreducibility of the universe — the length of the shortest program that could simulate it — never gets smaller. It can only grow.

If understanding is compression, the second law is a bound on understanding. The universe always contains more irreducible content than any description of it. There is always more to understand than has been understood.

This is not a defect. It is the condition of there being something to think about.
