# Rössler Attractor Sonification

A continuous sonification of the Rössler attractor — a simpler chaotic system than Lorenz with distinctly different topology.

## The Rössler Attractor

The Rössler system is defined by three coupled differential equations:

```
dx/dt = -(y + z)
dy/dt = x + ay
dz/dt = b + z(x - c)
```

With parameters a=0.2, b=0.2, c=5.7, this produces a single continuous spiral funnel. Unlike the Lorenz attractor (which has two lobes with a butterfly-like appearance), Rössler has a single spiral that winds around a torus, occasionally jumping outward and restarting.

The topology is simpler but the dynamics are still chaotic: nearby trajectories diverge exponentially, and the attractor has a fractal structure.

## Sonification Strategy

Like the Lorenz sonification, this uses continuous audio parameters derived from the trajectory:

- **z-coordinate (height)** → log-mapped pitch (MIDI 48–72, pentatonic quantized)
- **x-coordinate (spiral radius)** → stereo pan (left to right) and harmonic content (0–30% 2nd harmonic)
- **y-coordinate** → amplitude envelope (30–90%)

The single spiral structure produces a more "melodic" sonic character than Lorenz's two-lobe transitions. The pitch evolves continuously as the trajectory spirals, with periodic modulations as the system winds and jumps. The pan adds spatial dimension; the harmonic coloring adds textural variety.

## Files

- **sonify.py** — Main script. Integrates Rössler using RK4, applies low-pass filtering to control signals, quantizes pitch to pentatonic scale, generates stereo audio.
- **out/rossler.wav** — 22.05 kHz stereo audio, 16-bit, 24 seconds.
- **out/trajectory.png** — x–z projection of the trajectory, color-coded by time (blue → yellow).
- **out/spectrogram.png** — STFT showing frequency content over time.
- **out/panel.png** — Combined contact sheet.

## Comparison with Lorenz

| | Lorenz | Rössler |
|--|--------|---------|
| Topology | Two lobes (butterfly) | Single spiral funnel |
| Pitch transitions | Abrupt (switching lobes) | Smooth (spiraling) |
| Sonic character | Bimodal, alternating sections | Continuous, melodic |
| Dimension | 3D space | Projection to x–z plane |

The Rössler sonification demonstrates how topological differences in dynamical systems create different sonic experiences — even when using the same mapping strategy. The geometry of the attractor becomes the structure of the sound.
