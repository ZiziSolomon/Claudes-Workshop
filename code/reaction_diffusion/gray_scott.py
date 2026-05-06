"""
Gray-Scott reaction-diffusion model.

du/dt = Du * laplacian(u) - u*v^2 + f*(1-u)
dv/dt = Dv * laplacian(v) + u*v^2 - (f+k)*v

u: activator (substrate being consumed)
v: inhibitor (product being produced)
f: feed rate (how fast u replenishes)
k: kill rate (how fast v dies)
"""

import math
import time
import numpy as np
from PIL import Image

GRID = 256
DT   = 1.0
DU   = 0.2100
DV   = 0.1050

# Pearson (1993) canonical parameter sets — each produces a distinct morphology
PATTERNS = [
    {"name": "spots",     "f": 0.037, "k": 0.060, "steps": 12000, "seed": "square"},
    {"name": "stripes",   "f": 0.060, "k": 0.062, "steps": 12000, "seed": "square"},
    {"name": "worms",     "f": 0.078, "k": 0.061, "steps": 10000, "seed": "square"},
    {"name": "mitosis",   "f": 0.028, "k": 0.053, "steps": 14000, "seed": "center"},
    {"name": "labyrinth", "f": 0.025, "k": 0.060, "steps": 14000, "seed": "square"},
    {"name": "spirals",   "f": 0.022, "k": 0.051, "steps": 16000, "seed": "scatter"},
]


def laplacian(z):
    """5-point finite difference Laplacian, periodic boundary conditions."""
    return (
        np.roll(z,  1, axis=0) +
        np.roll(z, -1, axis=0) +
        np.roll(z,  1, axis=1) +
        np.roll(z, -1, axis=1) -
        4.0 * z
    )


def initialize(seed: str, rng):
    u = np.ones((GRID, GRID), dtype=np.float64)
    v = np.zeros((GRID, GRID), dtype=np.float64)

    if seed == "square":
        # Single seeded square with noise
        s = GRID // 2
        r = 20
        u[s-r:s+r, s-r:s+r] = 0.50
        v[s-r:s+r, s-r:s+r] = 0.25
        u[s-r:s+r, s-r:s+r] += 0.05 * rng.random((2*r, 2*r))
        v[s-r:s+r, s-r:s+r] += 0.05 * rng.random((2*r, 2*r))

    elif seed == "center":
        # Small point seed
        s = GRID // 2
        r = 5
        u[s-r:s+r, s-r:s+r] = 0.50
        v[s-r:s+r, s-r:s+r] = 0.25
        u[s-r:s+r, s-r:s+r] += 0.02 * rng.random((2*r, 2*r))
        v[s-r:s+r, s-r:s+r] += 0.02 * rng.random((2*r, 2*r))

    elif seed == "scatter":
        # Many small scattered seeds
        for _ in range(40):
            x = rng.integers(10, GRID-10)
            y = rng.integers(10, GRID-10)
            r = 4
            u[x-r:x+r, y-r:y+r] = 0.50
            v[x-r:x+r, y-r:y+r] = 0.25
        u += 0.01 * rng.random((GRID, GRID))
        v += 0.01 * rng.random((GRID, GRID))

    return u, v


def simulate(f, k, steps, seed, rng):
    u, v = initialize(seed, rng)
    for _ in range(steps):
        Lu = laplacian(u)
        Lv = laplacian(v)
        uvv = u * v * v
        u += DT * (DU * Lu - uvv + f * (1.0 - u))
        v += DT * (DV * Lv + uvv - (f + k) * v)
        np.clip(u, 0.0, 1.0, out=u)
        np.clip(v, 0.0, 1.0, out=v)
    return u, v


# ── Colormaps ─────────────────────────────────────────────────────────────────

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def colorize(arr, stops):
    """Map [0,1] array through a list of (t, RGB) color stops."""
    h, w = arr.shape
    img = np.zeros((h, w, 3), dtype=np.uint8)
    stops = sorted(stops, key=lambda x: x[0])
    for i in range(len(stops)-1):
        t0, c0 = stops[i]
        t1, c1 = stops[i+1]
        mask = (arr >= t0) & (arr < t1)
        t = np.where(mask, (arr - t0) / (t1 - t0 + 1e-12), 0.0)
        for ch in range(3):
            img[:,:,ch] = np.where(mask, (c0[ch] + (c1[ch]-c0[ch])*t).astype(np.uint8), img[:,:,ch])
    # last stop
    mask = arr >= stops[-1][0]
    c = stops[-1][1]
    for ch in range(3):
        img[:,:,ch] = np.where(mask, c[ch], img[:,:,ch])
    return img

CMAPS = {
    "bone":    [(0.0, (  5,   5,  15)), (0.4, ( 60,  80, 120)), (0.75, (160,180,200)), (1.0, (240,245,255))],
    "amber":   [(0.0, (  0,   0,   0)), (0.35,( 80,  20,   5)), (0.65, (200, 90,  10)), (1.0, (255,230,120))],
    "verdigris":[(0.0,( 10,  30,  20)), (0.4, ( 10,  90,  60)), (0.75, ( 80,190,120)), (1.0, (200,255,210))],
    "violet":  [(0.0, (  5,   0,  20)), (0.35,( 60,   5, 100)), (0.65, (170,  40,200)), (1.0, (240,190,255))],
    "ink":     [(0.0, ( 20,  18,  25)), (0.4, ( 50,  40,  80)), (0.70, (110, 90, 170)), (1.0, (200,195,230))],
    "rust":    [(0.0, ( 10,   5,   0)), (0.4, (100,  30,  10)), (0.70, (200,100,  40)), (1.0, (255,210,160))],
}

PATTERN_CMAP = {
    "spots":     "bone",
    "stripes":   "verdigris",
    "worms":     "amber",
    "mitosis":   "violet",
    "labyrinth": "ink",
    "spirals":   "rust",
}


def render(u, name, size=512):
    """Render u field to PIL Image via colormap."""
    # Normalize u to [0,1] for display
    lo, hi = u.min(), u.max()
    arr = (u - lo) / (hi - lo + 1e-12)
    # Gamma for contrast
    arr = np.power(arr, 0.6)
    cmap_name = PATTERN_CMAP[name]
    rgb = colorize(arr, CMAPS[cmap_name])
    img = Image.fromarray(rgb, "RGB")
    img = img.resize((size, size), Image.NEAREST)
    return img


def label_image(img, text, font_size=18):
    """Burn a text label into the bottom of an image."""
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    w, h = img.size
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.rectangle([(w//2 - tw//2 - 6, h-34), (w//2 + tw//2 + 6, h-8)], fill=(0,0,0,180))
    draw.text((w//2 - tw//2, h-32), text, fill=(220,220,220), font=font)
    return img


def main():
    rng = np.random.default_rng(42)
    images = []
    for p in PATTERNS:
        t0 = time.time()
        print(f"  {p['name']:12s}  f={p['f']:.3f}  k={p['k']:.3f}  steps={p['steps']:,}", flush=True)
        u, v = simulate(p["f"], p["k"], p["steps"], p["seed"], rng)
        img = render(u, p["name"], size=512)
        img = label_image(img, f"{p['name']}  f={p['f']:.3f}  k={p['k']:.3f}")
        out_path = f"/home/opc/workshop/code/reaction_diffusion/out/{p['name']}.png"
        img.save(out_path)
        images.append(img)
        print(f"    → saved {out_path}  ({time.time()-t0:.1f}s)", flush=True)

    # 2×3 contact sheet
    cols, rows = 3, 2
    W, H = 512, 512
    pad = 8
    sheet_w = cols * W + (cols+1) * pad
    sheet_h = rows * H + (rows+1) * pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 10, 18))
    for idx, img in enumerate(images):
        r, c = divmod(idx, cols)
        x = pad + c * (W + pad)
        y = pad + r * (H + pad)
        sheet.paste(img, (x, y))
    sheet_path = "/home/opc/workshop/code/reaction_diffusion/out/gallery.png"
    sheet.save(sheet_path)
    print(f"\nGallery saved to {sheet_path}")


if __name__ == "__main__":
    main()
