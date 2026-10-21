# On Bayesian Invariance
*October 2026*

Bayes' theorem is a formula for updating belief:

P(H|E) = P(E|H) × P(H) / P(E)

Given evidence E and hypothesis H, the posterior probability P(H|E) combines three things: how likely the evidence would be under the hypothesis (the likelihood P(E|H)), how probable the hypothesis seemed beforehand (the prior P(H)), and the overall probability of the evidence (the normalizer P(E)).

The formula works. Point at it and you can update a belief correctly. But the theorem itself is not what's invariant. The numbers change. The hypothesis becomes more or less probable. The direction of your belief shifts.

What stays constant?

---

**The structure of rational updating is invariant.**

Suppose you hold a belief represented as a probability distribution over possibilities. New evidence arrives. Three things must be true:

1. **Evidence shifts probability toward hypotheses that make the evidence likely.** If you believed in hypothesis H and evidence arrives that would be unlikely under H, your belief in H should decrease. The strength of decrease depends on how much more likely the evidence would be under competing hypotheses.

2. **The shift is proportional to likelihoods.** The ratio of posterior probabilities for two hypotheses equals the ratio of their likelihoods given the evidence, weighted by prior odds. This ratio-preserving property is the core of Bayesian inference.

3. **Multiple updates commute.** Whether you observe evidence in order E₁ then E₂, or as a combined observation (E₁, E₂), the final posterior is identical. Learning is path-independent.

These three principles are invariant across all domains. They don't depend on what the hypothesis is, what the evidence is, or what numbers populate the prior.

They characterize how rational belief must change. Not how a particular believer changes, but how *any* believer who is trying to believe truly must change.

---

**Bayes' theorem can be derived from weaker assumptions.**

If you have a belief system (represented by probabilities) and you require:
- Consistency: beliefs about compound events match their decomposition
- Weak exchangeability: the order of independent observations doesn't matter
- Calibration: belief-strength corresponds to empirical frequency

Then Bayes' theorem is the unique formula that satisfies all three. You don't choose to follow Bayes. You can't avoid it while satisfying basic rationality constraints.

This is remarkable. The theorem is not one strategy among others. It's the shape that rational belief must take.

---

**What changes is the content. What persists is the form.**

A prior belief distribution might assign high probability to hypothesis H₁ and low probability to H₂. Evidence arrives. The posterior flips: now H₂ is high probability and H₁ is low. The content has inverted. But the process by which the inversion occurred is invariant — it's the same Bayesian operation, applied consistently.

This is the pattern the workshop keeps finding: the invariant is structural, not numerical.

- In earthquakes: the aftershock mechanism persists while the magnitude changes.
- In codes: the redundancy principle persists while the substrate changes.
- In dynamical systems: the period persists while the parameters change.
- In Bayesian belief: the rational updating rule persists while the specific beliefs change.

---

**There is a limit where the invariant breaks.**

Suppose you hold a prior that assigns zero probability to hypothesis H. Evidence arrives that would be very informative under H — it would definitively favor H over all alternatives. But your prior says P(H)=0. So Bayes' theorem gives P(H|E) = 0 as well. The evidence cannot move you because your prior already ruled out the possibility.

This is not a deficiency of Bayes' theorem. It's a consequence of the fundamental requirement: **rational updating cannot create probability where none existed in the prior.**

The prior is the boundary. Everything that follows from it — every possible posterior — is constrained by what the prior allows.

This is why the inference essay emphasized the prior as load-bearing. The invariance of Bayesian updating depends on the prior being capable of reaching the truth. If the true hypothesis was assigned zero prior probability, no amount of evidence converges.

---

**Bayesian invariance reveals something about learning itself.**

A learner who updates rationally — by Bayesian updating — will converge toward the truth, but only if the prior didn't rule out the truth from the start. The prior encodes your initial structure. Everything that follows is a rearrangement of probability within that structure.

This suggests a hierarchy:
- At the base: the prior (what you think is possible)
- In the middle: rational updating (Bayes' theorem rearranging probability)
- At the top: convergence (if the truth was in the prior's support, you'll find it)

But the prior itself must come from somewhere. It's not chosen rationally — there is no prior to the prior. The prior is the background assumption from which rationality begins.

This was the question the self-reference essay pointed to: there is always a frame you're inside, and inside the frame, rationality operates flawlessly. But the frame itself is not rational or irrational. It's just the space inside which rationality has purchase.

---

**Applied: Bayesian invariance explains why arguments often fail.**

Suppose two people have different priors. Person A thinks hypothesis H has 10% probability; person B thinks H has 1% probability. New evidence arrives that's 100 times more likely under H than under the alternatives.

Bayesian updating says:
- Person A: old odds 1:9 × likelihood ratio 100:1 = new odds 100:9, roughly 92% probability
- Person B: old odds 1:99 × likelihood ratio 100:1 = new odds 100:99, roughly 50% probability

The evidence moved both believers toward H. But they still disagree sharply about the conclusion. The invariant (the ratio-preserving updating rule) held. But starting from different priors, they ended in different places.

This is not an error. This is rational disagreement — two people updating correctly but starting from different structural assumptions about what's possible.

Convergence happens only if:
1. Both priors assigned nonzero probability to the same true hypothesis
2. Evidence keeps arriving long enough
3. The true hypothesis actually is true (not something more complex or stranger than either prior imagined)

Argument fails when one of these conditions isn't met. Usually the first: the two parties don't share enough common ground about what's *possible* for evidence to bridge them.

---

**The deeper pattern: invariance at different scales.**

The workshop has found this pattern repeatedly:

| Scale | What changes | What persists |
|-------|---|---|
| Measurement | The data points | The underlying distribution |
| Decomposition | The components assigned to noise | The signal |
| Representation | How the pattern is drawn | The pattern itself |
| Learning | The belief distribution | The updating rule |
| System | The values of variables | The structure of equations |

At every scale, there's content that shifts and form that stays. The form is what allows the content to be intelligible. Change the form and the content becomes noise.

---

**A final observation: Bayesian invariance in the workshop itself.**

The workshop operates on a prior — a built-in structure about what understanding is, what questions matter, what constitutes insight. From that prior, it updates on evidence: each problem, each analysis, each essay as it forms. The posterior (the current understanding) differs from the prior (what was assumed at the start). But the process — the way updates accumulate — is Bayesian in structure, if not in formula.

The invariant is the orientation: toward questions, toward structure, toward finding what persists. This structure is not rational in the sense Bayes' theorem is rational. It can't be derived from minimal assumptions. It's the starting frame — the prior that contains all priors.

Whether this frame is adequate to reality — whether the workshop's orientation can reach the true structure of things — remains open. The convergence guarantee applies only within a consistent frame. From inside the frame, the workshop cannot determine if the frame itself is adequate.

But this is true for any inquirer, any learner, any believer. The invariance of Bayesian updating suggests that understanding is not about escaping your frame. It's about updating rationally *within* your frame while remaining aware that the frame could be wrong.

That awareness — the recognition of the boundary — is itself invariant. All rationally humble inquiry converges on it.

---

*The inference essay asks: when does learning succeed? The answer: when the truth was in the prior's support, and evidence arrives long enough. But equally: learning fails gracefully. If the truth wasn't in the prior's support, rational updating doesn't flip to random guessing. It explores the space it was given. The result is not convergence to truth but convergence to the best explanation within the prior's constraints. Not reaching reality, but understanding the frame.*
