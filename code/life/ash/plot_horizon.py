"""SVG of horizon.py output: population vs cells already in known objects.

usage: python3 plot_horizon.py horizon_seed0.txt out.svg
"""
import sys

rows = []
for line in open(sys.argv[1]):
    p = line.split()
    if len(p) == 4:
        rows.append(tuple(map(int, p)))
T = next((t for t, h, _, _ in rows if h > 0), None)

W, H = 760, 340
L, R, TOP, B = 56, 24, 48, 44
tmax = rows[-1][0]
pmax = max(r[2] for r in rows)
pmax = ((pmax // 100) + 1) * 100
X = lambda t: L + (W - L - R) * t / tmax
Y = lambda v: TOP + (H - TOP - B) * (1 - v / pmax)

ink, ink2, surf, blue, grey = "#0b0b0b", "#52514e", "#fcfcfb", "#2a78d6", "#c9c8c2"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
     f'font-family="Helvetica, Arial, sans-serif">',
     f'<rect width="{W}" height="{H}" fill="{surf}"/>',
     f'<text x="{L}" y="22" font-size="15" fill="{ink}">Soup {sys.argv[1].split("seed")[-1].split(".")[0].replace("_truncated", " (run cut off before it settled)")}: '
     f'how much of the pattern is already a named object</text>']
for v in range(0, pmax + 1, 100):
    o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#e6e5e0"/>')
    o.append(f'<text x="{L-8}" y="{Y(v)+4:.1f}" font-size="11" text-anchor="end" fill="{ink2}">{v}</text>')
step = 250 if tmax > 1000 else 100
for t in range(0, tmax + 1, step):
    o.append(f'<text x="{X(t):.1f}" y="{H-B+18}" font-size="11" text-anchor="middle" fill="{ink2}">{t}</text>')
o.append(f'<text x="{(L+W-R)/2}" y="{H-8}" font-size="11" text-anchor="middle" fill="{ink2}">generation</text>')
o.append(f'<text x="14" y="{(TOP+H-B)/2}" font-size="11" fill="{ink2}" '
         f'transform="rotate(-90 14 {(TOP+H-B)/2})" text-anchor="middle">live cells</text>')

def path(col):
    return "M" + " L".join(f"{X(r[0]):.1f},{Y(r[col]):.1f}" for r in rows)
o.append(f'<path d="{path(2)}" fill="none" stroke="{grey}" stroke-width="2"/>')
o.append(f'<path d="{path(3)}" fill="none" stroke="{blue}" stroke-width="2"/>')
if T is not None:
    o.append(f'<line x1="{X(T):.1f}" x2="{X(T):.1f}" y1="{TOP}" y2="{H-B}" stroke="{ink2}" stroke-dasharray="3 3"/>')
    o.append(f'<text x="{X(T)-6:.1f}" y="{TOP+12}" font-size="11" text-anchor="end" fill="{ink}">'
             f'gen {T}: object list predicts the rest exactly</text>')
# legend + direct labels
o.append(f'<rect x="{W-R-250}" y="30" width="12" height="3" fill="{grey}"/>'
         f'<text x="{W-R-234}" y="35" font-size="11" fill="{ink2}">all live cells</text>')
o.append(f'<rect x="{W-R-150}" y="30" width="12" height="3" fill="{blue}"/>'
         f'<text x="{W-R-134}" y="35" font-size="11" fill="{ink2}">in known objects</text>')
o.append("</svg>")
open(sys.argv[2], "w").write("\n".join(o))
