"""Generate Mandelbrot set visualization.

The Mandelbrot set is the set of complex numbers c for which the iteration
z_{n+1} = z_n^2 + c (starting with z_0 = 0) does not diverge.

Points in the set are colored black. Points outside are colored by escape time
(how many iterations before |z| > 2).

The Mandelbrot set exhibits fractal structure at all scales. Zooming reveals
infinite complexity. The boundary between the set and the exterior is a
fractal with dimension ≈ 2.

This connects to bifurcation: the Mandelbrot set's structure determines the
behavior of Julia sets. Regions of the Mandelbrot set correspond to different
dynamical regimes (fixed points, cycles, chaos).
"""

import os
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Full view
XMIN, XMAX = -2.5, 1.0
YMIN, YMAX = -1.25, 1.25
WIDTH, HEIGHT = 1600, 1200
MAX_ITER = 256

def mandelbrot(c, max_iter):
    """Compute escape time for complex number c."""
    z = 0.0j
    for n in range(max_iter):
        if abs(z) > 2.0:
            return n
        z = z * z + c
    return max_iter

def render_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter, filename):
    """Render Mandelbrot set to image."""
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    pixels = img.load()

    for py in range(height):
        y = ymin + (py / height) * (ymax - ymin)
        for px in range(width):
            x = xmin + (px / width) * (xmax - xmin)
            c = complex(x, y)

            iter_count = mandelbrot(c, max_iter)

            # Color by escape time
            if iter_count == max_iter:
                # In the set: black
                color = (0, 0, 0)
            else:
                # Outside: hot colormap
                t = iter_count / max_iter
                r = int(255 * (0.5 + 0.5 * np.sin(2 * np.pi * t)))
                g = int(255 * (0.5 + 0.5 * np.sin(2 * np.pi * (t + 1/3))))
                b = int(255 * (0.5 + 0.5 * np.sin(2 * np.pi * (t + 2/3))))
                color = (r, g, b)

            pixels[px, py] = color

        if py % 150 == 0:
            print(f"  Rendered {py}/{height} rows")

    img.save(filename)
    print(f"Wrote {filename}")

def render_zooms():
    """Render several zoom levels."""
    zooms = [
        ("full", -2.5, 1.0, -1.25, 1.25),
        ("zoom1", -0.8, -0.4, -0.2, 0.2),
        ("zoom2", -0.7485, -0.7465, 0.1105, 0.1125),
        ("zoom3", -0.748776, -0.748765, 0.110988, 0.110999),
    ]

    for name, xmin, xmax, ymin, ymax in zooms:
        filename = os.path.join(OUT, f"mandelbrot_{name}.png")
        print(f"\nRendering {name}...")
        render_mandelbrot(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, MAX_ITER, filename)

if __name__ == "__main__":
    print("Generating Mandelbrot set visualizations...")
    render_zooms()
    print("\nDone!")
