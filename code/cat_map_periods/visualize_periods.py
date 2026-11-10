"""Visualize the cat map period function Π(N)."""

import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def prime_factorization(n):
    """Return prime factorization as a list."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def get_prime_color(n):
    """Color based on largest prime factor."""
    if n == 1:
        return (100, 100, 100)

    factors = prime_factorization(n)
    largest_prime = factors[-1]

    # Color by prime: 2→red, 3→green, 5→blue, 7→yellow, etc.
    prime_colors = {
        2: (255, 100, 100),
        3: (100, 255, 100),
        5: (100, 100, 255),
        7: (255, 255, 100),
        11: (255, 100, 255),
        13: (100, 255, 255),
    }

    return prime_colors.get(largest_prime, (150, 150, 150))


def visualize_periods():
    """Create visualizations of the period function."""

    with open('/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/cat_map_periods/periods.json', 'r') as f:
        results = json.load(f)

    periods = {int(k): v for k, v in results['periods'].items()}
    n_max = results['n_max']

    # 1. Main plot: Π(N) with bounds
    fig_width, fig_height = 1600, 400
    img = Image.new("RGB", (fig_width, fig_height), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    margin_l, margin_r = 50, 50
    margin_t, margin_b = 40, 40
    plot_width = fig_width - margin_l - margin_r
    plot_height = fig_height - margin_t - margin_b

    # Scale
    y_max = 800  # a bit above max period 750

    # Plot grid lines
    for y_val in [0, 100, 200, 300, 400, 500, 600, 700, 800]:
        py = margin_t + plot_height * (1.0 - y_val / y_max)
        draw.line([(margin_l, py), (margin_l + plot_width, py)], fill=(50, 50, 50), width=1)

    # Plot 3N bound envelope
    prev_px, prev_py = None, None
    for n in range(1, n_max + 1):
        px = margin_l + (n - 1) / (n_max - 1) * plot_width
        py = margin_t + plot_height * (1.0 - (3 * n) / y_max)

        if prev_px is not None:
            draw.line([(prev_px, prev_py), (px, py)], fill=(100, 100, 100), width=1)

        prev_px, prev_py = px, py

    # Plot actual periods (colored by prime factor)
    for n in range(1, n_max + 1):
        period = periods[n]
        px = margin_l + (n - 1) / (n_max - 1) * plot_width
        py = margin_t + plot_height * (1.0 - period / y_max)

        color = get_prime_color(n)
        draw.ellipse([(px - 2, py - 2), (px + 2, py + 2)], fill=color)

    # Axes
    draw.rectangle(
        [(margin_l, margin_t), (margin_l + plot_width, margin_t + plot_height)],
        outline=(200, 200, 200),
        width=2
    )

    # Labels
    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw.text((fig_width // 2 - 20, fig_height - 20), "N", fill=(200, 200, 200), font=fnt)
    draw.text((10, fig_height // 2), "Π(N)", fill=(200, 200, 200), font=fnt)

    # Y-axis labels
    for y_val in [0, 200, 400, 600, 800]:
        py = margin_t + plot_height * (1.0 - y_val / y_max)
        draw.text((10, py - 5), str(y_val), fill=(150, 150, 150), font=fnt)

    # X-axis labels
    for n_val in [0, 100, 200, 300]:
        px = margin_l + (n_val - 1) / (n_max - 1) * plot_width
        draw.text((px - 10, margin_t + plot_height + 5), str(n_val), fill=(150, 150, 150), font=fnt)

    img_path = '/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/cat_map_periods/out/periods_plot.png'
    img.save(img_path)
    print(f"Saved {img_path}")

    # 2. Histogram plot
    fig_width, fig_height = 1200, 400
    img2 = Image.new("RGB", (fig_width, fig_height), color=(20, 20, 20))
    draw2 = ImageDraw.Draw(img2)

    margin_l, margin_r = 50, 50
    margin_t, margin_b = 40, 40
    plot_width = fig_width - margin_l - margin_r
    plot_height = fig_height - margin_t - margin_b

    # Bin periods into groups
    bins = list(range(0, 801, 50))
    hist = [0] * (len(bins) - 1)

    for n in range(1, n_max + 1):
        period = periods[n]
        for i in range(len(bins) - 1):
            if bins[i] <= period < bins[i + 1]:
                hist[i] += 1
                break

    max_count = max(hist)
    bin_width = plot_width / len(hist)

    for i, count in enumerate(hist):
        x_start = margin_l + i * bin_width
        x_end = x_start + bin_width
        bar_height = plot_height * count / max_count
        y_top = margin_t + plot_height - bar_height

        draw2.rectangle(
            [(x_start + 2, y_top), (x_end - 2, margin_t + plot_height)],
            fill=(100, 150, 255)
        )

    # Axes
    draw2.rectangle(
        [(margin_l, margin_t), (margin_l + plot_width, margin_t + plot_height)],
        outline=(200, 200, 200),
        width=2
    )

    draw2.text((fig_width // 2 - 40, fig_height - 20), "Period", fill=(200, 200, 200), font=fnt)
    draw2.text((10, fig_height // 2), "Count", fill=(200, 200, 200), font=fnt)

    img2_path = '/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/cat_map_periods/out/periods_histogram.png'
    img2.save(img2_path)
    print(f"Saved {img2_path}")

    # 3. Create panel (combined view)
    panel = Image.new("RGB", (fig_width, fig_height + 100), color=(20, 20, 20))
    panel.paste(img, (0, 0))
    panel.paste(img2, (0, 400))

    draw_panel = ImageDraw.Draw(panel)
    draw_panel.text((10, fig_height + 410), "Cat Map Period Function Π(N)", fill=(200, 200, 200), font=fnt)
    draw_panel.text((10, fig_height + 430), "Left: periods with 3N envelope. Right: histogram of period distribution.", fill=(150, 150, 150), font=fnt)

    panel_path = '/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/cat_map_periods/out/panel.png'
    panel.save(panel_path)
    print(f"Saved {panel_path}")


if __name__ == "__main__":
    import os
    out_dir = '/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/cat_map_periods/out'
    os.makedirs(out_dir, exist_ok=True)

    visualize_periods()
    print("Done!")
