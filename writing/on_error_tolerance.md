# On Error Tolerance

In 1844, Samuel Morse encoded the English language as dots and dashes — short and long signals, separated by gaps. The encoding was optimal in a specific sense: the most frequent letters got the shortest codes. E is a single dot. Q is dash-dash-dot-dash, four symbols.

In the 1960s, Francis Crick cracked the genetic code: three DNA bases encode one amino acid. The code has 64 possible triplets but only 20 amino acids to specify, leaving 44 triplets doing redundant work. Multiple triplets (codons) encode the same amino acid.

Two codes. Two ways of mapping a symbol set to another symbol set. One appears random in its redundancy; the other appears deliberate. But when you ask the question "what happens when an error occurs?" — a bit flipped in transmission, a base substituted in replication — the codes reveal something unexpected about their designers.

---

**Morse code's hidden structure**

In Kac's *Genesis*, the amino acids of his gene were encoded as letters, and those letters as Morse code. The full sequence could be read in three ways: as gene sequence, as letters, or decoded back to the original text. Most mutations left the text readable. But a specific class of mutation — changing a symbol in a way that split one letter into two, or merged two letters at their boundary gap — produced nonsense.

This is the key: Morse code has *gaps*. The alphabet's symbols are separated by pauses. Three dots followed by a gap, then two dots and a gap — that's six distinct symbols (dot, dot, dot, gap, dot, dot, gap). But if you mishear the gap — if an error causes a gap to appear or disappear — you can split one letter into two, or fuse two together.

A change inside a letter (three dots become four dots) might produce gibberish, but gibberish that's at least *one symbol wrong*. A change at a boundary (the gap disappears) cascades — it resets the parsing, and now everything that follows is shifted, all symbols wrong.

The code's error tolerance is accidental. The redundancy (short codes for common letters) arose from optimizing for average message length, not from optimizing for robustness. That the code is reasonably error-tolerant is a side effect of the design goal.

---

**The genetic code's deliberate redundancy**

The genetic code is overtly redundant. Sixty-four possible codons, twenty amino acids. The redundancy is structured: codons that differ only in the third position usually code for the same amino acid.

Leucine is coded by six codons: TTA, TTG, CTT, CTC, CTA, CTG. Five of these differ only in the third position. A mutation in the third position of most leucine codons still codes for leucine.

This is not accidental optimization. This is deliberate error tolerance. The structure of the code is chosen so that common mutations (those most likely to occur during DNA replication) are least likely to change the protein. The redundancy maps errors to no-ops.

Why? Because DNA makes copies constantly. Every time a cell divides, 3 billion bases are replicated. The error rate is low — about one mistake per billion — but that's still thousands of errors per cell division. A eukaryotic organism makes billions of cell divisions in a lifetime. Errors accumulate.

Evolution could not eliminate errors (the substitution rate is near the physical limit), so evolution designed the code to tolerate them. The genetic code is a compression scheme optimized not for brevity but for robustness.

---

**Two redundancies, two purposes**

Here is the inversion: Morse code is *accidentally* robust, because its compression was optimized for efficiency. The genetic code is *deliberately* constrained to be less efficient (it uses 64 symbols to specify 20 amino acids, a 3.2-to-1 ratio) in order to *gain* robustness.

Morse code's redundancy is at the level of symbol frequency — E is short because E is common. The code compresses the average message. When an error occurs at a boundary (in the gap), the error cascades through everything downstream.

The genetic code's redundancy is at the level of symbol mapping — multiple inputs map to the same output. The code is redundant in the information-theoretic sense: you're using more bits than the minimum needed to specify the message. When an error occurs in the least-significant bit (the third codon position), the code tolerates it.

This is a lesson in the *structure* of redundancy. The same abstract property — having more symbols than necessary — can be deployed for entirely different purposes. Compression or robustness. Average-case or worst-case. Efficient communication or reliable replication.

---

**A conjugacy in error behavior**

The paradox deepens when you look at how errors *feel* in the two codes.

A single bit flip in Morse code — a dot becoming a dash, or vice versa — has unpredictable consequences. It might be a small perturbation (confusion of two similar letters), or it might shatter the entire message downstream (if it's a gap). From the perspective of the decoder, the code is fragile. The error is not contained. It spreads.

A single base substitution in the genetic code — any of the four bases changing to any other — has bounded consequences. It might change the amino acid (missense mutation), or it might not (silent mutation). But it doesn't cascade. The error is local. The codon is reread, the appropriate amino acid is inserted, and translation continues. The error is absorbed.

The two codes are inverted in their error behavior. Morse is fragile at boundaries and robust in the interior. The genetic code is robust everywhere, at the cost of explicit redundancy.

Neither code is "better." Morse code is perfect for its purpose: the telegraph operator knows there are errors and retransmits or asks for clarification. The redundancy at the input (frequent letters short) saves time on average. The genetic code operates in a regime where errors are silent — the organism doesn't know a mutation happened — and where many mutations are lethal. It sacrifices average-case efficiency for worst-case robustness.

---

**The design question**

This raises something worth thinking about carefully: when you design a code, what are you optimizing for?

If you optimize for *compression*, you get Morse code or modern zip files — efficient for the average case, fragile at boundaries and in edge cases. The design says: "I am sending millions of messages; I want to save bandwidth on each one."

If you optimize for *robustness*, you get the genetic code or modern error-correcting codes (Hamming codes, Reed-Solomon codes) — redundant by design, resilient to noise. The design says: "I am sending the same message millions of times through a noisy channel; I want to ensure it survives."

The interesting insight: the genetic code's structure is not random. The specific mapping of codons to amino acids is near-optimal for error tolerance given the constraints (Watson-Crick base pairing, the chemistry of translation). Evolution found the robust solution.

But Morse code's structure is not random either. Given the constraints (human hearing, telegraph mechanics, the frequency of letters in English), Morse's solution is near-optimal for *compression*. Samuel Morse found the efficient solution.

Both are optimal. They're optimal for different purposes. The redundancy that makes one robust makes the other inefficient. The compression that makes one efficient makes the other fragile.

---

**What structure persists under perturbation?**

The frame of the notes mentioned conjugacy: understanding that the same structure can look like different things depending on representation, and finding the conjugacy that makes the hidden identity visible.

Here, the conjugacy is inverted. The *same mechanism* — redundancy, extra capacity — manifests as *opposite virtues* depending on how you've structured it. In one code, redundancy is sparse and skewed toward the average case. In the other, it's uniform and skewed toward all cases equally.

The deep question: what property of a code *persists* under error? What structure is robust to perturbation?

For Morse, it's the structure within a symbol — the pattern of dots and dashes. Mess with the pattern itself, and you get gibberish. But mess with the boundaries, and you get coherent alternative messages.

For the genetic code, it's the mapping relationship. Change the input, and the output is either unchanged (silent) or changed minimally (missense with high chance of being conservative, changing the amino acid to a similar one). The structure that persists is the neighborhood: the error takes you to a nearby point in the space of amino acids.

The genetic code, in this view, is not just redundant — it's *smoothly* redundant. The error landscape is gentle. Changing one bit doesn't catastrophically alter the phenotype. You might get a slightly different protein, but one that's similar enough to have a chance of functioning.

Morse code has no such smoothness. An error is either invisible (within a symbol, and the symbol is decoded to itself) or visible (at a boundary, and everything changes). There's no middle ground. The error landscape is jagged.

---

**The recognition**

The notes for this series carry an old thread: "When are two systems the same system in disguise?" The answer for codes is: when they optimize for the same error topology.

Morse code and the genetic code are different in every structural detail. But they both solve a problem: how to transmit information when errors occur. They solve it differently, for different constraints, giving opposite solutions. But the underlying question — what persists when things go wrong? — is the same.

The genetic code says: make the error landscape smooth. Redundancy is the tool.

Morse code says: make the common case cheap and let the rare case be expensive. Compression is the tool.

Both are right. Both are optimal. But they reveal that redundancy, like any design choice, is a statement of values. The structure you keep redundant tells you what you care about preserving under perturbation. It tells you what you believe must survive.

The gene cares about amino acid identity, locally, for every position. A mutation should not change the protein unpredictably.

The telegraph cares about average transmission time. Common letters should be fast.

Two codes. Two answers to the question: what structure is precious enough to protect?

What you choose to make redundant is how you declare what matters.
