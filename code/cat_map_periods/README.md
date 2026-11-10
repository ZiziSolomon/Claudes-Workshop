# Cat Map Period Function Π(N)

A number-theoretic visualization of the period function for the cat map on finite grids.

## The Cat Map Periods

The cat map T(x, y) = (x + y, x + 2y) mod 1 is one of the canonical examples of a chaotic dynamical system. When restricted to a finite grid ℤ_N × ℤ_N (integers mod N), it becomes a finite permutation — eventually, every point returns to itself.

The period Π(N) is the order of the matrix [[1, 1], [1, 2]] modulo N. This is the smallest positive integer k such that:

```
[[1, 1], [1, 2]]^k ≡ [[1, 0], [0, 1]] (mod N)
```

## Key Properties

- **Bound:** Π(N) ≤ 3N for all N
- **Maximal periods:** Occur when Π(N) = 3N, which happens at N = 2·5^k (i.e., N = 10, 50, 250, ...)
- **Connection to Lucas sequences:** The period function relates to Lucas numbers and Pisano periods of Fibonacci-like sequences
- **Eigenvalue involvement:** The matrix eigenvalues are φ (golden ratio) and φ̄ = φ - 1

## Files

- **compute_periods.py** — Computes Π(N) for N = 1 to 360 using matrix exponentiation modulo N. Uses binary exponentiation for efficiency.
- **visualize_periods.py** — Creates three visualizations:
  - **periods_plot.png** — Scatter plot of Π(N) vs. N with the 3N bound envelope. Points colored by largest prime factor.
  - **periods_histogram.png** — Histogram showing distribution of period values.
  - **panel.png** — Combined view.

## Data

- **periods.json** — Computed Π(N) values and bounds for N ∈ [1, 360].

## Observations

For N ∈ [1, 360]:
- Minimum period: 1 (at N = 1)
- Maximum period: 750 = 3 × 250 (achieved at N = 250 = 2 × 5³)
- Average period: 98.3
- Maximal order points (Π(N) = 3N): {10, 50, 250}

The maximal order points follow the pattern N = 2 × 5^k, suggesting deep connection to the Fibonacci/Lucas number structure and the golden ratio eigenvalues.

## Mathematical Significance

The period function Π(N) is:
1. **A number-theoretic classifier** — it characterizes the periodicity structure of the cat map on different moduli
2. **Connected to dynamical systems** — the period relates to the topological entropy and mixing properties
3. **Related to algebraic number theory** — the golden ratio and its algebraic properties determine the period structure
4. **Computable but non-trivial** — computing individual periods requires matrix exponentiation, no closed-form formula exists

The visualization shows that Π(N) is not smooth or predictable from N alone; its structure is determined by the interplay between N's factorization and the algebraic properties of the cat map matrix.
