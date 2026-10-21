#!/usr/bin/env python3
"""Print the exact c values of never-settled samples (recomputing the jitter).

usage: points.py out.bin W H
"""
import sys
import numpy as np

M = (1 << 64) - 1


def jitter(k):
    k = (k + 0x9E3779B97F4A7C15) & M
    k = ((k ^ (k >> 30)) * 0xBF58476D1CE4E5B9) & M
    k = ((k ^ (k >> 27)) * 0x94D049BB133111EB) & M
    k ^= k >> 31
    return (k >> 11) * (1.0 / 9007199254740992.0)


path, W, H = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
t = np.fromfile(path, dtype=np.int32).reshape(H, W)
for j, i in np.argwhere(t == 0):
    key = (int(j) << 32) | int(i)
    x = -2.0 + (i + jitter(2 * key)) * 2.5 / W
    y = 0.0 + (j + jitter(2 * key + 1)) * 1.25 / H
    print(f"{x:.17g} {y:.17g}")
