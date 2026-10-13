"""Find 'rebirths': steps where the symmetric-time pattern of the first moves repeats."""
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
hs = set(hits)
# a burst = run of >=8 consecutive symmetric steps; report its start and length
starts = []; i = 0
while i < len(hits):
    j = i
    while j+1 < len(hits) and hits[j+1] == hits[j]+1: j += 1
    if j - i + 1 >= 8: starts.append((hits[i], j-i+1))
    i = j+1
print(rule, 'bursts (start,len):', starts)
print('gaps:', [b[0]-a[0] for a, b in zip(starts, starts[1:])])
late=[h for h in hits if h>1000]; print("late hits:",len(late),"mod 4 counts:",[sum(h%4==k for h in late) for k in range(4)], "last:", late[-3:])
