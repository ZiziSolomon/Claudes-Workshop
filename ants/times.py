"""Exact steps at which a rule's pattern is mirror-symmetric (checked every step)."""
import sys
from ants import DIRS, is_symmetric
rule = sys.argv[1]; steps = int(sys.argv[2])
grid = {}; x = y = 0; d = 0; n = len(rule); hits = []
for t in range(1, steps+1):
    c = grid.get((x,y), 0)
    d = (d + (1 if rule[c]=='R' else -1)) % 4
    grid[(x,y)] = (c+1) % n
    x += DIRS[d][0]; y += DIRS[d][1]
    if is_symmetric(grid): hits.append(t)
print(rule, len(hits), hits)
