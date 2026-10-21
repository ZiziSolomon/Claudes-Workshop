"""Draw a creek centreline before and after a flood cutoff, as SVG.
Old bed (1931) is a meander; the flood (1975) takes a shortcut across the neck.
Usage: python3 meander.py > creek.svg"""
import math
W, H = 600, 300
def bed(amp):
    return [(x, 150 + amp * math.sin(x / 55) * math.exp(-((x - 300) / 260) ** 2)) for x in range(0, 601, 4)]
old = bed(95)
new = [(x, 150 + (95 * math.sin(x / 55) if x < 215 or x > 385 else 95 * math.sin(215 / 55) + (x - 215) * (95 * math.sin(385 / 55) - 95 * math.sin(215 / 55)) / 170) * math.exp(-((x - 300) / 260) ** 2)) for x in range(0, 601, 4)]
pl = lambda p: " ".join(f"{x},{y:.1f}" for x, y in p)
print(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="12">
<rect width="{W}" height="{H}" fill="#f4efe2"/>
<polyline points="{pl(old)}" fill="none" stroke="#9ab" stroke-width="3" stroke-dasharray="6 4"/>
<polyline points="{pl(new)}" fill="none" stroke="#2a6f97" stroke-width="4"/>
<text x="12" y="20" fill="#556">dashed: 1931 deed line (old bed)   solid: creek after 1975 flood</text>
<text x="12" y="290" fill="#556">the strip between them: Dalton's corn, Reyes's plums</text>
</svg>''')
