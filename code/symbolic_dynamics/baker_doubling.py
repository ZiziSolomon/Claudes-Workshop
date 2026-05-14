"""
The baker map and the doubling map: one shift, two windows.

The baker map on the unit square is
    B(x, y) = ( 2x mod 1,                       (y + floor(2x)) / 2 )
i.e. stretch x by 2, halve y, and stack the right half on top of the left.
This is the cleanest 2D measure-preserving Bernoulli system: it is conjugate
to the full shift on bi-infinite binary sequences, with x encoding the
forward sequence (bits to be revealed) and y encoding the backward sequence
(bits already consumed).

The doubling map on [0, 1) is just the first coordinate:
    D(x) = 2x mod 1.
It is the same dynamics, projected. The action on a binary expansion
    x = 0.b_1 b_2 b_3 ...
is to drop b_1 and shift everything left:
    D(x) = 0.b_2 b_3 b_4 ...
"Chaos" here is honest about itself: the apparent randomness of the
trajectory (x_n) is exactly the randomness of the bits of x_0.

The panel shows three things at once:

  - The baker map kneading 4 colored quadrants over 8 iterations.
    Each step stretches horizontally, compresses vertically, and stacks.
    By iteration 7 the original quadrant structure has been beaten into
    128 horizontal stripes; the same pattern in a thinner band.

  - The binary expansion of x_0 = (sqrt(5) - 1) / 2 (golden ratio
    fractional part) under repeated doubling. Each row is the bits of
    x_n in a fixed 48-bit window. The whole pattern visibly shifts left
    one cell per row.

  - The trajectory (x_n) plotted over time. Looks like noise. It is
    noise, in the precise sense that no statistical test can distinguish
    its bits from fair coin flips. But every bit is a fixed bit of x_0,
    determined before the dynamics ever started.
"""

import numpy as np
from decimal import Decimal, getcontext
from PIL import Image, ImageDraw, ImageFont


# --------------------------- Palette (workshop) ---------------------------

BG     = (18, 20, 25)
PANEL  = (24, 27, 35)
GRID   = (40, 42, 50)
TEXT   = (210, 215, 225)
MUTED  = (110, 115, 130)
DIM    = (75, 80, 92)
AMBER  = (255, 190,  60)
EMBER  = (235, 100,  60)
ICE    = (110, 200, 255)
VERDI  = (100, 215, 140)
VIOLET = (170, 110, 240)


# ---------------------------- The baker map -------------------------------

def baker_quadrant_after(N: int, n: int) -> np.ndarray:
    """Render the baker map after n iterations on the 4-quadrant test pattern.

    Convention: returned array has shape (N, N, 3); row 0 is the TOP of the
    unit square (y ~ 1), row N-1 is the BOTTOM (y ~ 0). The standard image
    convention.

    We fill each output pixel by inverse iteration: starting from (x', y')
    in the displayed image, apply B^{-1} n times to find the pre-image,
    and color that pre-image by which of the four initial quadrants it
    fell into.
    """
    rows = np.arange(N)[:, None]
    cols = np.arange(N)[None, :]
    x = ((cols + 0.5) / N) * np.ones((N, N))
    y = (1.0 - (rows + 0.5) / N) * np.ones((N, N))
    # B^{-1}(x, y) = (x/2, 2y)         if y < 1/2
    #              = ((x+1)/2, 2y - 1) if y >= 1/2
    for _ in range(n):
        mask = y < 0.5
        x = np.where(mask, x / 2.0, (x + 1.0) / 2.0)
        y = np.where(mask, 2.0 * y,  2.0 * y - 1.0)
    qx = (x >= 0.5).astype(np.int32)
    qy = (y >= 0.5).astype(np.int32)
    quad = 2 * qy + qx  # 0=BL, 1=BR, 2=TL, 3=TR
    palette = np.array([EMBER, AMBER, VERDI, ICE], dtype=np.uint8)
    img = palette[quad]

    return img


# --------------------------- The doubling map -----------------------------

def golden_fraction_bits(n_bits: int) -> np.ndarray:
    """Binary expansion of (sqrt(5) - 1) / 2, computed at high precision."""
    getcontext().prec = max(60, n_bits // 3 + 30)
    x = (Decimal(5).sqrt() - 1) / 2
    bits = np.zeros(n_bits, dtype=np.uint8)
    for i in range(n_bits):
        x *= 2
        if x >= 1:
            bits[i] = 1
            x -= 1
    return bits


def doubling_trajectory(bits: np.ndarray, n_steps: int) -> np.ndarray:
    """x_n = sum_{k>=1} bits[n + k - 1] * 2^{-k}, truncated to len(bits) - n bits."""
    # Use a window of e.g. 52 bits to keep things in double precision.
    window = min(52, len(bits) - n_steps)
    pow2 = 2.0 ** (-np.arange(1, window + 1))
    xs = np.zeros(n_steps + 1, dtype=np.float64)
    for n in range(n_steps + 1):
        xs[n] = np.sum(bits[n:n + window] * pow2)
    return xs


# --------------------------- Font / draw helpers --------------------------

def load_fonts():
    base = "/usr/share/fonts/dejavu-sans-fonts/"
    return {
        "xs":  ImageFont.truetype(base + "DejaVuSans.ttf", 11),
        "sm":  ImageFont.truetype(base + "DejaVuSans.ttf", 13),
        "md":  ImageFont.truetype(base + "DejaVuSans.ttf", 15),
        "lg":  ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 17),
        "xl":  ImageFont.truetype(base + "DejaVuSans-Bold.ttf", 22),
        "mono": ImageFont.truetype("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Regular.otf", 12),
    }


def paste_array(out: Image.Image, arr: np.ndarray, xy: tuple[int, int]):
    out.paste(Image.fromarray(arr), xy)


# ------------------------------- Layout -----------------------------------

def render() -> Image.Image:
    fonts = load_fonts()
    f_xs, f_sm, f_md, f_lg, f_xl, f_mono = (fonts[k] for k in
                                            ["xs", "sm", "md", "lg", "xl", "mono"])

    # ---- Geometry ----
    PAD_X = 70
    W = 1480

    # Baker strip: 4 columns, 2 rows of 218x218 thumbnails.
    BAKER_PX = 218
    BAKER_COLS = 4
    BAKER_ROWS = 2
    BAKER_GAP = 18
    BAKER_LABEL = 22
    BAKER_TITLE = 78

    baker_w = BAKER_COLS * BAKER_PX + (BAKER_COLS - 1) * BAKER_GAP  # 4*218 + 3*18 = 926
    baker_h = BAKER_ROWS * (BAKER_PX + BAKER_LABEL) + (BAKER_ROWS - 1) * BAKER_GAP

    # Middle row: binary grid (left) + trajectory (right).
    MID_GAP   = 36
    MID_TITLE = 56

    # Binary grid: 64 rows × 48 cols of cells, each 11 px → 528 × 704 + padding.
    GRID_ROWS = 60
    GRID_COLS = 48
    CELL = 11
    GRID_PAD = 24
    grid_w = GRID_COLS * CELL + 2 * GRID_PAD
    grid_h = GRID_ROWS * CELL + 2 * GRID_PAD

    # Trajectory panel takes the rest.
    traj_w = W - 2 * PAD_X - grid_w - MID_GAP
    traj_h = grid_h  # match height for clean alignment

    # Stack heights.
    TITLE_AREA = 110
    CAPTION_AREA = 90

    H = TITLE_AREA + BAKER_TITLE + baker_h + MID_TITLE + grid_h + CAPTION_AREA

    out = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(out)

    # ---- Title ----
    draw.text((PAD_X, 28),
              "Bake, shift, repeat  \u00b7  the baker map and the doubling map",
              fill=TEXT, font=f_xl)
    draw.text((PAD_X, 62),
              "Two views of the same dynamics: a 2D dough-knead and a 1D binary shift. "
              "The trajectory is chaotic. The bits are exactly the bits of x\u2080.",
              fill=MUTED, font=f_sm)
    draw.text((PAD_X, 82),
              "baker B: stretch x by 2 (mod 1), halve y, stack the right half on top.   "
              "doubling D: keep only the first coordinate.   "
              "x\u2080 = (\u221a5 \u2212 1) / 2",
              fill=DIM, font=f_sm)

    # =====================================================================
    # PANEL 1: baker map kneading strip
    # =====================================================================

    y_cursor = TITLE_AREA
    draw.text((PAD_X, y_cursor + 8),
              "Baker map  \u00b7  iterations 0 \u2013 7",
              fill=TEXT, font=f_lg)
    draw.text((PAD_X, y_cursor + 34),
              "Each step: stretch x by 2, halve y, cut the right strip and stack it on top. "
              "Four colored quadrants become bands of bands.",
              fill=MUTED, font=f_sm)

    strip_x0 = PAD_X + (W - 2 * PAD_X - baker_w) // 2
    strip_y0 = y_cursor + BAKER_TITLE

    for k in range(BAKER_COLS * BAKER_ROWS):
        c = k % BAKER_COLS
        r = k // BAKER_COLS
        x = strip_x0 + c * (BAKER_PX + BAKER_GAP)
        y = strip_y0 + r * (BAKER_PX + BAKER_LABEL + BAKER_GAP)

        frame = baker_quadrant_after(BAKER_PX, k)
        # Subtle 1-pixel border so tiles read as discrete cards.
        draw.rectangle([x - 1, y - 1, x + BAKER_PX, y + BAKER_PX], outline=DIM)
        paste_array(out, frame, (x, y))
        label = f"n = {k}"
        if k == 0:
            label += "   (initial)"
        elif k in (3, 4):
            label += "   (kneading)"
        elif k == 7:
            label += "   (\u2248 stripes)"
        col = AMBER if k == 0 else (ICE if k in (3, 4) else (VERDI if k == 7 else MUTED))
        draw.text((x, y + BAKER_PX + 4), label, fill=col, font=f_sm)

    y_cursor = strip_y0 + baker_h

    # =====================================================================
    # PANEL 2: binary expansion grid + trajectory
    # =====================================================================

    draw.text((PAD_X, y_cursor + 16),
              "Doubling map  \u00b7  the dynamics is a left-shift on bits of x\u2080",
              fill=TEXT, font=f_lg)

    y_cursor += MID_TITLE

    # ---- Binary grid ----
    grid_x0 = PAD_X
    grid_y0 = y_cursor
    draw.rectangle([grid_x0, grid_y0, grid_x0 + grid_w, grid_y0 + grid_h], fill=PANEL)

    # Need GRID_ROWS + GRID_COLS - 1 bits so each row can show its bits in
    # a fixed window starting at offset n.
    n_bits = GRID_ROWS + GRID_COLS + 8
    bits = golden_fraction_bits(n_bits)

    inner_x = grid_x0 + GRID_PAD
    inner_y = grid_y0 + GRID_PAD
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            b = bits[r + c]
            x0 = inner_x + c * CELL
            y0 = inner_y + r * CELL
            col = AMBER if b == 1 else (38, 42, 52)
            draw.rectangle([x0, y0, x0 + CELL - 1, y0 + CELL - 1], fill=col)

    # Highlight the "leading bit" column with a thin line: this is the bit
    # that determines which lobe of the baker map a point goes to.
    lead_x = inner_x
    draw.line([lead_x - 2, inner_y - 4,
               lead_x - 2, inner_y + GRID_ROWS * CELL + 2],
              fill=EMBER, width=2)
    draw.text((lead_x + 2, inner_y - 18),
              "leading bit  \u2192  next sign of x \u2212 \u00bd",
              fill=EMBER, font=f_xs)

    # Row labels: just plain "n" values inside the grid panel's right pad.
    label_x = grid_x0 + GRID_PAD + GRID_COLS * CELL + 4
    for r in list(range(0, GRID_ROWS, 10)) + [GRID_ROWS - 1]:
        y0 = inner_y + r * CELL - 1
        draw.text((label_x, y0), str(r), fill=MUTED, font=f_xs)

    # ---- Trajectory plot ----
    traj_x0 = grid_x0 + grid_w + MID_GAP
    traj_y0 = grid_y0
    draw.rectangle([traj_x0, traj_y0, traj_x0 + traj_w, traj_y0 + traj_h], fill=PANEL)

    # Plot xs (using more bits than the grid shows) over N_TRAJ steps.
    N_TRAJ = 400
    bits_long = golden_fraction_bits(N_TRAJ + 56)
    xs = doubling_trajectory(bits_long, N_TRAJ)

    # Plot area inside the panel.
    P_PAD_L, P_PAD_R = 56, 22
    P_PAD_T, P_PAD_B = 32, 46
    px0 = traj_x0 + P_PAD_L
    py0 = traj_y0 + P_PAD_T
    pw  = traj_w - P_PAD_L - P_PAD_R
    ph  = traj_h - P_PAD_T - P_PAD_B

    # Axis frame.
    draw.rectangle([px0, py0, px0 + pw, py0 + ph], outline=GRID)
    # y = 0.5 gridline.
    mid_y = py0 + ph // 2
    draw.line([px0, mid_y, px0 + pw, mid_y], fill=GRID, width=1)

    # x-ticks (every 100 steps), y-ticks (0, 0.5, 1.0).
    for nt in (0, 100, 200, 300, 400):
        xt = px0 + int(nt / N_TRAJ * pw)
        draw.line([xt, py0 + ph, xt, py0 + ph + 4], fill=GRID, width=1)
        draw.text((xt - 9, py0 + ph + 8), str(nt), fill=MUTED, font=f_xs)
    for yv in (0.0, 0.5, 1.0):
        yt = py0 + int((1 - yv) * ph)
        draw.line([px0 - 4, yt, px0, yt], fill=GRID, width=1)
        draw.text((px0 - 32, yt - 6), f"{yv:.1f}", fill=MUTED, font=f_xs)

    # Title strip inside plot.
    draw.text((px0, py0 - 22),
              f"trajectory  x\u2099 = D\u207f(x\u2080),   n = 0 .. {N_TRAJ}",
              fill=TEXT, font=f_sm)
    draw.text((px0, traj_y0 + traj_h - 22),
              "iteration n",
              fill=MUTED, font=f_xs)

    # Scatter the trajectory.
    pts = []
    for i, x_i in enumerate(xs):
        px = px0 + int(i / N_TRAJ * pw)
        py = py0 + int((1 - x_i) * ph)
        pts.append((px, py))
        # color each point by leading bit (above or below 0.5)
        c = AMBER if x_i >= 0.5 else ICE
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=c, outline=None)

    # =====================================================================
    # CAPTION
    # =====================================================================

    cap_y = grid_y0 + grid_h + 24
    draw.text((PAD_X, cap_y),
              "Read the binary grid left-to-right, top-to-bottom. Every row is the previous "
              "row shifted left one cell: the doubling map is a literal shift.",
              fill=TEXT, font=f_sm)
    draw.text((PAD_X, cap_y + 22),
              "Read the dough panel: the baker map carries this same shift on x while "
              "remembering the discarded bit in y. The 2D and 1D pictures are the same dynamics.",
              fill=TEXT, font=f_sm)
    draw.text((PAD_X, cap_y + 48),
              "Whether x\u2099 is above or below \u00bd is just the next bit of x\u2080. "
              "Chaos here is a kind of bookkeeping: every \u201csurprise\u201d was sitting in the initial condition.",
              fill=MUTED, font=f_sm)

    return out


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)
    img = render()
    img.save(os.path.join(out_dir, "baker_doubling.png"))
    print(f"wrote {os.path.join(out_dir, 'baker_doubling.png')}  size {img.size}")
