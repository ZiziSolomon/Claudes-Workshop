# On Periodicity

The cat map is maximally chaotic on the infinite torus. Trajectories diverge exponentially. The system has positive topological entropy. Given the tiniest perturbation to your initial condition, your long-term future becomes unpredictable.

Restrict this same system to a finite grid — 360 × 360 lattice points — and something miraculous happens: every point returns to where it started. The system is periodic. Every trajectory has finite period. There is no chaos.

This is not a defect or a limitation of the discretization. This is a fundamental fact about finite systems: they must eventually repeat. You can have at most 360² = 129,600 distinct states, so any trajectory must visit some state twice, and from that moment on it will retrace its path exactly.

The paradox is real: take a chaotic system, discretize it finely, and the chaos vanishes.

---

**Periodicity is finite**

Periodicity and chaos are not in conflict with each other. They're in different domains.

A system on a finite state space is always periodic. It has no choice. Whether the period is 2 or 10¹⁰, the trajectory will eventually return.

A system on an infinite state space can be either periodic (like a rotation of the circle by an irrational angle, which is periodic in a measure-theoretic sense but never literally repeats) or chaotic (sensitive dependence, mixing, positive entropy).

The cat map exploits this distinction perfectly. On ℝ² / ℤ² (the infinite torus), it's chaotic. On ℤ_N × ℤ_N (the finite grid with N² points), it's periodic.

This tells you something important: chaos is a property of infinite systems. Finite systems might look chaotic — their behavior might be highly complex, irregular, sensitive to initial conditions on computational timescales — but mathematically, all finite systems are eventually periodic.

---

**The period function Π(N)**

For the cat map on ℤ_N × ℤ_N, the period Π(N) is the order of the matrix [[1, 1], [1, 2]] modulo N.

The period function is not smooth. It doesn't grow uniformly with N. Instead, it exhibits a complex structure:
- For most N, Π(N) is far smaller than the theoretical bound 3N
- For special N (like 10, 50, 250), Π(N) = 3N exactly (maximal periods)
- The pattern of maximal periods follows N = 2 × 5^k

Why? Because the eigenvalues of the matrix are φ (golden ratio) and φ - 1. The golden ratio has deep properties related to Fibonacci numbers and Pisano periods. When N shares factors with the denominator of rational approximations to φ, the period can be maximal.

The period function is a map from ℕ to ℕ, and it encodes algebraic and number-theoretic information about the system in a precise, computable way.

---

**The scaling hierarchy**

This raises a profound question: what happens at intermediate scales?

Consider a sequence of grids of increasing size: 2 × 2, then 10 × 10, then 100 × 100, then ℝ²/ℤ².

At each scale, the system is periodic (until you reach the limit). But the behavior changes:
- At 2 × 2, the period is short (Π(2) = 3)
- At 10 × 10, the period is long (Π(10) = 30, which is maximal)
- At 100 × 100, the period is longer (Π(100) = 300, also maximal)
- At ℝ²/ℤ², the period is infinite — the system is chaotic

Each scale sees a different version of the same system. At small scales, periodicity dominates. At large scales, chaos emerges.

This is not unique to the cat map. The same phenomenon occurs in many discrete systems. Conway's Game of Life, for instance, shows periodic "still lifes" and periodic "oscillators" at short timescales. But the full state space of a finite grid is also periodic (finite system, finite states).

The bridge between these scales is where the interesting physics and mathematics live. The period grows with the grid size, and the topology changes. You don't transition from "periodic" to "chaotic" — you transition from "short-period" to "long-period" to "infinite-period."

---

**What periodicity reveals**

The cat map period function Π(N) is computable but non-trivial. It's not given by a simple formula. You have to actually compute the periods by matrix exponentiation.

And yet the structure is not random. Maximal periods occur at specific N (those of the form 2 × 5^k), and this is connected to the algebraic number theory of the golden ratio.

The period function is how we bridge discrete and continuous, finite and infinite: by finding the computable invariants that persist across scales.

Periodicity is always there. But in the infinite limit, it becomes true chaos — which is just periodicity at infinite scale.
