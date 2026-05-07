"""
Diagonal argument visualizer.
Three panels showing the same construction in three domains:
  Cantor  — uncountability of infinite binary sequences
  Turing  — undecidability of the halting problem
  Gödel   — incompleteness of formal arithmetic

In each case: enumerate objects as rows, properties as columns,
read the diagonal, invert it, exhibit the new row that can't be on the list.
"""

import math
from PIL import Image, ImageDraw, ImageFont

# ── palette ──────────────────────────────────────────────────────────────────

BG          = (12,  12,  18)
GRID_BORDER = (40,  40,  55)
CELL_0      = (22,  30,  45)   # value 0 / "no" / "disprovable"
CELL_1      = (28,  45,  65)   # value 1 / "yes" / "provable"
DIAG_0      = (180, 100,  40)  # diagonal cell, value 0  (amber dark)
DIAG_1      = (230, 160,  60)  # diagonal cell, value 1  (amber light)
INVERT_0    = ( 60, 140, 200)  # inverted diagonal, value 0  (ice dark)
INVERT_1    = (100, 190, 240)  # inverted diagonal, value 1  (ice light)
TEXT_MAIN   = (220, 220, 230)
TEXT_DIM    = (100, 110, 130)
TEXT_LABEL  = (200, 170,  80)  # amber label
TEXT_INVERT = (100, 190, 240)  # ice label

PANEL_W     = 560
PANEL_H     = 640
MARGIN      = 40
GAP         = 30   # gap between panels
TOTAL_W     = 3 * PANEL_W + 2 * GAP + 2 * MARGIN
TOTAL_H     = PANEL_H + 2 * MARGIN + 80  # extra bottom for title

N           = 8    # grid dimension (N rows × N cols)
CELL        = 44   # px per cell
BORDER      = 2

def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSansMono-Bold.ttf" if bold else
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()

FONT_SM   = load_font(11)
FONT_MD   = load_font(13)
FONT_LG   = load_font(15, bold=True)
FONT_TITLE= load_font(18, bold=True)
FONT_HEAD = load_font(12)


# ── grid data ─────────────────────────────────────────────────────────────────

# Each panel is defined by:
#   row_labels: list of N strings (what each row represents)
#   col_labels: list of N strings (what each column represents)
#   grid: N×N matrix of 0/1
#   title, subtitle: strings
#   val_labels: ("0_label", "1_label")

import random
rng = random.Random(42)

def cantor_data():
    """Infinite binary sequences; diagonal disproves countability."""
    rows = [f"s{i}" for i in range(N)]
    cols = [f"pos {i+1}" for i in range(N)]
    # Make a visually interesting grid with clear diagonal
    grid = []
    for i in range(N):
        row = [rng.randint(0,1) for _ in range(N)]
        grid.append(row)
    # Set diagonal entries to make inversion dramatic (alternate 0,1)
    for i in range(N):
        grid[i][i] = i % 2
    return {
        "title": "Cantor  (1891)",
        "subtitle": "Every supposed list of infinite\nbinary sequences is incomplete.",
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "row_intro": "Suppose all sequences are listed:",
        "diag_intro": "Diagonal: d\u1d62 = s\u1d62[i]",
        "new_label": "d\u0305",
        "new_intro": "Invert diagonal \u2192 new sequence\nnot equal to any s\u1d62",
        "val_labels": ("0", "1"),
    }

def turing_data():
    """Programs vs. inputs; diagonal constructs a program that defeats any decider."""
    progs = [f"P{i}" for i in range(N)]
    # columns are programs used as their own input
    cols = [f"\u27e8P{i}\u27e9" for i in range(N)]
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            if i == j:
                # diagonal: mix halts and doesn't
                row.append(i % 2)
            else:
                row.append(rng.randint(0,1))
        grid.append(row)
    return {
        "title": "Turing  (1936)",
        "subtitle": "No algorithm decides whether\nan arbitrary program halts.",
        "rows": progs,
        "cols": cols,
        "grid": grid,
        "row_intro": "H(P\u1d62, \u27e8P\u1d62\u27e9) — halts on its own code?",
        "diag_intro": "Diagonal: H(P\u1d62, \u27e8P\u1d62\u27e9)",
        "new_label": "D",
        "new_intro": "D halts iff diagonal says \u201cno halt\u201d\u2192 contradiction for any decider",
        "val_labels": ("loops", "halts"),
    }

def godel_data():
    """Formulas vs. provability predicate; diagonal builds G."""
    fmls = [f"\u03c6{i}" for i in range(N)]
    cols = [f"Prov(\u03c6{i})" for i in range(N)]
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            if i == j:
                row.append(i % 2)
            else:
                row.append(rng.randint(0,1))
        grid.append(row)
    return {
        "title": "Gödel  (1931)",
        "subtitle": "Every consistent system of sufficient\npower has true unprovable sentences.",
        "rows": fmls,
        "cols": cols,
        "grid": grid,
        "row_intro": "Prov(\u03c6\u1d62) — provable in PA?",
        "diag_intro": "Diagonal: Prov(\u03c6\u1d62) for each \u03c6\u1d62",
        "new_label": "G",
        "new_intro": "G \u2194 \u00acProv(\u27e8G\u27e9)\nIf provable: false. If unprovable: true.",
        "val_labels": ("\u00ac Prov", "Prov"),
    }


# ── drawing ───────────────────────────────────────────────────────────────────

def text_centered(draw, text, cx, y, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    w = bb[2] - bb[0]
    draw.text((cx - w // 2, y), text, font=font, fill=fill)

def draw_panel(draw, data, ox, oy):
    """Draw one panel at offset (ox, oy)."""
    grid  = data["grid"]
    rows  = data["rows"]
    cols  = data["cols"]

    # ── title ────────────────────────────────────────────────────────────────
    text_centered(draw, data["title"], ox + PANEL_W // 2, oy, FONT_LG, TEXT_LABEL)
    oy += 28

    # ── subtitle ─────────────────────────────────────────────────────────────
    for line in data["subtitle"].split("\n"):
        text_centered(draw, line, ox + PANEL_W // 2, oy, FONT_SM, TEXT_DIM)
        oy += 16
    oy += 10

    # ── row intro ─────────────────────────────────────────────────────────────
    text_centered(draw, data["row_intro"], ox + PANEL_W // 2, oy, FONT_SM, TEXT_DIM)
    oy += 18

    # ── grid origin ──────────────────────────────────────────────────────────
    grid_x = ox + (PANEL_W - (N + 1) * (CELL + BORDER)) // 2 + CELL + BORDER
    grid_y = oy

    # column headers
    for j, col in enumerate(cols):
        cx = grid_x + j * (CELL + BORDER) + CELL // 2
        draw.text((cx - 12, grid_y - 16), col, font=FONT_SM, fill=TEXT_DIM)

    # rows
    for i in range(N):
        ry = grid_y + i * (CELL + BORDER)
        # row label
        draw.text((ox + PANEL_W // 2 - (N * (CELL + BORDER)) // 2 - 30,
                   ry + CELL // 2 - 7),
                  rows[i], font=FONT_SM, fill=TEXT_DIM)

        for j in range(N):
            val = grid[i][j]
            cx = grid_x + j * (CELL + BORDER)

            on_diagonal = (i == j)
            if on_diagonal:
                color = DIAG_1 if val else DIAG_0
                text_color = BG
            else:
                color = CELL_1 if val else CELL_0
                text_color = TEXT_DIM

            draw.rectangle([cx, ry, cx + CELL - 1, ry + CELL - 1],
                           fill=color, outline=GRID_BORDER)
            label = data["val_labels"][val]
            bb = draw.textbbox((0,0), label, font=FONT_SM)
            tw = bb[2] - bb[0]
            draw.text((cx + CELL // 2 - tw // 2,
                       ry + CELL // 2 - 7),
                      label, font=FONT_SM, fill=text_color)

    grid_bottom = grid_y + N * (CELL + BORDER)

    # ── diagonal label ────────────────────────────────────────────────────────
    oy2 = grid_bottom + 14
    text_centered(draw, data["diag_intro"], ox + PANEL_W // 2, oy2, FONT_SM, TEXT_LABEL)
    oy2 += 20

    # ── inverted row ──────────────────────────────────────────────────────────
    text_centered(draw, data["new_label"] + "  =  inverted diagonal:", ox + PANEL_W // 2, oy2, FONT_SM, TEXT_INVERT)
    oy2 += 18

    for j in range(N):
        diag_val = grid[j][j]
        inv_val  = 1 - diag_val
        cx = grid_x + j * (CELL + BORDER)
        color = INVERT_1 if inv_val else INVERT_0
        draw.rectangle([cx, oy2, cx + CELL - 1, oy2 + CELL - 1],
                       fill=color, outline=GRID_BORDER)
        label = data["val_labels"][inv_val]
        bb = draw.textbbox((0,0), label, font=FONT_SM)
        tw = bb[2] - bb[0]
        draw.text((cx + CELL // 2 - tw // 2,
                   oy2 + CELL // 2 - 7),
                  label, font=FONT_SM, fill=BG)

    oy2 += CELL + 12

    # ── new row explanation ────────────────────────────────────────────────────
    for line in data["new_intro"].split("\n"):
        text_centered(draw, line, ox + PANEL_W // 2, oy2, FONT_SM, TEXT_DIM)
        oy2 += 16

    # ── diagonal annotation: draw line from top-left to bottom-right of grid ──
    for i in range(N):
        cx = grid_x + i * (CELL + BORDER)
        ry = grid_y + i * (CELL + BORDER)
        # small corner markers
        draw.rectangle([cx + CELL - 6, ry + CELL - 6, cx + CELL - 1, ry + CELL - 1],
                       fill=TEXT_LABEL)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    img  = Image.new("RGB", (TOTAL_W, TOTAL_H), BG)
    draw = ImageDraw.Draw(img)

    # overall title
    title = "The Diagonal Argument"
    subtitle = "One construction — three impossibility proofs"
    text_centered(draw, title,    TOTAL_W // 2, 18, FONT_TITLE, TEXT_MAIN)
    text_centered(draw, subtitle, TOTAL_W // 2, 44, FONT_MD,    TEXT_DIM)

    panels = [cantor_data(), turing_data(), godel_data()]

    for k, data in enumerate(panels):
        ox = MARGIN + k * (PANEL_W + GAP)
        oy = MARGIN + 50
        draw_panel(draw, data, ox, oy)

    # bottom legend
    ly = TOTAL_H - 50
    legend = (
        "Amber = diagonal cells     "
        "Ice = inverted diagonal (new object)     "
        "Dark = off-diagonal"
    )
    text_centered(draw, legend, TOTAL_W // 2, ly, FONT_SM, TEXT_DIM)

    out_path = "/home/opc/workshop/code/incompleteness/out/diagonal.png"
    img.save(out_path)
    print(f"Saved {TOTAL_W}×{TOTAL_H} → {out_path}")


if __name__ == "__main__":
    main()
