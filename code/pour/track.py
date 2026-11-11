"""Model-free check: per-frame spectral peak in a band, then test whether
1/f is linear in time (quarter-wave + steady fill) better than f is.
Usage: python3 track.py file t0 t1 fmin fmax"""
import sys, numpy as np, soundfile as sf
from scipy.signal import spectrogram
from scipy.ndimage import uniform_filter1d
f_path, t0, t1, fmin, fmax = sys.argv[1], *map(float, sys.argv[2:6])
x, sr = sf.read(f_path); x = x.mean(1) if x.ndim > 1 else x
x = x[int(t0*sr):int(t1*sr)]
fr, t, S = spectrogram(x, sr, nperseg=4096, noverlap=3072)
t += t0
m = (fr >= fmin) & (fr <= fmax)
D = 10*np.log10(S[m] + 1e-12)
D = D - np.median(D, axis=1, keepdims=True)          # remove fixed resonances/colour
D = uniform_filter1d(D, 5, axis=0)                     # smooth across freq
D = uniform_filter1d(D, 5, axis=1)                     # and across time
pk = fr[m][D.argmax(0)]
# running median over 9 frames to kill outliers
pk_s = np.array([np.median(pk[max(0,i-4):i+5]) for i in range(len(pk))])
def r2(y):
    A = np.vstack([t, np.ones_like(t)]).T; c, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    return 1 - res[0]/((y-y.mean())**2).sum(), c
r_inv, c_inv = r2(1/pk_s); r_lin, _ = r2(pk_s)
print(f"frames={len(t)}  f from {pk_s[:5].mean():.0f} to {pk_s[-5:].mean():.0f} Hz")
print(f"R^2 linear in 1/f: {r_inv:.3f}   R^2 linear in f: {r_lin:.3f}")
print(f"implied L_eff: {343/4*c_inv[1]+343/4*c_inv[0]*t[0]:.3f} m at t0, dL/dt = {343/4*c_inv[0]*1000:.1f} mm/s")
for ti, p in zip(t[::6], pk_s[::6]): print(f"  {ti:5.2f}s {p:6.0f} Hz  L_eff={343/4/p*100:5.1f} cm")
