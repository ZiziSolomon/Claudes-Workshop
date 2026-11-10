# Pisano Periods: Structure in Fibonacci Modulo n

The Pisano period π(n) is the period of the Fibonacci sequence modulo n.

## Discovery

For each n, take the Fibonacci sequence and reduce each term modulo n:
- Fib(n) = 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...
- Fib(n) mod 5 = 1, 1, 2, 3, 0, 3, 3, 1, 4, 0, 4, 4, 3, 2, 0, 2, 2, 4, 1, 0, 1, 1, ... (repeats)
- **Period π(5) = 20**

## Key Findings

### Golden Ratio Structure (!)

Powers of 5 show perfect algebraic structure:

```
π(5^k) = 4 · 5^k

π(5)   = 20
π(25)  = 100
π(125) = 500
π(625) = 2500
```

Why? The golden ratio φ = (1+√5)/2 is **fundamental to Fibonacci**. The matrix for Fibonacci recurrence is [[1,1],[1,2]], whose eigenvalues involve φ and the conjugate 1-φ = -1/φ. The power-of-5 structure arises from 5 = (2φ+1)² algebraically.

### Other Power Structures

**Powers of 2:** π(2^k) = 3 · 2^(k-1)
- π(2) = 3, π(4) = 6, π(8) = 12, π(16) = 24, π(32) = 48, ...

**Powers of 3:** π(3^k) = 8 · 3^(k-1)
- π(3) = 8, π(9) = 24, π(27) = 72, π(81) = 216, ...

### Ratio Structure

π(n)/n varies from 1.5 to 6 depending on n's factorization:

```
π(10) / 10 = 6.00
π(20) / 20 = 3.00
π(50) / 50 = 6.00
π(100) / 100 = 3.00
π(500) / 500 = 3.00
π(1000) / 1000 = 1.50
```

The ratio is determined by n's prime factorization and the Pisano periods of those prime powers.

## Connection to the Workshop

**This connects multiple threads:**

1. **Periodicity & Cat Map** (Branch 2): Like Π(N) for the cat map, Pisano periods show how **integer discretization creates period structure** from a fundamentally irrational base (φ).

2. **Number Theory** (Branch 2): The golden ratio appears again, now **embedded in pure number theory** via Fibonacci modular arithmetic.

3. **Universality**: Powers-of-5 structure showing π(5^k) = 4·5^k is a **universal algebraic fact**, independent of implementation.

4. **Structure Across Scales**: Pisano periods grow with n, but the *ratio* π(n)/n remains bounded — showing how **structure persists** across different scales.

## Files

- **pisano.py** — Computes π(n) for n up to 1000, visualizes, sonifies
- **out/pisano_periods.png** — Scatter plot showing period growth
- **out/pisano_10.wav**, **pisano_20.wav**, **pisano_50.wav** — Sonified Pisano sequences

## Sonification Strategy

Each Pisano sequence is mapped to a pentatonic scale:
- Fib(n) mod m → pitch in {C3, D3, E3, G3, A3}
- Duration of each note = time for one Fibonacci step

As the Fibonacci sequence evolves modulo n, it cycles through that period, creating an evolving harmonic texture.

## Key Insight

Pisano periods demonstrate that **mathematical structure is universal and algebraic**: the same structure appears across

- Continuous eigenvalues (cat map, attractors)
- Discrete periodicity (cat map Π(N), Pisano π(n))
- Pure number theory (Fibonacci modular arithmetic)

Golden ratio, the universal constant of Fibonacci, drives structure at every scale.
