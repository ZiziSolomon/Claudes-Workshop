# ash: Life soup census and the object-level prediction check

Experiments behind `writing/on_the_ash.md`. Pure Python, no dependencies.

- `census.py N SEED0`: runs N random 16×16 soups (density ½) to their ash and names the objects. It then predicts 2000 more generations from the object list alone and compares that with an honest re-simulation. Writes `census_SEED0_N.json`. 300 soups take about 6 min on 4 cores. 2000 soups did not finish in 30 min.
- `horizon.py SEED CAP`: prints, for each generation, how far ahead an object list predicts the whole pattern, and how many cells are already in known objects.
- `plot_horizon.py IN.txt OUT.svg`: draws the horizon output (render it with cairosvg).

Known limits:
- Departing ships are peeled off by a bounding-box heuristic.
- `split_objects` only merges 8-connected pieces and never splits them, so a ship-tie counts as one object even though it is two independent ships.
- 11 of 300 soups did not settle by generation 20,000: seeds 10068, 10099, 10102, 10138, 10164, 10193, 10207, 10209, 10226, 10242, 10244. I've examined only 10068. Two gliders leave side by side on parallel lanes (about 13 and 10 cells apart), each inside the other's bounding box, so the peel rule never releases either. Fixed in census.py: ships with the same velocity no longer count as "the rest". After the fix all 11 settle (max T = 5759), and all 11 pass the prediction check. The 289 that already passed were not rerun under the patched rule.
