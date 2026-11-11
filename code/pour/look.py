"""Quick-look spectrograms of pour recordings. Usage: python3 look.py out.png file1 file2 ..."""
import sys, numpy as np, soundfile as sf, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.signal import spectrogram
out, files = sys.argv[1], sys.argv[2:]
fig, axes = plt.subplots(len(files), 1, figsize=(14, 3.2*len(files)))
for ax, f in zip(np.atleast_1d(axes), files):
    x, sr = sf.read(f); x = x.mean(axis=1) if x.ndim > 1 else x
    fr, t, S = spectrogram(x, sr, nperseg=4096, noverlap=3584)
    m = fr < 8000
    ax.pcolormesh(t, fr[m], 10*np.log10(S[m]+1e-12), shading="auto", cmap="magma", vmin=np.percentile(10*np.log10(S[m]+1e-12), 30))
    ax.set_title(f.split("/")[-1]); ax.set_ylabel("Hz")
fig.tight_layout(); fig.savefig(out, dpi=70)
