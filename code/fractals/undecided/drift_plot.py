#!/usr/bin/env python3
"""Plot r(n) for the slowest orbit: double precision vs. high precision.

Top panel: out/drift.txt (drift.c, double). Bottom: out/precision/trace1024.txt
(precision_mpf.c at 1024 bits, which agrees with 2048 bits on every close
pass and on the escape step). Dashed lines are the outward spiral predicted
by the 4-cycle's multiplier, anchored just after each reinjection.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAM_EXCESS = 1.745e-8            # |lambda| - 1 for the 4-cycle
ink, muted, grid, line = "#1f1f24", "#6b6b76", "#e4e4ea", "#3b5ba5"


def load(path):
    rows = [l.split() for l in open(path) if l[0].isdigit()]
    d = np.array(rows, dtype=float)
    return d[:, 0], d[:, 1]


def reinjections(n, r):
    """Indices where the lower envelope of r drops: r falls below 60% of the
    minimum over the previous 30 samples and below 0.06."""
    out = []
    for i in range(30, len(r)):
        if r[i] < 0.06 and r[i] < 0.6 * r[i - 30:i].min() and (not out or i - out[-1] > 30):
            out.append(i)
    return out


def panel(ax, n, r, escape, label):
    ax.semilogy(n / 1e8, r, color=line, lw=1.0)
    for i in reinjections(n, r):
        j = slice(i, min(i + 150, len(r)))
        r0 = r[j].min() * 0.8
        # run the prediction until the data next leaves the spiral (rim ~0.07)
        k = i + np.argmax(r[i:] > 0.07) if (r[i:] > 0.07).any() else len(r) - 1
        t = np.linspace(n[i], n[k], 50)
        ax.semilogy(t / 1e8, r0 * np.exp((t - n[i]) * LAM_EXCESS / 4), color=ink, lw=1.1, ls="--")
    ax.axvline(escape / 1e8, color=muted, lw=0.8)
    ax.text(escape / 1e8 - 0.1, 0.0105, f"escapes at\nn = {escape:,}", color=muted,
            fontsize=8.5, ha="right")
    ax.text(0.15, 0.17, label, color=ink, fontsize=9.5)
    ax.grid(True, which="major", color=grid, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(muted)
    ax.tick_params(colors=muted)
    ax.set_ylim(0.0075, 0.3)
    ax.set_ylabel("distance from 4-cycle", color=ink)


fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 6.8), dpi=150, sharex=True)
n, r = load("out/drift.txt")
panel(a1, n, r, 1192804929, "double precision (53 bits): three deep resets")
n, r = load("out/precision/trace1024.txt")
panel(a2, n, r, 223621176, "1024 bits (agrees with 2048 to the step): no deep dive at all")
a2.set_xlabel("iteration n (×10⁸)", color=ink)
a2.set_xlim(0, 12.2)
a1.set_title("The slowest orbit spirals out, is reset by close passes to 0, and escapes.\n"
             "Dashed: the spiral rate predicted by |λ|−1 = 1.7×10⁻⁸. The details depend on precision.",
             color=ink, fontsize=10.5, loc="left")
fig.tight_layout()
fig.savefig("out/drift.png")
print("wrote out/drift.png")
