"""Sonify Conway's Game of Life.

The grid is divided into vertical bands. The population density of each band
maps to a pitch. As generations evolve, the density changes, creating a
temporal evolving soundscape.

The sonification reveals the dynamics of Life: growth, oscillation, collisions,
emergence of gliders and patterns.

Outputs in ./out:
  life.wav        — 16-bit mono, 22.05 kHz
  spectrogram.png — STFT of the audio
  evolution.png   — Grid state over time (population heatmap)
  panel.png       — combined contact sheet
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

GRID_SIZE = 128
N_GENERATIONS = 240  # 240 generations × sample_rate/30 ≈ 24 seconds
SAMPLE_RATE = 22050
SAMPLES_PER_GEN = SAMPLE_RATE // 10  # 10 generations per second

# Pentatonic scale: C, D, E, G, A (MIDI relative to C3 = 48)
PENTATONIC_MIDI = [48, 50, 52, 55, 57]  # C3, D3, E3, G3, A3

def create_random_seed(size, density=0.3):
    """Create random initial configuration."""
    return np.random.rand(size, size) < density

def count_neighbors(grid, i, j):
    """Count live neighbors (with wraparound)."""
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = (i + di) % len(grid)
            nj = (j + dj) % len(grid)
            if grid[ni, nj]:
                count += 1
    return count

def step_life(grid):
    """Perform one generation of Game of Life."""
    new_grid = np.zeros_like(grid)
    for i in range(len(grid)):
        for j in range(len(grid)):
            neighbors = count_neighbors(grid, i, j)
            if grid[i, j]:  # cell is alive
                if neighbors in [2, 3]:
                    new_grid[i, j] = True
            else:  # cell is dead
                if neighbors == 3:
                    new_grid[i, j] = True
    return new_grid

def sonify_life():
    """Generate Game of Life sonification."""
    # Initialize
    grid = create_random_seed(GRID_SIZE, density=0.25)
    
    # Storage for evolution and audio
    evolution = []
    densities = []
    
    # Generate generations and compute densities
    for gen in range(N_GENERATIONS):
        evolution.append(grid.copy())
        
        # Divide grid into vertical bands (7 bands for pentatonic)
        n_bands = len(PENTATONIC_MIDI)
        band_width = GRID_SIZE // n_bands
        band_densities = []
        
        for band_idx in range(n_bands):
            start_col = band_idx * band_width
            end_col = start_col + band_width if band_idx < n_bands - 1 else GRID_SIZE
            band = grid[:, start_col:end_col]
            density = np.mean(band)
            band_densities.append(density)
        
        densities.append(band_densities)
        grid = step_life(grid)
        
        if gen % 50 == 0:
            print(f"  Generation {gen}/{N_GENERATIONS}")
    
    # Generate audio from densities
    audio = np.zeros(N_GENERATIONS * SAMPLES_PER_GEN, dtype=np.float64)
    
    t = np.arange(SAMPLES_PER_GEN) / SAMPLE_RATE
    
    for gen in range(N_GENERATIONS):
        band_densities = densities[gen]
        start_sample = gen * SAMPLES_PER_GEN
        end_sample = start_sample + SAMPLES_PER_GEN
        
        # Synthesize: combine all bands into a chord
        wave_sum = np.zeros(SAMPLES_PER_GEN, dtype=np.float64)
        
        for band_idx, density in enumerate(band_densities):
            midi_note = PENTATONIC_MIDI[band_idx]
            hz = 440.0 * 2.0 ** ((midi_note - 69) / 12.0)
            
            # Only include band if there's significant population
            if density > 0.02:
                # Amplitude proportional to density
                amplitude = 0.1 + 0.5 * density
                
                # Synthesize tone
                phase = 2.0 * np.pi * hz * t
                wave = np.sin(phase) * amplitude
                wave_sum += wave
        
        # Add small envelope to avoid clicks
        envelope = np.hanning(SAMPLES_PER_GEN)
        wave_sum *= envelope
        
        # Normalize
        max_val = np.max(np.abs(wave_sum))
        if max_val > 0:
            wave_sum /= max_val
        
        audio[start_sample:end_sample] = wave_sum
    
    # Normalize overall
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95
    
    # Convert to 16-bit
    audio_int16 = (audio * 32767).astype(np.int16)
    
    # Write WAV using scipy
    import scipy.io.wavfile
    wav_path = os.path.join(OUT, "life.wav")
    scipy.io.wavfile.write(wav_path, SAMPLE_RATE, audio_int16)
    print(f"Wrote {wav_path}")
    
    # Generate evolution visualization
    fig_width, fig_height = 1200, 400
    img = Image.new("RGB", (fig_width, fig_height), color=(20, 20, 20))
    pixels = img.load()
    
    # Create heatmap of grid evolution
    for gen_idx in range(min(N_GENERATIONS, fig_width)):
        grid_state = evolution[gen_idx]
        col_sum = np.sum(grid_state, axis=0)
        
        # Map column to x-position
        x = int(gen_idx * fig_width / N_GENERATIONS)
        
        # Draw vertical line showing population at this generation
        for y in range(fig_height):
            # Invert y so top is recent
            y_inv = fig_height - y - 1
            
            # Map y to column position
            col_idx = int(y_inv * GRID_SIZE / fig_height)
            if col_idx < GRID_SIZE:
                col_value = col_sum[col_idx] / GRID_SIZE
                
                # Color by density
                r = int(50 + 200 * col_value)
                g = int(100 + 100 * (1 - col_value))
                b = int(150 - 100 * col_value)
                pixels[x, y] = (r, g, b)
    
    img_path = os.path.join(OUT, "evolution.png")
    img.save(img_path)
    print(f"Wrote {img_path}")
    
    # Generate spectrogram
    import scipy.signal
    
    f, t_spec, Sxx = scipy.signal.spectrogram(
        audio,
        fs=SAMPLE_RATE,
        nperseg=2048,
        noverlap=1024,
        window='hann'
    )
    
    # Convert to dB
    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    Sxx_db = np.clip(Sxx_db, -60, 0)
    
    # Create image
    spec_height, spec_width = Sxx_db.shape[0], Sxx_db.shape[1]
    spec_img = Image.new("RGB", (spec_width, spec_height), color=(0, 0, 0))
    spec_pixels = spec_img.load()
    
    for i in range(spec_height):
        for j in range(spec_width):
            val = Sxx_db[i, j]
            norm_val = (val + 60) / 60.0
            r = int(255 * max(0, norm_val - 0.5) * 2)
            g = int(255 * max(0, min(norm_val, 0.5) * 2))
            b = int(255 * (1.0 - norm_val))
            spec_pixels[j, i] = (r, g, b)
    
    spec_path = os.path.join(OUT, "spectrogram.png")
    spec_img.save(spec_path)
    print(f"Wrote {spec_path}")
    
    # Create panel
    panel = Image.new("RGB", (fig_width * 2, fig_height * 2), color=(20, 20, 20))
    panel.paste(img, (0, 0))
    panel.paste(spec_img.resize((fig_width, fig_height)), (fig_width, 0))
    
    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None
    
    draw_panel = ImageDraw.Draw(panel)
    draw_panel.text((10, fig_height + 10), "Game of Life Sonification", fill=(200, 200, 200), font=fnt)
    draw_panel.text((10, fig_height + 30), "Left: grid evolution. Right: audio spectrogram.", fill=(150, 150, 150), font=fnt)
    
    panel_path = os.path.join(OUT, "panel.png")
    panel.save(panel_path)
    print(f"Wrote {panel_path}")
    
    # Print stats
    print(f"\nGame of Life Sonification Complete")
    print(f"  Generations: {N_GENERATIONS}")
    print(f"  Grid size: {GRID_SIZE}x{GRID_SIZE}")
    print(f"  Audio duration: {N_GENERATIONS * SAMPLES_PER_GEN / SAMPLE_RATE:.1f} seconds")
    print(f"  Sample rate: {SAMPLE_RATE} Hz")


if __name__ == "__main__":
    sonify_life()
