"""Re-check the non-cyclically-paired rules (length <= 8) for symmetry at EVERY step,
since ants.py only samples every 500 steps. Reports each rule's last symmetric step."""
import itertools, sys
from ants import DIRS, is_symmetric, cyc_paired
steps = int(sys.argv[1])
worst = 0
for n in range(2, 9):
    for r in map(''.join, itertools.product('LR', repeat=n)):
        if r[0] != 'R' or len(set(r)) < 2 or cyc_paired(r): continue
        if any(n % k == 0 and r == r[:k]*(n//k) for k in range(1, n)): continue
        grid = {}; x = y = 0; d = 0; last = 0
        for t in range(1, steps+1):
            c = grid.get((x,y), 0)
            d = (d + (1 if r[c]=='R' else -1)) % 4
            grid[(x,y)] = (c+1) % n
            x += DIRS[d][0]; y += DIRS[d][1]
            if is_symmetric(grid): last = t
        worst = max(worst, last)
        if last > 200: print(r, 'last symmetric step', last, flush=True)
print('latest symmetric step of any non-paired rule:', worst)
