# Lightbox

**To play:** open `play.html` in a browser. Both sets are built in. Click
cells to place mirrors, click edge points to fire beams through your guess,
and progress is saved in the browser. **Hint** points at the next clue
worth looking at and the cells it settles; press it again to fill them in.
The hints come from `grade.explain`, which re-solves each box one clue at a
time, always taking the clue with the fewest possible routes. (First-set
puzzles that need trial and error get no hints.) Rebuild the page with
`python3 build_play.py`.

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

One fact is worth having in your pocket. Every mirror has two faces, and
each face is used by exactly one path through the box. So if you add up the
bounce counts of all the paths, counting each path once, you get exactly
twice the number of mirrors. (Strictly, at most twice: four mirrors set
in a rectangle could trap light in a closed loop that no beam from outside
ever sees. Exactly one of these ten boxes has one.) Big numbers use up that budget
quickly.

## Where they came from

`lightbox.py` makes them. It scatters mirrors at random, writes down every
clue the layout implies, then throws clues away one at a time (in random
order) for as long as an SMT solver (z3) still finds exactly one layout that
fits. The early puzzles get a clue or two handed back afterwards to be kind.
Uniqueness is machine-checked; whether each one is pleasant to solve by
reasoning rather than by trial is something only a person working it finds
out.

    pip install z3-solver
    python3 lightbox.py 2026     # finished puzzles are cached in set.json
    python3 make_html.py         # printable lightbox.html

With `set.json` removed it starts from scratch. Each puzzle has its own
seed, but each solver check gives up after 20 seconds (and keeps the clue
it was testing), so a slower machine may end up with a few more clues on
the 6x6 boxes.

## Puzzle 1, worked (spoiler)

Rows and columns are numbered from 0 at the top left.

- `B` runs from the top of column 0 to the bottom of column 1. A beam can't
  change columns without turning twice: it must turn east off a `\` somewhere
  in column 0, then south off another `\` in column 1, in the same row.
  That's two of the three mirrors.
- `E` runs from the top of column 1 to the right end of row 0. Going down and
  coming out to the east needs at least one `\` turn, and doing it any other
  way costs three. `A` (row 2 into column 2) needs a mirror of its own too.
  So `E` gets no new mirror: it must share one of `B`'s, which means the
  beam down column 1 meets `B`'s column-1 mirror in row 0. `B`'s pair sits
  in row 0: `\` at (0,0) and `\` at (0,1).
- `C` checks out: in at the left of row 0, off the `\` at (0,0), straight
  down column 0. The third mirror is `A`'s, a `\` at (2,2), and `D` runs
  straight down an empty column 3.

The later puzzles don't all fall this neatly. The number-only ones (2 and 5)
reward looking at what a `0` forbids and what a large number forces. In
puzzle 5, two beams each bounce six times in a box with six mirrors: twelve
faces, all spent, unless those two 6s are the two ends of one path. There
are 1s on the board, so they are.

## Grading, and a second set

Machine-checked uniqueness doesn't make a puzzle solvable by reasoning, so
`grade.py` tries to solve each box the way a person might. Each cell holds
its remaining options (empty, `/`, `\`). For one clue at a time, it lists
every route that clue's beam could take given those options and the mirror
count, and strikes out any value no route uses. It repeats that until
nothing changes. Level 2 then tries "suppose this cell were `/`" one cell at
a time and strikes the value out if propagation hits a contradiction.

Grades for the first set (1 = propagation alone, 2 = needs suppositions,
3 = still stuck after them):

| puzzle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------:|---|---|---|---|---|---|---|---|---|----|
| grade  | 1 | 3 | 2 | 3 | 2 | 2 | 2 | 3 | 3 | 3  |

So most of the first set needs trial and error, and puzzles 2, 4, 8, 9 and 10
need more of it than one level of supposition gives. Minimal clue sets make
hard puzzles, not nice ones.

`fair.py` makes a second set (`fair_puzzles.md`, `fair_solutions.md`,
`fair.html`): ten boxes, 4x4 up to 8x8, where a clue is only dropped if the
puzzle stays grade 1. Every mirror follows from looking at one clue at a time
plus the count. You never need to chain "suppose" across clues. Grade-1
deductions are sound, so every box is unique; z3 confirms it independently.
"Fair" doesn't mean quick. Listing a single beam's possible routes can still
be a lot of cases, and the 8x8s have 14 and 17 mirrors.

One finding along the way. Take 40 random 5x5 layouts with 5 mirrors, write
down every clue of one kind, and see what you get:

| clues given    | unique (z3) | solvable one clue at a time |
|----------------|------------:|----------------------------:|
| letters only   | 15          | 0                           |
| numbers only   | 6           | 1                           |
| both           | 30          | 30                          |

Numbers alone usually don't even pin the box down. Letters alone often do,
but only through interactions between clues: a letter fixes where a beam
ends up, not how it gets there. With both kinds of clue, every unique box in
the sample was also solvable one clue at a time. The fair set mixes both.

    python3 grade.py            # grades set.json
    python3 fair.py 7           # regenerates the fair set (fast: ~1 minute)
