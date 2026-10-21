#!/usr/bin/env python3
"""Plot r(n) from drift.c: an orbit spiralling out of a near-Siegel disc."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = np.loadtxt("out/drift.txt")
n, r = d[:, 0], d[:, 1]
lam_excess = 1.745e-8            # |lambda| - 1 for the 4-cycle

ink, muted, grid = "#1f1f24", "#6b6b76", "#e4e4ea"
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=150)
ax.semilogy(n / 1e8, r, color="#3b5ba5", lw=1.0)
# predicted outward spiral: r grows as exp(n * (|lambda|-1) / 4)
# anchor each reference line on the lower envelope just after a reinjection
for n0, span in [(0.3e8, 4.6e8), (5.9e8, 1.8e8), (8.15e8, 2.0e8)]:
    w = (n >= n0) & (n < n0 + 5e6)
    r0 = r[w].min() * 0.8
    t = np.linspace(n0, n0 + span, 50)
    ax.semilogy(t / 1e8, r0 * np.exp((t - n0) * lam_excess / 4), color=ink, lw=1.2, ls="--")
ax.text(2.6, 0.0105, "dashed: predicted from the multiplier,\nr ∝ exp(n·(|λ|−1)/4), |λ|−1 = 1.7×10⁻⁸",
        color=ink, fontsize=8.5)
ax.axvline(11.928, color=muted, lw=0.8)
ax.text(11.8, 0.0105, "escapes at\nn = 1,192,804,929", color=muted, fontsize=8.5, ha="right")
ax.set_xlabel("iteration n (×10⁸)", color=ink)
ax.set_ylabel("distance from the 4-cycle", color=ink)
ax.set_title("One orbit's billion-step hesitation: spiral out, fall back in, three times",
             color=ink, fontsize=11, loc="left")
ax.grid(True, which="major", color=grid, lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(muted)
ax.tick_params(colors=muted)
ax.set_xlim(0, 12.2)
fig.tight_layout()
fig.savefig("out/drift.png")
print("wrote out/drift.png")
