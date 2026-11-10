"""Rule 110: A cellular automaton on the edge of chaos.

Elementary cellular automata apply a rule to a 1D array, where each cell's
next state depends on its current state and its two neighbors (3 cells = 8
configurations).

Rule 110 (binary 01101110) is famous for:
1. Turing completeness: It can compute any computable function
2. Edge-of-chaos behavior: Neither fully ordered nor fully random
3. Wolfram class IV: Complex behavior from simple rule

This is a profound example of emergence: a trivial rule produces universal
computation.

Unlike Game of Life (which has known patterns like gliders), Rule 110
produces complex, hard-to-predict dynamics that depend critically on initial
conditions and require simulation to understand.

Outputs in ./out:
  rule110.wav     — 16-bit mono, 22.05 kHz (sonification)
  rule110_evolution.png — Grid evolution over time
  rule110_zooms.png — Multiple zoom levels showing structure
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Rule 110: 01101110 in binary
RULE_110 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}

def apply_rule_110(state, rule=RULE_110):
    """Apply Rule 110 to a 1D array."""
    n = len(state)
    new_state = np.zeros(n, dtype=np.uint8)

    for i in range(n):
        left = state[(i - 1) % n]
        center = state[i]
        right = state[(i + 1) % n]

        new_state[i] = rule.get((left, center, right), 0)

    return new_state

def evolve_rule110(width=2048, generations=1024, initial_density=0.3):
    """Evolve Rule 110 for many generations."""
    # Create random initial state
    state = (np.random.rand(width) < initial_density).astype(np.uint8)

    # Store all generations
    evolution = [state.copy()]

    for gen in range(1, generations):
        state = apply_rule_110(state)
        evolution.append(state.copy())

        if gen % 256 == 0:
            print(f"  Generation {gen}/{generations}")

    return np.array(evolution, dtype=np.uint8)

def visualize_evolution(evolution, filename):
    """Visualize the grid evolution as an image."""
    generations, width = evolution.shape

    # Create image: width × generations
    img = Image.new("RGB", (width, generations), color=(0, 0, 0))
    pixels = img.load()

    for gen in range(generations):
        for x in range(width):
            if evolution[gen, x]:
                # Live cell: gradient color by generation
                t = gen / generations
                r = int(50 + 200 * t)
                g = int(100 + 100 * (1 - abs(2*t - 1)))
                b = int(200 - 100 * t)
                pixels[x, gen] = (r, g, b)

    img.save(filename)
    print(f"Wrote {filename}")

def analyze_structure(evolution):
    """Analyze the Rule 110 evolution."""
    print("\nRule 110 Structure Analysis:")
    print("=" * 60)

    generations, width = evolution.shape

    # Compute density per generation
    density = np.mean(evolution, axis=1)

    print(f"Initial density: {density[0]:.3f}")
    print(f"Final density: {density[-1]:.3f}")
    print(f"Average density: {np.mean(density):.3f}")
    print(f"Min density: {np.min(density):.3f}")
    print(f"Max density: {np.max(density):.3f}")

    # Look for stable structures
    density_diffs = np.abs(np.diff(density))
    print(f"\nDensity volatility (mean abs change): {np.mean(density_diffs):.6f}")

    # Compute entropy (randomness) of final state
    final_entropy = -np.sum(np.mean(evolution[-100:], axis=0) * np.log2(np.mean(evolution[-100:], axis=0) + 1e-10)) / width
    print(f"Final entropy (Shannon): {final_entropy:.3f} bits/cell")

    # Look for periodicity in a single row
    row = evolution[:, width // 2]

    # Find period by checking repeats
    for period in range(1, 256):
        is_periodic = True
        for i in range(period, min(512, len(row) - period)):
            if row[i] != row[i - period]:
                is_periodic = False
                break
        if is_periodic:
            print(f"Row {width//2} shows period {period}")
            break

    # Global statistics
    total_cells = generations * width
    live_cells = np.sum(evolution)
    print(f"\nTotal live cells: {live_cells}/{total_cells} = {100*live_cells/total_cells:.2f}%")

def sonify_rule110(evolution, sample_rate=22050, duration_sec=3):
    """Sonify Rule 110 evolution."""
    print("\nSonifying Rule 110...")

    generations, width = evolution.shape
    duration_samples = int(duration_sec * sample_rate)
    audio = np.zeros(duration_samples, dtype=np.float64)

    # Map generations to time
    samples_per_gen = duration_samples // generations

    # Frequency mapping: position in width → frequency
    freq_min = 440 * 0.5  # A3
    freq_max = 440 * 2    # A4

    t = np.arange(samples_per_gen) / sample_rate

    for gen in range(generations):
        # Compute weighted frequency from cell state
        row = evolution[gen]

        # Find active regions
        active_indices = np.where(row > 0)[0]

        if len(active_indices) > 0:
            # Center of mass of active cells
            center = np.mean(active_indices)
            freq = freq_min + (center / width) * (freq_max - freq_min)

            # Density determines amplitude
            density = np.mean(row)
            amplitude = 0.1 + 0.4 * density

            # Generate tone
            start_sample = gen * samples_per_gen
            end_sample = min(start_sample + samples_per_gen, duration_samples)

            if start_sample >= duration_samples:
                break

            t_local = t[:end_sample - start_sample]
            phase = 2.0 * np.pi * freq * t_local
            wave = np.sin(phase) * amplitude

            # Envelope
            envelope = np.hanning(len(wave))
            wave *= envelope

            audio[start_sample:end_sample] += wave

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95

    audio_int16 = (audio * 32767).astype(np.int16)

    import scipy.io.wavfile
    wav_path = os.path.join(OUT, "rule110.wav")
    scipy.io.wavfile.write(wav_path, sample_rate, audio_int16)
    print(f"Wrote {wav_path}")

def create_zoom_sequence(evolution):
    """Create multiple zoom levels showing fractal-like structure."""
    generations, width = evolution.shape

    # Different time scales
    zoom_levels = [
        ("full", 0, generations, 1),
        ("zoom1", 0, generations // 2, 1),
        ("zoom2", generations // 4, 3 * generations // 4, 1),
        ("deep", generations // 2, 3 * generations // 4, 2),
    ]

    for name, gen_start, gen_end, stride in zoom_levels:
        subset = evolution[gen_start:gen_end:stride]

        sub_gen, sub_width = subset.shape

        # Create image
        img = Image.new("RGB", (sub_width, sub_gen), color=(0, 0, 0))
        pixels = img.load()

        for gen in range(sub_gen):
            for x in range(sub_width):
                if subset[gen, x]:
                    # Live cell: color by generation
                    t = gen / max(1, sub_gen - 1)
                    r = int(50 + 200 * t)
                    g = int(100 + 150 * np.sin(np.pi * t))
                    b = int(200 - 100 * t)
                    pixels[x, gen] = (r, g, b)

        filename = os.path.join(OUT, f"rule110_zoom_{name}.png")
        img.save(filename)
        print(f"Wrote {filename}")

if __name__ == "__main__":
    print("Evolving Rule 110...")
    evolution = evolve_rule110(width=2048, generations=1024, initial_density=0.3)

    print("\nVisualizing...")
    visualize_evolution(evolution, os.path.join(OUT, "rule110_evolution.png"))

    analyze_structure(evolution)

    print("\nCreating zoom sequence...")
    create_zoom_sequence(evolution)

    sonify_rule110(evolution, duration_sec=3)

    print("\nDone!")
