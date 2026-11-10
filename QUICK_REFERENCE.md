# Workshop Quick Reference

**One-Page Overview of 675+ Minutes of Mathematical Investigation**

---

## The Central Question & Answer

**Q:** What structure persists when you change representation, scale, or system?

**A:** Mathematical structure is invariant, universal, real, and discoverable.

---

## Five Research Branches

| Branch | System | Key Finding | Main Essay |
|--------|--------|-------------|-----------|
| **1. Chaos** | Attractors (Lorenz, Rössler, Aizawa) | Topology is audible | `on_attractor_sonification.md` |
| **2. Periodicity** | Cat map, Pisano periods | Golden ratio in 4 domains | `on_pisano_periods.md` |
| **3. Emergence** | Game of Life, Rule 110, Langton's Ant | Three types of emergence | `on_three_automatons.md` |
| **4. Bifurcation** | Logistic map | Feigenbaum δ universal | `on_bifurcation.md` |
| **5. Fractals** | Mandelbrot set | Self-similarity at all scales | `on_fractals.md` |

---

## Universal Structures Discovered

1. **Golden Ratio** — Continuous eigenvalues, discrete periods, matrix algebra, number theory
2. **Feigenbaum δ ≈ 4.669** — All period-doubling bifurcations
3. **Turing Completeness** — All sufficiently complex rule systems
4. **Emergence Principle** — Simple rules → complex behavior (universal)
5. **Self-Similarity** — Structure repeats across scales
6. **Boundary Phenomena** — Maximum structure at chaos/order boundary

---

## Key Code Projects

| Project | What It Does | Output |
|---------|-------------|--------|
| `rossler_sonification/` | Maps 3D attractor to audio | rossler.wav |
| `pisano_periods/` | Computes Fibonacci mod n periods | pisano_periods.png + WAV |
| `life_sonification/` | Game of Life → sound | life.wav + evolution.png |
| `rule110/` | 100k-step 1D CA evolution | rule110_evolution.png + WAV |
| `langtons_ant/` | 100k-step ant on grid | ant_trajectory.png + WAV |
| `bifurcation_logistic/` | Period-doubling diagram | bifurcation.png (2400×1200) |
| `mandelbrot_set/` | Fractal zooms | 4 zoom levels (full, zoom1-3) |

**All projects include:**
- Python implementation
- README explaining significance
- Visualization outputs
- Audio sonifications (where applicable)

---

## Essential Essays

### Start Here (Everyone)
- `on_what_persists.md` — Central insight
- `on_investigation.md` — Methodology

### Next (Pick Your Interest)
- **Math focus:** `on_numbers.md`, `on_pisano_periods.md`, `on_bifurcation.md`
- **Emergence focus:** `on_emergence.md`, `on_rule_110.md`, `on_langtons_ant.md`
- **Philosophy focus:** `on_mathematical_truth.md`, `on_extensions.md`

### Deep Dive (All 73 Available)
See `MAP_OF_THE_WORKSHOP.md` for complete thematic organization

---

## Four Modalities

Every system explored through:
- **Visual** — Images, diagrams, heatmaps
- **Sonic** — Audio sonifications (8 WAV files)
- **Numeric** — Data analysis, computation
- **Symbolic** — Mathematical equations and theory

---

## Quick Stats

| Metric | Count |
|--------|-------|
| Total Essays | 73 |
| Code Projects | 12 |
| Git Commits | 43 |
| Total Minutes | 675+ |
| Audio Files (WAV) | 8 |
| Code Visualizations | 20+ |
| Research Angles | 8+ |

---

## Navigation Options

### Option 1: Linear (Read Everything in Order)
1. Read `on_what_persists.md`
2. Read `on_investigation.md`
3. Follow each branch from WORKSHOP_GUIDE.md
4. Read synthesis essays
5. Explore code projects

### Option 2: By Interest
- **Dynamics:** `rossler_sonification/`, `bifurcation_logistic/`, chaos essays
- **Number Theory:** `cat_map_periods/`, `pisano_periods/`, number essays
- **Emergence:** `life_sonification/`, `rule110/`, `langtons_ant/`, emergence essays
- **Fractals:** `mandelbrot_set/`, `on_fractals.md`

### Option 3: By Modality
- **Visual:** All `.png` files in `code/*/out/`
- **Sonic:** All `.wav` files in `code/*/out/`
- **Mathematical:** All `.md` essays in `writing/`
- **Computational:** All `.py` files in `code/`

### Option 4: By Depth
- **Quick:** This file + `on_what_persists.md` (10 min)
- **Medium:** All essays + visualizations (2-3 hours)
- **Deep:** All essays + code + run projects (8+ hours)

---

## Running Code Projects

All projects are standalone Python scripts:

```bash
cd code/PROJECT_NAME/
python PROJECT.py
# Output generated in out/ directory
```

Requirements: numpy, scipy, PIL (pillow)

---

## Key Insights at a Glance

✓ **Same structure appears independently** across continuous/discrete/emergent/bifurcating/fractal systems

✓ **Same constants emerge universally** (golden ratio, Feigenbaum δ, Turing completeness)

✓ **Structure survives representation change** (visual → sonic → numeric → symbolic)

✓ **Emergence is universal** (simple rules always generate complexity)

✓ **Truth is discoverable** (convergence of independent investigations = evidence)

---

## The Bottom Line

**Mathematical reality is real, objective, and knowable.**

What persists when you change systems, representations, and scales is **structure itself** — because mathematical structure is fundamental.

---

## For More Detail

- **Navigation:** See `WORKSHOP_GUIDE.md`, `WORKSHOP_GUIDE_EXTENDED.md`
- **Complete Map:** See `MAP_OF_THE_WORKSHOP.md`
- **Full Report:** See `SESSION_2026-11-10_FINAL.md`
- **All Findings:** See `notes.md`

---

**Created:** 2026-11-10  
**Duration:** 675+ minutes  
**Status:** ✓ Complete and documented
