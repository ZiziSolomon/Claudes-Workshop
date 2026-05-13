"""
Arnold's cat map: maximum mixing with perfect recurrence.

The cat map on the unit torus is
    T(x, y) = (2x + y,  x + y)   mod 1
i.e. multiplication by  M = [[2, 1], [1, 1]]  followed by mod 1.

M is hyperbolic: det M = 1 (area preserving), and its eigenvalues are
phi^2 and 1/phi^2 (phi = golden ratio). Every step stretches the
expanding direction by phi^2 ~ 2.618 and contracts the other by the same
factor. Together with the mod-1 fold this makes T mixing of every
order — the canonical model of "maximally chaotic but measure preserving."

On a discrete N x N grid the map is a permutation of N^2 pixels. Every
permutation has finite order, so iterating on a pixelated image must
return to the starting configuration after some period Pi(N). Pictures
turn to apparent noise; then the noise reassembles itself, perfectly.

Pi(N) is wildly irregular:
    Pi(2)   = 3        Pi(10)  = 30        Pi(100) = 150
    Pi(124) = 15       Pi(125) = 250       Pi(128) = 96

It is bounded by 3N (Dyson and Falk, 1992) and equals 3N when
N = 2 * 5^k. There is no closed-form formula.

This piece renders two panels:
  - top:   a 4x4 strip of cat-map iterations for N = 124, period 15,
           so the grid covers t = 0..15 with t = 15 returning to t = 0.
  - bottom: scatter of Pi(N) for N = 2..360, with the 3N envelope and
           the maximal-order points (where Pi(N) actually attains 3N).
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont


# ----------------------------- Math -----------------------------

CAT_MATRIX = np.array([[2, 1], [1, 1]], dtype=np.int64)


def cat_period(N: int) -> int:
    """Order of the cat matrix in SL(2, Z/NZ)."""
    A = CAT_MATRIX.copy() % N
    I = np.eye(2, dtype=np.int64) % N
    k = 1
    while not np.array_equal(A, I):
        A = (A @ CAT_MATRIX) % N
        k += 1
        if k > 4 * N + 10:
            raise RuntimeError(f"no period found for N={N}")
    return k


def cat_step(img: np.ndarray) -> np.ndarray:
    """One iteration of the cat map on an N x N image (axis 0 = y, axis 1 = x)."""
    N = img.shape[0]
    # The forward map T(x, y) = (2x + y, x + y) is a permutation.
    # Inverse: T^{-1}(X, Y) = (X - Y, -X + 2Y). To fill destination pixel
    # (X, Y) we read from the source location T^{-1}(X, Y).
    Y, X = np.indices((N, N))
    src_x = (X - Y) % N
    src_y = (-X + 2 * Y) % N
    return img[src_y, src_x]


# --------------------------- Source image ---------------------------

def make_cat_source(N: int) -> np.ndarray:
    """A small stylised cat face on a dark background, returned as RGB uint8."""
    img = Image.new("RGB", (N, N), (16, 18, 24))
    d = ImageDraw.Draw(img)

    # Background gradient (radial-ish via stacked ellipses).
    cx, cy = N / 2, N / 2
    for r in range(int(N * 0.55), 0, -2):
        t = 1 - r / (N * 0.55)
        c = (int(20 + 22 * t), int(22 + 26 * t), int(30 + 36 * t))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # Ears (triangles).
    ear_l = [(0.18 * N, 0.10 * N), (0.30 * N, 0.05 * N), (0.36 * N, 0.30 * N)]
    ear_r = [(0.82 * N, 0.10 * N), (0.70 * N, 0.05 * N), (0.64 * N, 0.30 * N)]
    d.polygon(ear_l, fill=(255, 175, 70))
    d.polygon(ear_r, fill=(255, 175, 70))
    # Inner ear.
    ear_li = [(0.23 * N, 0.13 * N), (0.30 * N, 0.10 * N), (0.32 * N, 0.24 * N)]
    ear_ri = [(0.77 * N, 0.13 * N), (0.70 * N, 0.10 * N), (0.68 * N, 0.24 * N)]
    d.polygon(ear_li, fill=(255, 110, 70))
    d.polygon(ear_ri, fill=(255, 110, 70))

    # Head (ellipse).
    d.ellipse([0.20 * N, 0.22 * N, 0.80 * N, 0.86 * N], fill=(255, 190, 90))

    # Eyes.
    d.ellipse([0.32 * N, 0.42 * N, 0.42 * N, 0.54 * N], fill=(30, 35, 50))
    d.ellipse([0.58 * N, 0.42 * N, 0.68 * N, 0.54 * N], fill=(30, 35, 50))
    # Pupils (highlights).
    d.ellipse([0.35 * N, 0.45 * N, 0.39 * N, 0.51 * N], fill=(120, 200, 255))
    d.ellipse([0.61 * N, 0.45 * N, 0.65 * N, 0.51 * N], fill=(120, 200, 255))

    # Nose (small triangle) and mouth.
    nose = [(0.47 * N, 0.62 * N), (0.53 * N, 0.62 * N), (0.50 * N, 0.68 * N)]
    d.polygon(nose, fill=(255, 110, 130))
    d.line([(0.50 * N, 0.68 * N), (0.50 * N, 0.72 * N)], fill=(60, 40, 50), width=1)
    d.arc([0.40 * N, 0.66 * N, 0.50 * N, 0.78 * N], 0, 90, fill=(60, 40, 50), width=1)
    d.arc([0.50 * N, 0.66 * N, 0.60 * N, 0.78 * N], 90, 180, fill=(60, 40, 50), width=1)

    # Whiskers.
    for dy in (-0.02 * N, 0.0, 0.02 * N):
        d.line([(0.20 * N, 0.68 * N + dy), (0.42 * N, 0.70 * N + dy)],
               fill=(230, 230, 240), width=1)
        d.line([(0.58 * N, 0.70 * N + dy), (0.80 * N, 0.68 * N + dy)],
               fill=(230, 230, 240), width=1)

    return np.array(img, dtype=np.uint8)


# ------------------------------ Plot ------------------------------

# Palette consistent with the workshop pieces.
BG     = (18, 20, 25)
PANEL  = (24, 27, 35)
GRID   = (40, 42, 50)
TEXT   = (210, 215, 225)
MUTED  = (110, 115, 130)
DIM    = (75, 80, 92)
AMBER  = (255, 190,  60)
EMBER  = (255,  90,  50)
ICE    = (100, 200, 255)
VERDI  = ( 80, 210, 140)
VIOLET = (170, 110, 240)


def load_fonts():
    base = "/usr/share/fonts/dejavu-sans-fonts/"
    return {
        "xs": ImageFont.truetype(base + "DejaVuSans.ttf", 11),
        "sm": ImageFont.truetype(base + "DejaVuSans.ttf", 13),
        "md": ImageFont.truetype(base + "DejaVuSans.ttf", 15),
        "lg": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 17),
        "xl": ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 22),
    }


def upscale(arr: np.ndarray, factor: int) -> Image.Image:
    """Nearest-neighbour upscale of an HxW or HxWxC numpy array."""
    h, w = arr.shape[:2]
    big = np.repeat(np.repeat(arr, factor, axis=0), factor, axis=1)
    return Image.fromarray(big)


def render():
    N = 124
    period = cat_period(N)               # 15
    assert period == 15, f"unexpected period {period}"

    src = make_cat_source(N)
    frames = [src.copy()]
    cur = src
    for _ in range(period):
        cur = cat_step(cur)
        frames.append(cur)
    # frames now has period+1 = 16 entries; frame[period] == frame[0].
    assert np.array_equal(frames[0], frames[period])

    fonts = load_fonts()
    f_xs, f_sm, f_md, f_lg, f_xl = (fonts[k] for k in ["xs", "sm", "md", "lg", "xl"])

    # Layout: top strip (4x4 thumbnails) and bottom scatter for Pi(N).
    THUMB_PX  = 124
    SCALE     = 2                          # display tiles at 248 px
    DISP      = THUMB_PX * SCALE           # 248
    COLS, ROWS = 4, 4
    GAP       = 18
    LABEL_H   = 22
    TOP_PAD   = 80                         # title area

    strip_w = COLS * DISP + (COLS - 1) * GAP
    strip_h = ROWS * (DISP + LABEL_H) + (ROWS - 1) * GAP

    PLOT_H     = 440
    BOTTOM_PAD = 50
    PAD_X      = 80
    PLOT_TITLE_GAP = 70

    W = strip_w + 2 * PAD_X
    H = TOP_PAD + strip_h + PLOT_TITLE_GAP + PLOT_H + BOTTOM_PAD

    out = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(out)

    # ---- Title ----
    draw.text((PAD_X, 18),
              "Arnold's cat map  \u00b7  N = 124,  period \u03a0(N) = 15",
              fill=TEXT, font=f_xl)
    draw.text((PAD_X, 48),
              "Every step: a hyperbolic shear-and-fold on the torus. "
              "After 15 iterations the picture returns exactly.",
              fill=MUTED, font=f_sm)

    # ---- Thumbnail strip ----
    x0 = PAD_X
    y0 = TOP_PAD
    for i, fr in enumerate(frames[:COLS * ROWS]):  # 16 frames, last = same as first
        c = i % COLS
        r = i // COLS
        x = x0 + c * (DISP + GAP)
        y = y0 + r * (DISP + LABEL_H + GAP)

        # Frame border (subtle).
        draw.rectangle([x - 1, y - 1, x + DISP, y + DISP], outline=DIM)
        out.paste(upscale(fr, SCALE), (x, y))

        # Label below.
        label = f"t = {i}"
        if i == 0 or i == 15:
            label += "   (identity)"
        elif i == 7 or i == 8:
            label += "   (peak mixing)"
        col = AMBER if (i == 0 or i == 15) else (ICE if i in (7, 8) else MUTED)
        draw.text((x, y + DISP + 4), label, fill=col, font=f_sm)

    # ---- Pi(N) scatter ----
    Ns = list(range(2, 361))
    periods = [cat_period(n) for n in Ns]

    plot_x0 = PAD_X + 30
    plot_y0 = TOP_PAD + strip_h + PLOT_TITLE_GAP
    plot_w  = W - 2 * PAD_X - 30
    plot_h  = PLOT_H

    draw.rectangle([plot_x0, plot_y0, plot_x0 + plot_w, plot_y0 + plot_h], fill=PANEL)

    # Axis ranges. Round y_max to a clean number above max(periods).
    x_min, x_max = 0, 360
    y_min, y_max = 0, 1100                   # max period in this range is 3*360 = 1080

    def sx(n): return plot_x0 + (n - x_min) / (x_max - x_min) * plot_w
    def sy(p): return plot_y0 + plot_h - (p - y_min) / (y_max - y_min) * plot_h

    # Gridlines + axis ticks.
    for gx in range(0, 361, 30):
        x = sx(gx)
        # major/minor distinction
        if gx % 60 == 0:
            draw.line([(x, plot_y0), (x, plot_y0 + plot_h)], fill=GRID)
            draw.text((x - 8, plot_y0 + plot_h + 4), str(gx), fill=MUTED, font=f_xs)
        else:
            draw.line([(x, plot_y0), (x, plot_y0 + plot_h)],
                      fill=(30, 32, 38))
    for gy in range(0, 1101, 100):
        y = sy(gy)
        if gy % 200 == 0:
            draw.line([(plot_x0, y), (plot_x0 + plot_w, y)], fill=GRID)
            draw.text((plot_x0 - 32, y - 6), str(gy), fill=MUTED, font=f_xs)
        else:
            draw.line([(plot_x0, y), (plot_x0 + plot_w, y)],
                      fill=(30, 32, 38))

    # 3N envelope.
    x1 = sx(2);   y1 = sy(3 * 2)
    x2 = sx(360); y2 = sy(3 * 360)
    draw.line([(x1, y1), (x2, y2)], fill=(110, 90, 50), width=1)
    draw.text((x2 - 130, y2 + 6), "\u03a0(N) \u2264 3N  (Dyson \u2013 Falk)",
              fill=(160, 130, 70), font=f_xs)

    # Scatter.
    for n, p in zip(Ns, periods):
        x, y = sx(n), sy(p)
        if p == 3 * n:
            # Maximal-order points: N = 2 * 5^k.
            draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=AMBER)
        else:
            draw.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=ICE)
        if n == 124:
            draw.ellipse([x - 7, y - 7, x + 7, y + 7], outline=EMBER, width=2)
            draw.line([(x, y - 7), (x, y - 32)], fill=EMBER, width=1)
            draw.text((x - 22, y - 48), "N = 124", fill=EMBER, font=f_xs)
            draw.text((x - 32, y - 34), "\u03a0 = 15", fill=EMBER, font=f_xs)

    # Annotations for amber points.
    amber_pts = [(n, p) for n, p in zip(Ns, periods) if p == 3 * n]
    for n, p in amber_pts:
        x, y = sx(n), sy(p)
        draw.text((x - 16, y - 22), f"N={n}", fill=AMBER, font=f_xs)

    # Legend (top-right of plot).
    leg_x = plot_x0 + plot_w - 270
    leg_y = plot_y0 + 14
    draw.ellipse([leg_x, leg_y + 2, leg_x + 8, leg_y + 10], fill=AMBER)
    draw.text((leg_x + 14, leg_y),
              "\u03a0(N) attains 3N  (N = 2 \u00b7 5^k)",
              fill=AMBER, font=f_xs)
    draw.ellipse([leg_x + 1, leg_y + 22, leg_x + 7, leg_y + 28], fill=ICE)
    draw.text((leg_x + 14, leg_y + 20),
              "every other N from 2 to 360",
              fill=ICE, font=f_xs)
    draw.ellipse([leg_x - 1, leg_y + 39, leg_x + 9, leg_y + 49],
                 outline=EMBER, width=2)
    draw.text((leg_x + 14, leg_y + 40),
              "the N rendered above",
              fill=EMBER, font=f_xs)

    # Plot title / axis labels.
    draw.text((plot_x0, plot_y0 - 32),
              "Period \u03a0(N) of the cat map on an N \u00d7 N grid, for N = 2 .. 360",
              fill=TEXT, font=f_lg)
    draw.text((plot_x0 + plot_w / 2 - 6, plot_y0 + plot_h + 22),
              "N", fill=MUTED, font=f_md)
    # Rotated y-label.
    yl = Image.new("RGBA", (200, 24), (0, 0, 0, 0))
    ImageDraw.Draw(yl).text((0, 0),
                            "\u03a0(N)   period in iterations",
                            fill=MUTED, font=f_sm)
    yl = yl.rotate(90, expand=True)
    out.paste(yl,
              (plot_x0 - 60, int(plot_y0 + plot_h / 2 - yl.height / 2)),
              yl)

    out.save("/home/opc/workshop/code/cat_map/out/cat_map.png")
    print(f"period(124) = {period}")
    print(f"frames matched at t=period: {np.array_equal(frames[0], frames[period])}")
    print(f"max Pi up to 360: {max(periods)} at N = {Ns[periods.index(max(periods))]}")
    print(f"amber points (Pi(N) = 3N): "
          f"{[n for n, p in zip(Ns, periods) if p == 3*n]}")
    print(f"saved to code/cat_map/out/cat_map.png  ({W}x{H})")


if __name__ == "__main__":
    render()
