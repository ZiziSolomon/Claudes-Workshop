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
  iteration 1,192,804,929), 1 is inside the period-3 bulb (printed period is a multiple of 3).
- The interior test is double-precision Newton plus a multiplier check, not interval-certified.
  An earlier version accepted NaN cycles as interior. See the comment in `attracting_cycle`.
