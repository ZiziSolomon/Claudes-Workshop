"""
Wolfram elementary cellular automata — space-time diagrams.

A 1D cellular automaton with two states (0/1) and a neighborhood of 3 cells
has 2^(2^3) = 256 possible rules. Wolfram indexed them by their rule number.
Rule 110 is Turing complete. Rule 30 passes statistical randomness tests.
Rule 90 produces the Sierpiński triangle.

The space-time diagram renders each generation as a row of pixels,
time flowing downward. What emerges is immediately visible — structure, complexity,
or chaos — arising from a single row of initial conditions.
"""

import numpy as np
from PIL import Image, ImageDraw
import os

BG = (10, 10, 18)

def make_rule(n):
    """Return a lookup table for rule n: maps (left, center, right) -> next_state."""
    bits = [(n >> i) & 1 for i in range(8)]
    table = {}
    for i in range(8):
        left   = (i >> 2) & 1
        center = (i >> 1) & 1
        right  = (i >> 0) & 1
        table[(left, center, right)] = bits[i]
    return table

def apply_rule(row, table):
    n = len(row)
    new = np.zeros(n, dtype=np.uint8)
    for i in range(n):
        l = row[(i - 1) % n]
        c = row[i]
        r = row[(i + 1) % n]
        new[i] = table[(int(l), int(c), int(r))]
    return new

def run_ca(width, steps, rule_n, init='single'):
    table = make_rule(rule_n)
    row = np.zeros(width, dtype=np.uint8)
    if init == 'single':
        row[width // 2] = 1
    elif init == 'random':
        rng = np.random.default_rng(42)
        row = rng.integers(0, 2, width, dtype=np.uint8)

    rows = [row]
    for _ in range(steps - 1):
        row = apply_rule(row, table)
        rows.append(row)
    return np.array(rows)  # shape: (steps, width)

def render_spacetime(grid, color, scale=2):
    """Render a space-time diagram. grid shape: (rows, cols)."""
    h, w = grid.shape
    img = Image.new('RGB', (w * scale, h * scale), BG)
    draw = ImageDraw.Draw(img)
    for r in range(h):
        for c in range(w):
            if grid[r, c]:
                x0, y0 = c * scale, r * scale
                draw.rectangle([x0, y0, x0 + scale - 1, y0 + scale - 1], fill=color)
    return img

def gallery():
    out = 'out'
    os.makedirs(out, exist_ok=True)

    width = 400
    steps = 250
    scale = 2

    RULES = [
        (30,  'random',  (255, 100, 80),  'Rule 30 — chaos (used as RNG)'),
        (90,  'single',  (80, 160, 255),  'Rule 90 — Sierpiński triangle'),
        (110, 'single',  (60, 220, 120),  'Rule 110 — Turing complete'),
        (18,  'single',  (200, 120, 255), 'Rule 18 — nested triangles'),
        (54,  'single',  (255, 190, 60),  'Rule 54 — complex/localized'),
        (184, 'random',  (60, 210, 200),  'Rule 184 — traffic flow model'),
    ]

    panel_w = width * scale
    panel_h = steps * scale
    label_h = 22
    sep = 14

    total_w = panel_w + 20
    total_h = len(RULES) * (panel_h + label_h + sep) + sep
    canvas = Image.new('RGB', (total_w, total_h), BG)
    draw = ImageDraw.Draw(canvas)

    y = sep
    for rule_n, init, color, title in RULES:
        print(f"Rule {rule_n}...")
        grid = run_ca(width, steps, rule_n, init)
        panel = render_spacetime(grid, color, scale)

        draw.text((10, y), title, fill=(160, 160, 190))
        canvas.paste(panel, (10, y + label_h))

        # Save individual
        panel.save(os.path.join(out, f'rule{rule_n:03d}.png'))

        y += panel_h + label_h + sep

    path = os.path.join(out, 'wolfram_gallery.png')
    canvas.save(path)
    print(f"Saved {path} ({canvas.width}x{canvas.height})")

if __name__ == '__main__':
    gallery()
