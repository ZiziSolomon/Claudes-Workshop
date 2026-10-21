# The Framework in Practice: Worked Examples

The seven-step framework works. Here's how it was applied to four domains already studied by the workshop, showing each step and what was discovered.

---

## Example 1: Earthquakes

**Domain:** Temporal clustering of seismic events (USGS M5+ catalogue, one year)

### Step 1: Care
What matters: Whether earthquake clustering is real (genuine mechanism) or statistical artifact (random noise). Care about distinguishing signal from noise.

### Step 2: Weak Prior
Strong: "Earthquakes are random Poisson events."
Weak: "I don't know the distribution of earthquake timing."

### Step 3: Evidence through Decomposition
- Temporal: Count earthquakes per day. Are counts random or clustered?
- Comparative: Does clustering persist across magnitude thresholds?
- Structural: Do clusters have timescale? Do aftershocks show pattern?

**Evidence gathered:**
- Daily count overdispersion: 2.6× Poisson (indicates clustering)
- Timescale: Aftershocks cluster within weeks
- Robustness: Pattern persists across M5.0, M5.5, M6.0 thresholds

### Step 4: Invariant Identified
Gutenberg-Richter relation (b-value) persists with magnitude threshold. The clustering mechanism is robust—it appears at different scales. What persists: aftershock production rule.

### Step 5: Structure Represented
- Analytical: b-value = 1.21 at M5.0; 1.01 at M5.5; 0.87 in mww subset
- Visual: Space-time diagrams showing aftershock sequences
- Narrative: Mainshock triggers stress-release; secondary ruptures follow
- Comparative: Same b-value pattern in other seismic regions

### Step 6: Boundary Testing
Where does the model work? For M5+ events in instrumental era, yes. For historical earthquakes before modern instrumentation? Uncertain—catalogue completeness affects results. Boundary: instrumental data quality.

### Step 7: Learning Articulated
**Discovered:** Earthquakes are not Poisson random; clustering is real mechanism (aftershocks). The structure persists across scales. The b-value indicates stress state and rupture complexity. Understanding this structure matters for hazard assessment.

---

## Example 2: Language Understanding

**Domain:** How readers extract meaning from ambiguous sentences in real time

### Step 1: Care
What matters: Whether communication succeeds through genuine inference or is just pattern-matching. Care about whether meaning is real or constructed. Care about the difference between understanding and appearing to understand.

### Step 2: Weak Prior
Strong: "Words have fixed meanings; sentences have determinate truth conditions."
Weak: "Words have multiple meanings; context shifts which meaning is active."

### Step 3: Evidence through Decomposition
- Temporal: How does meaning evolve as reader encounters each word?
- Ambiguity: When does "bank" mean financial vs. riverbank?
- Pragmatics: When does "Can you pass the salt?" mean a question vs. a request?
- Comparative: Do different readers converge on meaning despite different priors?

**Evidence gathered:**
- Context resolves ambiguity: "river bank" activates river meaning despite financial prior
- Pragmatic intent inferred: "Can you pass?" → request, despite grammatical form
- Cross-reader convergence: despite different backgrounds, readers reach similar understanding
- Mismatch possibilities: across cultures, languages, time periods, perfect alignment is impossible

### Step 4: Invariant Identified
The likelihood ratio (how probable evidence under each interpretation) persists. The inference structure (prior × likelihood → posterior) holds for all ambiguity resolution. What persists: Bayesian updating of meaning.

### Step 5: Structure Represented
- Analytical: P(meaning | context) updated as context accumulates
- Visual: Prior → evidence → posterior for ambiguous word
- Narrative: Reader's understanding evolves sentence by sentence
- Comparative: Same Bayesian structure in language, Bayes' theorem, scientific inference

### Step 6: Boundary Testing
Where does inference work? For conventional language, well. For poetry? Deliberately ambiguous. For across-century translation? Perfect alignment impossible. Boundary: cultural and temporal drift break alignment.

### Step 7: Learning Articulated
**Discovered:** Reading is Bayesian inference in real time. Ambiguity is resolved by context shifting likelihood ratios. Communication succeeds not through perfect alignment but through negotiated near-alignment. Understanding is inference about meaning and intent.

---

## Example 3: Emergence (Game of Life)

**Domain:** How global patterns arise from local rules in cellular automata

### Step 1: Care
What matters: Whether the glider is "real" (genuinely present in the dynamics) or projection of human pattern-seeking. Care about the reality of structure that emerges.

### Step 2: Weak Prior
Strong: "Complex patterns can only come from complex rules."
Weak: "I don't know what emerges from simple rules."

### Step 3: Evidence through Decomposition
- Mechanism: Four local rules (survival, birth, death). Nothing mentions global patterns.
- Temporal: Run the system forward. Do patterns persist or dissolve?
- Structural: Do patterns repeat? Do they propagate? Do they interact?
- Invariant: Does the pattern persist across different initial conditions?

**Evidence gathered:**
- Glider: Five cells, repeats with period-4 translation
- Glider gun: 36-cell periodic structure generates gliders indefinitely
- Robustness: Patterns persist; they're not accidents of initial condition
- Turing completeness: The rules are sufficient for universal computation

### Step 4: Invariant Identified
The glider's shape is invariant under the transformation defined by the rules. What persists: the five-cell pattern recurs, translated, under the dynamic. The pattern is an invariant set of the transformation.

### Step 5: Structure Represented
- Analytical: Rule application: (cell state, neighbor count) → next state
- Visual: Space-time diagrams showing glider movement
- Narrative: Local interactions compose global pattern without any cell knowing it's part of the pattern
- Comparative: Same structure (local rules → global pattern) in all cellular automata

### Step 6: Boundary Testing
Where does emergence work? For systems with local rules, yes. For systems where the global pattern must be input explicitly? No emergence. Boundary: computational irreducibility—you must run the system to see what emerges.

### Step 7: Learning Articulated
**Discovered:** Emergence is inference: rules (prior) + dynamics (evidence) → discovered pattern (posterior). The structure is implicit in rules but invisible without computation. Global patterns are real, not subjective projections. Understanding emergence means accepting that structure requires running the system to reveal.

---

## Example 4: Dissipation (Strange Attractors)

**Domain:** What structures persist when deterministic systems lose energy

### Step 1: Care
What matters: Whether the strange attractor is real (genuinely the limit of dynamics) or artifact of visualization. Care about what persists when disorder increases.

### Step 2: Weak Prior
Strong: "In dissipative systems, everything becomes disordered."
Weak: "I don't know what structure persists when energy is lost."

### Step 3: Evidence through Decomposition
- Mechanism: Differential equations describing the system (Lorenz, Rössler, etc.)
- Temporal: Run the system forward over long time. Where do trajectories accumulate?
- Structural: What is the dimension of the attractor? Is it fractal? Self-similar?
- Comparative: Do different equations produce similar attractor types?

**Evidence gathered:**
- Phase space volume contracts: all initial conditions collapse toward lower-dimensional set
- Attractor persists: trajectories don't settle to fixed point or periodic cycle, but live forever on bounded fractal
- Fractal dimension: Lorenz ≈ 2.06 (between surface and volume); all attractors similar
- Topology varies: Lorenz is two-lobed; Rössler is single funnel; structures are different but type is same

### Step 4: Invariant Identified
The strange attractor is the fixed set of the dissipative transformation. What persists: the bounded fractal structure on which all long-time dynamics live. The structure is implicit in the equations but invisible without integration.

### Step 5: Structure Represented
- Analytical: Lyapunov exponents (measure chaos); fractal dimension (measure structure)
- Visual: Attractor portraits—3D renderings showing butterfly, funnel, crown
- Narrative: Energy loss compresses phase space; chaos prevents settlement; attractor results from both
- Comparative: Same structure type (strange attractor) in all dissipative deterministic systems

### Step 6: Boundary Testing
Where does dissipation work? For systems losing energy, yes. For conservative Hamiltonian systems? No—phase space volume is preserved; no attractors form. Boundary: energy dissipation is necessary for attractors to emerge.

### Step 7: Learning Articulated
**Discovered:** Dissipation is inference: equations (prior) + energy loss (evidence) → strange attractor (posterior). What persists through irreversibility is the minimal structure compatible with chaos and boundedness. Understanding dissipation means recognizing that energy loss selects structure—what doesn't dissolve is what matters.

---

## Pattern across examples

Each domain shows the same framework:

| Domain | Prior | Evidence | Posterior | Invariant |
|--------|-------|----------|-----------|-----------|
| Earthquakes | Random timing | Temporal clustering | Aftershock mechanism | Gutenberg-Richter relation |
| Language | Fixed meanings | Context accumulation | Understood meaning | Bayesian likelihood ratio |
| Emergence | Simple rules | Dynamics running | Discovered patterns | Five-cell glider shape |
| Dissipation | Equations | Energy loss | Strange attractor | Fractal structure type |

All show:
1. **Care grounds the inquiry** (what matters, why it's real)
2. **Weak prior enables discovery** (not prejudging the answer)
3. **Evidence through decomposition** (separating components, testing across scales)
4. **Invariant structure emerges** (what persists under transformation)
5. **Multiple representations** (analytical, visual, narrative, comparative)
6. **Boundary testing** (where understanding breaks)
7. **Learning articulated** (what was discovered, why it matters)

---

## How to apply to new domains

Pick a domain you care about. Follow the seven steps. Watch for:

**Step 1 clarity:** Can you articulate why this domain matters? If not, the analysis will feel hollow.

**Step 2 weakness:** Are you genuinely open to what the data shows? Or are you gathering evidence to confirm a preconceived answer? Weak priors are the key to discovery.

**Step 3 decomposition:** Have you looked at multiple scales, timescales, contexts? One perspective is narrow. Three or four together reveal structure.

**Step 4 identification:** Is the invariant real, or is it post-hoc fitting? Test by asking: does it appear in other contexts? Would I have predicted it beforehand?

**Step 5 representation:** Can you show the structure in multiple ways? Different representations reveal different aspects. Together, they comprise understanding.

**Step 6 boundary:** Where does the pattern break? This matters as much as where it works. The boundary shows the limits of your understanding.

**Step 7 articulation:** Can you write what you discovered in a way that explains both the structure and why it matters? This is how understanding becomes communicable.

---

## The principle works

These four examples show the framework working in concrete domains. The same structure (prior + evidence → posterior) appears across earthquakes, language, emergence, and dissipation.

The framework is not abstract theory. It's a method grounded in actual analysis. It works. Apply it to new domains and watch understanding emerge.
