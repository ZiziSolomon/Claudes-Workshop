"""Did the pourer slow near the brim? Compare, over time, the resonance
pitch (from the tracker) with the loudness of the splash in a band above the
resonance (4-10 kHz), a rough proxy for how much water is landing.
Usage: python3 slowing.py file t0 t1 fmin fmax"""
import sys, numpy as np, soundfile as sf
from scipy.signal import spectrogram
from scipy.ndimage import uniform_filter1d
f_path, t0, t1, fmin, fmax = sys.argv[1], *map(float, sys.argv[2:6])
x, sr = sf.read(f_path); x = x.mean(1) if x.ndim > 1 else x
x = x[int(t0*sr):int(t1*sr)]
fr, t, S = spectrogram(x, sr, nperseg=4096, noverlap=3072); t += t0
m = (fr >= fmin) & (fr <= fmax)
D = 10*np.log10(S[m] + 1e-12); D -= np.median(D, 1, keepdims=True)
D = uniform_filter1d(uniform_filter1d(D, 5, 0), 5, 1)
pk = fr[m][D.argmax(0)]
pk = np.array([np.median(pk[max(0,i-4):i+5]) for i in range(len(pk))])
hb = (fr >= 4000) & (fr <= 10000)
splash = 10*np.log10(S[hb].sum(0) + 1e-12)
splash = np.array([np.median(splash[max(0,i-4):i+5]) for i in range(len(splash))])
n = len(t); q = n // 4
print(f"{'window':>14} {'pitch Hz':>9} {'oct/s':>7} {'splash dB':>10}")
for i in range(4):
    sl = slice(i*q, (i+1)*q if i < 3 else n)
    tt, pp = t[sl], pk[sl]
    rate = np.polyfit(tt, np.log2(pp), 1)[0]
    print(f"{tt[0]:5.2f}-{tt[-1]:5.2f}s {np.median(pp):9.0f} {rate:7.2f} {np.median(splash[sl]):10.1f}")
