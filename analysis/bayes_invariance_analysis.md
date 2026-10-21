# Bayesian Invariance: A case study in finding what persists

The Bayesian inference framework reveals another domain where the workshop's unifying principle applies:

**Understanding = Finding what doesn't change under transformation**

## The disease testing case

Consider the classic problem: A medical test is 95% sensitive (detects disease when present) and 95% specific (correctly shows negative when absent). You test positive. What's the probability you have the disease?

The naive answer: 95% (the test accuracy).
The correct answer: **It depends on the prior.**

With 1% disease prevalence → posterior is 16.1% (not 95%!)
With 5% disease prevalence → posterior is 49.2%
With 50% disease prevalence → posterior is 95%

## What's invariant

The **likelihood ratio** remains constant: 19:1 (the ratio of how likely a positive test is under disease vs. no disease).

The **structure of updating** is invariant: priors multiply by likelihood ratio to produce posteriors.

The **curve of posteriors vs. priors** has the same shape regardless of the test characteristics.

## What changes

- The specific probability you assign initially (the prior)
- The specific probability you end with (the posterior)
- The absolute position on the probability scale

## How this connects to the workshop's findings

### Earthquakes
- What changes: magnitudes, locations, timings
- What persists: the aftershock mechanism (explains temporal clustering everywhere)

### Error codes
- What changes: the substrate (Morse vs. DNA)
- What persists: redundancy principle (reveals what matters)

### Dynamical systems
- What changes: the parameters, starting conditions
- What persists: periodicity structure at finite scales

### Bayesian inference
- What changes: the prior, the posterior, the specific beliefs
- What persists: the rational updating rule

## The deeper insight

Bayes' theorem is not *one* correct way to update belief. It's the *only* way to update belief rationally.

You can derive it from three basic requirements:
1. **Consistency**: Beliefs about compound events must match their decomposition
2. **Exchangeability**: Independent observations can be processed in any order
3. **Calibration**: Belief strength corresponds to empirical frequency

Given these constraints, Bayes' theorem is uniquely determined. It's not a choice. It's the shape rationality must take.

This reveals something profound: the invariant structure in belief updating is not something we impose. It's something we discover by requiring consistency.

## The limit where the invariant breaks

Bayes' theorem fails in one case: if your prior assigns zero probability to the true hypothesis.

Then no amount of evidence will move you. The prior is load-bearing. Everything downstream depends on it.

This suggests a hierarchy:
1. **The prior** (what seems possible) — not chosen rationally, just assumed
2. **Bayesian updating** (the rational form) — invariant across all domains
3. **Convergence** (if the prior was right, you'll find the truth) — conditional on the prior

The prior itself isn't rational or irrational. It's the frame inside which rationality operates.

## Practical implication

When people disagree despite evidence, it's often because they start from different priors (different assumptions about what's possible). 

Rational disagreement is possible. Two people can both update correctly by Bayes' theorem and still reach opposite conclusions if they started from sufficiently different priors.

The solution isn't more evidence. It's finding common ground about *what's possible*.

## Summary

Bayesian invariance is another example of what the workshop keeps finding:

| Domain | Invariant | Application |
|--------|-----------|---|
| Seismic | Aftershock mechanism | Explains clustering across regions |
| Codes | Redundancy principle | Reveals values in different substrates |
| Dynamics | Period structure | Persists across parameter changes |
| Belief | Bayesian updating | Holds across all priors and evidence |

The workshop's method works because **structure is fundamental**. It's not something we impose; it's something we discover.

And the structure is invariant: it persists across representations, domains, and applications.
