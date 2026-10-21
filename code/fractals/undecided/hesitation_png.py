#!/usr/bin/env python3
"""Log-density image of an orbit histogram from hesitation.c.

usage: hesitation_png.py hist.bin S out.png
"""
import sys
import numpy as np
from PIL import Image

path, S, png = sys.argv[1], int(sys.argv[2]), sys.argv[3]
h = np.fromfile(path, dtype=np.uint64).reshape(S, S).astype(float)
v = np.log1p(h)
v /= v.max()
lo, mid, hi = np.array([8, 6, 14]), np.array([150, 70, 40]), np.array([255, 236, 200])
v = v[..., None]
img = np.where(v < 0.5, lo + (mid - lo) * (v / 0.5), mid + (hi - mid) * ((v - 0.5) / 0.5))
img[h == 0] = lo
Image.fromarray(img.astype(np.uint8)).save(png)
nz = h[h > 0]
print("wrote", png, "visited cells", nz.size, "max count %.3g" % h.max())
