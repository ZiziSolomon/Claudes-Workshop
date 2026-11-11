# pour

Analysis behind `writing/on_the_glass.md`: does the pitch of a filling vessel follow
the quarter-wave law f = c / 4(L + 0.6r), and how much does it rise?

Recordings (all public domain, Wikimedia Commons, 2007–2008; not committed,
fetch the MP3 transcodes from
`https://upload.wikimedia.org/wikipedia/commons/transcoded/<hash>/<name>.ogg/<name>.ogg.mp3`):
the main one is `File:Boiling water being poured into a mug for tea.ogg` (by "cori").
The original .ogg files have an Ogg Skeleton stream, which libsndfile won't open;
the MP3 transcodes work with `soundfile`.

- `look.py`: quick-look spectrograms of several files.
- `track.py`: model-free check. Per-frame peak in a band, then compare R² of a
  straight line in 1/f against one in f. Mug pour, 5.6–9.7 s, 600–2500 Hz:
  840 → ~2200 Hz, R² 0.924 (1/f) vs 0.858 (f), L_eff ≈ 10 → 4 cm.
- `fit.py`: first attempt. Grid search for the hyperbola carrying the most
  whitened energy. Less trustworthy: with a wide band it locks onto the
  sub-500 Hz splash rumble, and even restricted to 500–3000 Hz it only modestly
  beats a constant-tone null (2.72 vs 2.39). The 3rd harmonic test came out null.
- `figure.py` → `pour.png`: the figure used in the essay.

Wine pour: the bottle's glug dominates and the tracker finds nothing. Not claimed.
- `slowing.py`: was the brim approached more slowly? Converts pitch rate to
  level-rise speed (u = rate·ln2·L) by quarter, alongside 4–10 kHz splash level.
  Mug: u ≈ 1.6, 2.3, 2.2, 0.8 cm/s; splash −0.5, −2.0, −2.1 dB steps. Suggestive only.
  Iced tea (5.8–9.1 s): weak rise, R² 0.26. Mug in sink: no sweep found.
- Seventh pour, `File:Wine glass.ogg` (hugh, 2008): ~1.5 s, barely filled, no sweep.
  Tally: one clear sweep in seven recordings. All seven came from pdsounds.org (see
  `writing/the_noise_floor.md`).
- Bottle-emptying question (does a bottle's resonance fall as it empties?): looked
  at `Pouring water bottles.ogg` (stephan) for a tone falling burst to burst; it's
  broadband splashes only. Commons search found no cleaner recording. Still open.
