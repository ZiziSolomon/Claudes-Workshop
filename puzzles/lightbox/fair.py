"""Second set: puzzles that never need a guess.

Same generator idea as lightbox.py, but a clue may only be thrown away if
grade.py can still solve the puzzle by propagation alone (grade 1): every
mirror follows from looking at one clue at a time, plus the mirror count.
That's a sound test, so anything it passes has exactly one solution; no z3.

    python3 fair.py [seed]     -> fair.json, fair_puzzles.md, fair_solutions.md
"""
import json
import os
import random
import sys

from grade import Contradiction, port_constraints, propagate, solved
from lightbox import all_items, labels, random_grid, render

SET = [  # (size, mirrors, numbers?, pairs?); single-kind clue sets are
    # almost never solvable one clue at a time, so these are all mixed
    (4, 4, True, True),
    (5, 5, True, True),
    (5, 7, True, True),
    (6, 7, True, True),
    (6, 9, True, True),
    (6, 11, True, True),
    (7, 10, True, True),
    (7, 13, True, True),
    (8, 14, True, True),
    (8, 17, True, True),
]


def fair(n, k, clues, g):
    dom = {(r, c): {0, 1, 2} for r in range(n) for c in range(n)}
    try:
        propagate(n, k, dom, port_constraints(clues))
    except Contradiction:
        raise AssertionError("true layout contradicted: grader bug")
    if not solved(dom):
        return False
    assert all(dom[(r, c)] == {g[r][c]} for r in range(n) for c in range(n))
    return True


def make_fair(n, k, rng, numbers, pairs):
    while True:
        g = random_grid(n, k, rng)
        items = all_items(g, numbers, pairs)
        if not fair(n, k, items, g):
            continue
        rng.shuffle(items)
        clues = list(items)
        for it in items:
            trial = [x for x in clues if x is not it]
            if fair(n, k, trial, g):
                clues = trial
        return g, clues


def write(done, prefix):
    puz, sol = [], []
    for i in sorted(done, key=int):
        n, k, g, clues = done[i]
        clues = [(kind, tuple(p), tuple(v) if kind == "pair" else v)
                 for kind, p, v in clues]
        lab = labels(n, clues)
        head = f"### {i}. {n}x{n}, {k} mirrors"
        puz.append(head + "\n\n```\n" + render(n, lab) + "\n```\n")
        sol.append(head + "\n\n```\n" + render(n, lab, g) + "\n```\n")
    open(prefix + "_puzzles.md", "w").write("\n".join(puz))
    open(prefix + "_solutions.md", "w").write("\n".join(sol))


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    done = json.load(open("fair.json")) if os.path.exists("fair.json") else {}
    for i, (n, k, nums, prs) in enumerate(SET, 1):
        if str(i) in done:
            continue
        rng = random.Random(seed * 100 + i)
        g, clues = make_fair(n, k, rng, nums, prs)
        done[str(i)] = (n, k, g, clues)
        json.dump(done, open("fair.json", "w"))
        write(done, "fair")
        print(f"puzzle {i}: {n}x{n}, {k} mirrors, {len(clues)} clues", flush=True)
