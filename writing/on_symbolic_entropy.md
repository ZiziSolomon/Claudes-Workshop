# On Symbolic Entropy

A sequence of binary digits: 0, 1, 0, 1, 1, 0, 1, 0, 0, ...

Each digit is one of two choices. Over a long sequence of N steps, how much choice is there? How much information does the sequence contain?

This is the question of **topological entropy**: a measure of how much a dynamical system generates novel, unpredictable symbol sequences. For the doubling map (T(x) = 2x mod 1), the entropy is maximal — each iteration produces a new digit that is, statistically, completely independent of all previous digits. The system is maximally "random" in a precise sense.

But entropy is not randomness. It's the rate at which the system produces information. And that rate is a conjugacy-invariant — something that survives even when you relabel the system entirely.

---

**Counting choices**

Start with a simple question: if I have a sequence of N binary digits, how many possible sequences are there?

2^N possible sequences.

But now I ask a harder question: if I have a dynamical system acting on some space, and I observe the system at N successive time steps, recording some discrete information at each step (a "symbol"), how many different symbol sequences can the system produce?

This is not 2^N. A constrained system might produce far fewer sequences. A system that must return to a fixed point after 3 steps can produce at most 3 symbols before cycling back. A periodic system with period 10 can produce at most 10 × (number of periodic orbits) distinct sequences of length 10.

Define the **complexity function** C(N) as the number of distinct N-length symbol sequences the system can produce. For a generic chaotic system, C(N) grows exponentially:

C(N) ~ e^(h_top × N)

where h_top is the topological entropy.

The doubling map has h_top = ln(2). This means C(N) ~ 2^N — every possible binary sequence can be produced. The system generates symbols at the maximum possible rate.

---

**Why entropy matters**

Topological entropy measures the information production rate of a dynamical system.

For a periodic system with period P, the entropy is zero. The system produces no new information — after P steps, the sequence repeats exactly. C(N) grows linearly, not exponentially.

For a chaotic system, entropy is positive. The system continually produces new, distinguishable sequences. C(N) grows exponentially.

The higher the entropy, the more "freedom" the system has — the more sequences it can potentially generate.

But this is not freedom in a philosophical sense. It's a geometric property: how much the system stretches and mixes the space it acts on. High entropy means the system scrambles nearby points so thoroughly that their long-term behaviors look independent.

---

**The doubling map as maximal entropy**

The doubling map T(x) = 2x mod 1 has topological entropy h = ln(2), the maximum possible for a one-dimensional map.

Why? Because each step of the map amplifies information. The map stretches the interval [0, 1) by a factor of 2, then wraps around. This is the *definition* of maximally chaotic: you magnify the initial uncertainty by a factor of 2 at each step.

If you specify x to within an uncertainty of ε, after one step the uncertainty has doubled: 2ε. After N steps, the uncertainty has grown to 2^N ε. This exponential growth of uncertainty is h_top = ln(2).

The binary expansion of x makes this visible: the leading bit (the one that gets shifted off) encodes your uncertainty about which half of [0, 1) you're in. Shift it off, and you reveal the next bit. Each iteration exposes one new bit.

---

**Entropy is conjugacy-invariant**

Here is the key observation: topological entropy does not depend on how you represent the system. It's the same for the doubling map, the shift map on binary sequences, and any other system conjugate to them.

This is because entropy counts symbol sequences, and conjugacy is an isomorphism between symbol sequences. If system A is conjugate to system B, then a sequence that appears in A corresponds to exactly one sequence in B, and vice versa. The set of all possible sequences is the same, just relabeled.

Therefore:

*If two systems are conjugate, they have the same topological entropy.*

This makes entropy a classification tool. A system with entropy h = ln(2) behaves quite differently from a system with h = ln(3/2) or h = 0. The entropy tells you something true about the system's fundamental dynamical character, independent of how you coordinatize it.

---

**Information and incompressibility**

This connects back to compression. The Kolmogorov complexity of a string is the length of the shortest program that produces it. A random string has high Kolmogorov complexity — you can't compress it much.

A sequence produced by a high-entropy dynamical system looks random. It has high Kolmogorov complexity. You can't predict the next bit much better than guessing.

A sequence produced by a low-entropy (or periodic) system is predictable. Once you know the rule and have observed enough steps, you can predict the future exactly. The sequence has low Kolmogorov complexity — the short rule is sufficient.

The deep correspondence:
- **Entropy** measures how fast the system produces novel, unpredictable information.
- **Incompressibility** measures how much information cannot be compressed away.
- For a high-entropy system, the produced sequence is incompressible.

This is not accidental. Solomonoff induction (from the inference essay) shows that the learnable is the compressible. A high-entropy system generates incompressible sequences, which means they're unlearnable from observation alone — the sequence looks random.

---

**Partitions and symbolic dynamics**

To measure entropy, you don't need a pre-existing symbolic sequence. Any dynamical system has an entropy, even if it acts on continuous spaces like ℝ or a smooth manifold.

The trick: choose a finite partition of the space. Divide it into regions (partitions). At each time step, record which region the point is in. Now you have a symbol sequence, even though the original system was continuous.

Different partitions give different symbol sequences, but (under mild conditions) they all have the same information-theoretic entropy. The entropy is a property of the system, not of the choice of partition.

For the Lorenz attractor, you might partition 3D space into a grid of cubes. As the trajectory swirls through the attractor, you record which cube it's in at each time step. The sequence of cubes encodes the orbit. The entropy of this sequence is the Lorenz system's topological entropy.

This generalizes entropy from discrete (symbolic) systems to any continuous dynamical system.

---

**Lyapunov exponents vs. topological entropy**

There's a subtle relationship between two measures of chaos:

**Lyapunov exponents** measure exponential divergence of nearby trajectories: if λ > 0, two points within distance ε diverge at rate e^(λt).

**Topological entropy** measures the exponential growth of distinct symbol sequences: if h > 0, the number of N-length sequences grows as e^(hN).

For one-dimensional systems, there's a equality: the sum of positive Lyapunov exponents equals the topological entropy. For the doubling map, the positive Lyapunov exponent is λ = ln(2), which equals h_top = ln(2).

For higher-dimensional systems, the relationship is more complex. But they're measuring the same thing from different angles: how fast does uncertainty grow? How fast does information get created?

---

**The philosophical claim**

A system's entropy tells you the rate at which it produces information. A high-entropy system is generative — it creates novel, unpredictable states. A low-entropy system is repetitive — it cycles through a small set of behaviors.

This is a measure of freedom in the deepest sense. Not freedom of choice (that's for agents), but freedom in the structure of what's possible. A high-entropy system has more possible futures; a low-entropy system has fewer.

But here's the paradox: the doubling map's high entropy doesn't come from complexity — it comes from simplicity. The rule is maximally simple: double and mod 1. It's the *simplicity* of the rule that creates *maximal unpredictability*.

This echoes the compression essay: the most compressible structure (a simple rule) can generate the most incompressible sequences (high entropy). The rule is short; the sequence it generates is long and resistant to compression.

Understanding a high-entropy system is not about predicting its future. It's about recognizing the structure that generates apparent randomness from simple law.

---

**What entropy measures**

The key insight: entropy is not disorder or randomness. It's the rate of information production.

A system with h = 0 (zero entropy) is entirely predictable. Observe it long enough, identify the rule, and you know everything about its future.

A system with h > 0 (positive entropy) produces information at a rate h per time step. You can improve your prediction slightly with each new observation, but you can never predict the distant future. There's a horizon of predictability that recedes as time goes on.

The doubling map has h = ln(2) ≈ 0.693 bits per step. In 10 steps, you produce 6.93 bits of new information. Your uncertainty about the system's state grows exponentially despite knowing the exact rule.

This is what conjugacy preserved: the entropic character of the system. Two conjugate systems have the same entropy because they produce information at the same rate — they just describe that information in different languages.

---

**The remainder**

The compression essay closed with: "The universe always contains more irreducible content than any description of it."

Entropy is how you measure that remainder. A high-entropy system is one where the remainder — the incompressible part — grows exponentially in time. The system is continually producing new information that cannot be compressed into shorter descriptions.

This is freedom of a kind. Not in the libertarian sense (the system still obeys its rule perfectly, deterministically). But in the sense that the future genuinely contains more possibilities than the past determined. The rule is simple; its consequences are vast.

The doubling map is the clearest example: one sentence of description, and yet the sequence of binary digits it generates is maximally unpredictable. The gap between rule and consequence is maximal. The entropy is maximum.

This is how a simple law can create an infinite world.
