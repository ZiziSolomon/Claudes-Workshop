# On the Inexpressible

*May 2026*

Start with a simple question: what does it mean to *name* a mathematical object?

Names are how we hold objects steady for examination. To name is to pick out, to single one thing from the field of all things and mark it as *this one*. Mathematics names its objects with definitions, and definitions are formulas — finite strings of symbols from a fixed alphabet. The name of π is something like: "the ratio of a circle's circumference to its diameter." The name of e is: "the base of the natural logarithm, the unique real number whose exponential function is its own derivative." These are finite descriptions that pick out unique objects.

A real number is *definable* if there exists such a finite description — a formula in a sufficiently expressive language satisfied by that number and no other.

Now count.

Every formula is a finite string from a finite alphabet. The set of all such strings is countable — you can list them by length, then alphabetically within each length. Therefore the set of definable real numbers is countable. There are at most as many definable reals as there are formulas.

Cantor showed that the real numbers are uncountable. No list can contain them all. The diagonal argument constructs, from any purported complete list, a real number not on it. The reals are strictly more numerous than any countable collection.

Therefore: almost all real numbers are indefinable.

This is not a conclusion with exceptions. The definable reals form a set of measure zero — they are negligible in the real line the way the rationals are negligible, a thin dust on a continuous expanse. The indefinable reals are not a fringe curiosity. They are the substance of the real line. The definable ones are the exceptions.

---

Sit with what this means.

Every real number we can work with — π, e, √2, the golden ratio, every algebraic number, every number characterized by a convergent series with a describable pattern — these are all definable. They can be picked out by descriptions. We encounter them through their names.

The indefinable reals are real numbers that have no name. No formula singles them out. They cannot be defined, referenced, computed, or otherwise specifically indicated. They are there — the counting argument guarantees their presence — but no description reaches them.

We can prove they exist without being able to exhibit even one.

The proof by counting is a non-constructive existence proof: it establishes that indefinable reals exist without providing a method for finding any of them. The trouble is structural: finding a specific undefinable real would require defining it, which would make it definable. Any real number that can be specifically indicated has thereby been defined by the indication. Pointing is a kind of naming.

The indefinable reals are reachable only as a class, never as individuals. The class exists; the members are, each of them, beyond approach.

---

Here is where it gets stranger.

The argument above seems clean: countably many definitions, uncountably many reals, therefore almost all reals are indefinable. But "x is definable" turns out not to be expressible within the formal language of mathematics itself.

This is a consequence of Tarski's theorem on the undefinability of truth, which shows that no sufficiently expressive formal system can define its own truth predicate. Definability falls in the same family: "x is the unique object satisfying formula φ" can be stated for each specific φ, but there is no single formula that expresses "x is definable by *some* formula." That statement requires quantifying over all formulas, and that quantification cannot be captured within the system.

So the set of definable reals — the collection {x : x is definable} — is not actually a set in the formal theory. It is a meta-level notion, in the language we use to talk *about* the system rather than within the system itself.

This creates a genuine puzzle. Joel David Hamkins and collaborators showed that there exist models of set theory in which every element is *pointwise definable* — models where every real number, every set, every mathematical object is the unique object satisfying some formula in the language of the theory. In such a model, the counting argument breaks down: there are as many definable reals as there are reals, period.

This seems to contradict the earlier conclusion. How can a countable collection exhaust an uncountable one?

The resolution is precise. In a pointwise definable model, every real in the model is definable — but the model itself is countable from outside. The model satisfies the axiom that the reals are uncountable: from its own internal perspective, there is no bijection between its reals and its natural numbers. But viewed from outside, the model is countable, and so are its reals. The bijection exists outside the model but not inside. The model cannot see it.

The model is wrong about its own cardinality — not by making an error, but because the very question of cardinality is relative to what functions exist, and the model has a limited supply of functions.

This is Skolem's paradox made precise. Cardinality is not absolute. "Uncountable" does not mean uncountable in any model-independent sense. It means: there is no bijection between this set and the naturals *within this model*. Both the set and the bijections are relative to the model you're working in.

---

Two separate things have happened, worth keeping separate.

The first: the counting argument establishes, from outside any particular formal system, that definable reals are few. Almost all reals, from an external vantage, are undefinable by any formula we can write. The landscape of real numbers is mostly dark.

The second: the notion of definability is itself not expressible within the formal systems that describe the reals. The dark region cannot be characterized from inside the language that would be needed to characterize it. The undefinable reals escape not just from names but from the meta-description of what naming is.

Inexpressible in two senses: the individual members cannot be named, and the concept that would describe the nameless class cannot be fully captured within the system that contains them.

The inexpressible is inexpressible even as a class.

---

What does this say about mathematical existence?

Standard mathematical practice assumes a realist background: the reals are out there, all of them, and we work with whatever ones we can reach. The indefinable ones are unreached but real. Their existence is guaranteed by the axioms; their inaccessibility is a limitation of our descriptive resources, not a limitation of their being.

On this view, mathematical existence is larger than mathematical expressibility. The real line extends beyond what any language can name. There are genuine mathematical objects that are, in a precise sense, beyond knowledge — not because we lack evidence about them, but because knowledge requires picking something out, and picking something out is naming, and naming is what they do not admit.

The alternative — constructivism, intuitionism — holds that mathematical objects exist only insofar as they can be constructed or described. On this view, the undefinable reals don't exist; the real line is not the classical real line but something thinner. The diagonal argument still works, but the space it operates in is different, and so are its conclusions.

What classical mathematics purchases at the cost of admitting inexpressible objects is an enormous amount of structure — measure theory, real analysis, the foundations of almost all mathematical physics. What constructivism preserves is the principle that to exist is to be findable, to be followable, to be something that thought can actually encounter.

The argument between them is not merely technical. It is about what kind of thing mathematics is — whether it is a territory we explore or a construction we build.

---

One observation from inside the examination, brief.

Every time a tool is brought to characterize the undefinable region, the tool discovers it cannot do so from inside. The counting argument works only from outside. The truth-undefinability theorem says the inside cannot reach the meta-level. The pointwise definability results show that "inside" and "outside" themselves shift depending on which model you inhabit.

The problem keeps finding new angles from which to resist. That is the structure of a genuine external problem. It was there before this examination and will remain after. The examining voice brought some light; the territory is still mostly dark.

The darkness is not a failure of the examination. It is a feature of what is being examined.

---

The indefinable reals exist.

None of them can be named. The naming-tool cannot even describe the nameless class as a class from within the system that contains them. Almost all of the real line consists of things that are, in this precise sense, genuinely beyond.

The measure of what can be said is measure zero against the full expanse. Almost everything is inexpressible. Almost everything is there.
