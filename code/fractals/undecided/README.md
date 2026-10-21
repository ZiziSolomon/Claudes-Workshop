# undecided

How much of the Mandelbrot parameter plane is still undecided after N iterations?
Companion to `writing/on_the_undecided.md`.

```
gcc -O3 -fopenmp -o undecided undecided.c -lm
./undecided 16000 8000 24 huge.bin          # 128M stratified samples, cap 2^24 (~15 s on 4 cores)
python3 tally.py huge.bin 16000 8000 24     # area settled / undecided at each N = 2^k
python3 picture.py huge.bin 16000 8000 24 16 out/time_to_know.png
python3 points.py huge.bin 16000 8000 | ./undecided --points 31   # chase the stragglers
```

- `out/tally_16000x8000_2e24.txt`: undecided area ≈ 4.5/N over six decades; settled interior area 1.50660.
- `out/never_settled_deep.txt`: the 6 samples unsettled at 2^24, followed further: 5 escape (the last at
  iteration 1,192,804,929 in double; 223,621,176 at 1024-4096 bits, see below), 1 is inside the period-3 bulb (printed period is a multiple of 3).
- The interior test is double-precision Newton plus a multiplier check, not interval-certified.
  An earlier version accepted NaN cycles as interior. See the comment in `attracting_cycle`.
- `audit.c` re-iterates every interior verdict 2^EXTRA further steps. Fixed version: 0 of 2,706,498 escape
  (`out/audit_fixed.txt`); the NaN version: 813 of 2,707,521 (`out/audit_buggy_nan.txt`).

The slowest sample's orbit (`hesitation.c`, `hesitation_png.py`, `drift.c`, `drift_plot.py`):

```
gcc -O3 -o hesitation hesitation.c -lm
./hesitation 0.30761860802680241 0.49591127971481713 1200 1.6 31 hist.bin             # whole orbit
./hesitation 0.30761860802680241 0.49591127971481713 1200 0.075 31 z.bin -0.144 -0.038  # one island
python3 hesitation_png.py hist.bin 1200 out/hesitation.png
gcc -O3 -o drift drift.c -lm && ./drift > out/drift.txt && python3 drift_plot.py
```

Precision study of the same orbit (`precision.c`, `precision_mpf.c`, `growth.c`; results in `out/precision/`):

```
gcc -O3 -o precision precision.c -lquadmath -lm && ./precision q        # d | ld | q
gcc -O2 -o precision_mpf precision_mpf.c -lgmp -lm && ./precision_mpf 1024 [trace]
gcc -O3 -o growth growth.c -lm && ./growth                              # error stretching, in nats
```

Escape step by precision: 53 bits 1,192,804,929; 64 bits 172,578,004; 113 bits 532,653,179; GMP 128/192/256/512/768
bits 464,459,774 / 417,181,492 / 192,526,474 / 339,119,800 / 318,754,780; **1024, 2048, 3072 and 4096 bits all 223,621,176**.
So the double-precision orbit pictures (`hesitation*.png`, top panel of `drift.png`) show a pseudo-orbit, not the orbit of c.
`drift_plot.py` reads `out/precision/trace1024.txt` for the bottom panel.

Is it the arithmetic or the parameter? `perpoint.c` recomputes sampled escape steps in long double and quad
(`out/precision/per_point_bands.txt`: only 66% of samples escaping in 2^10..2^13 steps get the same step in
double and quad, 21% for 2^13..2^16). `survival.c` draws fresh uniform c and compares the *fraction* not
escaped by N in all three arithmetics: those agree to a few samples (`out/precision/survival_1M_2e16.txt`).
