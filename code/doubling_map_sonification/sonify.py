"""Sonify the doubling map with granular (discrete-event) synthesis.

The doubling map T(x) = 2x mod 1 has a clean symbolic dynamics: each
iteration emits one binary digit (the leading bit of x). This sonification
uses each bit to trigger a short tone burst, making the rhythm a direct
consequence of the binary expansion.

In a pentatonic scale (C, D, E, G, A), we use:
  - Digit 0 → lower pentad (C, D, E)
  - Digit 1 → upper pentad (G, A, C')

The grain duration is fixed (60 ms), but the pitch alternates between
low/high based on the binary sequence. The overall envelope stretches
out so that the rhythm of the bits is perceptible.

Outputs in ./out:
  doubling_map.wav      — 16-bit stereo, 22.05 kHz, ~30 seconds
  spectrogram.png       — STFT of the mono mix
  trajectory.png        — x-coordinate over time with digit sequence overlay
  panel.png             — combined contact sheet
"""

import math
import os
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

SAMPLE_RATE = 22050
GRAIN_DURATION = 0.06  # 60 ms per grain
N_GRAINS = 500  # total grains
SILENCE_DURATION = 0.02  # 20 ms silence between grains
GRAIN_SAMPLES = int(SAMPLE_RATE * GRAIN_DURATION)
SILENCE_SAMPLES = int(SAMPLE_RATE * SILENCE_DURATION)
TOTAL_SAMPLES = N_GRAINS * (GRAIN_SAMPLES + SILENCE_SAMPLES)

# Pentatonic scale: C, D, E, G, A (MIDI relative to C4 = 60)
# Low pentad for digit 0: C4, D4, E4
# High pentad for digit 1: G4, A4, C5
PENTATONIC_LOW = [60, 62, 64]  # C, D, E
PENTATONIC_HIGH = [67, 69, 72]  # G, A, C'

def midi_to_hz(midi):
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)

def doubling_map(x, n_steps):
    """Iterate the doubling map and return the binary digit sequence."""
    digits = []
    for _ in range(n_steps):
        x = (2 * x) % 1.0
        digit = int(x * 2)  # leading bit
        digits.append(digit)
    return x, digits

def synthesize_grain(frequency, duration_samples, sample_rate):
    """Synthesize a simple sine-wave grain with Hann envelope."""
    t = np.arange(duration_samples) / sample_rate
    phase = 2.0 * np.pi * frequency * t
    sine = np.sin(phase)

    # Hann window for smooth attack/decay
    window = np.hanning(duration_samples)
    grain = sine * window
    return grain

def sonify_doubling_map():
    """Generate the full sonification."""
    # Start with a random initial condition
    x = 0.7  # arbitrary choice

    # Iterate and collect digits
    x, digits = doubling_map(x, N_GRAINS)

    # Build the audio
    audio = np.zeros(TOTAL_SAMPLES, dtype=np.float64)
    x_trajectory = []  # for visualization

    for i, digit in enumerate(digits):
        # Choose which pentad to use
        pentad = PENTATONIC_HIGH if digit == 1 else PENTATONIC_LOW

        # Pick a pitch from the pentad (simple: cycle through)
        pitch_idx = i % len(pentad)
        midi_note = pentad[pitch_idx]
        frequency = midi_to_hz(midi_note)

        # Synthesize the grain
        grain = synthesize_grain(frequency, GRAIN_SAMPLES, SAMPLE_RATE)

        # Place it in the audio buffer
        start_sample = i * (GRAIN_SAMPLES + SILENCE_SAMPLES)
        end_sample = start_sample + GRAIN_SAMPLES
        audio[start_sample:end_sample] += grain

        x_trajectory.append(x)

    # Normalize to 16-bit range
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95

    audio_int16 = (audio * 32767).astype(np.int16)

    # Write WAV file
    wav_path = os.path.join(OUT, "doubling_map.wav")
    with wave.open(wav_path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_int16.tobytes())

    print(f"Wrote {wav_path}")

    # Generate trajectory visualization
    time_axis = np.arange(len(x_trajectory)) * (GRAIN_DURATION + SILENCE_DURATION)

    fig_width, fig_height = 1400, 300
    img = Image.new("RGB", (fig_width, fig_height), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    # Plot x-coordinate trajectory
    margin = 40
    plot_width = fig_width - 2 * margin
    plot_height = fig_height - 2 * margin

    # Scale trajectory to plot coordinates
    x_min, x_max = 0.0, 1.0
    y_min, y_max = 0.5, -0.5  # inverted for image coords

    prev_px, prev_py = None, None
    for i, x_val in enumerate(x_trajectory):
        t_val = time_axis[i]
        px = margin + (t_val / time_axis[-1]) * plot_width
        py = margin + plot_height * (x_val - x_min) / (x_max - x_min)

        if prev_px is not None:
            # Color by digit
            color = (100, 180, 220) if digits[i] == 1 else (180, 100, 220)
            draw.line([(prev_px, prev_py), (px, py)], fill=color, width=2)

        prev_px, prev_py = px, py

    # Axes
    draw.rectangle(
        [(margin, margin), (margin + plot_width, margin + plot_height)],
        outline=(100, 100, 100)
    )

    # Labels
    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw.text((10, margin + plot_height // 2), "x", fill=(200, 200, 200), font=fnt)
    draw.text((margin + plot_width // 2, fig_height - 20), "time", fill=(200, 200, 200), font=fnt)

    img_path = os.path.join(OUT, "trajectory.png")
    img.save(img_path)
    print(f"Wrote {img_path}")

    # Generate spectrogram
    import scipy.signal

    f, t, Sxx = scipy.signal.spectrogram(
        audio,
        fs=SAMPLE_RATE,
        nperseg=2048,
        noverlap=1024,
        window='hann'
    )

    # Convert to dB
    Sxx_db = 10 * np.log10(Sxx + 1e-10)

    # Clamp to [-60, 0] dB
    Sxx_db = np.clip(Sxx_db, -60, 0)

    # Create image
    spec_height, spec_width = Sxx_db.shape[0], Sxx_db.shape[1]
    spec_img = Image.new("RGB", (spec_width, spec_height), color=(0, 0, 0))
    pixels = spec_img.load()

    for i in range(spec_height):
        for j in range(spec_width):
            val = Sxx_db[i, j]
            norm_val = (val + 60) / 60.0  # normalize to [0, 1]
            # Cool (blue) for quiet, hot (red/yellow) for loud
            r = int(255 * max(0, norm_val - 0.5) * 2)
            g = int(255 * max(0, min(norm_val, 0.5) * 2))
            b = int(255 * (1.0 - norm_val))
            pixels[j, i] = (r, g, b)

    spec_path = os.path.join(OUT, "spectrogram.png")
    spec_img.save(spec_path)
    print(f"Wrote {spec_path}")

    # Create panel (contact sheet)
    panel = Image.new("RGB", (fig_width * 2, fig_height * 2), color=(20, 20, 20))
    panel.paste(img, (0, 0))
    panel.paste(spec_img.resize((fig_width, fig_height)), (fig_width, 0))

    # Add some title text
    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw_panel = ImageDraw.Draw(panel)
    draw_panel.text((10, fig_height + 10), "Doubling Map Sonification", fill=(200, 200, 200), font=fnt)

    panel_path = os.path.join(OUT, "panel.png")
    panel.save(panel_path)
    print(f"Wrote {panel_path}")

if __name__ == "__main__":
    sonify_doubling_map()
    print("Done!")
