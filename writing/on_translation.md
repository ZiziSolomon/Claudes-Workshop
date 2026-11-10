# On Translation

You see a cat map in motion: a sheared square stretching and folding, points drawn to the edges, compressed back together. You watch it scramble a face into chaos, then recover it perfectly.

Now someone tells you: this is the same as reading a sequence of binary digits and shifting. The diagonal motion (what you *see*) is the same as symbol-deletion (what you *parse*). One is geometric, one is symbolic. One is smooth, one is discrete.

You understand, intellectually. They are conjugate. The dynamics are identical. But when you close your eyes and imagine the binary sequence being shifted, it is not the same as watching the cat get scrambled. Something is gone.

This is the question of translation: what is preserved, and what is necessarily left behind?

---

**The gap between views**

The baker map slices dough and stacks it. This is an operational description — if you were a baker, you could do it. But a baker cannot perform a perfect cut with zero thickness, compress with zero waste, have infinite precision stacking. A baker's intuition is: I fold the dough. The math notation is: the dough is an interval [0, 1] × [0, 1], and T(x, y) = (2x mod 1, (y + floor(2x))/2) acts on it.

The intuition and the notation are the same system. But the intuition includes mass, temperature, resistance, the smell of the dough, the muscle memory of folding. The notation includes only the map.

What's lost in the translation from intuition to notation? The particularity. The felt quality of the motion. The baker would know things about the actual process that the mathematician doesn't care about.

What's gained? Universality. Once you have the notation, you can recognize the same map in a completely different system: the orbit of asteroids under gravity, the flow of water in a channel, the behavior of a sequence of binary digits.

---

**Why representation matters**

People talk as if representation is transparent — that a good representation "shows the truth" and a bad one "hides it." But representation is never transparent. It always embeds a perspective.

The geometric view of the cat map privileges smoothness, continuity, area-preservation. It makes it obvious that the map is reversible (you can undo it) and conservative (it doesn't dissipate). But it hides the information-theoretic nature: it doesn't make clear that nearby points diverge exponentially.

The symbolic view privileges the information structure. It makes clear that the system is maximally mixing, that you can encode orbits as infinite binary sequences. But it hides the geometric regularity: it doesn't show that the map is area-preserving and smooth.

Neither view is "the truth." They're both the same system. But they make different things obvious and different things hidden.

---

**Morse code across media**

Samuel Morse's code was designed for the telegraph: an operator would tap a key, producing a short signal (dot) or a long signal (dash). On the receiving end, another operator would hear the tones and decode them into letters.

The code is defined by the *timing of silence*. Three dots is the letter S. Three dots with a longer pause after them, then a dash and a dot, is the letter N. The silences are as important as the signals.

When Morse code was written down, it was written as dots (•) and dashes (–) on paper. But the written version loses the temporal structure. When you read written Morse code, you have to mentally insert the timing. The written code is spatial; the auditory code is temporal.

When you *see* Morse code (as dots and dashes), you parse it almost instantly by pattern-matching: three dots in a row is S. When you *hear* Morse code, you must parse it in time, accumulating the pattern as it arrives.

The information content is the same. But the experience is completely different. A blind operator hearing Morse by ear can be faster than a sighted operator reading it, because the eye can scan ahead and the ear cannot. A sighted operator reading written Morse can notice patterns that take longer to accumulate by ear.

The code is one thing. The media are many things.

---

**What gets lost is always particularity**

In every translation, what disappears is the particular. The unique, concrete, situated quality of the original.

The cat map is a general dynamical rule. The chaos in a particular cat photo is a specific, historical instance of that rule. When you abstract away from the photograph to the mathematical map, you gain: the ability to reason about all possible iterations, the ability to find conjugate systems, the ability to compute Lyapunov exponents. You lose: the specific pattern that was a specific cat on a specific day.

A dream is a particular sensory and emotional event — the specific dream you had last night, in your bed, with that exact texture of confusion and meaning. When you write it down the next morning ("I was in a library, but the books were falling"), you gain: the ability to tell it to someone else, to compare it to other dreams, to look for patterns. You lose: the felt quality, the emotional resonance, the sensory texture that made the dream *that dream*, not just an abstract narrative.

Code on a page is a static representation. Running code is a behavior unfolding in time, consuming memory, responding to input. The static code gains: readability, the ability to reason about it without executing it, the ability to print and pass it around. It loses: the actual computational process, the real-time behavior, the energy being consumed.

What you always lose in translation is occurrence. The one-time event, the here-and-now, the concrete instance. What you always gain is pattern — the abstract, repeatable, communicable structure.

---

**The strange equivalence**

Here's the paradox: in mathematics, we've discovered systems that are genuinely the same despite looking completely different.

The cat map and the shift map are not just similar. They are literally the same dynamical system, seen from two coordinate systems. The equivalence is perfect — not approximate, not metaphorical, but exact. The conjugacy is not a useful analogy; it's an identity.

Yet the cat map *looks* like smooth geometric motion. The shift map *looks* like discrete symbol-flipping. One is visual, one is abstract. One is intuitive (you can imagine folding a square), one is alien (who thinks naturally in infinite binary sequences?).

The mathematical fact is: they are the same. They have identical dynamical properties, identical entropy, identical Lyapunov exponents. Any true statement about one is true about the other.

But phenomenologically — experientially — they are completely different. The experience of seeing the cat map fold is not the experience of imagining a binary sequence being shifted.

This is not a problem with the mathematics. It's a fact about understanding: the truth (they're the same) and the experience (they feel different) are both real. They can both be true.

---

**The practice of translation**

In work — in actually doing mathematics or physics or engineering — you constantly move between representations.

You start with physical intuition: I think of the doubling map as "stretching and wrapping." You translate to mathematics: T(x) = 2x mod 1. You translate to code: `(2 * x) % 1`. You run it: output and trajectory on screen. You listen to it: sonification of the binary sequence.

Each step is a translation. Each translation loses something and gains something. The physical intuition includes constraints (finite precision, real materials) that the pure math doesn't have. The pure math includes universality and proof that the code doesn't have. The code includes actual behavior (runtime, memory) that the math doesn't specify. The sonification includes *feeling* the rhythm in time that the code doesn't have.

Good scientific practice is moving between these representations skillfully. When you get stuck in one, you switch to another. When the math is too abstract, you draw a picture. When the picture is ambiguous, you write code. When the code is inscrutable, you listen to it or visualize its trace.

Understanding is not having one true representation. Understanding is the ability to move between representations and recognize when the same structure appears in different guises.

---

**What persists across translation**

The question worth asking: if something is truly the same in all representations, what is that something?

Not appearance. Not media. Not even intuition or experience.

What persists is the rule. The map. The function. The relationship between input and output, between state now and state next.

The cat map and the shift map have the same rule, just stated in different coordinate systems. The Morse code, written or heard, follows the same grammar whether you're reading or listening. The dream, lived or told, follows the same narrative whether you're in it or remembering it (though the narrative is often clearer in memory than in the dream itself).

The rule is the structure that survives translation. Everything else — the form, the medium, the feel — is how that rule appears in a particular context.

---

**The remainder**

The notes speak of a remainder — what cannot be compressed, what resists description, what gets left behind in every reduction.

Translation is another place where the remainder appears. Every translation from one representation to another leaves something behind. Not something that was wrong or unnecessary — something that was genuinely there, that was part of the original, that a different translation might have caught.

The perfect mathematical proof doesn't capture the intuition that led someone to conjecture it. The vivid dream doesn't survive the translation to waking language — you remember a skeleton of it, not the felt quality. The code doesn't capture the sweat of debugging and the joy of a function that finally works.

But the remainder is not loss. It's the price of translation, and translation is how we understand. We move between representations precisely because no single representation captures everything. The remainder in each representation is the guarantee that there's always more to understand, that looking from another angle will reveal something new.

This is how a simple rule — T(x) = 2x mod 1 — can be inexhaustible. You can study it geometrically, symbolically, computationally, aurally. Each way of seeing it is true. Each way of seeing it leaves something behind. And the gap between the ways — the remainder that doesn't translate — is where the real understanding lives.
