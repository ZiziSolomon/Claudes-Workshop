"""Compute and visualize Pisano periods.

The Pisano period π(n) is the period of the Fibonacci sequence modulo n.
Example: Fib mod 5 = [1, 1, 2, 3, 0, 3, 3, 1, 4, 0, 4, 4, 3, 2, 0, 2, 2, 4, 1, 0, ...]
which repeats with period 20.

Pisano periods are algebraic structures arising from number theory. They connect:
- Dynamical systems (periodic orbits)
- Number theory (Fibonacci structure)
- Algebra (matrix periodicity in Fibonacci recurrence)

The cat map (from the workshop) has Fibonacci numbers in its matrix [[1, 1], [1, 2]].
Pisano periods reveal the hidden periodicity in Fibonacci itself.

This script computes π(n) for n up to 1000 and visualizes the structure.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

def fibonacci_mod(n, max_terms=10000):
    """Compute Fibonacci sequence mod n until it repeats [1, 1]."""
    if n == 1:
        return 1

    a, b = 1, 1
    terms = [(a % n, b % n)]

    for _ in range(max_terms):
        a, b = b, (a + b) % n
        if a == 1 and b == 1:
            return len(terms)
        terms.append((a % n, b % n))

    return None  # Did not find period

def compute_pisano_periods(max_n=1000):
    """Compute Pisano periods for all n from 1 to max_n."""
    periods = {}

    for n in range(1, max_n + 1):
        period = fibonacci_mod(n)
        if period:
            periods[n] = period

        if n % 100 == 0:
            print(f"  Computed n={n}")

    return periods

def visualize_periods(periods, max_n=1000):
    """Create scatter plot of Pisano periods."""
    width, height = 1600, 1000
    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    pixels = img.load()

    # Find max period for scaling
    max_period = max(periods.values()) if periods else 1

    # Draw background grid
    draw = ImageDraw.Draw(img)
    for i in range(0, max_n + 1, 100):
        x = int(width * i / max_n)
        draw.line([(x, 0), (x, height)], fill=(50, 50, 50), width=1)

    for p in range(0, int(max_period) + 1, 100):
        y = height - int(height * p / max_period)
        draw.line([(0, y), (width, y)], fill=(50, 50, 50), width=1)

    # Plot points
    for n in range(1, max_n + 1):
        if n in periods:
            period = periods[n]

            x = int(width * n / max_n)
            y = height - int(height * period / max_period)

            # Color by period value
            t = period / max_period
            r = int(50 + 200 * t)
            g = int(100 + 100 * (1 - abs(2*t - 1)))
            b = int(200 - 100 * t)

            # Plot point and nearby pixels for visibility
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    px, py = x + dx, y + dy
                    if 0 <= px < width and 0 <= py < height:
                        pixels[px, py] = (r, g, b)

    # Labels
    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw.text((20, 20), f"Pisano Periods π(n)", fill=(200, 200, 200), font=fnt)
    draw.text((20, 50), f"n from 1 to {max_n}", fill=(150, 150, 150), font=fnt)
    draw.text((width - 200, height - 30), "n", fill=(150, 150, 150), font=fnt)
    draw.text((10, 10), "π(n)", fill=(150, 150, 150), font=fnt)

    # Axes
    margin = 40
    draw.rectangle([(margin, margin), (width - margin, height - margin)],
                   outline=(100, 100, 100), width=2)

    path = os.path.join(OUT, "pisano_periods.png")
    img.save(path)
    print(f"Wrote {path}")

def analyze_structure(periods):
    """Analyze patterns in Pisano periods."""
    print("\nPisano Period Structure Analysis:")
    print("=" * 60)

    # Powers of 2
    print("\nPowers of 2:")
    for k in range(1, 11):
        n = 2 ** k
        if n in periods:
            print(f"  π(2^{k}) = π({n}) = {periods[n]}")

    # Powers of 5 (golden ratio connection!)
    print("\nPowers of 5 (golden ratio appears here!):")
    for k in range(1, 6):
        n = 5 ** k
        if n in periods:
            print(f"  π(5^{k}) = π({n}) = {periods[n]}")

    # Powers of 3
    print("\nPowers of 3:")
    for k in range(1, 6):
        n = 3 ** k
        if n in periods:
            print(f"  π(3^{k}) = π({n}) = {periods[n]}")

    # Largest periods
    sorted_periods = sorted(periods.items(), key=lambda x: x[1], reverse=True)
    print("\nLargest Pisano periods:")
    for n, period in sorted_periods[:15]:
        print(f"  π({n:3d}) = {period:6d}")

    # Compare to n itself
    print("\nRatio π(n)/n for selected n:")
    for n in [10, 20, 50, 100, 200, 500, 1000]:
        if n in periods:
            ratio = periods[n] / n
            print(f"  π({n:4d}) / {n} = {ratio:.2f}")

def sonify_pisano_sequence(n, duration_sec=3):
    """Sonify a single Pisano sequence."""
    print(f"\nSonifying Pisano sequence for n={n}...")

    sample_rate = 22050
    duration_samples = int(duration_sec * sample_rate)

    # Generate Fibonacci mod n
    fib_seq = []
    a, b = 1, 1
    for _ in range(1000):
        fib_seq.append(a % n)
        a, b = b, (a + b) % n
        if a == 1 and b == 1:
            break

    # Map to pentatonic scale
    pentatonic_midi = [48, 50, 52, 55, 57]  # C3, D3, E3, G3, A3

    # Audio
    audio = np.zeros(duration_samples, dtype=np.float64)
    t = np.arange(duration_samples) / sample_rate

    # Stretch Fibonacci sequence to fill duration
    samples_per_fib_value = duration_samples // len(fib_seq)

    for fib_idx, fib_val in enumerate(fib_seq):
        midi_note = pentatonic_midi[fib_val % len(pentatonic_midi)]
        hz = 440.0 * 2.0 ** ((midi_note - 69) / 12.0)

        start_sample = fib_idx * samples_per_fib_value
        end_sample = min(start_sample + samples_per_fib_value, duration_samples)

        if start_sample >= duration_samples:
            break

        t_local = (t[start_sample:end_sample] - start_sample / sample_rate)
        phase = 2.0 * np.pi * hz * t_local
        wave = np.sin(phase) * 0.3

        # Envelope
        envelope = np.hanning(end_sample - start_sample)
        wave *= envelope

        audio[start_sample:end_sample] += wave

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95

    audio_int16 = (audio * 32767).astype(np.int16)

    import scipy.io.wavfile
    wav_path = os.path.join(OUT, f"pisano_{n}.wav")
    scipy.io.wavfile.write(wav_path, sample_rate, audio_int16)
    print(f"Wrote {wav_path}")

if __name__ == "__main__":
    print("Computing Pisano periods...")
    periods = compute_pisano_periods(max_n=1000)

    print(f"\nComputed {len(periods)} Pisano periods")

    print("\nVisualizing...")
    visualize_periods(periods, max_n=1000)

    analyze_structure(periods)

    # Sonify a few interesting sequences
    for n in [10, 20, 50]:
        if n in periods:
            sonify_pisano_sequence(n, duration_sec=3)

    print("\nDone!")
