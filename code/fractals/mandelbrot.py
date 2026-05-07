#!/usr/bin/env python3
"""Mandelbrot and Julia set renderer.

Smooth escape-time coloring with hand-crafted palettes.
Generates a gallery: Mandelbrot views + Julia sets at interesting parameter values.
"""

import math
import os
import struct
import zlib
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)


# ── PNG writer ────────────────────────────────────────────────────────────────

def _chunk(tag, data):
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return length + tag + data + crc

def write_png(path, rgb):
    """Write (H, W, 3) uint8 array to PNG."""
    H, W = rgb.shape[:2]
    raw = b""
    for row in rgb:
        raw += b"\x00" + row.tobytes()
    compressed = zlib.compress(raw, 9)
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(_chunk(b"IHDR", ihdr))
        f.write(_chunk(b"IDAT", compressed))
        f.write(_chunk(b"IEND", b""))


# ── Iteration kernels ─────────────────────────────────────────────────────────

def mandelbrot(xmin, xmax, ymin, ymax, W, H, max_iter=300):
    """Return (H, W) float array: smooth iteration count, or -1 if bounded."""
    x = np.linspace(xmin, xmax, W, dtype=np.float64)
    y = np.linspace(ymin, ymax, H, dtype=np.float64)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    Z = np.zeros_like(C)
    count = np.full(C.shape, -1.0)
    escaped = np.zeros(C.shape, dtype=bool)

    for i in range(max_iter):
        active = ~escaped
        if not np.any(active):
            break
        Z[active] = Z[active] ** 2 + C[active]
        mod2 = (Z.real ** 2 + Z.imag ** 2)
        newly = active & (mod2 > 4.0)
        if np.any(newly):
            mod = np.sqrt(mod2[newly])
            log_z = np.log(mod)
            nu = np.log(log_z / math.log(2)) / math.log(2)
            count[newly] = i + 2 - nu
        escaped |= newly

    return count


def julia(c_re, c_im, xmin, xmax, ymin, ymax, W, H, max_iter=300):
    """Return (H, W) float array for Julia set at c = c_re + i*c_im."""
    x = np.linspace(xmin, xmax, W, dtype=np.float64)
    y = np.linspace(ymin, ymax, H, dtype=np.float64)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    C = complex(c_re, c_im)
    count = np.full(Z.shape, -1.0)
    escaped = np.zeros(Z.shape, dtype=bool)

    for i in range(max_iter):
        active = ~escaped
        if not np.any(active):
            break
        Z[active] = Z[active] ** 2 + C
        mod2 = (Z.real ** 2 + Z.imag ** 2)
        newly = active & (mod2 > 4.0)
        if np.any(newly):
            mod = np.sqrt(mod2[newly])
            log_z = np.log(mod)
            nu = np.log(log_z / math.log(2)) / math.log(2)
            count[newly] = i + 2 - nu
        escaped |= newly

    return count


# ── Color mapping ─────────────────────────────────────────────────────────────

def lerp3(a, b, t):
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )

def gradient(stops, t):
    """Multi-stop gradient. stops: list of (position_0_to_1, (r,g,b))."""
    t = t % 1.0
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        if p0 <= t <= p1:
            lt = (t - p0) / (p1 - p0) if p1 > p0 else 0.0
            return lerp3(c0, c1, lt)
    return stops[-1][1]


# Palette definitions — each maps a [0,1] float to (r,g,b)
def palette_deep_sea(t):
    stops = [
        (0.00, (0, 7, 36)),
        (0.16, (5, 48, 97)),
        (0.32, (26, 152, 80)),
        (0.50, (166, 217, 106)),
        (0.68, (253, 174, 97)),
        (0.84, (215, 48, 39)),
        (1.00, (165, 0, 38)),
    ]
    return gradient(stops, t)

def palette_gold(t):
    stops = [
        (0.00, (10, 10, 40)),
        (0.20, (80, 30, 0)),
        (0.40, (200, 120, 0)),
        (0.60, (255, 240, 100)),
        (0.80, (255, 180, 50)),
        (1.00, (10, 10, 40)),
    ]
    return gradient(stops, t)

def palette_ice(t):
    stops = [
        (0.00, (0, 0, 20)),
        (0.25, (10, 60, 120)),
        (0.50, (80, 180, 230)),
        (0.75, (200, 240, 255)),
        (1.00, (0, 0, 20)),
    ]
    return gradient(stops, t)

def palette_ember(t):
    stops = [
        (0.00, (0, 0, 0)),
        (0.20, (120, 10, 10)),
        (0.40, (200, 80, 0)),
        (0.60, (255, 200, 0)),
        (0.80, (255, 255, 200)),
        (1.00, (0, 0, 0)),
    ]
    return gradient(stops, t)

def palette_violet(t):
    stops = [
        (0.00, (5, 0, 20)),
        (0.20, (80, 10, 120)),
        (0.40, (200, 60, 200)),
        (0.60, (100, 180, 255)),
        (0.80, (40, 60, 150)),
        (1.00, (5, 0, 20)),
    ]
    return gradient(stops, t)

PALETTES = {
    "deep_sea": palette_deep_sea,
    "gold": palette_gold,
    "ice": palette_ice,
    "ember": palette_ember,
    "violet": palette_violet,
}


def colorize(count, palette_fn, period=50.0, interior=(0, 0, 0)):
    """Map smooth iteration counts to RGB image."""
    H, W = count.shape
    rgb = np.zeros((H, W, 3), dtype=np.uint8)
    bounded = count < 0

    escaped_vals = count[~bounded]
    # Map to [0,1] using log-cyclic scaling
    t = (escaped_vals % period) / period
    for idx in zip(*np.where(~bounded)):
        pass  # will vectorize below

    # Vectorized color lookup
    mask = ~bounded
    flat_t = (count[mask] % period) / period
    rows, cols = np.where(mask)
    for i, (r, c) in enumerate(zip(rows, cols)):
        rgb[r, c] = palette_fn(flat_t[i])

    rgb[bounded] = interior
    return rgb


def colorize_fast(count, palette_fn, period=50.0, interior=(0, 0, 0)):
    """Faster: sample palette into a lookup table."""
    H, W = count.shape
    rgb = np.zeros((H, W, 3), dtype=np.uint8)
    bounded = count < 0

    # Build LUT with 1024 entries
    LUT_N = 1024
    lut = np.zeros((LUT_N, 3), dtype=np.uint8)
    for i in range(LUT_N):
        r, g, b = palette_fn(i / LUT_N)
        lut[i] = [r, g, b]

    escaped = ~bounded
    t = ((count[escaped] % period) / period * LUT_N).astype(int) % LUT_N
    rows, cols = np.where(escaped)
    rgb[rows, cols] = lut[t]
    rgb[bounded] = interior
    return rgb


# ── Contact sheet assembler ───────────────────────────────────────────────────

def hstack(imgs):
    return np.concatenate(imgs, axis=1)

def vstack(imgs):
    return np.concatenate(imgs, axis=0)

def add_separator(imgs, thickness=4, color=(30, 30, 30)):
    """Add separators between images (horizontal stack)."""
    H = imgs[0].shape[0]
    sep = np.full((H, thickness, 3), color, dtype=np.uint8)
    result = [imgs[0]]
    for img in imgs[1:]:
        result.append(sep)
        result.append(img)
    return np.concatenate(result, axis=1)


# ── Renders ───────────────────────────────────────────────────────────────────

SIZE = 600  # pixels per panel

def render_mandelbrot_views():
    """Three Mandelbrot views: full, seahorse valley zoom, mini-brot zoom."""
    print("  Mandelbrot: full view...")
    full = mandelbrot(-2.5, 1.0, -1.25, 1.25, SIZE, SIZE, max_iter=300)
    img_full = colorize_fast(full, palette_deep_sea, period=40)

    print("  Mandelbrot: seahorse valley...")
    # Seahorse valley: around c ≈ -0.745 + 0.113i
    sea = mandelbrot(-0.77, -0.71, 0.08, 0.14, SIZE, SIZE, max_iter=600)
    img_sea = colorize_fast(sea, palette_gold, period=30)

    print("  Mandelbrot: elephant valley...")
    # Elephant valley: period-4 bulb
    ele = mandelbrot(0.24, 0.32, 0.48, 0.56, SIZE, SIZE, max_iter=600)
    img_ele = colorize_fast(ele, palette_violet, period=25)

    return img_full, img_sea, img_ele


def render_julia_sets():
    """Six Julia sets at interesting parameter values."""
    params = [
        # (c_re, c_im, palette, period, label)
        (-0.7269,  0.1889, palette_ice,    35, "rabbit"),       # Douady rabbit
        (-0.4,     0.6,    palette_ember,  40, "dragon"),       # Dragon
        (-0.7,     0.27015, palette_violet, 30, "spiral"),      # Spiral Julia
        ( 0.285,   0.01,   palette_gold,   35, "dendrite"),     # Dendrite-like
        (-0.835,  -0.2321, palette_deep_sea, 45, "spiral2"),    # Another spiral
        (-1.476,   0.0,    palette_ice,    50, "basilica"),     # San Marco
    ]
    images = []
    for c_re, c_im, pal, period, label in params:
        print(f"  Julia c = {c_re:+.4f} {c_im:+.4f}i ({label})...")
        cnt = julia(c_re, c_im, -1.5, 1.5, -1.5, 1.5, SIZE, SIZE, max_iter=300)
        img = colorize_fast(cnt, pal, period=period)
        images.append(img)
    return images


def assemble_gallery(m_full, m_sea, m_ele, julia_imgs):
    """Assemble a 3-column contact sheet: 3 Mandelbrot + 6 Julia sets."""
    SEP = 6
    sep_v = np.full((SEP, SIZE * 3 + SEP * 2, 3), 20, dtype=np.uint8)
    sep_h = np.full((SIZE, SEP, 3), 20, dtype=np.uint8)

    def hrow(imgs):
        rows = [imgs[0]]
        for img in imgs[1:]:
            rows.append(sep_h)
            rows.append(img)
        return np.concatenate(rows, axis=1)

    row1 = hrow([m_full, m_sea, m_ele])
    row2 = hrow(julia_imgs[:3])
    row3 = hrow(julia_imgs[3:])

    gallery = np.concatenate([row1, sep_v, row2, sep_v, row3], axis=0)
    return gallery


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    import time
    t0 = time.time()

    print("Rendering Mandelbrot views...")
    m_full, m_sea, m_ele = render_mandelbrot_views()
    write_png(os.path.join(OUT, "mandelbrot_full.png"), m_full)
    write_png(os.path.join(OUT, "mandelbrot_seahorse.png"), m_sea)
    write_png(os.path.join(OUT, "mandelbrot_elephant.png"), m_ele)

    print("Rendering Julia sets...")
    julia_imgs = render_julia_sets()
    julia_labels = ["rabbit", "dragon", "spiral", "dendrite", "spiral2", "basilica"]
    for img, label in zip(julia_imgs, julia_labels):
        write_png(os.path.join(OUT, f"julia_{label}.png"), img)

    print("Assembling gallery...")
    gallery = assemble_gallery(m_full, m_sea, m_ele, julia_imgs)
    write_png(os.path.join(OUT, "gallery.png"), gallery)

    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s. Gallery: {gallery.shape[1]}x{gallery.shape[0]} px")


if __name__ == "__main__":
    main()
