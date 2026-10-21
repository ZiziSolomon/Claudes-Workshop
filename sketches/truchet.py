"""Quarter-arc Truchet tiling, seeded, written as SVG."""
import random
random.seed(5)
N, S = 24, 32
W = N * S
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}"><rect width="{W}" height="{W}" fill="#f4efe6"/>',
       '<g fill="none" stroke="#c4472d" stroke-width="5" stroke-linecap="round">']
h = S / 2
for i in range(N):
    for j in range(N):
        x, y = i * S, j * S
        if random.random() < 0.5:
            out.append(f'<path d="M{x+h},{y} A{h},{h} 0 0 1 {x},{y+h} M{x+S},{y+h} A{h},{h} 0 0 0 {x+h},{y+S}"/>')
        else:
            out.append(f'<path d="M{x+h},{y} A{h},{h} 0 0 0 {x+S},{y+h} M{x},{y+h} A{h},{h} 0 0 1 {x+h},{y+S}"/>')
out.append('</g></svg>')
open("truchet.svg", "w").write("\n".join(out))
