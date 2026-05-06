"""Clifford strange attractors, rendered as density images.

x_{n+1} = sin(a*y_n) + c*cos(a*x_n)
y_{n+1} = sin(b*x_n) + d*cos(b*y_n)

The orbit never settles, but its closure is bounded — a fractal set in the plane.
A single trajectory traces it densely; the image is the histogram of where the
orbit visits, gamma-corrected so dim regions stay visible.
"""

import numpy as np
from PIL import Image
import sys
import os


def render(a, b, c, d, n_iter=8_000_000, res=1600, gamma=0.35,
           cmap="viridis", out=None, burn_in=2000):
    x, y = 0.1, 0.0
    for _ in range(burn_in):
        x, y = np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)

    # Generate the full trajectory in vectorized chunks.
    chunk = 200_000
    n_chunks = n_iter // chunk
    xs_all = np.empty(n_iter, dtype=np.float64)
    ys_all = np.empty(n_iter, dtype=np.float64)
    idx = 0
    for _ in range(n_chunks):
        xs = np.empty(chunk)
        ys = np.empty(chunk)
        for i in range(chunk):
            x, y = np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)
            xs[i] = x
            ys[i] = y
        xs_all[idx:idx + chunk] = xs
        ys_all[idx:idx + chunk] = ys
        idx += chunk

    # The bounding box for Clifford attractors is contained in [-1-|c|, 1+|c|] x [-1-|d|, 1+|d|].
    bx = 1 + abs(c)
    by = 1 + abs(d)
    # Use a square frame matching the larger extent so the aspect is preserved.
    extent = max(bx, by) * 1.02

    # Histogram into a 2D grid.
    H, _, _ = np.histogram2d(
        ys_all, xs_all,
        bins=res,
        range=[[-extent, extent], [-extent, extent]],
    )
    # Flip vertically so positive y is up in the image.
    H = H[::-1, :]

    # Logarithmic density compression then gamma.
    norm = np.log1p(H)
    norm /= norm.max()
    norm = norm ** gamma

    # Apply colormap. Hand-rolled simple colormaps so we don't need matplotlib.
    img = colorize(norm, cmap)

    if out is None:
        out = f"clifford_{a:+.3f}_{b:+.3f}_{c:+.3f}_{d:+.3f}.png".replace("+", "p").replace("-", "m")
    Image.fromarray(img).save(out)
    return out


def colorize(norm, cmap):
    """Map a 2D float array in [0,1] to RGB uint8 using a small palette."""
    palettes = {
        # background dark, going to warm highlights
        "ember": [(0.02, 0.02, 0.06), (0.25, 0.07, 0.20), (0.85, 0.30, 0.15), (1.0, 0.92, 0.65), (1.0, 1.0, 1.0)],
        # cool blue/teal
        "ice":   [(0.01, 0.02, 0.05), (0.04, 0.10, 0.25), (0.10, 0.50, 0.65), (0.55, 0.90, 0.95), (1.0, 1.0, 1.0)],
        # green-purple
        "viridis": [(0.27, 0.00, 0.33), (0.23, 0.32, 0.55), (0.13, 0.57, 0.55), (0.37, 0.79, 0.38), (0.99, 0.91, 0.14)],
        # mono
        "ink":   [(1.0, 1.0, 1.0), (0.0, 0.0, 0.0)],
    }
    pts = palettes[cmap]
    n_stops = len(pts)
    # For each pixel, find which segment of the palette it's in and interpolate.
    scaled = norm * (n_stops - 1)
    lo = np.floor(scaled).astype(np.int32)
    lo = np.clip(lo, 0, n_stops - 2)
    t = scaled - lo
    pal = np.array(pts, dtype=np.float64)
    c0 = pal[lo]
    c1 = pal[lo + 1]
    rgb = c0 + (c1 - c0) * t[..., None]
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)


# A small curated catalog of (a, b, c, d, name, cmap) chosen for visual interest.
GALLERY = [
    (-1.4, 1.6, 1.0, 0.7,   "ember_wing",   "ember"),
    (1.7, 1.7, 0.6, 1.2,    "ice_lattice",  "ice"),
    (-1.7, 1.3, -0.1, -1.21, "viridis_petal", "viridis"),
    (-1.8, -2.0, -0.5, -0.9, "ember_storm",  "ember"),
    (1.5, -1.8, 1.6, 0.9,   "ice_currents", "ice"),
    (-2.0, -2.0, -1.2, 2.0, "ink_braid",    "ink"),
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    for a, b, c, d, name, cmap in GALLERY:
        path = os.path.join(out_dir, f"{name}.png")
        print(f"rendering {name}: a={a} b={b} c={c} d={d} cmap={cmap}", flush=True)
        render(a, b, c, d, out=path, cmap=cmap, n_iter=4_000_000, res=1400)
        print(f"  -> {path}", flush=True)


if __name__ == "__main__":
    main()
