"""
Phyllotaxis gallery — renders nine spiral patterns at different divergence angles.
Static counterpart to explore.html.

Vogel's formula: seed n at radius c·sqrt(n), angle n·alpha.
"""

import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np

PHI = (1 + math.sqrt(5)) / 2
GOLDEN = 360 / (PHI * PHI)
SILVER = 360 - 360 / (1 + math.sqrt(2)) ** 2
BRONZE = 360 / ((3 + math.sqrt(13)) / 2) ** 2

PANELS = [
    ("60°",            60,            "6-fold (rational, 360/6)"),
    ("90°",            90,            "4-fold (rational, 360/4)"),
    ("144°",           144,           "5-fold (rational, 360·2/5)"),
    ("137°",           137.0,         "near-rational, weak structure"),
    ("137.4°",         137.4,         "near-golden (8 arms)"),
    ("Golden 137.508°", GOLDEN,       "Fibonacci packing"),
    ("137.6°",         137.6,         "near-golden (8 arms, other way)"),
    ("Silver 137.755°", SILVER,       "noble (silver-type)"),
    ("Bronze 134.075°", BRONZE,       "noble (bronze-type)"),
]

W, H = 480, 480
N_SEEDS = 1800
SCALE = 5.0
PADDING = 24
LABEL_HEIGHT = 56

def render_panel(alpha_deg, title, subtitle):
    img = Image.new("RGB", (W, H + LABEL_HEIGHT), (6, 8, 14))
    pixels = np.zeros((H, W, 3), dtype=np.float32)

    cx, cy = W / 2, H / 2
    alpha_rad = math.radians(alpha_deg)
    max_r = min(W, H) / 2 - 6

    for n in range(1, N_SEEDS + 1):
        r = SCALE * math.sqrt(n)
        if r > max_r:
            break
        theta = n * alpha_rad
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)

        t = math.sqrt(n / N_SEEDS)
        size = 1.6 + 1.6 * t
        rr = 120 + 130 * t
        gg = 85 + 95 * t
        bb = 50 + 50 * (1 - t)

        # paint a small disk with anti-aliasing via additive splat
        ix0 = max(0, int(x - size - 1))
        ix1 = min(W, int(x + size + 2))
        iy0 = max(0, int(y - size - 1))
        iy1 = min(H, int(y + size + 2))
        for px in range(ix0, ix1):
            for py in range(iy0, iy1):
                d = math.hypot(px + 0.5 - x, py + 0.5 - y)
                if d < size + 0.5:
                    a = max(0.0, min(1.0, size + 0.5 - d)) * 0.85
                    pixels[py, px, 0] = max(pixels[py, px, 0], rr * a + pixels[py, px, 0] * (1 - a) * 0)
                    pixels[py, px, 1] = max(pixels[py, px, 1], gg * a + pixels[py, px, 1] * (1 - a) * 0)
                    pixels[py, px, 2] = max(pixels[py, px, 2], bb * a + pixels[py, px, 2] * (1 - a) * 0)

    arr = np.clip(pixels, 0, 255).astype(np.uint8)
    img_seeds = Image.fromarray(arr)
    img.paste(img_seeds, (0, 0))

    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 16)
        font_s = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 11)
    except Exception:
        font_t = ImageFont.load_default()
        font_s = ImageFont.load_default()

    draw.text((14, H + 8), title, fill=(224, 232, 255), font=font_t)
    draw.text((14, H + 32), subtitle, fill=(85, 96, 128), font=font_s)
    return img


def assemble_gallery():
    panels = [render_panel(a, t, s) for (t, a, s) in PANELS]
    cols, rows = 3, 3
    pw, ph = panels[0].size
    gap = 6
    gw = cols * pw + (cols - 1) * gap + 2 * PADDING
    gh = rows * ph + (rows - 1) * gap + 2 * PADDING + 60

    canvas = Image.new("RGB", (gw, gh), (10, 12, 20))
    draw = ImageDraw.Draw(canvas)
    try:
        font_h = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 22)
        font_sub = ImageFont.truetype("/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 12)
    except Exception:
        font_h = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((PADDING, 14), "PHYLLOTAXIS", fill=(232, 236, 248), font=font_h)
    draw.text((PADDING, 46), "Vogel spirals at nine divergence angles. Rational angles spoke; irrational angles spiral; the golden angle packs.",
              fill=(85, 96, 128), font=font_sub)

    for i, panel in enumerate(panels):
        c = i % cols
        r = i // cols
        x = PADDING + c * (pw + gap)
        y = PADDING + 60 + r * (ph + gap)
        canvas.paste(panel, (x, y))

    return canvas


if __name__ == "__main__":
    import os, sys, time
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    gallery = assemble_gallery()
    out_path = os.path.join(out_dir, "gallery.png")
    gallery.save(out_path, optimize=True)
    print(f"wrote {out_path} in {time.time()-t0:.1f}s")
