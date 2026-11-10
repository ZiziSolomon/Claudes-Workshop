# Aizawa Attractor Sonification

A continuous sonification of the Aizawa attractor — a chaotic system with toroidal + crown topology, distinct from Lorenz's butterfly shape and Rössler's single spiral.

## The Aizawa Attractor

The Aizawa system is defined by:

```
dx/dt = (z - b) x - d y
dy/dt = d x + (z - b) y
dz/dt = c + a z - (z³/3) - (x² + y²)(1 + e z) + f z (x³)
```

With canonical parameters (a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1), this creates a toroidal band with periodic crown-like oscillations. The trajectory spirals on the torus, then periodically escapes to a crown region, creating alternating sections with distinct rhythm.

## Sonification Strategy

Unlike Rössler (which is smooth) or Lorenz (which has two distinct lobes), Aizawa creates punctuated structure:

- **z-coordinate (height)** → log-mapped pitch (MIDI 48–76, wider range than Lorenz, pentatonic quantized)
- **Distance from z-axis (spiral radius)** → stereo pan and harmonic content (0–40% 2nd harmonic)
- **Rate of x-change** → amplitude modulation (texture), creating rhythmic punctuation

The toroidal geometry produces a tighter pitch range within sections, then jumps. The crown topology creates abrupt transitions. The result is a sonic structure that's more rhythmically complex than Rössler but more continuous than Lorenz.

## Files

- **sonify.py** — Main script. Integrates Aizawa using RK4, applies low-pass filtering, quantizes to pentatonic, generates stereo audio with amplitude modulation.
- **out/aizawa.wav** — 22.05 kHz stereo audio, 16-bit, 28 seconds.
- **out/trajectory.png** — x–z projection, color-coded by time (purple → cyan).
- **out/spectrogram.png** — STFT showing frequency and amplitude over time.
- **out/panel.png** — Combined contact sheet.

## The Attractor Trio

Three attractors, three topologies, three sonic characters:

| | Lorenz | Rössler | Aizawa |
|--|--------|---------|--------|
| Topology | Two lobes | Single spiral | Torus + crown |
| Sonic character | Bimodal (two registers) | Continuous melodic | Punctuated (sections) |
| Transitions | Abrupt (lobe switches) | Smooth (spiral) | Rhythmic (torus to crown) |
| Pitch range | Moderate | Smooth gradient | Wider extremes |
| Overall feel | Conversational | Lyrical | Episodic |

All three are chaotic (sensitive dependence on initial conditions), but their topologies are fundamentally different — and this difference is perceivable in the sonification.
