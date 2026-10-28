"""Lightbox: hidden-mirror puzzles, generated and checked for unique solutions.

A square box holds some two-sided diagonal mirrors ('/' or '\\'), one per cell
at most. Light fired into the box from an edge port travels straight until it
meets a mirror, turns 90 degrees, and eventually leaves through another port.

Clues around the edge:
  - a LETTER pair: light entering at one letter leaves at the other.
  - a NUMBER: the light that enters (or leaves) here bounces off exactly that
    many mirrors along its path.
The total number of mirrors is always given.

Usage:  python3 lightbox.py [seed]     -> writes puzzles.md and solutions.md
"""
import random
import sys
import z3

# directions: 0 = S (down), 1 = W, 2 = N (up), 3 = E
DR = [1, 0, -1, 0]
DC = [0, -1, 0, 1]
# turn tables: new direction after hitting a mirror while moving in d
SLASH = {3: 2, 2: 3, 1: 0, 0: 1}      # '/'
BACK = {3: 0, 0: 3, 1: 2, 2: 1}       # '\'
TURN = {1: SLASH, 2: BACK}


def ports(n):
    """Port list: (name, entry cell, entry direction)."""
    out = []
    for c in range(n):
        out.append((("T", c), (0, c), 0))
    for r in range(n):
        out.append((("R", r), (r, n - 1), 1))
    for c in range(n):
        out.append((("B", c), (n - 1, c), 2))
    for r in range(n):
        out.append((("L", r), (r, 0), 3))
    return out


def exit_port(n, r, c, d):
    """Port reached when leaving cell (r,c) moving in d, or None if still inside."""
    nr, nc = r + DR[d], c + DC[d]
    if 0 <= nr < n and 0 <= nc < n:
        return None
    return {0: ("B", c), 1: ("L", r), 2: ("T", c), 3: ("R", r)}[d]


def trace(grid, port):
    n = len(grid)
    _, (r, c), d = next(p for p in ports(n) if p[0] == port)
    bounces = 0
    while True:
        t = grid[r][c]
        if t:
            d = TURN[t][d]
            bounces += 1
        q = exit_port(n, r, c, d)
        if q:
            return q, bounces
        r, c = r + DR[d], c + DC[d]


def all_paths(grid):
    n = len(grid)
    seen, paths = set(), []
    for name, _, _ in ports(n):
        if name in seen:
            continue
        q, k = trace(grid, name)
        seen.update([name, q])
        paths.append((name, q, k))
    return paths


def satisfies(grid, clues, total):
    if sum(1 for row in grid for t in row if t) != total:
        return False
    for kind, p, val in clues:
        q, k = trace(grid, p)
        if kind == "pair" and q != val:
            return False
        if kind == "num" and k != val:
            return False
    return True


class Checker:
    """z3 model of a box: every light state (cell, heading) carries the index
    of the port its light came in from. Clues are switched on per query."""

    def __init__(self, n, total, items, timeout_ms=None):
        self.n = n
        self.s = s = z3.Solver()
        if timeout_ms:
            s.set("timeout", timeout_ms)
        self.m = m = [[z3.BitVec(f"m{r}_{c}", 2) for c in range(n)] for r in range(n)]
        for row in m:
            for v in row:
                s.add(z3.ULE(v, 2))
        s.add(z3.PbEq([(v != 0, 1) for row in m for v in row], total))
        plist = ports(n)
        pid = {p[0]: i for i, p in enumerate(plist)}
        bv = lambda name: z3.BitVec(name, 6)
        src = {(r, c, d): bv(f"s{r}_{c}_{d}")
               for r in range(n) for c in range(n) for d in range(4)}
        out = {p[0]: bv(f"o{p[0]}") for p in plist}
        for name, (r, c), d in plist:
            s.add(src[(r, c, d)] == pid[name])
        for (r, c, d), v in src.items():
            for t in (0, 1, 2):
                nd = d if t == 0 else TURN[t][d]
                q = exit_port(n, r, c, nd)
                tgt = out[q] if q else src[(r + DR[nd], c + DC[nd], nd)]
                s.add(z3.Implies(m[r][c] == t, tgt == v))
        self.lits = {}
        for it in items:
            kind, p, val = it
            lit = z3.Bool(f"use{len(self.lits)}")
            if kind == "pair":
                s.add(z3.Implies(lit, out[val] == pid[p]))
            else:
                s.add(z3.Implies(lit, z3.PbEq(
                    [(z3.And(v == pid[p], m[r][c] != 0), 1)
                     for (r, c, d), v in src.items()], val)))
            self.lits[it] = lit

    def solutions(self, clues, total, limit=2, exclude=None):
        s, m, n = self.s, self.m, self.n
        s.push()
        if exclude is not None:
            s.add(z3.Or([m[r][c] != exclude[r][c] for r in range(n) for c in range(n)]))
        found, spurious = [], 0
        assume = [self.lits[it] for it in clues]
        while len(found) < limit:
            res = s.check(*assume)
            if res == z3.unknown:  # timed out: can't vouch for uniqueness
                found.append(None)
                break
            if res == z3.unsat:
                break
            mod = s.model()
            g = [[mod.eval(m[r][c]).as_long() for c in range(n)] for r in range(n)]
            s.add(z3.Or([m[r][c] != g[r][c] for r in range(n) for c in range(n)]))
            if satisfies(g, clues, total):
                found.append(g)
            else:
                # a closed interior loop let the model fake a bounce count;
                # if that keeps happening, give up and report "not unique"
                spurious += 1
                if spurious > 25:
                    found.append(None)
        s.pop()
        return found


def count_solutions(n, clues, total, limit=2):
    found = Checker(n, total, clues).solutions(clues, total, limit)
    return len(found), found


def random_grid(n, k, rng):
    cells = rng.sample([(r, c) for r in range(n) for c in range(n)], k)
    g = [[0] * n for _ in range(n)]
    for r, c in cells:
        g[r][c] = rng.choice((1, 2))
    return g


def all_items(g, numbers, pairs):
    items = []
    for p, q, b in all_paths(g):
        if pairs and p != q:
            items.append(("pair", p, q))
        if numbers:
            items.append(("num", p, b))
            items.append(("num", q, b))
    return items


def make_puzzle(n, k, rng, numbers=True, pairs=True):
    while True:
        g = random_grid(n, k, rng)
        items = all_items(g, numbers, pairs)
        chk = Checker(n, k, items, timeout_ms=20000)
        if chk.solutions(items, k, 1, exclude=g):
            continue
        rng.shuffle(items)
        clues = list(items)
        for it in items:
            trial = [x for x in clues if x is not it]
            if not chk.solutions(trial, k, 1, exclude=g):
                clues = trial
        return g, clues


# ---------------------------------------------------------------- rendering

def labels(n, clues):
    """Map port -> label string."""
    lab = {}
    letters = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for kind, p, q in clues:
        if kind == "pair":
            ch = next(letters)
            lab[p] = lab.get(p, "") + ch
            lab[q] = lab.get(q, "") + ch
    for kind, p, v in clues:
        if kind == "num":
            lab[p] = lab.get(p, "") + str(v)
    return lab


def render(n, lab, grid=None):
    W = 3

    def cell(r, c):
        if grid is None:
            return " · "
        return {0: " · ", 1: " / ", 2: " \\ "}[grid[r][c]]
    def port(p):
        return lab.get(p, "").center(W)
    lines = []
    lines.append(" " * W + "".join(port(("T", c)) for c in range(n)))
    lines.append(" " * (W - 1) + "+" + "-" * (W * n) + "+")
    for r in range(n):
        lines.append(lab.get(("L", r), "").rjust(W - 1) + "|" + "".join(cell(r, c) for c in range(n))
                     + "|" + port(("R", r)))
    lines.append(" " * (W - 1) + "+" + "-" * (W * n) + "+")
    lines.append(" " * W + "".join(port(("B", c)) for c in range(n)))
    return "\n".join(l.rstrip() for l in lines)


SET = [  # (size, mirrors, numbers?, pairs?, clues given back after minimising)
    (4, 3, False, True, 2),
    (4, 4, True, False, 2),
    (4, 4, True, True, 1),
    (5, 5, False, True, 1),
    (5, 6, True, False, 1),
    (5, 6, True, True, 1),
    (5, 7, True, True, 0),
    (6, 8, False, True, 0),
    (6, 9, True, True, 0),
    (6, 10, True, True, 0),
]


def write_set(done):
    puz, sol = [], []
    for i in sorted(done, key=int):
        n, k, g, clues = done[i]
        clues = [(kind, tuple(p), tuple(v) if kind == "pair" else v)
                 for kind, p, v in clues]
        lab = labels(n, clues)
        head = f"### {i}. {n}x{n}, {k} mirrors"
        puz.append(head + "\n\n```\n" + render(n, lab) + "\n```\n")
        sol.append(head + "\n\n```\n" + render(n, lab, g) + "\n```\n")
    open("puzzles.md", "w").write("\n".join(puz))
    open("solutions.md", "w").write("\n".join(sol))


if __name__ == "__main__":
    # each puzzle gets its own seed, and finished ones are cached in set.json,
    # so an interrupted run picks up where it stopped
    import json
    import os
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    done = json.load(open("set.json")) if os.path.exists("set.json") else {}
    for i, (n, k, nums, prs, extra) in enumerate(SET, 1):
        if str(i) in done:
            continue
        rng = random.Random(seed * 100 + i)
        g, clues = make_puzzle(n, k, rng, nums, prs)
        spare = [x for x in all_items(g, nums, prs) if x not in clues]
        clues += rng.sample(spare, min(extra, len(spare)))
        assert count_solutions(n, clues, k)[1] == [g]
        done[str(i)] = (n, k, g, clues)
        json.dump(done, open("set.json", "w"))
        write_set(done)
        print(f"puzzle {i}: {n}x{n}, {k} mirrors, {len(clues)} clues", flush=True)
