"""Grade Lightbox puzzles by solving them without search, the way a person might.

Each cell keeps a set of possibilities: empty, '/', '\\'. One round of
propagation looks at each clue on its own: it lists every way the beam could
run through the box that agrees with the current possibilities (and with the
mirror count), and strikes out any cell value that no such route uses. The
mirror count is used on its own too. Rounds repeat until nothing changes.

If that stalls, level 2 tries each remaining value in each cell, propagates,
and strikes the value out if it leads to a contradiction ("if this were a
mirror, then ... impossible"). Grades:

  1  propagation alone solves it
  2  needs one or more single-step "suppose" eliminations
  3  stalled even with those (needs deeper search)

Route enumeration is capped; a clue with too many possible routes is simply
skipped that round, as a person would set it aside for later.

    python3 grade.py            -> grades every puzzle in set.json
"""
import json
import sys

from lightbox import DR, DC, TURN, exit_port, ports

BUDGET = 3000       # route-search nodes allowed per clue per round


class Contradiction(Exception):
    pass


def clue_routes(n, k, dom, port, want_exit, want_bounces):
    """For one clue, the values each cell can still take, judged by every
    route the beam could follow. None if there are too many routes to list."""
    _, (r0, c0), d0 = next(p for p in ports(n) if p[0] == port)
    fixed = sum(1 for v in dom.values() if 0 not in v)
    seen = {}            # cell -> values used by routes that visit it
    visits = {}          # cell -> number of routes that visit it
    routes = [0]
    nodes = [0]

    def dfs(r, c, d, local, bounces, extra):
        nodes[0] += 1
        if nodes[0] > BUDGET:
            raise OverflowError
        opts = [local[(r, c)]] if (r, c) in local else sorted(dom[(r, c)])
        for t in opts:
            new = (r, c) not in local
            e = extra + (1 if new and t and 0 in dom[(r, c)] else 0)
            if fixed + e > k:
                continue
            b = bounces + (1 if t else 0)
            if want_bounces is not None and b > want_bounces:
                continue
            nd = TURN[t][d] if t else d
            if new:
                local[(r, c)] = t
            q = exit_port(n, r, c, nd)
            if q:
                if ((want_exit is None or q == want_exit) and
                        (want_bounces is None or b == want_bounces)):
                    routes[0] += 1
                    for cell, v in local.items():
                        seen.setdefault(cell, set()).add(v)
                        visits[cell] = visits.get(cell, 0) + 1
            else:
                dfs(r + DR[nd], c + DC[nd], nd, local, b, e)
            if new:
                del local[(r, c)]

    try:
        dfs(r0, c0, d0, {}, 0, 0)
    except OverflowError:
        return None
    if routes[0] == 0:
        raise Contradiction
    # only cells on every route are narrowed; a route that skips a cell
    # leaves it free
    return {cell: vals for cell, vals in seen.items() if visits[cell] == routes[0]}


def port_constraints(clues):
    """port -> (exit port or None, bounce count or None), both ends of pairs."""
    con = {}
    for kind, p, v in clues:
        if kind == "pair":
            for a, b in ((p, v), (v, p)):
                con[a] = (b, con.get(a, (None, None))[1])
    for kind, p, v in clues:
        if kind == "num":
            con[p] = (con.get(p, (None, None))[0], v)
    return con


def propagate(n, k, dom, con):
    """Shrink domains in place until nothing changes. Raises Contradiction."""
    changed = True
    while changed:
        changed = False
        for p, (e, b) in con.items():
            narrowed = clue_routes(n, k, dom, p, e, b)
            if narrowed is None:
                continue
            for cell, vals in narrowed.items():
                new = dom[cell] & vals
                if new != dom[cell]:
                    if not new:
                        raise Contradiction
                    dom[cell] = new
                    changed = True
        sure = [c for c, v in dom.items() if 0 not in v]
        maybe = [c for c, v in dom.items() if v != {0}]
        if len(sure) > k or len(maybe) < k:
            raise Contradiction
        for c in maybe:
            if len(sure) == k and 0 in dom[c] and c not in sure:
                dom[c] = {0}
                changed = True
            elif len(maybe) == k and 0 in dom[c]:
                dom[c] = dom[c] - {0}
                changed = True
    return dom


def solved(dom):
    return all(len(v) == 1 for v in dom.values())


def grade(n, k, clues, stats=None):
    con = port_constraints(clues)
    dom = {(r, c): {0, 1, 2} for r in range(n) for c in range(n)}
    propagate(n, k, dom, con)
    if solved(dom):
        return 1, dom
    suppositions = 0
    progress = True
    while progress and not solved(dom):
        progress = False
        for cell in sorted(dom):
            for t in sorted(dom[cell]):
                if len(dom[cell]) == 1:
                    break
                trial = {c: set(v) for c, v in dom.items()}
                trial[cell] = {t}
                try:
                    propagate(n, k, trial, con)
                except Contradiction:
                    dom[cell] = dom[cell] - {t}
                    suppositions += 1
                    propagate(n, k, dom, con)
                    progress = True
    if stats is not None:
        stats["suppositions"] = suppositions
    return (2 if solved(dom) else 3), dom


def load(entry):
    n, k, g, clues = entry
    clues = [(kind, tuple(p), tuple(v) if kind == "pair" else v)
             for kind, p, v in clues]
    return n, k, g, clues


if __name__ == "__main__":
    import time
    done = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "set.json"))
    for i in sorted(done, key=int):
        n, k, g, clues = load(done[i])
        t = time.time()
        st = {}
        lvl, dom = grade(n, k, clues, st)
        if lvl < 3:
            assert all(dom[(r, c)] == {g[r][c]} for r in range(n) for c in range(n))
        left = sum(len(v) > 1 for v in dom.values())
        print(f"{i:>2}. {n}x{n} k={k:<2} grade {lvl}  suppositions={st.get('suppositions', 0):<3}"
              f" undecided={left:<3} {time.time() - t:.1f}s", flush=True)
