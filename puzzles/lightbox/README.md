# Lightbox

Ten hidden-mirror puzzles, in rising order of difficulty.
Puzzles are in `puzzles.md`, answers in `solutions.md`.

## Rules

Each box is a square grid. Some cells hold a two-sided mirror set on the
diagonal, either `/` or `\`; every other cell is empty. You are told how many
mirrors there are, but not where.

A beam of light can be shone into the box from just outside any edge cell.
It travels in a straight line, turns 90° whenever it meets a mirror, and
eventually leaves the box somewhere on the edge. (It can't get stuck: light
that comes in from outside always gets back out.)

Clues sit around the edge:

- **Letters come in pairs.** A beam shone in at one `A` comes out at the
  other `A` (and, light being reversible, the other way round too).
- **A number** says how many mirrors the beam entering at that point
  bounces off before it leaves. `0` means it goes straight through.
- A label like `A2` carries both kinds of clue at once.
- An unlabelled edge point tells you nothing.

Find every mirror. Each puzzle has exactly one solution.

## How the turns work

```
   moving →  hits /  goes ↑        moving →  hits \  goes ↓
   moving ↓  hits /  goes ←        moving ↓  hits \  goes →
```

## A first hint

A straight-through pair — letters directly opposite one another — doesn't
mean the row is empty: mirrors can turn a beam out of a row and back into
it. But a `0` does mean the whole row (or column) is empty, and that's the
strongest clue there is. Start from zeros and from short paths between
neighbouring edge points.

## Where they came from

`lightbox.py` makes them. It scatters mirrors at random, writes down every
clue the layout implies, then throws clues away one at a time (in random
order) for as long as an SMT solver (z3) still finds exactly one layout that
fits. The early puzzles get a clue or two handed back afterwards to be kind.
Uniqueness is machine-checked; whether each one is pleasant to solve by
reasoning rather than by trial is something only a person working it finds
out.

    pip install z3-solver
    python3 lightbox.py 2026     # regenerates this exact set
