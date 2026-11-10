# On Conjugacy

Two things look completely different. One is a chaotic swirl of points in a square, one is a sequence of binary digits, one is dough being folded and stretched. They look like three entirely separate phenomena. But ask the right question — how do points move? What rule governs the next step? — and you discover they are the same. The same dynamics, three different views. One system in disguise.

This is conjugacy: the structure of sameness underneath the appearance of difference.

---

**What does it mean for two things to be "the same"?**

Identity is obvious at first and mysterious on reflection. Two copies of a book are the same book in an obvious sense — same text, same binding. Two people who have identical DNA are the same genetically, different in every other way. Two pieces of music in different keys are the same song, or different songs — it depends on what you care about.

In dynamics, the question sharpens. You have a system that evolves in time: a map, a flow, a process of change. Two different systems might evolve according to the same underlying rule. The surface looks different, but the shape of the change is identical.

Consider two different spaces:
- A square [0,1) × [0,1) with a map T(x, y) = (2x mod 1, (y + floor(2x))/2) — the baker transformation, which stretches, cuts, and stacks.
- An infinite sequence of binary digits: 0, 1, 0, 1, 1, 0, 1, ... with a map S(d₀, d₁, d₂, ...) = (d₁, d₂, d₃, ...) — the shift map, which deletes the first digit.

These are different spaces. One is a geometric object, one is purely symbolic. The transformations look completely unrelated. But there exists a map between them: read the first coordinate x as a binary decimal 0.d₀d₁d₂... — the binary expansion of x. Under this reading, evolving the baker map on (x, y) corresponds exactly to evolving the shift map on the binary sequence.

Not just similar. Exact correspondence. The dynamics are conjugate.

---

**The definition**

Formally: two dynamical systems (X, T) and (Y, S) are **conjugate** if there exists a homeomorphism φ: X → Y such that the following diagram commutes:

```
X → T → X
↓φ    φ↓
Y → S → Y
```

In other words, φ ∘ T = S ∘ φ. You can either (1) apply T in the original space then map to Y, or (2) map to Y then apply S, and you get the same result.

What this means: the map φ is a relabeling of points. It's a translation from one language to another. When you apply T in the original space and then translate, you get the same result as if you had translated first and then applied S.

The transformation T in the X-space is invisible from the Y-space perspective. The structure of change is identical. The two spaces are coordinatizations of the same dynamics.

---

**Topological conjugacy vs. measure-theoretic conjugacy**

There's a choice in how strict you want to be about the correspondence.

**Topological conjugacy** requires φ to be a continuous bijection with continuous inverse — a homeomorphism. This preserves the geometric structure, the notion of "closeness." If you're nearby in X, you're nearby in Y after the map.

**Measure-theoretic conjugacy** (or ergodic conjugacy) is weaker. It requires the correspondence to work almost everywhere with respect to some measure. You can ignore a set of measure zero. This is closer to "the same dynamics" in a probabilistic sense — ignoring rare events.

The distinction matters. Two systems can be topologically conjugate but fail to be ergodically conjugate, or vice versa (though less commonly). The stronger condition (topological) requires you to preserve geometry. The weaker condition (measure-theoretic) requires you to preserve statistics.

For most of what follows, topological conjugacy is the stronger interesting case: if two systems are topologically conjugate, not only do they have the same long-term behavior, but they look geometrically similar at every scale.

---

**Why conjugacy matters**

Conjugacy is how classification works in dynamical systems.

If you can find a homeomorphism φ between two systems, you know they are the same system. Anything true about one is true about the other — you just have to translate the language.

But certain properties are even more universal. **Conjugacy-invariant** properties are things that don't depend on φ at all. They're true for both systems if they're true for either.

Examples:
- **Topological entropy**: a measure of how much the system scrambles nearby points. Conjugate systems have the same entropy.
- **Lyapunov exponents**: a measure of exponential divergence of nearby trajectories. Conjugate systems have the same spectrum of exponents.
- **Period structure**: the set of periodic points and their periods. Conjugate systems have isomorphic period structures.

These are the *true* invariants of a system — the properties that survive no matter how you relabel the space.

---

**The baker map and the shift map**

The baker transformation and the shift map are the canonical example. They are topologically conjugate.

The baker map T(x, y) = (2x mod 1, (y + floor(2x))/2) acts on a square: it stretches the square horizontally (doubling x-width), compresses it vertically (halving y-width), then cuts it in half and stacks one half on top of the other. The effect is a churning, smearing motion — the baker's dough.

The shift map S(d₀, d₁, d₂, ...) = (d₁, d₂, ...) acts on infinite binary sequences: it erases the first digit and shifts everything left.

The conjugacy φ reads the first coordinate x as a binary decimal: φ(x, y) = (x, y) but where x is interpreted as the binary string 0.d₀d₁d₂d₃... and the evolution of this binary string under the shift map corresponds exactly to the evolution of the first coordinate of the baker map.

What's remarkable: the shift map is one of the simplest possible dynamics (just erase the first symbol), yet when conjugated back to the geometric space, it produces the complex visual pattern of dough-stretching. The appearance of complexity is an artifact of the representation.

---

**The cat map and its disguises**

The cat map is even more striking. T(x, y) = (x + y, x + 2y) mod 1 acts on a square. The name comes from the classical image: apply the map repeatedly to a photograph of a cat, and the cat gets sheared and scrambled into chaos, then eventually returns to the original (since the square has finite area and the map is area-preserving).

The cat map is conjugate to a shift on a sequence of symbols. The conjugacy is less obvious than for the baker map — it requires understanding the eigenvectors and eigenvalues of the 2×2 matrix and doing a change of coordinates — but it exists. Under the right relabeling, the cat map is conjugate to a symbolic shift.

And here's the philosophical turn: the cat map looks like smooth geometric dynamics — a linear transformation that preserves area. The shift map looks like discrete symbol-flipping. They're conjugate. Same system, different languages.

The cat map teaches you that what looks like smooth, continuous chaos is, from another perspective, discrete symbol manipulation. The chaos is not hidden in complex geometry — the geometry of chaos is the visible form of symbol scrambling.

---

**What persists in conjugacy? What doesn't?**

Conjugacy preserves the dynamics but not the geometry. Geometry is optional.

If two systems are conjugate, they have:
- The same set of periodic orbits and periods.
- The same topological entropy.
- The same Lyapunov exponents.
- The same recurrence behavior (if a point returns to close to itself, the other system has the same recurrence rate).

If two systems are conjugate, they do NOT necessarily have:
- The same shape. The cat map looks like a sheared parallelogram; the shift map looks like discrete. The baker map looks like cutting and stacking; the shift map looks like erasing.
- The same continuity structure. The shift map is discontinuous; the cat map is smooth.
- The same dimensionality in the geometric representation. You can conjugate a 2D system to a 1D symbolic space or vice versa.

What's preserved is **structure under iteration**. What's lost is **shape, appearance, geometry**.

This is the profound observation: the essence of a dynamical system is not visual. It's the rule of change. Different geometries can harbor the same rule.

---

**The conjugacy hierarchy**

Not all systems are conjugate to a shift. Shifts are special — they're Bernoulli systems, the most "mixing" or "random-looking" dynamics. Most systems are more constrained.

There's a hierarchy:
- **Bernoulli systems**: conjugate to a shift of a finite alphabet. Maximally mixing.
- **K-systems** (Kolmogorov-mixing): weaker than Bernoulli. Ergodic and mixing but not Bernoulli.
- **Mixing systems**: weaker still. The mixing condition alone doesn't pin down the structure.
- **Ergodic systems**: weakest. Weaker than mixing.

At each level, you're asking "how much structure remains invariant?" A Bernoulli system is conjugate to a shift — you can fully understand it by symbol-reading. A K-system is not Bernoulli, but it still has a lot of mixing. An ergodic system might have arbitrarily complicated structure beneath the surface.

---

**The conjugacy question in error tolerance**

The earlier essay on error tolerance raised this: when are two codes the "same"?

Morse code and the genetic code look completely different. Morse has boundary artifacts (gaps between symbols). The genetic code has third-position redundancy (silent mutations). One is fragile to errors at boundaries; the other is robust everywhere.

But is there a sense in which they're conjugate? Could there be a relabeling under which they're the same?

The answer is no — not topologically. They're not even close. But they're solving the same *problem*: how to encode information robustly when errors occur. They solve it in opposite ways (Morse optimizes for average case, genetic code for worst case), but they're both optimal solutions to the error-tolerance problem.

This is weaker than conjugacy. It's something like: same problem, different representations, both optimal. Not the same system, but the same solution space.

---

**The philosophical claim**

Conjugacy reveals that what we think of as the "true" nature of a system is just one representation of it. The cat map's smooth shearing-rotation, the baker map's cutting-and-stacking, the shift map's symbol-erasing — these are the same system seen three ways.

Which view is "correct"? All of them. Each view makes something obvious:
- The geometric view shows that the system is area-preserving, symmetric, smooth.
- The shift view shows that the system is maximally mixing, that trajectories are determined by binary sequences, that it's as "random" as possible.
- The baker view shows the physical mechanism (stretching and cutting) that might apply to an actual material system.

None is more true than the others. They're conjugate representations of the same rule.

This changes how you think about understanding. Understanding is not discovering the "true" representation — it's finding multiple representations that illuminate different aspects. The system is not the cat map, not the shift, not the baker transformation. The system is the conjugacy class of all three together. The system is the structure that's invariant across all representations.

---

**What structure is precious?**

The notes that frame this series ask: "When are two systems the same system in disguise?" The answer is: when they're conjugate. When one can be relabeled to look exactly like the other, step by step.

But the deeper observation: conjugacy is rare. Most systems are not conjugate to simple things. Most dynamics cannot be reduced to a clean shift map or a simple geometric rule.

What conjugacy tells you is this: the structure that matters is the structure that survives conjugation. Not the appearance, not the coordinate system, not whether you see it as smooth or symbolic. The structure that survives is the answer to: "How do points move relative to each other? How do nearby points diverge? What set of patterns is invariant under the map?"

This is close to the theme of the earlier essays on compression and invariance. Compression asks: what can you leave out? Invariance asks: what persists? Conjugacy asks: what structures look the same from every angle?

The answer in all three cases is the same: the structure that resists erasure, that appears in every representation, that cannot be compressed away.

That's what's precious. That's what's real.
