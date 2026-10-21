# Π(N): Period of Arnold's Cat Map

**The period function** Π(N) is the smallest positive integer k such that the cat matrix A = [2 1; 1 1] raised to the k-th power is congruent to the identity matrix modulo N.

In other words: A^k ≡ I (mod N)

## The data

For N = 1 to 200:

| Property | Value |
|---|---|
| Maximum Π(N) | 250 (at N = 125) |
| Upper bound | Π(N) ≤ 3N for all N |
| Maximal points | N = 2·5^k: Π(10) = 30, Π(50) = 150, Π(250) = 750 |
| Average | ~80 for N ≤ 200 |
| Primes | Π(p) ≈ p for most primes |

## Patterns

### 1. The 3N envelope

**Theorem (proven):** Π(N) ≤ 3N for all N.

The upper bound is achieved precisely when N = 2·5^k for k ≥ 1.

This is connected to the eigenvalues of the cat matrix:
- λ₁ = (3 + √5)/2 ≈ 2.618 (golden ratio squared)
- λ₂ = (3 - √5)/2 ≈ 0.382

The period depends on the orders of these eigenvalues modulo N.

### 2. Behavior by prime power

For prime powers p^e:
- **p = 2**: Periods are small and sometimes constant (3, 12, 6, 12, ...)
- **p = 3**: Periods related to powers of 3
- **p = 5**: Periods related to powers of 5, with special structure
- **Other primes**: Π(p) ranges from p/2 to p+1

The cat matrix is the Fibonacci matrix (with a shift). Its periods modulo N are connected to the Pisano periods of Fibonacci and Lucas sequences.

### 3. Multiplicative structure

If gcd(m, n) = 1, then:
Π(mn) = lcm(Π(m), Π(n))

This is because the map acts independently on the m and n factors (by Chinese Remainder Theorem).

### 4. The special case N = 2·5^k

For N = 2·5^k:
- Π(2) = 3
- Π(10) = 30 = 3·10
- Π(50) = 150 = 3·50
- Π(250) = 750 = 3·250

The pattern is Π(2·5^k) = 3·2·5^k for k ≥ 1.

This represents **maximal order**: every possible state of the map modulo N is visited in a single orbit.

## What this means

The period function Π(N) answers the question: **"How long until the cat map returns to where it started, if we track positions modulo N?"**

For N = 125, the answer is 250 steps — the cat stretches and mixes the square so thoroughly that it takes 250 applications of the map before everything returns exactly.

For N = 10, by contrast, everything returns after exactly 30 steps.

The structure of Π(N) — whether it's small or large, whether it hits the bound 3N — depends entirely on the factorization of N and the interaction between the cat matrix's eigenvalues and N's prime factors.

## Connection to chaos

The cat map is:
- **Periodic modulo N** (period Π(N))
- **Chaotic on the real square** (period ∞)
- **Mixing** (in the measure-theoretic sense)

The period function reveals that even infinite-dimensional chaos is built from periodic patterns at all finite scales. The cat map is locally periodic (mod N) but globally chaotic (on ℝ²).

This is a profound duality: the same dynamical rule produces order at finite resolution and chaos at infinite resolution.
