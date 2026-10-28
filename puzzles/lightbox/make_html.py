"""Render set.json as a printable page: puzzles first, then solutions with the
clued beams drawn through the box.   python3 make_html.py  -> lightbox.html"""
import json

from lightbox import DR, DC, TURN, exit_port, labels, ports, trace

S = 44          # cell size
M = 34          # margin for edge labels
COLOURS = ["#d1495b", "#00798c", "#edae49", "#66a182", "#8d6cab",
           "#2e4057", "#e07a5f", "#3d405b", "#81b29a", "#c06c84"]


def port_xy(n, p):
    side, i = p
    mid = M + S * i + S / 2
    return {"T": (mid, M - 14), "B": (mid, M + n * S + 20),
            "L": (M - 16, mid + 5), "R": (M + n * S + 16, mid + 5)}[side]


def beam_points(n, grid, p):
    """Polyline for the beam entering at port p, from outside to outside."""
    _, (r, c), d = next(x for x in ports(n) if x[0] == p)
    cx = lambda r, c: (M + S * c + S / 2, M + S * r + S / 2)
    x, y = cx(r, c)
    pts = [(x - DC[d] * S * 0.6, y - DR[d] * S * 0.6)]
    while True:
        if grid[r][c]:
            pts.append(cx(r, c))
            d = TURN[grid[r][c]][d]
        if exit_port(n, r, c, d):
            x, y = cx(r, c)
            pts.append((x + DC[d] * S * 0.6, y + DR[d] * S * 0.6))
            return pts
        r, c = r + DR[d], c + DC[d]


def svg(n, clues, grid=None):
    size = 2 * M + n * S
    out = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">']
    for i in range(n + 1):
        w = 2 if i in (0, n) else 0.6
        a, b = M + i * S, M + n * S
        out.append(f'<line x1="{M}" y1="{a}" x2="{b}" y2="{a}" stroke="#333" stroke-width="{w}"/>')
        out.append(f'<line x1="{a}" y1="{M}" x2="{a}" y2="{b}" stroke="#333" stroke-width="{w}"/>')
    lab = labels(n, clues)
    if grid:
        beams, covered = [], set()
        for kind, p, v in clues:
            if p not in covered:
                beams.append(p)
                covered.update([p, trace(grid, p)[0]])
        for j, p in enumerate(beams):
            pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in beam_points(n, grid, p))
            out.append(f'<polyline points="{pts}" fill="none" stroke="{COLOURS[j % len(COLOURS)]}" '
                       f'stroke-width="3" stroke-opacity="0.75" stroke-linejoin="round"/>')
        for r in range(n):
            for c in range(n):
                t = grid[r][c]
                if not t:
                    continue
                x0, y0, k = M + c * S, M + r * S, 7
                if t == 1:
                    x1, y1, x2, y2 = x0 + k, y0 + S - k, x0 + S - k, y0 + k
                else:
                    x1, y1, x2, y2 = x0 + k, y0 + k, x0 + S - k, y0 + S - k
                out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                           f'stroke="#111" stroke-width="5" stroke-linecap="round"/>')
    for p, text in lab.items():
        x, y = port_xy(n, p)
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="16" '
                   f'font-family="Georgia, serif">{text}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    done = json.load(open("set.json"))
    items = []
    for i in sorted(done, key=int):
        n, k, g, clues = done[i]
        clues = [(kind, tuple(p), tuple(v) if kind == "pair" else v)
                 for kind, p, v in clues]
        items.append((i, n, k, g, clues))
    css = """body{font-family:Georgia,serif;max-width:900px;margin:2em auto;color:#222}
.grid{display:flex;flex-wrap:wrap;gap:28px}
figure{margin:0}figcaption{text-align:center;font-size:14px}
h2{page-break-before:always}h2:first-of-type{page-break-before:auto}"""
    html = [f"<!doctype html><meta charset='utf-8'><title>Lightbox</title><style>{css}</style>",
            "<h1>Lightbox</h1>",
            "<p>Each box hides some diagonal mirrors (<code>/</code> or <code>\\</code>), "
            "at most one per cell; the count is given. Light shone in at one letter "
            "leaves at the matching letter. A number is how many mirrors that beam "
            "bounces off. Find every mirror.</p>",
            "<h2>Puzzles</h2><div class='grid'>"]
    for i, n, k, g, clues in items:
        html.append(f"<figure>{svg(n, clues)}<figcaption>{i}. {k} mirrors</figcaption></figure>")
    html.append("</div><h2>Solutions</h2><div class='grid'>")
    for i, n, k, g, clues in items:
        html.append(f"<figure>{svg(n, clues, g)}<figcaption>{i}.</figcaption></figure>")
    html.append("</div>")
    open("lightbox.html", "w").write("\n".join(html))


if __name__ == "__main__":
    main()
