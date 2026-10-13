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
  goes for `RLLRRR`, `RRRLLR`, `RLLLLLLR` and the others. All 17 cyclically paired rules
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
