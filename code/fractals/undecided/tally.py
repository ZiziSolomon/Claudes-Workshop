#!/usr/bin/env python3
"""Tally settle-times from undecided.c: how much area is still undecided at N?

usage: tally.py out.bin W H LOG2CAP [image.png]
"""
import sys
import numpy as np

path, W, H, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
t = np.fromfile(path, dtype=np.int32).reshape(H, W)
cell = (2.5 / W) * (1.25 / H) * 2  # x2: the grid covers the upper half only

esc = np.where(t > 0, t, 0)
intr = np.where(t < 0, -t, 0)
never = (t == 0).sum()

print(f"grid {W}x{H}, cap 2^{L}, cell area {cell:.3e}")
print(f"{'N':>9} {'in (found)':>11} {'undecided':>11} {'->escapes':>10} {'->inside':>10} {'->never':>9}  area bounds (sample-point sense)")
for k in range(4, L + 1):
    N = 1 << k
    inside = ((t < 0) & (intr <= N)).sum()
    out = ((t > 0) & (esc <= N)).sum()
    und = W * H - inside - out
    u_esc = ((t > 0) & (esc > N)).sum()
    u_in = ((t < 0) & (intr > N)).sum()
    print(f"{N:>9} {inside*cell:>11.5f} {und*cell:>11.3e} {u_esc*cell:>10.2e} {u_in*cell:>10.2e} {never:>9}  "
          f"[{inside*cell:.5f}, {(inside+und)*cell:.5f}]")
print(f"never settled by cap: {never} points ({never*cell:.3e} area)")

if len(sys.argv) > 5:
    from PIL import Image
    # brightness by log2 of settle time; escaped = warm, interior = cool,
    # never settled = white
    lg = np.log2(np.maximum(np.abs(t), 1)).astype(float) / L
    img = np.zeros((H, W, 3), dtype=np.uint8)
    e = t > 0
    i = t < 0
    img[e, 0] = (40 + 215 * lg[e]).astype(np.uint8)
    img[e, 1] = (10 + 120 * lg[e] ** 2).astype(np.uint8)
    img[e, 2] = 20
    img[i, 0] = 10
    img[i, 1] = (20 + 120 * lg[i]).astype(np.uint8)
    img[i, 2] = (60 + 195 * lg[i]).astype(np.uint8)
    img[t == 0] = 255
    full = np.vstack([img[::-1], img])  # reflect to show the whole set
    Image.fromarray(full).save(sys.argv[5])
    print("wrote", sys.argv[5])
