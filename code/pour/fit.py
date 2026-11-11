"""Fit the quarter-wave filling law to a real pour recording.

Model: the air column above the liquid is a tube closed at the bottom (the
liquid surface) and open at the top. Its fundamental is f = c / (4 L_eff),
where L_eff = (air column length) + end correction. If liquid rises at a
steady speed u, L_eff(t) = L0 - u (t - t0), so 1/f falls linearly in time
and f traces a hyperbola that steepens toward the brim.

We don't track peaks frame by frame (too noisy); instead we grid-search
(L0, u) for the curve along which the spectrogram has the most energy,
relative to the local median (so broadband splashes don't dominate).

Usage: python3 fit.py recording.mp3 t_start t_end out.png
"""
import sys, numpy as np, soundfile as sf, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.ndimage import median_filter

C = 343.0
f_path, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
x, sr = sf.read(f_path); x = x.mean(1) if x.ndim > 1 else x
x = x[int(t0*sr):int(t1*sr)]
fr, t, S = spectrogram(x, sr, nperseg=4096, noverlap=3584)
t = t + t0
FMIN, FMAX = 500, 3000  # the band we search in; below 500 Hz is splash rumble
keep = fr < 6000; fr, S = fr[keep], S[keep]
D = 10*np.log10(S + 1e-12)
# whiten: subtract per-frame median and per-bin median so a narrow band stands out
W = D - np.median(D, axis=0, keepdims=True)
W = W - median_filter(W, size=(1, 41))
W = np.clip(W, 0, None)

def score(L0, u, harmonic=1):
    L = L0 - u*(t - t[0])
    ok = L > 0.005
    f = harmonic*C/(4*np.where(ok, L, 1))
    idx = np.searchsorted(fr, f)
    ok &= (idx > 0) & (idx < len(fr)-1) & (f >= FMIN) & (f <= (FMAX if harmonic == 1 else 6000))
    s = W[np.clip(idx, 0, len(fr)-1), np.arange(len(t))]
    return s[ok].mean() if ok.sum() > len(t)//2 else 0

best = (0, None)
for L0 in np.arange(0.02, 0.25, 0.001):
    for u in np.arange(0.0, 0.10, 0.0005):
        s = score(L0, u)
        if s > best[0]: best = (s, (L0, u))
s, (L0, u) = best
# null: same search but with u forced to 0 (a constant tone)
null = max(score(L0_, 0) for L0_ in np.arange(0.02, 0.25, 0.001))
h3 = score(L0, u, 3)
# control for harmonic: random constant offsets
rng = np.random.default_rng(0)
h_ctrl = np.mean([score(L0*k, u*k, 3) for k in rng.uniform(0.6, 0.9, 30)])
Lend = L0 - u*(t[-1]-t[0])
print(f"best fit: L0={L0*100:.1f} cm, rise speed u={u*1000:.1f} mm/s, score={s:.2f}")
print(f"  f at start {C/(4*L0):.0f} Hz, at end {C/(4*Lend):.0f} Hz  (L_end={Lend*100:.1f} cm)")
print(f"  octaves swept: {np.log2(L0/Lend):.2f}")
print(f"  constant-tone null best score: {null:.2f}")
print(f"  energy along 3f (odd harmonic) curve: {h3:.2f}  vs detuned controls {h_ctrl:.2f}")

fig, ax = plt.subplots(figsize=(11, 5))
ax.pcolormesh(t, fr, D, shading="auto", cmap="magma", vmin=np.percentile(D, 35))
tt = np.linspace(t[0], t[-1], 300); LL = L0 - u*(tt - t[0])
for h, ls in [(1, "-"), (3, "--")]:
    ax.plot(tt, h*C/(4*LL), color="#7fdcff", lw=1.2, ls=ls, alpha=.85,
            label=f"{'fundamental' if h==1 else '3rd harmonic (odd: closed-open tube)'}")
ax.set_ylim(0, 6000); ax.set_xlabel("seconds"); ax.set_ylabel("Hz")
ax.set_title(f"{f_path.split('/')[-1]}  —  fitted f = c / 4(L₀ − u·t),  L₀={L0*100:.1f} cm, u={u*1000:.1f} mm/s")
ax.legend(loc="upper left", fontsize=8); fig.tight_layout(); fig.savefig(out, dpi=90)
