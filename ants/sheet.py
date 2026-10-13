"""Contact sheet: every cyclically paired rule up to length 8, at a symmetric moment."""
import itertools, zlib, struct
from ants import run, cyc_paired

T, PAD, COLS = 120, 6, 6
rules = [r for n in range(4, 9) for r in map(''.join, itertools.product('LR', repeat=n))
         if r[0] == 'R' and cyc_paired(r)
         and not any(n % k == 0 and r == r[:k]*(n//k) for k in range(1, n))]
tiles = []
for r in rules:
    g, h = run(r, 20000)
    g, _ = run(r, h[-1])
    n = len(r)
    xs = [p[0] for p in g]; ys = [p[1] for p in g]
    x0, y0 = min(xs), min(ys)
    side = max(max(xs)-x0, max(ys)-y0) + 1
    ox = (side - (max(xs)-x0+1)) // 2; oy = (side - (max(ys)-y0+1)) // 2
    pal = [(250,248,240)] + [tuple(int(40+180*((i*k) % n)/n) for k in (3,5,7)) for i in range(1, n)]
    tile = [[pal[g.get((x0 - ox + px*side//T, y0 - oy + py*side//T), 0)] for px in range(T)] for py in range(T)]
    tiles.append(tile); print(r, h[-1], side)
rows = (len(tiles) + COLS - 1) // COLS
W = COLS*(T+PAD)+PAD; H = rows*(T+PAD)+PAD
img = [[(30,30,34)]*W for _ in range(H)]
for i, tile in enumerate(tiles):
    bx = PAD + (i % COLS)*(T+PAD); by = PAD + (i//COLS)*(T+PAD)
    for py in range(T): img[by+py][bx:bx+T] = tile[py]
raw = b''.join(b'\0' + bytes(c for px in row for c in px) for row in img)
def chunk(t, d): return struct.pack('>I', len(d))+t+d+struct.pack('>I', zlib.crc32(t+d))
open('sheet.png', 'wb').write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
    + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
print('order:', ' '.join(rules))
