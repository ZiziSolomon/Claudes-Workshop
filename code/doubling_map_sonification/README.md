# Doubling Map Sonification

A granular (discrete-event) sonification of the doubling map T(x) = 2x mod 1.

## The Doubling Map

The doubling map is one of the simplest chaotic dynamical systems. On the unit interval [0, 1), the dynamics are:

```
T(x) = 2x mod 1
```

Each iteration has a clean symbolic dynamics: reading x as a binary decimal 0.d₀d₁d₂d₃..., the map simply shifts the binary expansion left, discarding the first bit.

T(0.0110...) = 0.1100... (shift left)
T(0.1100...) = 0.1000... (shift left)

This means: each application of T extracts one binary digit. This digit sequence is the fundamental symbolic structure of the map.

## Sonification Strategy

Unlike the Lorenz sonification (which maps continuous coordinates to continuous audio parameters), this sonification treats each digit as a discrete event triggering a short tone burst (grain).

- Each iteration emits one binary digit (0 or 1).
- Digit 0 → triggers a pitch from the low pentad {C4, D4, E4}.
- Digit 1 → triggers a pitch from the high pentad {G4, A4, C5}.
- Each grain is 60 ms, followed by 20 ms silence.
- Total: 500 grains × 80 ms = 40 seconds of audio.

The pitch within each pentad cycles through the available notes, so the rhythm of the binary sequence creates the temporal structure of the sonification.

## Files

- **sonify.py** — Main script. Iterates the doubling map, extracts binary digits, synthesizes Hann-windowed sine-wave grains, and generates output files.
- **out/doubling_map.wav** — 22.05 kHz mono audio, 16-bit.
- **out/trajectory.png** — X-coordinate over time, color-coded by digit (purple for 0, blue for 1).
- **out/spectrogram.png** — STFT, showing the pitch content as a function of time. The discrete grains are visible as vertical columns.
- **out/panel.png** — Combined contact sheet.

## Key Insight

The doubling map's binary symbolic dynamics are made audible as rhythm. The alternation between low and high pentads directly encodes the 0–1 sequence, making the abstract mathematical structure (binary digits) perceivable as sound. This contrasts with the Lorenz sonification, where the sonic output is continuous and represents the trajectory's geometric path.
