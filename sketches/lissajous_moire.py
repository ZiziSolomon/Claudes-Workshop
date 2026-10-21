"""Overlay of two slightly detuned Lissajous curves -> moire-like SVG."""
import math, colorsys

W = 800
def curve(a, b, phase, n=2000, r=360):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        pts.append((W/2 + r*math.sin(a*t + phase), W/2 + r*math.sin(b*t)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}"><rect width="{W}" height="{W}" fill="#0e1116"/>']
for k in range(24):
    ph = k * math.pi / 48
    r,g,b = colorsys.hls_to_rgb((200+k*6)%360/360, 0.6, 0.8); col = "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))
    parts.append(f'<path d="{curve(7, 8, ph)}" fill="none" stroke="{col}" stroke-width="0.6" opacity="0.55"/>')
parts.append('</svg>')
open("lissajous_moire.svg", "w").write("\n".join(parts))
