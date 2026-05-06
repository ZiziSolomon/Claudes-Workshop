"""
Conway's Game of Life simulator and gallery renderer.

Shows emergence: complex patterns arising from local rules with no global coordination.
Each cell follows the same four rules; no cell knows about the global pattern it's part of.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# --- Simulation ---

def neighbors(grid):
    n = np.zeros_like(grid, dtype=np.int32)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            n += np.roll(np.roll(grid, di, axis=0), dj, axis=1)
    return n

def step(grid):
    n = neighbors(grid)
    alive = grid.astype(bool)
    return (alive & ((n == 2) | (n == 3))) | (~alive & (n == 3))

def run(grid, steps):
    frames = [grid.copy()]
    for _ in range(steps):
        grid = step(grid)
        frames.append(grid.copy())
    return frames

def population(grid):
    return int(grid.sum())

# --- Pattern definitions ---

def make_grid(h, w):
    return np.zeros((h, w), dtype=bool)

def place(grid, pattern, row, col):
    for r, c in pattern:
        grid[row + r, col + c] = True
    return grid

GLIDER = [(0,1),(1,2),(2,0),(2,1),(2,2)]

R_PENTOMINO = [(0,1),(0,2),(1,0),(1,1),(2,1)]

ACORN = [(0,1),(1,3),(2,0),(2,1),(2,4),(2,5),(2,6)]

# Gosper Glider Gun
GOSPER_GUN = [
    (0,24),
    (1,22),(1,24),
    (2,12),(2,13),(2,20),(2,21),(2,34),(2,35),
    (3,11),(3,15),(3,20),(3,21),(3,34),(3,35),
    (4,0),(4,1),(4,10),(4,16),(4,20),(4,21),
    (5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),
    (6,10),(6,16),(6,24),
    (7,11),(7,15),
    (8,12),(8,13),
]

def random_soup(h, w, density=0.35, seed=42):
    rng = np.random.default_rng(seed)
    return rng.random((h, w)) < density

# --- Rendering ---

CELL = 3      # pixels per cell
GAP = 1       # gap between cells
BORDER = 8    # border around each panel
PANEL_SEP = 12

BG = (10, 10, 18)
ALIVE_COLORS = {
    'blue':  (80, 160, 255),
    'amber': (255, 180, 60),
    'green': (60, 220, 120),
    'red':   (255, 90, 90),
    'teal':  (60, 210, 200),
}

def render_grid(grid, color_name='blue', max_h=None, max_w=None):
    g = grid.astype(np.uint8)
    h, w = g.shape
    if max_h:
        h = min(h, max_h)
        g = g[:h]
    if max_w:
        w = min(w, max_w)
        g = g[:, :w]

    px_h = h * (CELL + GAP) - GAP + 2 * BORDER
    px_w = w * (CELL + GAP) - GAP + 2 * BORDER

    img = Image.new('RGB', (px_w, px_h), BG)
    draw = ImageDraw.Draw(img)

    color = ALIVE_COLORS[color_name]
    for r in range(h):
        for c in range(w):
            if g[r, c]:
                x = BORDER + c * (CELL + GAP)
                y = BORDER + r * (CELL + GAP)
                draw.rectangle([x, y, x + CELL - 1, y + CELL - 1], fill=color)
    return img

def render_strip(frames_at_gens, grid_h, grid_w, color_name, title, gen_labels):
    """Render a horizontal strip: one row of panels at different generations."""
    panels = []
    for frame in frames_at_gens:
        panels.append(render_grid(frame, color_name, max_h=grid_h, max_w=grid_w))

    panel_w = panels[0].width
    panel_h = panels[0].height
    label_h = 20
    strip_w = len(panels) * panel_w + (len(panels) - 1) * PANEL_SEP + 120
    strip_h = panel_h + label_h + 30

    strip = Image.new('RGB', (strip_w, strip_h), BG)
    draw = ImageDraw.Draw(strip)

    # Title on the left
    draw.text((4, panel_h // 2 + label_h // 2), title, fill=(180, 180, 200))

    x = 115
    for i, (panel, label) in enumerate(zip(panels, gen_labels)):
        strip.paste(panel, (x, label_h))
        draw.text((x + panel_w // 2 - len(label) * 3, 4), label, fill=(120, 120, 150))
        x += panel_w + PANEL_SEP

    return strip

def vstack(strips, sep=16):
    w = max(s.width for s in strips)
    h = sum(s.height for s in strips) + (len(strips) - 1) * sep
    img = Image.new('RGB', (w, h), BG)
    y = 0
    for s in strips:
        img.paste(s, (0, y))
        y += s.height + sep
    return img

# --- Gallery ---

def gallery():
    out = 'out'
    os.makedirs(out, exist_ok=True)
    strips = []

    # 1. Glider — period 4, moves (1,1) per period
    print("Glider...")
    G = 64
    grid = make_grid(G, G)
    place(grid, GLIDER, 2, 2)
    frames = run(grid, 100)
    sel = [frames[g] for g in [0, 4, 12, 28, 60, 100]]
    labels = ['gen 0', 'gen 4', 'gen 12', 'gen 28', 'gen 60', 'gen 100']
    strips.append(render_strip(sel, G, G, 'blue', 'Glider', labels))

    # 2. R-pentomino — 5 cells, takes 1103 gens to stabilize, produces 8 gliders
    print("R-pentomino...")
    G = 80
    grid = make_grid(G, G)
    place(grid, R_PENTOMINO, 35, 35)
    frames = run(grid, 500)
    sel = [frames[g] for g in [0, 20, 100, 250, 500]]
    labels = ['gen 0', 'gen 20', 'gen 100', 'gen 250', 'gen 500']
    strips.append(render_strip(sel, G, G, 'amber', 'R-pentomino', labels))

    # 3. Acorn — 7 cells, takes 5206 gens to fully stabilize
    print("Acorn...")
    G = 90
    grid = make_grid(G, G)
    place(grid, ACORN, 40, 25)
    frames = run(grid, 600)
    pops = [population(f) for f in frames]
    sel = [frames[g] for g in [0, 50, 200, 400, 600]]
    labels = [f'gen {g}\npop={pops[g]}' for g in [0, 50, 200, 400, 600]]
    labels = [f'gen {g}' for g in [0, 50, 200, 400, 600]]
    strips.append(render_strip(sel, G, G, 'green', 'Acorn', labels))

    # 4. Gosper Glider Gun — infinite growth, produces one glider per 30 gens
    print("Gosper Gun...")
    H, W = 60, 120
    grid = make_grid(H, W)
    place(grid, GOSPER_GUN, 10, 10)
    frames = run(grid, 180)
    sel = [frames[g] for g in [0, 30, 60, 120, 180]]
    labels = ['gen 0', 'gen 30', 'gen 60', 'gen 120', 'gen 180']
    strips.append(render_strip(sel, H, W, 'teal', 'Gosper Gun', labels))

    # 5. Random soup — emergence of stable islands from chaos
    print("Random soup...")
    H, W = 70, 70
    grid = random_soup(H, W, density=0.38)
    frames = run(grid, 300)
    pops = [population(f) for f in frames]
    sel = [frames[g] for g in [0, 5, 20, 80, 200, 300]]
    labels = [f'gen {g}' for g in [0, 5, 20, 80, 200, 300]]
    strips.append(render_strip(sel, H, W, 'red', 'Random soup', labels))

    gallery_img = vstack(strips, sep=20)
    path = os.path.join(out, 'life_gallery.png')
    gallery_img.save(path)
    print(f"Saved {path} ({gallery_img.width}x{gallery_img.height})")

    # Individual saves for the most interesting
    frames_r = run(make_grid(80, 80), 0)
    grid2 = make_grid(80, 80)
    place(grid2, R_PENTOMINO, 35, 35)
    for gen in [0, 50, 200, 500, 1000]:
        g = make_grid(80, 80)
        place(g, R_PENTOMINO, 35, 35)
        for _ in range(gen):
            g = step(g)
        img = render_grid(g, 'amber', 80, 80)
        img.save(os.path.join(out, f'rpentomino_gen{gen:04d}.png'))
    print("R-pentomino series saved.")

    return gallery_img

if __name__ == '__main__':
    gallery()
