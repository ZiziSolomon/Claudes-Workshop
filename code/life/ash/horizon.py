"""Prediction horizon of the object-level description, generation by generation.

At each generation t of a soup, try to describe the whole pattern as a list
of independent objects with known period and velocity (still lifes,
oscillators, spaceships). If every part is such an object, predict the state
at t+k by object rules alone and find the first k at which the prediction is
wrong. If some part is not a known periodic object, the horizon is 0: there
is no description shorter than running it.

usage: python3 horizon.py SEED [CAP]
prints t, horizon(t), population, cells in known objects, for every t until the horizon reaches CAP.
"""
import random
import sys

from census import step, split_objects, identify

seed = int(sys.argv[1])
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

rng = random.Random(seed)
states = [{(x, y) for x in range(16) for y in range(16) if rng.random() < 0.5}]


def state(t):
    while len(states) <= t:
        states.append(step(states[-1]))
    return states[t]


def advance(comp, ps, k):
    p, (dx, dy) = ps
    q, r = divmod(k, p)
    cur = comp
    for _ in range(r):
        cur = step(cur)
    return {(x + q * dx, y + q * dy) for x, y in cur}


t = 0
while True:
    s = state(t)
    objs = []
    known = 0
    for part in split_objects(s, 1):
        key, ps = identify(part)
        if key is None:
            objs = None
        else:
            known += len(part)
            if objs is not None:
                objs.append((part, ps))
    h = 0
    if objs is not None:
        while h < CAP:
            pred = set().union(*(advance(c, ps, h + 1) for c, ps in objs)) if objs else set()
            if pred != state(t + h + 1):
                break
            h += 1
    print(t, h, len(s), known, flush=True)
    if h >= CAP:
        break
    t += 1
