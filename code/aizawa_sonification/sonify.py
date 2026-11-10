"""Sonify the Aizawa attractor.

The Aizawa system exhibits a toroidal shape with crown-like oscillations,
creating a different sonic character than Lorenz (two lobes) or Rössler
(single spiral).

The topology creates alternating sections: the trajectory spirals on the
torus, then periodically escapes to the crown region, creating a punctuated
rhythmic structure.

Sonification:
- z-coordinate (height) → log-mapped pitch
- Distance from z-axis → pan and harmonic content
- x-coordinate rate of change → amplitude modulation (texture)

Outputs in ./out:
  aizawa.wav        — 16-bit stereo, 22.05 kHz
  spectrogram.png   — STFT of the mono mix
  trajectory.png    — x–z projection of the trajectory, color = time
  panel.png          — combined contact sheet
"""

import math
import os
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

SAMPLE_RATE = 22050
DURATION = 28.0  # seconds (longer to capture crown structure)
N = int(SAMPLE_RATE * DURATION)

# Aizawa time per audio sample
AIZAWA_DT = 0.0001

# Aizawa parameters (canonical chaotic regime)
# These create the toroidal + crown structure
A = 0.95
B = 0.7
C = 0.6
D = 3.5
E = 0.25
F = 0.1


def aizawa(x, y, z):
    """Aizawa differential equations."""
    x_dot = (z - B) * x - D * y
    y_dot = D * x + (z - B) * y
    z_dot = C + A * z - (z ** 3) / 3 - (x ** 2 + y ** 2) * (1 + E * z) + F * z * (x ** 3)
    return x_dot, y_dot, z_dot


def integrate(n_steps, dt):
    """Integrate Aizawa using RK4."""
    x, y, z = 0.1, 0.0, 0.0
    xs = np.empty(n_steps, dtype=np.float64)
    ys = np.empty(n_steps, dtype=np.float64)
    zs = np.empty(n_steps, dtype=np.float64)

    for i in range(n_steps):
        xs[i], ys[i], zs[i] = x, y, z

        # RK4
        k1_x, k1_y, k1_z = aizawa(x, y, z)
        k2_x, k2_y, k2_z = aizawa(x + dt * k1_x / 2, y + dt * k1_y / 2, z + dt * k1_z / 2)
        k3_x, k3_y, k3_z = aizawa(x + dt * k2_x / 2, y + dt * k2_y / 2, z + dt * k2_z / 2)
        k4_x, k4_y, k4_z = aizawa(x + dt * k3_x, y + dt * k3_y, z + dt * k3_z)

        x += dt * (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        y += dt * (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        z += dt * (k1_z + 2 * k2_z + 2 * k3_z + k4_z) / 6

    return xs, ys, zs


def low_pass_filter(signal, cutoff_freq, sample_rate):
    """Simple exponential low-pass filter."""
    rc = 1.0 / (2 * np.pi * cutoff_freq)
    dt = 1.0 / sample_rate
    alpha = dt / (rc + dt)

    filtered = np.zeros_like(signal)
    filtered[0] = signal[0]
    for i in range(1, len(signal)):
        filtered[i] = filtered[i - 1] + alpha * (signal[i] - filtered[i - 1])

    return filtered


def sonify_aizawa():
    """Generate the full sonification."""
    # Integrate Aizawa
    xs, ys, zs = integrate(N, AIZAWA_DT)

    # Compute control signals
    # Z coordinate: pitch
    z_filtered = low_pass_filter(zs, 2.5, SAMPLE_RATE)
    z_norm = (z_filtered - np.min(z_filtered)) / (np.max(z_filtered) - np.min(z_filtered))
    midi_pitch = 48 + z_norm * 28  # MIDI 48–76 (wider range than Lorenz)
    hz_pitch = 440.0 * 2.0 ** ((midi_pitch - 69) / 12.0)

    # Distance from z-axis: pan and harmonic
    radius = np.sqrt(xs ** 2 + ys ** 2)
    radius_filtered = low_pass_filter(radius, 2.0, SAMPLE_RATE)
    radius_norm = (radius_filtered - np.min(radius_filtered)) / (np.max(radius_filtered) - np.min(radius_filtered))
    pan = radius_norm
    harmonic_mix = radius_norm * 0.4  # up to 40% 2nd harmonic

    # X rate of change: amplitude modulation (texture)
    dx_dt = np.gradient(xs, AIZAWA_DT)
    dx_dt_filtered = low_pass_filter(np.abs(dx_dt), 3.0, SAMPLE_RATE)
    dx_dt_norm = np.clip((dx_dt_filtered - np.min(dx_dt_filtered)) / (np.max(dx_dt_filtered) - np.min(dx_dt_filtered)), 0, 1)
    amplitude_mod = 0.3 + 0.6 * dx_dt_norm

    # Quantize to pentatonic
    pentatonic_midi = [60, 62, 64, 67, 69]  # C, D, E, G, A
    quantized_pitch = np.zeros_like(hz_pitch)
    for i, hz in enumerate(hz_pitch):
        midi = 69 + 12 * np.log2(hz / 440.0)
        best_midi = pentatonic_midi[0]
        best_dist = abs(midi - best_midi)
        for p_midi in pentatonic_midi:
            dist = abs(midi - p_midi)
            if dist < best_dist:
                best_dist = dist
                best_midi = p_midi
        quantized_pitch[i] = best_midi

    hz_quantized = 440.0 * 2.0 ** ((quantized_pitch - 69) / 12.0)

    # Synthesize
    phase_quantized = 2.0 * np.pi * np.cumsum(hz_quantized) / SAMPLE_RATE
    fundamental_q = np.sin(phase_quantized)
    harmonic_2_q = np.sin(2 * phase_quantized)

    wave_mix_q = fundamental_q * (1.0 - harmonic_mix) + harmonic_2_q * harmonic_mix

    # Apply modulation
    left = wave_mix_q * amplitude_mod * (1.0 - pan)
    right = wave_mix_q * amplitude_mod * pan

    # Normalize
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if max_val > 0:
        left = left / max_val * 0.95
        right = right / max_val * 0.95

    # Interleave to stereo
    audio = np.zeros(2 * N, dtype=np.float64)
    audio[0::2] = left
    audio[1::2] = right

    audio_int16 = (audio * 32767).astype(np.int16)

    # Write WAV
    wav_path = os.path.join(OUT, "aizawa.wav")
    with wave.open(wav_path, 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_int16.tobytes())

    print(f"Wrote {wav_path}")

    # Trajectory visualization
    fig_width, fig_height = 1400, 300
    img = Image.new("RGB", (fig_width, fig_height), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    # x–z projection
    margin = 40
    plot_width = fig_width - 2 * margin
    plot_height = fig_height - 2 * margin

    x_min, x_max = np.min(xs), np.max(xs)
    z_min, z_max = np.min(zs), np.max(zs)

    prev_px, prev_py = None, None
    for i in range(N):
        px = margin + (xs[i] - x_min) / (x_max - x_min) * plot_width
        py = margin + plot_height * (1.0 - (zs[i] - z_min) / (z_max - z_min))

        if prev_px is not None:
            # Color by time (purple → cyan)
            progress = i / N
            r = int(180 * (1 - progress) + 100 * progress)
            g = int(100 + 155 * progress)
            b = int(200 - 100 * progress)
            draw.line([(prev_px, prev_py), (px, py)], fill=(r, g, b), width=1)

        prev_px, prev_py = px, py

    # Axes
    draw.rectangle(
        [(margin, margin), (margin + plot_width, margin + plot_height)],
        outline=(100, 100, 100),
        width=2
    )

    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw.text((10, margin + plot_height // 2), "z", fill=(200, 200, 200), font=fnt)
    draw.text((margin + plot_width // 2, fig_height - 20), "x", fill=(200, 200, 200), font=fnt)

    img_path = os.path.join(OUT, "trajectory.png")
    img.save(img_path)
    print(f"Wrote {img_path}")

    # Spectrogram
    import scipy.signal

    mono = (left + right) / 2

    f, t, Sxx = scipy.signal.spectrogram(
        mono,
        fs=SAMPLE_RATE,
        nperseg=2048,
        noverlap=1024,
        window='hann'
    )

    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    Sxx_db = np.clip(Sxx_db, -60, 0)

    spec_height, spec_width = Sxx_db.shape[0], Sxx_db.shape[1]
    spec_img = Image.new("RGB", (spec_width, spec_height), color=(0, 0, 0))
    pixels = spec_img.load()

    for i in range(spec_height):
        for j in range(spec_width):
            val = Sxx_db[i, j]
            norm_val = (val + 60) / 60.0
            r = int(255 * max(0, norm_val - 0.5) * 2)
            g = int(255 * max(0, min(norm_val, 0.5) * 2))
            b = int(255 * (1.0 - norm_val))
            pixels[j, i] = (r, g, b)

    spec_path = os.path.join(OUT, "spectrogram.png")
    spec_img.save(spec_path)
    print(f"Wrote {spec_path}")

    # Panel
    panel = Image.new("RGB", (fig_width * 2, fig_height * 2), color=(20, 20, 20))
    panel.paste(img, (0, 0))
    panel.paste(spec_img.resize((fig_width, fig_height)), (fig_width, 0))

    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw_panel = ImageDraw.Draw(panel)
    draw_panel.text((10, fig_height + 10), "Aizawa Attractor Sonification", fill=(200, 200, 200), font=fnt)

    panel_path = os.path.join(OUT, "panel.png")
    panel.save(panel_path)
    print(f"Wrote {panel_path}")


if __name__ == "__main__":
    sonify_aizawa()
    print("Done!")
