"""Sonify the Lorenz attractor.

The trajectory drives audio in three ways:
- z-coordinate (height) → log-mapped pitch
- x-coordinate (lobe selector) → stereo pan
- y-coordinate → amplitude envelope

The control signals are heavily low-pass filtered so the swirls and lobe
transitions of the Lorenz attractor are perceivable as pitch motion (cycles
per second), not as broadband FM noise. The integration is paced so that one
"swirl" of the attractor occupies several hundred milliseconds of audio.

Outputs in ./out:
  lorenz.wav        — 16-bit stereo, 22.05 kHz
  spectrogram.png   — STFT of the mono mix
  trajectory.png    — x–z projection of the trajectory, color = time
  panel.png         — combined contact sheet
"""

import math
import os
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

SAMPLE_RATE = 22050
DURATION = 24.0  # seconds
N = int(SAMPLE_RATE * DURATION)

# Lorenz time per audio sample. Canonical Lorenz has a "swirl" period of
# roughly 0.7 time units. With dt = 8e-5 per sample, one swirl takes about
# 8750 samples ≈ 0.4 s — well-paced for the ear.
LORENZ_DT = 0.00008

# Lorenz parameters (canonical)
SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def lorenz(x, y, z):
    return SIGMA * (y - x), x * (RHO - z) - y, x * y - BETA * z


def integrate(n_steps, dt):
    x, y, z = 1.0, 1.0, 1.0
    xs = np.empty(n_steps, dtype=np.float64)
    ys = np.empty(n_steps, dtype=np.float64)
    zs = np.empty(n_steps, dtype=np.float64)
    for i in range(n_steps):
        k1x, k1y, k1z = lorenz(x, y, z)
        k2x, k2y, k2z = lorenz(
            x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, z + 0.5 * dt * k1z
        )
        k3x, k3y, k3z = lorenz(
            x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, z + 0.5 * dt * k2z
        )
        k4x, k4y, k4z = lorenz(x + dt * k3x, y + dt * k3y, z + dt * k3z)
        x += dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0
        y += dt * (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0
        z += dt * (k1z + 2 * k2z + 2 * k3z + k4z) / 6.0
        xs[i] = x
        ys[i] = y
        zs[i] = z
    return xs, ys, zs


def smooth(arr, window_samples):
    if window_samples < 2:
        return arr
    k = np.ones(window_samples) / window_samples
    return np.convolve(arr, k, mode="same")


def synth(xs, ys, zs):
    # Smooth all control signals so they vary at perceptual timescales,
    # not audio-rate FM noise.
    z_smooth = smooth(zs, int(0.05 * SAMPLE_RATE))  # ~50 ms smoothing
    x_smooth = smooth(xs, int(0.10 * SAMPLE_RATE))  # ~100 ms smoothing
    y_smooth = smooth(ys, int(0.20 * SAMPLE_RATE))  # ~200 ms smoothing

    # Pitch mapping: z drives pitch over a clean 2-octave range. Pentatonic
    # quantization (A minor) makes the result musically coherent without
    # losing the trajectory's continuity — we round the log-frequency to
    # nearest scale degree.
    z_lo, z_hi = float(np.percentile(z_smooth, 2)), float(np.percentile(z_smooth, 98))
    z_norm = np.clip((z_smooth - z_lo) / (z_hi - z_lo), 0.0, 1.0)
    freq_lo = 220.0  # A3
    n_octaves = 2.0
    log_freq = np.log2(freq_lo) + z_norm * n_octaves
    # A minor pentatonic in semitones from A: 0, 3, 5, 7, 10
    scale = np.array([0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24]) / 12.0
    # Quantize: for each sample, snap log_freq's fractional-octave part to
    # the nearest scale degree.
    base_log = np.log2(freq_lo)
    rel = log_freq - base_log  # offset in octaves
    # Snap to scale grid
    rel_q = scale[np.argmin(np.abs(scale[None, :] - rel[:, None]), axis=1)]
    freqs = 2.0 ** (base_log + rel_q)

    # Glide between quantized notes — short slew so attacks aren't jarring
    slew_samples = int(0.015 * SAMPLE_RATE)
    if slew_samples > 1:
        kernel = np.ones(slew_samples) / slew_samples
        freqs = np.convolve(freqs, kernel, mode="same")

    # Phase accumulator → carrier
    dt = 1.0 / SAMPLE_RATE
    phase = np.cumsum(2.0 * np.pi * freqs * dt)

    # Layered timbre: fundamental + soft 2nd harmonic + softer 3rd
    voice = (
        1.00 * np.sin(phase)
        + 0.35 * np.sin(2.0 * phase)
        + 0.12 * np.sin(3.0 * phase + 0.4)
    )

    # A second voice an octave below for body, modulated separately
    bass_phase = np.cumsum(2.0 * np.pi * freqs * 0.5 * dt)
    bass = 0.45 * np.sin(bass_phase) + 0.18 * np.sin(2.0 * bass_phase)

    mono = voice + bass

    # Amplitude envelope: gentle swells driven by smoothed |y|
    y_env = 0.6 + 0.35 * np.tanh(np.abs(y_smooth) / 12.0)
    mono = mono * y_env

    # Stereo pan from smoothed x. Equal-power panning.
    pan = np.tanh(x_smooth / 10.0)
    pan_theta = (pan + 1.0) * (math.pi / 4.0)
    left = mono * np.cos(pan_theta)
    right = mono * np.sin(pan_theta)

    # Fade in/out
    fade = int(0.8 * SAMPLE_RATE)
    fade_in = np.linspace(0.0, 1.0, fade)
    fade_out = np.linspace(1.0, 0.0, fade)
    for arr in (left, right):
        arr[:fade] *= fade_in
        arr[-fade:] *= fade_out

    # Peak normalize with headroom
    peak = max(float(np.max(np.abs(left))), float(np.max(np.abs(right))))
    if peak > 0:
        scale = 0.82 / peak
        left = left * scale
        right = right * scale
    return left, right, freqs


def write_wav(path, left, right):
    interleaved = np.empty(2 * len(left), dtype=np.int16)
    interleaved[0::2] = np.clip(left * 32767, -32768, 32767).astype(np.int16)
    interleaved[1::2] = np.clip(right * 32767, -32768, 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(interleaved.tobytes())


# --- visualization ----------------------------------------------------------

def stft(signal, window_size=2048, hop=512):
    n_windows = 1 + (len(signal) - window_size) // hop
    window = np.hanning(window_size)
    spec = np.empty((window_size // 2 + 1, n_windows), dtype=np.float64)
    for i in range(n_windows):
        chunk = signal[i * hop : i * hop + window_size] * window
        f = np.fft.rfft(chunk)
        spec[:, i] = np.abs(f)
    return spec


def palette_inferno(t):
    stops = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.05, 0.02, 0.18],
            [0.25, 0.05, 0.34],
            [0.55, 0.10, 0.40],
            [0.85, 0.25, 0.30],
            [1.0, 0.55, 0.18],
            [1.0, 0.92, 0.55],
            [1.0, 1.0, 0.92],
        ]
    )
    positions = np.linspace(0, 1, len(stops))
    r = np.interp(t, positions, stops[:, 0])
    g = np.interp(t, positions, stops[:, 1])
    b = np.interp(t, positions, stops[:, 2])
    return np.stack([r, g, b], axis=-1)


def load_fonts():
    try:
        title = ImageFont.truetype(
            "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf", 26
        )
        small = ImageFont.truetype(
            "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf", 17
        )
        return title, small
    except Exception:
        return ImageFont.load_default(), ImageFont.load_default()


def render_spectrogram(left, right, path):
    mono = 0.5 * (left + right)
    spec = stft(mono, window_size=2048, hop=512)
    log_spec = np.log10(spec + 1e-6)
    lo, hi = np.percentile(log_spec, 5), np.percentile(log_spec, 99.5)
    norm = np.clip((log_spec - lo) / (hi - lo), 0.0, 1.0)

    max_freq = 3000.0
    nyquist = SAMPLE_RATE / 2.0
    max_bin = int(max_freq / nyquist * norm.shape[0])
    norm = norm[:max_bin]

    h_out = 600
    bin_freqs = np.linspace(0.0, max_freq, norm.shape[0])
    log_bins = np.logspace(np.log10(100.0), np.log10(max_freq), h_out)
    out = np.empty((h_out, norm.shape[1]), dtype=np.float64)
    for col in range(norm.shape[1]):
        out[:, col] = np.interp(log_bins, bin_freqs, norm[:, col])
    out = out[::-1]

    rgb = (palette_inferno(out) * 255).astype(np.uint8)
    img = Image.fromarray(rgb)
    img = img.resize((1600, h_out), Image.LANCZOS)

    title_font, small_font = load_fonts()
    canvas = Image.new("RGB", (1700, 720), (12, 12, 16))
    canvas.paste(img, (80, 80))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (24, 24),
        "Lorenz attractor — sonification spectrogram",
        fill=(230, 230, 230),
        font=title_font,
    )
    draw.text(
        (24, 56),
        "z → pitch (A minor pentatonic, A3–A5);  x → stereo pan;  y → amplitude.",
        fill=(170, 170, 180),
        font=small_font,
    )

    # Frequency ticks
    tick_freqs = [110, 220, 440, 880, 1760]
    for f in tick_freqs:
        t = (np.log10(f) - np.log10(100.0)) / (np.log10(max_freq) - np.log10(100.0))
        if 0 <= t <= 1:
            y = 80 + int((1 - t) * h_out)
            draw.line([(70, y), (80, y)], fill=(200, 200, 200), width=1)
            draw.text((24, y - 9), f"{f}", fill=(200, 200, 200), font=small_font)
    draw.text((24, 80 + h_out + 6), "time →", fill=(170, 170, 180), font=small_font)
    canvas.save(path)
    return path


def render_trajectory(xs, ys, zs, path):
    w, h = 1700, 720
    img = Image.new("RGB", (w, h), (10, 10, 14))
    draw = ImageDraw.Draw(img)
    x_lo, x_hi = float(np.min(xs)), float(np.max(xs))
    z_lo, z_hi = float(np.min(zs)), float(np.max(zs))

    margin = 60
    step = max(1, len(xs) // 100000)
    px = ((xs[::step] - x_lo) / (x_hi - x_lo) * (w - 2 * margin) + margin).astype(np.int32)
    py = (
        h
        - (
            (zs[::step] - z_lo) / (z_hi - z_lo) * (h - 2 * margin) + margin
        )
    ).astype(np.int32)
    t_norm = np.linspace(0, 1, len(px))
    colors = (palette_inferno(t_norm) * 255).astype(np.uint8)

    pixels = img.load()
    for x_pt, y_pt, c in zip(px, py, colors):
        if 0 <= x_pt < w and 0 <= y_pt < h:
            cr, cg, cb = int(c[0]), int(c[1]), int(c[2])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    xx, yy = x_pt + dx, y_pt + dy
                    if 0 <= xx < w and 0 <= yy < h:
                        pr, pg, pb = pixels[xx, yy]
                        pixels[xx, yy] = (
                            min(255, pr + cr // 7),
                            min(255, pg + cg // 7),
                            min(255, pb + cb // 7),
                        )
    title_font, small_font = load_fonts()
    draw.text(
        (24, 20),
        "Lorenz trajectory (x–z projection)",
        fill=(230, 230, 230),
        font=title_font,
    )
    draw.text(
        (24, 52),
        "σ=10, ρ=28, β=8/3.   Color = time, dark → bright over 24 s of audio.",
        fill=(170, 170, 180),
        font=small_font,
    )
    img.save(path)
    return path


def render_panel(traj_path, spec_path, panel_path):
    traj = Image.open(traj_path)
    spec = Image.open(spec_path)
    w = max(traj.width, spec.width)
    canvas = Image.new("RGB", (w, traj.height + spec.height + 20), (8, 8, 12))
    canvas.paste(traj, ((w - traj.width) // 2, 0))
    canvas.paste(spec, ((w - spec.width) // 2, traj.height + 20))
    canvas.save(panel_path)
    return panel_path


def main():
    print(f"Integrating {N} steps...")
    xs, ys, zs = integrate(N, LORENZ_DT)
    print(f"  x ∈ [{xs.min():.2f}, {xs.max():.2f}]")
    print(f"  y ∈ [{ys.min():.2f}, {ys.max():.2f}]")
    print(f"  z ∈ [{zs.min():.2f}, {zs.max():.2f}]")
    print(f"  Lorenz time covered: {N * LORENZ_DT:.2f} units")

    print("Synthesizing audio...")
    left, right, freqs = synth(xs, ys, zs)
    print(f"  pitch range: {freqs.min():.1f} – {freqs.max():.1f} Hz")

    wav_path = os.path.join(OUT, "lorenz.wav")
    write_wav(wav_path, left, right)
    print(f"Wrote {wav_path}  ({len(left) / SAMPLE_RATE:.1f} s stereo)")

    spec_path = render_spectrogram(left, right, os.path.join(OUT, "spectrogram.png"))
    print(f"Wrote {spec_path}")

    traj_path = render_trajectory(xs, ys, zs, os.path.join(OUT, "trajectory.png"))
    print(f"Wrote {traj_path}")

    panel_path = render_panel(traj_path, spec_path, os.path.join(OUT, "panel.png"))
    print(f"Wrote {panel_path}")


if __name__ == "__main__":
    main()
