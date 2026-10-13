# Which Langton's ants draw symmetric pictures?

A generalized Langton's ant has a rule string such as `RLLR`. On a cell of colour *c* it
turns `rule[c]` and then moves the cell to colour *c+1 mod n*. A known result (Propp and
others) says that when the letters come in adjacent equal pairs, as in `RRLL` or `RRLLRR`,
the pattern keeps coming back to perfect mirror symmetry.

`ants.py` checks every rule up to length 8. It skips mirror twins, trivial rules and
repetitions of shorter rules. Every 500 steps it tests the pattern for mirror symmetry
about a horizontal, vertical or diagonal axis. It doesn't test rotational symmetry.

## Results (100k steps, `results_100k.txt`)

- **Recurring symmetry shows up exactly for the rules that are paired *cyclically*.**
  `RLLR` isn't paired as written, but read as a cycle it splits into `R|LL|R`. The same
  goes for `RLLRRR`, `RRRLLR`, `RLLLLLLR` and the others. All 20 cyclically paired rules
  return to symmetry again and again, up to step 100,000.
- No rule outside that class is symmetric after step 5000. The odd-length rules
  (`RRLLLLL`, `RRRLLRR` and so on) only pass the test a few times early on, as
  transients.
- Cyclic rotation isn't a free symmetry of the problem: rotating a rule by *k* means
  starting on a background of colour *k*. So the result implies the parity argument only
  needs the pairs to line up around the cycle, wherever colour 0 happens to fall.
- Paired rules can grow very slowly. After 60k steps `RRLLRR` covers only about 16×16
  cells, while `RL` (Langton's original ant) has already built its highway.

PNGs: `RLLR.png`, `RRLLRR.png` and `RLLRRRRR.png`, each captured at a symmetric moment.

## Extension to length 10 (40k steps, `results_len10_40k.txt`)

There are 50 cyclically paired rules up to length 10 (the 20 from before plus 30 of length 10),
and every one of them is still returning to symmetry after step 8000. Of the other 16
rules, which are mostly odd-length near-misses, none is symmetric after step 7000. No
counterexamples at length 10 either. (Running the script writes a PNG for every hit, so
delete the extras before committing.)

## When exactly is it symmetric? (`times.py`, `bursts.py`, checked every step, 30k steps)

- **After step 1000, every symmetric moment falls on a multiple of 4.** I checked
  `RRLL`, `RLLR`, `RRLLRR` and `RRRLLR` (several hundred to about 3000 such moments
  each) and found no exceptions. Early on there are also symmetric moments at other step
  counts.
- Those early odd-timed moments come in **bursts**: runs of 9–19 consecutive symmetric
  steps. For `RRLL` the bursts come in groups of three, 28 steps apart (starting at steps
  1/27/55, then 383/411/439, then 767/795/823), each group 384 steps after the last.
  Each burst replays the symmetric-step pattern of the opening moves, with the same gaps.
  It looks as if the ant is running its first moves again in a clean spot. After step
  823 the bursts stop, and only the every-4-steps symmetry is left.

## Contact sheet (`sheet.py` → `sheet.png`)

The 20 cyclically paired rules up to length 8, each at its last symmetric checkpoint up
to step 20k, in reading order: RLLR RRLL RLLLLR RLLRRR RRLLLL RRLLRR RRRLLR RRRRLL
RLLLLLLR RLLLLRRR RLLRRRRR RRLLLLLL RRLLLLRR RRLLRRRR RRRLLLLR RRRLLRRR RRRRLLLL
RRRRLLRR RRRRRLLR RRRRRRLL.

**Correction to the multiple-of-4 claim.** I checked four more rules for 15k steps.
`RLLLLLLR`, `RRLLRRLLRR` and `RRRLLLLLLR` follow it: every symmetric moment after step
1000 falls on a multiple of 4. `RRRRLLLL` doesn't. It has 58 symmetric moments off the
multiple-of-4 steps, all between steps 1535 and 1665, which looks like a late burst of
the same replay kind. So "after step 1000" was only a property of the first four rules
I tried. The better statement is that, outside the replay bursts, symmetric moments
fall on multiples of 4, and the bursts can come later than step 1000.

## Second correction: sampling every 500 steps hid some symmetric rules (`everystep.py`)

The main result came from `ants.py`, which only checks every 500 steps. Re-checking the
non-cyclically-paired rules at **every** step (10k steps; `results_everystep_10k.txt`,
turns up rules that are still symmetric late:

| rule | symmetric steps after 1000 | spacing |
|---|---|---|
| `RRRLLL`  | 237 (last at 9987) | every 38 |
| `RRLLLRL` | 215 (last at 9999) | every 42 |
| `RRRRLLL` | 98 (last at 9967)  | every 92 |

None of the 500-step checkpoints landed on them. `RRRLLL_9987.png` shows what's going
on: these ants build a **diagonal highway**, a stripe that goes on forever, and the
stripe is mirror-symmetric about its own diagonal once per highway period. That's a
different kind of symmetry from the paired rules, whose whole pattern grows into a
symmetric blob. So the honest version of the main claim is: *the cyclically paired rules
are the ones whose growing pattern keeps returning to symmetry. Some other rules settle
into highways that are symmetric once per period.* My checker doesn't tell the two
apart. A fair test would have to exclude highways first (for example by tracking the
ant's distance from the origin).

**After the full every-step run:** two more length-8 rules are symmetric late, `RRRLLRLR`
(last at 9935) and `RRRRRLLL` (last at 9967). I measured where each ant is at step 10k.
All five late rules are 368–526 steps away from the origin along an exact or near-exact
diagonal, so they're all highways. The paired ants stay close to home: `RRLLRR` is back
at (0,0) and `RLLR` is 12 away. So, up to length 8 and 10k steps: **every rule whose
symmetry persists either is cyclically paired (symmetric blob) or has turned into a
diagonal highway.** Nothing else turned up.

**The other direction (`paired_distance_50k.txt`):** none of the 20 cyclically paired rules
turns into a highway within 50k steps. The farthest any of them ever gets from the origin
is 68 steps (`RLLR`), and most finish within a few cells of it. The highways had travelled
368–526 by step 10k. So, up to step 50k, the two kinds of symmetry come from separate sets
of rules: blobs come from the paired rules, highways from the others.
