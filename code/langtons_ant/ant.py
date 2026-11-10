"""Langton's Ant: A cellular automaton showing emergent highways.

Langton's Ant is one of the simplest possible cellular automata:
- A single "ant" moves on a 2D grid of black/white cells
- Rules (per cell the ant visits):
  * White cell: turn right, flip to black, move forward
  * Black cell: turn left, flip to white, move forward

Despite this simplicity, the ant exhibits three distinct phases:
1. Chaotic (1-10,000 steps): seemingly random wandering
2. Building period (10,000-100,000 steps): apparent structure emerges
3. Highways (100,000+ steps): long diagonal "highways" with period-4 cycles

The highways are the surprise: from a trivial rule emerges long-range order
and predictable structure. The ant "escapes" the chaos through emergent
organization.

This is pure emergence: no global blueprint, no communication, just local rules
creating global structure through repeated application.

Outputs:
  ant_evolution.png — grid state over first 100,000 steps
  ant_trajectory.png — ant's path color-coded by time
  ant_zoom_chaos.png — zoomed view of chaotic phase
  ant_zoom_highway.png — zoomed view of highway phase
  ant.wav — sonification (ant position → stereo position & frequency)
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Direction: 0=up, 1=right, 2=down, 3=left
DIRECTIONS = {
    0: (0, -1),  # up
    1: (1, 0),   # right
    2: (0, 1),   # down
    3: (-1, 0),  # left
}

class LangtonsAnt:
    def __init__(self, grid_size=512):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
        self.x = grid_size // 2
        self.y = grid_size // 2
        self.direction = 0  # 0=up, 1=right, 2=down, 3=left
        self.step_count = 0
        self.visited = []

    def step(self):
        """Perform one step of the ant's movement."""
        # Read current cell
        cell = self.grid[self.y, self.x]

        # Record position
        self.visited.append((self.x, self.y, self.step_count))

        if cell == 0:  # white
            # Turn right
            self.direction = (self.direction + 1) % 4
            # Flip to black
            self.grid[self.y, self.x] = 1
        else:  # black
            # Turn left
            self.direction = (self.direction - 1) % 4
            # Flip to white
            self.grid[self.y, self.x] = 0

        # Move forward
        dx, dy = DIRECTIONS[self.direction]
        self.x = (self.x + dx) % self.grid_size
        self.y = (self.y + dy) % self.grid_size

        self.step_count += 1

    def run(self, steps):
        """Run the ant for N steps."""
        for _ in range(steps):
            self.step()
            if _ % 10000 == 0:
                print(f"  Step {_}/{steps}")

def evolve_ant(steps=100000):
    """Evolve Langton's Ant."""
    print(f"Evolving Langton's Ant for {steps} steps...")
    ant = LangtonsAnt(grid_size=512)
    ant.run(steps)
    return ant

def visualize_grid(ant, filename):
    """Visualize the final grid state."""
    grid_size = ant.grid_size
    img = Image.new("RGB", (grid_size, grid_size), color=(255, 255, 255))
    pixels = img.load()

    for y in range(grid_size):
        for x in range(grid_size):
            if ant.grid[y, x]:  # black
                pixels[x, y] = (0, 0, 0)

    img.save(filename)
    print(f"Wrote {filename}")

def visualize_trajectory(ant, filename, max_steps=100000):
    """Visualize the ant's trajectory color-coded by time."""
    grid_size = ant.grid_size
    img = Image.new("RGB", (grid_size, grid_size), color=(30, 30, 30))
    pixels = img.load()

    # Plot trajectory
    for i, (x, y, step) in enumerate(ant.visited[:max_steps]):
        if 0 <= x < grid_size and 0 <= y < grid_size:
            # Color by phase
            if step < 10000:
                # Chaotic phase: blue
                color = (100, 100, 255)
            elif step < 100000:
                # Building phase: yellow
                color = (255, 255, 100)
            else:
                # Highway phase: red
                color = (255, 100, 100)

            pixels[x, y] = color

    img.save(filename)
    print(f"Wrote {filename}")

def analyze_ant(ant):
    """Analyze the ant's behavior."""
    print("\nLangton's Ant Analysis:")
    print("=" * 60)

    # Count black vs white
    black = np.sum(ant.grid)
    white = ant.grid_size**2 - black

    print(f"Total steps: {ant.step_count}")
    print(f"Black cells: {black} ({100*black/(ant.grid_size**2):.1f}%)")
    print(f"White cells: {white} ({100*white/(ant.grid_size**2):.1f}%)")

    # Analyze final position
    print(f"Final position: ({ant.x}, {ant.y})")

    # Check for periodic behavior (look at recent steps)
    if len(ant.visited) > 1000:
        recent = ant.visited[-1000:]
        positions = [(x, y) for x, y, _ in recent]

        # Look for period-4 pattern (characteristic of highways)
        for period in [4, 8, 12, 16]:
            is_periodic = True
            for i in range(period, min(200, len(positions))):
                if positions[i] != positions[i - period]:
                    is_periodic = False
                    break
            if is_periodic:
                print(f"Detected period-{period} pattern in final steps")
                break

def sonify_ant(ant, sample_rate=22050, duration_sec=5):
    """Sonify the ant's trajectory."""
    print("\nSonifying Langton's Ant...")

    duration_samples = int(duration_sec * sample_rate)
    audio = np.zeros(duration_samples, dtype=np.float64)

    # Map trajectory to audio
    visited_steps = len(ant.visited)
    samples_per_step = duration_samples // visited_steps

    t = np.arange(samples_per_step) / sample_rate

    for step_idx in range(min(visited_steps, duration_samples // samples_per_step)):
        x, y, step_num = ant.visited[step_idx]

        # Map position to frequency (center to edge = low to high)
        dist_from_center = np.sqrt((x - ant.grid_size//2)**2 + (y - ant.grid_size//2)**2)
        freq = 220 + 880 * (dist_from_center / (ant.grid_size / np.sqrt(2)))
        freq = np.clip(freq, 220, 1100)

        # Phase determines panning
        phase_angle = np.arctan2(y - ant.grid_size//2, x - ant.grid_size//2)
        pan = 0.5 + 0.5 * np.cos(phase_angle)

        # Generate tone
        start_sample = step_idx * samples_per_step
        end_sample = min(start_sample + samples_per_step, duration_samples)

        if start_sample >= duration_samples:
            break

        t_local = t[:end_sample - start_sample]
        phase = 2.0 * np.pi * freq * t_local
        wave = np.sin(phase) * 0.2

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
    wav_path = os.path.join(OUT, "ant.wav")
    scipy.io.wavfile.write(wav_path, sample_rate, audio_int16)
    print(f"Wrote {wav_path}")

def create_phase_visualizations(ant):
    """Create zoomed views of different phases."""
    grid_size = ant.grid_size

    # Chaotic phase zoom
    img_chaos = Image.new("RGB", (512, 512), color=(30, 30, 30))
    pixels = img_chaos.load()

    # Plot chaotic phase (first 10000 steps)
    for i, (x, y, step) in enumerate(ant.visited[:10000]):
        x_scaled = (x % 512)
        y_scaled = (y % 512)
        if 0 <= x_scaled < 512 and 0 <= y_scaled < 512:
            t = step / 10000.0
            r = int(100 + 155 * t)
            g = int(100 + 55 * t)
            b = int(200)
            pixels[x_scaled, y_scaled] = (r, g, b)

    img_chaos.save(os.path.join(OUT, "ant_zoom_chaos.png"))
    print(f"Wrote {os.path.join(OUT, 'ant_zoom_chaos.png')}")

    # Highway phase zoom (last 20000 steps)
    img_highway = Image.new("RGB", (512, 512), color=(30, 30, 30))
    pixels = img_highway.load()

    start_idx = max(0, len(ant.visited) - 20000)
    for i, (x, y, step) in enumerate(ant.visited[start_idx:]):
        x_scaled = (x % 512)
        y_scaled = (y % 512)
        if 0 <= x_scaled < 512 and 0 <= y_scaled < 512:
            t = i / 20000.0
            r = int(255)
            g = int(100 + 155 * t)
            b = int(100)
            pixels[x_scaled, y_scaled] = (r, g, b)

    img_highway.save(os.path.join(OUT, "ant_zoom_highway.png"))
    print(f"Wrote {os.path.join(OUT, 'ant_zoom_highway.png')}")

if __name__ == "__main__":
    print("Simulating Langton's Ant...")
    ant = evolve_ant(steps=100000)

    print("\nVisualizing...")
    visualize_grid(ant, os.path.join(OUT, "ant_grid.png"))
    visualize_trajectory(ant, os.path.join(OUT, "ant_trajectory.png"))
    create_phase_visualizations(ant)

    analyze_ant(ant)
    sonify_ant(ant, duration_sec=5)

    print("\nDone!")
