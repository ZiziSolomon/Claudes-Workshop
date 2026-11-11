"""Final figure for writing/on_the_glass.md.
Left: a real pour (public-domain Commons recording, boiling water into a mug)
with per-frame resonance peaks and a straight-line fit in 1/f.
Right: the quarter-wave law for an idealised 12 cm glass, showing where in
the fill the pitch rise happens.
Usage: python3 figure.py path/to/Boiling_water_being_poured_into_a_mug_for_tea.mp3 out.png"""
import sys, numpy as np, soundfile as sf, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.ndimage import uniform_filter1d
C = 343.0
src, out = sys.argv[1], sys.argv[2]
x, sr = sf.read(src); x = x.mean(1) if x.ndim > 1 else x
T0, T1 = 4.0, 10.5
seg = x[int(T0*sr):int(T1*sr)]
fr, t, S = spectrogram(seg, sr, nperseg=4096, noverlap=3072); t += T0
D = 10*np.log10(S + 1e-12)
# same tracker as track.py, on the pour window 5.6-9.7 s, band 600-2500 Hz
w = (t >= 5.6) & (t <= 9.7); m = (fr >= 600) & (fr <= 2500)
Dm = D[m][:, w]; Dm = Dm - np.median(Dm, 1, keepdims=True)
Dm = uniform_filter1d(uniform_filter1d(Dm, 5, 0), 5, 1)
pk = fr[m][Dm.argmax(0)]; tw = t[w]
pk = np.array([np.median(pk[max(0,i-4):i+5]) for i in range(len(pk))])
a, b = np.polyfit(tw, 1/pk, 1)

fig, (ax, bx) = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw=dict(width_ratios=[1.35, 1]))
ax.pcolormesh(t, fr, D, shading="auto", cmap="magma", vmin=np.percentile(D, 35))
ax.plot(tw, pk, ".", ms=3, color="#9fe7ff", alpha=.7, label="loudest resonance, 600–2500 Hz, per frame")
ax.plot(tw, 1/(a*tw + b), color="white", lw=1.4, label="straight line in 1/f  (air column shrinking steadily)")
ax.set_ylim(0, 4000); ax.set_xlabel("seconds"); ax.set_ylabel("Hz")
ax.set_title("A real pour: boiling water into a mug (Wikimedia Commons, public domain)", fontsize=10)
ax.legend(loc="upper left", fontsize=8, framealpha=.6)
for tt in (5.7, 7.0, 8.3, 9.6):
    L = C/4*(a*tt + b)*100
    ax.annotate(f"{L:.0f} cm", (tt, 1/(a*tt+b)), xytext=(0, 14), textcoords="offset points",
                color="white", fontsize=8, ha="center")

H, r = 0.12, 0.035; e = 0.6*r
phi = np.linspace(0, 0.995, 400)
f = C/(4*((1-phi)*H + e))
oct_ = np.log2(f/f[0])
bx.plot(phi*100, f, color="#1f6f8b", lw=2)
bx.set_yscale("log", base=2); bx.set_yticks([500, 1000, 2000, 4000]); bx.set_yticklabels(["500", "1000", "2000", "4000"])
bx.set_xlabel("percent full"); bx.set_ylabel("Hz (log scale: equal steps = equal octaves)")
tot = np.log2(C/(4*e)/f[0])
for p0, p1, col in [(0, 50, "#dfe8ec"), (75, 100, "#f6d7c3")]:
    o = np.log2((H*(1-p0/100)+e)/(H*(1-p1/100)+e))
    bx.axvspan(p0, p1, color=col, zorder=0)
    bx.text((p0+p1)/2, 560, f"{p0}–{p1}%:\n{o:.2f} of {tot:.2f}\noctaves", ha="center", fontsize=8.5)
bx.set_title("The law, for a 12 cm glass (r = 3.5 cm): f = c / 4(air column + 0.6 r)", fontsize=10)
bx.set_xlim(0, 100); bx.grid(alpha=.3, which="both")
fig.tight_layout(); fig.savefig(out, dpi=100)
print("1/f fit: L_eff(t) slope", a*C/4*1000, "mm/s; frames", len(tw))
