"""Bifurcation diagram for the logistic map.

The logistic map is x_{n+1} = r * x_n * (1 - x_n), where r is the parameter.

For low r, the system has a stable fixed point (period 1).
As r increases, the fixed point becomes unstable and period-doubling occurs
(period 2, 4, 8, 16, ...).

Then chaos emerges. Then periodic windows within the chaos.
Then full chaos.

The bifurcation diagram visualizes this transition: x-axis is r, y-axis is x
(long-term behavior after transients). Each point shows the attractor at that r.

Outputs in ./out:
  bifurcation.png     — high-resolution bifurcation diagram
  logistic_map.txt    — parameter list and period information
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Parameters
R_MIN = 2.8
R_MAX = 4.0
X_MIN = 0.0
X_MAX = 1.0

N_R = 2000  # resolution in r dimension
N_ITERATIONS = 1000  # iterations to reach attractor
N_PLOT = 100  # iterations to plot

IMG_WIDTH = 2400
IMG_HEIGHT = 1200

def logistic_map(r, x):
    """Apply one iteration of the logistic map."""
    return r * x * (1.0 - x)

def compute_bifurcation():
    """Compute bifurcation diagram data."""
    # Create image
    img = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), color=(0, 0, 0))
    pixels = img.load()

    # For each r value
    for r_idx in range(N_R):
        r = R_MIN + (r_idx / N_R) * (R_MAX - R_MIN)

        # Start from initial condition
        x = 0.5

        # Iterate to reach attractor (skip transients)
        for _ in range(N_ITERATIONS):
            x = logistic_map(r, x)

        # Plot points on the attractor
        for _ in range(N_PLOT):
            x = logistic_map(r, x)

            # Map x to pixel coordinates
            px = r_idx
            py = int(IMG_HEIGHT * (1.0 - (x - X_MIN) / (X_MAX - X_MIN)))

            # Clamp to image bounds
            if 0 <= py < IMG_HEIGHT:
                # Color by x value (low=cool, high=hot)
                r_val = int(255 * x)
                g_val = int(128 * (1.0 - abs(2*x - 1)))
                b_val = int(255 * (1.0 - x))
                pixels[px, py] = (r_val, g_val, b_val)

        if r_idx % 500 == 0:
            print(f"  r progress: {r_idx}/{N_R} ({100*r_idx/N_R:.1f}%)")

    # Add axes and labels
    draw = ImageDraw.Draw(img)

    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    # Draw axes
    margin = 40
    draw.rectangle(
        [(margin, margin), (IMG_WIDTH - margin, IMG_HEIGHT - margin)],
        outline=(100, 100, 100),
        width=2
    )

    # Axis labels
    draw.text((IMG_WIDTH // 2 - 40, IMG_HEIGHT - 20), "r (parameter)", fill=(200, 200, 200), font=fnt)
    draw.text((10, IMG_HEIGHT // 2 - 20), "x", fill=(200, 200, 200), font=fnt)

    # Tick marks and values on r axis
    for r_val in [2.8, 3.0, 3.2, 3.4, 3.5, 3.56, 3.8, 4.0]:
        r_normalized = (r_val - R_MIN) / (R_MAX - R_MIN)
        x_pixel = margin + r_normalized * (IMG_WIDTH - 2 * margin)
        draw.line([(x_pixel, IMG_HEIGHT - margin), (x_pixel, IMG_HEIGHT - margin + 5)], fill=(100, 100, 100))
        draw.text((x_pixel - 10, IMG_HEIGHT - margin + 10), f"{r_val:.1f}", fill=(150, 150, 150), font=fnt)

    img_path = os.path.join(OUT, "bifurcation.png")
    img.save(img_path)
    print(f"Wrote {img_path}")

    # Analyze key r values for periods
    print("\nAnalyzing period-doubling cascade:")
    for r in [3.0, 3.44, 3.5, 3.56, 3.57, 3.58, 3.8, 4.0]:
        x = 0.5
        for _ in range(N_ITERATIONS):
            x = logistic_map(r, x)

        # Detect period by looking for repeats
        trajectory = []
        for _ in range(200):
            x = logistic_map(r, x)
            trajectory.append(x)

        # Simple period detection (look for closest match)
        period = None
        for p in range(1, 101):
            is_period = True
            for i in range(p, min(len(trajectory), 100)):
                if abs(trajectory[i] - trajectory[i - p]) > 1e-4:
                    is_period = False
                    break
            if is_period:
                period = p
                break

        if period is None:
            behavior = "chaotic"
        else:
            behavior = f"period {period}"

        print(f"  r = {r:.2f}: {behavior}")


def create_annotation():
    """Create an annotated version highlighting key regions."""
    # Load the base bifurcation diagram
    base_path = os.path.join(OUT, "bifurcation.png")
    img = Image.open(base_path)
    draw = ImageDraw.Draw(img)

    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    # Annotate key regions
    annotations = [
        (2.8, 3.0, "Stable\nfixed point", (100, 200, 255)),
        (3.0, 3.44, "Period\ndoubling", (255, 200, 100)),
        (3.56, 3.57, "Chaos\nbegins", (255, 100, 100)),
        (3.8, 4.0, "Chaotic\nwith windows", (200, 100, 255)),
    ]

    for r_start, r_end, label, color in annotations:
        r_norm_start = (r_start - R_MIN) / (R_MAX - R_MIN)
        r_norm_end = (r_end - R_MIN) / (R_MAX - R_MIN)

        x_start = 40 + r_norm_start * (img.width - 80)
        x_end = 40 + r_norm_end * (img.width - 80)

        # Draw annotation box
        draw.rectangle(
            [(x_start + 2, 20), (x_end - 2, 50)],
            outline=color,
            width=2
        )

        # Draw label
        draw.text((x_start + 5, 22), label, fill=color, font=fnt)

    ann_path = os.path.join(OUT, "bifurcation_annotated.png")
    img.save(ann_path)
    print(f"Wrote {ann_path}")


if __name__ == "__main__":
    print("Computing bifurcation diagram for logistic map...")
    compute_bifurcation()
    create_annotation()
    print("Done!")
