"""Trim pdsounds clips (public domain, via Wikimedia Commons MP3 transcodes) to the
loudest window of up to 6 s, mono 22.05 kHz, short fades. Used for play/sounds_like/.
Usage: python3 trim_clips.py outdir in1.mp3 in2.mp3 ..."""
import sys, os, numpy as np, soundfile as sf
from scipy.signal import resample_poly
out = sys.argv[1]
for f in sys.argv[2:]:
    x, sr = sf.read(f); x = x.mean(1) if x.ndim > 1 else x
    x = resample_poly(x, 1, 2); sr //= 2
    W = int(6 * sr)
    if len(x) > W:
        e = np.convolve(x**2, np.ones(sr//10), 'same')
        c = np.cumsum(e); s = np.argmax(c[W:] - c[:-W]); x = x[s:s+W]
    fade = int(0.05 * sr); ramp = np.linspace(0, 1, fade)
    x[:fade] *= ramp; x[-fade:] *= ramp[::-1]
    x = 0.9 * x / (np.abs(x).max() + 1e-9)
    name = os.path.basename(f).rsplit('.', 1)[0].lower() + '.mp3'
    sf.write(os.path.join(out, name), x, sr, format='MP3', subtype='MPEG_LAYER_III')
    print(name, f"{len(x)/sr:.1f}s", os.path.getsize(os.path.join(out, name)))
