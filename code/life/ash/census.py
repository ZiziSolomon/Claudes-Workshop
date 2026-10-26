"""Soup census for Conway's Life, pure Python.

Each soup is a 16x16 random square at density 1/2 on the unbounded plane.
It is run until the part that stays near the origin is periodic with a small
period, and every component that has flown away is a spaceship. The final
"ash" is split into connected components and each is identified by its shape
(canonical under the 8 symmetries) and period.

Then the reducibility check: from the settle time T, the future is predicted
*without running Life* -- still lifes stay, oscillators repeat, gliders shift
one cell diagonally per 4 generations -- and the prediction is compared with
an honest simulation a long way further on.

usage: python3 census.py NSOUPS [SEED]
"""
import random
import sys
from collections import Counter
from multiprocessing import Pool

NB = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


def step(cells):
    counts = Counter()
    for (x, y) in cells:
        for dx, dy in NB:
            counts[(x + dx, y + dy)] += 1
    return {c for c, n in counts.items() if n == 3 or (n == 2 and c in cells)}


def components(cells):
    return components_r(cells, 2)


def components_r(cells, rad):
    """8-connected clusters, with a gap of one dead cell still joining them
    (distance <= 2), so that a blinker next to a block is two objects only
    if they are genuinely apart."""
    left = set(cells)
    out = []
    while left:
        seed = left.pop()
        comp = {seed}
        stack = [seed]
        while stack:
            x, y = stack.pop()
            for dx in range(-rad, rad + 1):
                for dy in range(-rad, rad + 1):
                    c = (x + dx, y + dy)
                    if c in left:
                        left.remove(c)
                        comp.add(c)
                        stack.append(c)
        out.append(comp)
    return out


def evolve(cells, k):
    for _ in range(k):
        cells = step(cells)
    return cells


def split_objects(cells, P):
    """Finest partition of a periodic pattern into independently evolving
    parts. Start from 8-connected pieces; merge any pair that interacts
    (evolving them together differs from evolving them apart), repeat."""
    parts = [frozenset(c) for c in components_r(cells, 1)]
    k = 2 * P + 4
    changed = True
    while changed:
        changed = False
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                a, b = parts[i], parts[j]
                if min(max(abs(x - u), abs(y - v)) for x, y in a for u, v in b) > 4:
                    continue
                if any(evolve(set(a | b), t) != evolve(set(a), t) | evolve(set(b), t)
                       for t in (1, 2, k)):
                    parts[i] = a | b
                    del parts[j]
                    changed = True
                    break
            if changed:
                break
    return [set(p) for p in parts]


SYMS = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y),
        lambda x, y: (-x, -y), lambda x, y: (y, x), lambda x, y: (-y, x),
        lambda x, y: (y, -x), lambda x, y: (-y, -x)]


def normalise(cells):
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))


def canon(cells):
    return min(normalise([f(x, y) for x, y in cells]) for f in SYMS)


def period_and_shift(comp, maxp=30):
    """Run an isolated component; return (period, (dx,dy)) or None."""
    base = normalise(comp)
    ox = min(x for x, _ in comp)
    oy = min(y for _, y in comp)
    cur = comp
    for p in range(1, maxp + 1):
        cur = step(cur)
        if not cur:
            return None
        if normalise(cur) == base:
            return p, (min(x for x, _ in cur) - ox, min(y for _, y in cur) - oy)
    return None


def identify(comp):
    """Name an isolated object by the min canonical shape over its phases."""
    ps = period_and_shift(comp)
    if ps is None:
        return None, None
    p, shift = ps
    phases = [comp]
    cur = comp
    for _ in range(p - 1):
        cur = step(cur)
        phases.append(cur)
    key = min(canon(ph) for ph in phases)
    return (key, p, shift != (0, 0)), ps


NAMES = {}


def name_of(key):
    return NAMES.get(key[0], f"{'ship' if key[2] else 'p' + str(key[1])}"
                             f"_{len(key[0])}c")


def _register():
    known = {
        "block": {(0, 0), (0, 1), (1, 0), (1, 1)},
        "blinker": {(0, 0), (1, 0), (2, 0)},
        "beehive": {(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)},
        "loaf": {(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (3, 2), (2, 3)},
        "boat": {(0, 0), (1, 0), (0, 1), (2, 1), (1, 2)},
        "ship": {(0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (2, 2)},
        "tub": {(1, 0), (0, 1), (2, 1), (1, 2)},
        "pond": {(1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (3, 2), (1, 3), (2, 3)},
        "glider": {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)},
        "toad": {(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)},
        "beacon": {(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)},
        "long boat": {(0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (3, 2), (2, 3)},
        "barge": {(1, 0), (0, 1), (2, 1), (1, 2), (3, 2), (2, 3)},
        "mango": {(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (4, 2), (2, 3), (3, 3)},
        "eater 1": {(0, 0), (1, 0), (0, 1), (2, 1), (2, 2), (2, 3), (3, 3)},
        "LWSS": {(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)},
        "pulsar": None, "pentadecathlon": None,
    }
    for n, cells in known.items():
        if cells:
            key, _ = identify(cells)
            NAMES[key[0]] = n


_register()


def run_soup(seed, size=16, maxgen=20000, horizon=2000):
    rng = random.Random(seed)
    cells = {(x, y) for x in range(size) for y in range(size) if rng.random() < 0.5}
    escaped = []          # (key, cells-at-removal, gen)
    M = 24                # margin before a departing ship counts as gone
    history = {}
    T = None
    for g in range(maxgen + 1):
        # Peel off spaceships that have left: outside the bounding box of
        # everything else (plus a margin) on some axis, and moving outward
        # along it. (Heuristic -- the honest re-simulation below checks it.)
        if g % 8 == 0 and cells:
            comps = components(cells)
            if len(comps) > 1:
                gone = []
                for i, comp in enumerate(comps):
                    rest = [c for j, cc in enumerate(comps) if j != i for c in cc]
                    rx0 = min(x for x, _ in rest); rx1 = max(x for x, _ in rest)
                    ry0 = min(y for _, y in rest); ry1 = max(y for _, y in rest)
                    cx0 = min(x for x, _ in comp); cx1 = max(x for x, _ in comp)
                    cy0 = min(y for _, y in comp); cy1 = max(y for _, y in comp)
                    out = (cx0 > rx1 + M, cx1 < rx0 - M, cy0 > ry1 + M, cy1 < ry0 - M)
                    if not any(out):
                        continue
                    key, ps = identify(comp)
                    if key is None or not key[2]:
                        continue
                    dx, dy = ps[1]
                    if (out[0] and dx > 0) or (out[1] and dx < 0) or \
                       (out[2] and dy > 0) or (out[3] and dy < 0):
                        gone.append(i)
                        escaped.append((key, frozenset(comp), g, ps))
                if gone:
                    cells = set().union(*(c for i, c in enumerate(comps) if i not in gone))
        h = frozenset(cells)
        if h in history:
            T = history[h]   # first time this state was seen
            P = g - T
            break
        history[h] = g
        if len(history) > 64:   # only remember the recent past (periods <= 64)
            del history[next(iter(history))]
        cells = step(cells)
    if T is None:
        return dict(seed=seed, settled=False)

    # The ash at gen g (state repeats with period P from T on).
    ash = split_objects(cells, P)
    objs = []
    for comp in ash:
        key, ps = identify(comp)
        objs.append((key, comp, ps))
    unknown = [o for o in objs if o[0] is None]

    # Reducibility check: predict the far future of everything (ash + ships)
    # by object-level rules alone, then compare with simulation.
    G = g + horizon
    def advance(comp, ps, k):
        p, (dx, dy) = ps
        q, r = divmod(k, p)
        cur = comp
        for _ in range(r):
            cur = step(cur)
        return {(x + q * dx, y + q * dy) for x, y in cur}
    predicted = set()
    ok = not unknown
    if ok:
        for key, comp, ps in objs:
            predicted |= advance(comp, ps, G - g)
        for key, comp, g0, ps in escaped:
            predicted |= advance(set(comp), ps, G - g0)
    # honest simulation: rerun from scratch with nothing removed
    rng = random.Random(seed)
    sim = {(x, y) for x in range(size) for y in range(size) if rng.random() < 0.5}
    for _ in range(G):
        sim = step(sim)
    return dict(seed=seed, settled=True, T=T, P=P,
                ash=Counter(name_of(o[0]) if o[0] else "??" for o in objs),
                ships=Counter(name_of(e[0]) for e in escaped),
                ship_times=[e[2] for e in escaped],
                predicted_ok=(ok and predicted == sim), G=G,
                simpop=len(sim))


if __name__ == "__main__":
    n = int(sys.argv[1])
    s0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    with Pool() as pool:
        res = pool.map(run_soup, range(s0, s0 + n), chunksize=4)
    import json
    json.dump(res, open(f"census_{s0}_{n}.json", "w"), default=dict)
    settled = [r for r in res if r["settled"]]
    ash = Counter(); ships = Counter()
    for r in settled:
        ash.update(r["ash"]); ships.update(r["ships"])
    print(f"{len(settled)}/{n} settled")
    print("ash:", ash.most_common(25))
    print("ships:", ships.most_common())
    print("predicted ok:", sum(r["predicted_ok"] for r in settled))
    Ts = sorted(r["T"] for r in settled)
    print("T quartiles:", Ts[len(Ts)//4], Ts[len(Ts)//2], Ts[3*len(Ts)//4], Ts[-1])
