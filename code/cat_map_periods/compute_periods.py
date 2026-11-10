"""Compute the period function Π(N) for the cat map.

The cat map is T(x,y) = (x+y, x+2y) mod 1.
When applied to a finite grid ZN × ZN (mod N), the period Π(N) is the order
of the matrix [[1,1],[1,2]] modulo N.

Key facts:
- The eigenvalues are φ (golden ratio ≈ 1.618) and φ̄ ≈ 0.618
- The period is bounded: Π(N) ≤ 3N
- Π(N) relates to Lucas and Pisano periods
- Maximal periods occur at N = 2·5^k (period = 3·5^k)
"""

import numpy as np
from math import gcd
from collections import defaultdict


def mat_mod(A, B, n):
    """Multiply two 2×2 matrices mod n."""
    C = np.zeros((2, 2), dtype=int)
    for i in range(2):
        for j in range(2):
            C[i, j] = sum(A[i, k] * B[k, j] for k in range(2)) % n
    return C


def mat_pow_mod(A, k, n):
    """Compute A^k mod n using binary exponentiation."""
    result = np.eye(2, dtype=int)
    base = np.array(A, dtype=int)

    while k > 0:
        if k % 2 == 1:
            result = mat_mod(result, base, n)
        base = mat_mod(base, base, n)
        k //= 2

    return result


def is_identity(A, n):
    """Check if A ≡ I (mod n)."""
    return (A[0, 0] % n == 1 and A[0, 1] % n == 0 and
            A[1, 0] % n == 0 and A[1, 1] % n == 1)


def compute_period(n):
    """Compute Π(n): the period of the cat matrix mod n."""
    if n == 1:
        return 1

    A = np.array([[1, 1], [1, 2]], dtype=int)
    A_pow = A.copy()

    # Binary search upper bound
    upper_bound = 3 * n

    for k in range(1, upper_bound + 1):
        if is_identity(A_pow, n):
            return k
        A_pow = mat_mod(A_pow, A, n)

    return upper_bound + 1  # Period exceeds bound (shouldn't happen)


def prime_factorization(n):
    """Return prime factorization as a list of primes (with repetition)."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def compute_periods(n_max):
    """Compute Π(n) for n = 1 to n_max."""
    periods = {}
    factorizations = {}

    for n in range(1, n_max + 1):
        periods[n] = compute_period(n)
        factorizations[n] = prime_factorization(n)

        if n % 100 == 0:
            print(f"  Computed up to n={n}")

    return periods, factorizations


def compute_bound(n):
    """The theoretical bound: Π(N) ≤ 3N."""
    return 3 * n


def is_maximal_order(n, period):
    """Check if period is maximal for this n (period = 3N)."""
    return period == 3 * n


if __name__ == "__main__":
    n_max = 360
    print(f"Computing cat map periods up to N={n_max}...")
    periods, factorizations = compute_periods(n_max)

    # Save results
    import json

    results = {
        'periods': periods,
        'n_max': n_max,
        'bound_3n': {str(n): 3*n for n in range(1, n_max+1)},
    }

    with open('/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/cat_map_periods/periods.json', 'w') as f:
        json.dump(results, f)

    print(f"Saved to periods.json")

    # Print some statistics
    max_period = max(periods.values())
    min_period = min(periods.values())
    avg_period = sum(periods.values()) / len(periods)

    maximal = [n for n in periods if is_maximal_order(n, periods[n])]

    print(f"\nStatistics for N ∈ [1, {n_max}]:")
    print(f"  Min period: {min_period}")
    print(f"  Max period: {max_period}")
    print(f"  Avg period: {avg_period:.1f}")
    print(f"  Maximal order points: {sorted(maximal)}")

    # Check pattern of maximal points
    print(f"\nMaximal order points (Π(N) = 3N):")
    for n in sorted(maximal)[:15]:
        factors = factorizations[n]
        print(f"  N={n:3d}: factors={factors}")
