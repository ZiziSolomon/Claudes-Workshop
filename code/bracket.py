"""Kauffman bracket / Jones polynomial from PD codes, to see what an invariant can and can't tell apart."""
import itertools
from collections import defaultdict
# Laurent polynomials in A as {exponent: coeff}
def mul(p, q):
    r = defaultdict(int)
    for i, a in p.items():
        for j, b in q.items(): r[i + j] += a * b
    return {k: v for k, v in r.items() if v}
def add(p, q):
    r = defaultdict(int, p)
    for k, v in q.items(): r[k] += v
    return {k: v for k, v in r.items() if v}
def pw(p, n):
    r = {0: 1}
    for _ in range(n): r = mul(r, p)
    return r
d = {2: -1, -2: -1}

def loops(pairs):
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in pairs: parent[find(a)] = find(b)
    return len({find(x) for x in list(parent)})

def jones(pd):
    br = {}
    for s in itertools.product([0, 1], repeat=len(pd)):
        pairs = []
        for (a, b, c, e), t in zip(pd, s):
            pairs += [(a, b), (c, e)] if t == 0 else [(a, e), (b, c)]
        na = s.count(0); nb = s.count(1)
        br = add(br, mul({na - nb: 1}, pw(d, loops(pairs) - 1)))
    w = sum(1 if (j - l == 1 or l - j > 1) else -1 for _, j, _, l in pd)
    return mul({-3 * w: -1 if w % 2 else 1}, br)

def mirror(pd): return [(b, c, e, a) for a, b, c, e in pd]
def t(p):  # A = t^(-1/4)
    return ' '.join(f"{v:+d}t^{-k/4:g}" for k, v in sorted(p.items(), key=lambda kv: -kv[0]))
    return sp.expand(poly.subs(A, sp.Symbol('t')**sp.Rational(-1, 4)))

# Only the trefoil is included: a figure-eight PD I typed from memory gave writhe 2 (should be 0),
# so it was wrong, and I dropped it rather than fiddle with the writhe rule until it "worked".
tref = [(1,4,2,5),(3,6,4,1),(5,2,6,3)]
print('trefoil       ', t(jones(tref)))
print('mirror trefoil', t(jones(mirror(tref))))
