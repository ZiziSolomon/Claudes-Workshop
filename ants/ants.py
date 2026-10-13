"""Generalized Langton's ants: which turn-rules ever draw a mirror-symmetric picture?
Known observation (Propp et al.): rules whose letters come in consecutive identical
pairs (LLRR, RRLLRR...) give symmetric growth. Test every rule up to length 8."""
import itertools, sys, zlib, struct

DIRS = [(0,-1),(1,0),(0,1),(-1,0)]

def run(rule, steps):
    grid = {}; x = y = 0; d = 0; n = len(rule)
    sym_hits = []
    for t in range(1, steps+1):
        c = grid.get((x,y), 0)
        d = (d + (1 if rule[c]=='R' else -1)) % 4
        grid[(x,y)] = (c+1) % n
        dx, dy = DIRS[d]; x += dx; y += dy
        if t % 500 == 0 and is_symmetric(grid):
            sym_hits.append(t)
    return grid, sym_hits

def is_symmetric(grid):
    pts = {k: v for k, v in grid.items() if v}
    if not pts: return False
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    cx = min(xs)+max(xs); cy = min(ys)+max(ys)
    mirrors = [lambda p:(cx-p[0],p[1]), lambda p:(p[0],cy-p[1])]
    if cx - cy == (min(xs)+max(xs)) - (min(ys)+max(ys)):
        mirrors += [lambda p:(p[1]+(cx-cy)//2, p[0]-(cx-cy)//2) if (cx-cy)%2==0 else None,
                    lambda p:((cx+cy)//2-p[1], (cx+cy)//2-p[0]) if (cx+cy)%2==0 else None]
    for m in mirrors:
        if all(pts.get(m(p)) == v for p, v in pts.items()):
            return True
    return False

def paired(rule):
    return len(rule) % 2 == 0 and all(rule[i]==rule[i+1] for i in range(0,len(rule),2))

def cyc_paired(rule):
    return any(paired(rule[k:]+rule[:k]) for k in range(len(rule)))

def png(grid, n, path, scale=2):
    xs=[p[0] for p in grid]; ys=[p[1] for p in grid]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    w=(x1-x0+1)*scale; h=(y1-y0+1)*scale
    pal=[(250,248,240)]+[tuple(int(40+180*((i*k)%n)/n) for k in (3,5,7)) for i in range(1,n)]
    raw=bytearray()
    for yy in range(y0,y1+1):
        row=bytearray([0])
        for xx in range(x0,x1+1):
            row+=bytes(pal[grid.get((xx,yy),0)])*scale
        raw+=bytes(row)*scale
    def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
    open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))
        +chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b''))

if __name__ == '__main__':
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    seen = set()
    for n in range(2, maxlen+1):
        for rule in map(''.join, itertools.product('LR', repeat=n)):
            if rule[0] != 'R' or len(set(rule)) < 2: continue  # mirror twin / trivial
            # skip rules that are repetitions of a shorter rule
            if any(n % k == 0 and rule == rule[:k]*(n//k) for k in range(1,n)): continue
            g, hits = run(rule, steps)
            frac = len(hits) / (steps//500)
            cp = cyc_paired(rule)
            if hits or cp:
                print(f"{rule:10s} paired={str(paired(rule)):5s} cyclic_paired={str(cp):5s} symmetric_checkpoints={len(hits):3d}/{steps//500} last={hits[-1] if hits else '-'}", flush=True)
            if hits: png(g, n, f"{rule}.png")
