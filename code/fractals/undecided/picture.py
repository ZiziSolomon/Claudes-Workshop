#!/usr/bin/env python3
"""Render 'how long it takes to know' from undecided.c output.

Each output pixel covers a block of samples and shows the *slowest* sample in
it: brightness = log2(settle time). Escaped samples are drawn warm, interior
ones cool. The boundary itself never appears; what you see is the halo of
points that take a long time to give up their answer.

usage: picture.py out.bin W H LOG2CAP BLOCK out.png
"""
import sys
import numpy as np
from PIL import Image

path, W, H, L, B, png = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
t = np.fromfile(path, dtype=np.int32).reshape(H // B, B, W // B, B)
t = t.transpose(0, 2, 1, 3).reshape(H // B, W // B, B * B)
mag = np.abs(t).astype(np.int64)
mag[t == 0] = 1 << (L + 1)             # never settled: brighter than anything
k = mag.argmax(axis=2)
slow = np.take_along_axis(t, k[..., None], axis=2)[..., 0]
v = np.log2(np.maximum(np.abs(slow), 1)) / L
v = np.clip(v, 0, 1)[..., None]

# two ramps from near-black to a pale end colour
warm_lo, warm_hi = np.array([18, 8, 6]), np.array([255, 214, 150])
cool_lo, cool_hi = np.array([6, 10, 22]), np.array([170, 220, 255])
g = v ** 0.8
warm = warm_lo + (warm_hi - warm_lo) * g
cool = cool_lo + (cool_hi - cool_lo) * g
img = np.where((slow < 0)[..., None], cool, warm)
img[slow == 0] = 255
img = img.astype(np.uint8)
full = np.vstack([img[::-1], img])     # the grid holds the upper half only
Image.fromarray(full).save(png)
print("wrote", png, full.shape)
