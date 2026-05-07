"""3D strange attractors of dissipative continuous-time dynamical systems.

Each system is a triple of coupled ODEs dx/dt = f(x,y,z). Integrate with RK4,
project to 2D, histogram into a density grid with depth shading, then map to
color. The orbit is a single long trajectory; the closure is the attractor.

Six systems with characteristic shapes:
  Lorenz     — the canonical butterfly; two lobes, infinite leaves
  Rossler    — single funnel band; period-doubling cascade then chaos
  Aizawa     — torus-with-spike; rotation around the z-axis with a crown
  Halvorsen  — three-lobed cyclic structure
  Thomas     — labyrinth in a cubical region; cyclic symmetry
  Chen       — double-scroll, related to Lorenz but distinctly different
"""

import math
import os
import sys
import numpy as np
from PIL import Image


# --- Vector fields. Each returns dx/dt, dy/dt, dz/dt at (x, y, z) ---


def lorenz(x, y, z, sigma=10.0, rho=28.0, beta=8.0/3.0):
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    return -y - z, x + a * y, b + z * (x - c)


def aizawa(x, y, z, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1):
    return ((z - b) * x - d * y,
            d * x + (z - b) * y,
            c + a * z - z * z * z / 3.0 - (x * x + y * y) * (1.0 + e * z) + f * z * x * x * x)


def halvorsen(x, y, z, a=1.4):
    return -a * x - 4.0 * y - 4.0 * z - y * y, -a * y - 4.0 * z - 4.0 * x - z * z, -a * z - 4.0 * x - 4.0 * y - x * x


def thomas(x, y, z, b=0.208186):
    return math.sin(y) - b * x, math.sin(z) - b * y, math.sin(x) - b * z


def chen(x, y, z, a=35.0, b=3.0, c=28.0):
    return a * (y - x), (c - a) * x - x * z + c * y, x * y - b * z


# --- Integration ---


def integrate(field, x0, dt, n_steps, burn_in=2000):
    """Classical RK4 integration. Returns (n_steps, 3) array of points."""
    x, y, z = x0
    # Burn-in: discard transient.
    for _ in range(burn_in):
        x, y, z = rk4_step(field, x, y, z, dt)
    out = np.empty((n_steps, 3), dtype=np.float64)
    for i in range(n_steps):
        x, y, z = rk4_step(field, x, y, z, dt)
        out[i, 0] = x
        out[i, 1] = y
        out[i, 2] = z
    return out


def rk4_step(field, x, y, z, dt):
    k1x, k1y, k1z = field(x, y, z)
    k2x, k2y, k2z = field(x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, z + 0.5 * dt * k1z)
    k3x, k3y, k3z = field(x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, z + 0.5 * dt * k2z)
    k4x, k4y, k4z = field(x + dt * k3x, y + dt * k3y, z + dt * k3z)
    return (x + dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0,
            y + dt * (k1y + 2 * k2y + 2 * k3y + k4y) / 6.0,
            z + dt * (k1z + 2 * k2z + 2 * k3z + k4z) / 6.0)


# --- Projection and rendering ---


def project(points, theta, phi):
    """Project 3D points onto a viewing plane.

    theta is azimuth (rotation around z), phi is elevation. Returns u, v, depth.
    Depth is the component along the viewing direction (greater = closer for our
    convention here: we shade lighter where depth is larger, i.e. closer).
    """
    ct, st = math.cos(theta), math.sin(theta)
    cp, sp = math.cos(phi), math.sin(phi)
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    # Right-handed: rotate by theta around z, then tilt by phi.
    xr = ct * x - st * y
    yr = st * x + ct * y
    u = xr
    v = cp * yr + sp * z
    depth = -sp * yr + cp * z
    return u, v, depth


def render_attractor(points, view, res=1400, gamma=0.4, cmap_name="ember",
                     pad=1.05, depth_blend=0.45):
    """Render points to an RGBA image.

    view: (theta, phi) in radians.
    depth_blend: weight (0..1) of depth shading layered over density.
    """
    theta, phi = view
    u, v, d = project(points, theta, phi)

    # Center and frame. Use percentiles to avoid letting rare excursions waste pixels.
    u_lo, u_hi = np.percentile(u, 0.05), np.percentile(u, 99.95)
    v_lo, v_hi = np.percentile(v, 0.05), np.percentile(v, 99.95)
    uc, vc = 0.5 * (u_lo + u_hi), 0.5 * (v_lo + v_hi)
    half = 0.5 * max(u_hi - u_lo, v_hi - v_lo) * pad

    # Density histogram.
    H, _, _ = np.histogram2d(
        v, u,
        bins=res,
        range=[[vc - half, vc + half], [uc - half, uc + half]],
    )
    H = H[::-1, :]  # image y-axis points downward

    # Depth-weighted histogram (mean depth per cell, weighted by density).
    H_depth, _, _ = np.histogram2d(
        v, u,
        bins=res,
        range=[[vc - half, vc + half], [uc - half, uc + half]],
        weights=d,
    )
    H_depth = H_depth[::-1, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        depth_avg = np.where(H > 0, H_depth / np.maximum(H, 1), 0.0)

    # Density compression.
    H_log = np.log1p(H)
    H_norm = H_log / max(H_log.max(), 1e-9)
    H_g = H_norm ** gamma

    # Depth normalization to [0, 1]; only meaningful where density > 0.
    occupied = H > 0
    if occupied.any():
        d_lo = np.percentile(depth_avg[occupied], 5)
        d_hi = np.percentile(depth_avg[occupied], 95)
        d_range = max(d_hi - d_lo, 1e-9)
        depth_norm = np.clip((depth_avg - d_lo) / d_range, 0.0, 1.0)
    else:
        depth_norm = np.zeros_like(depth_avg)

    rgba = colorize(H_g, depth_norm, cmap_name, depth_blend)
    return rgba


def colorize(intensity, depth, cmap_name, depth_blend):
    """Map intensity (and depth modulation) to RGBA."""
    cmap = COLORMAPS[cmap_name]
    # Look up base color from intensity.
    idx = (intensity * (len(cmap) - 1)).astype(np.int32)
    base = cmap[idx]  # (H, W, 3) in [0, 1]

    # Depth shading: brighten near, darken far. Depth in [0, 1], 1 = closer.
    # Scale brightness by 1 - depth_blend + 2*depth_blend*depth, so depth=0 -> dim, 1 -> bright.
    shade = (1.0 - depth_blend) + 2.0 * depth_blend * depth
    shade = shade[:, :, None]
    color = np.clip(base * shade, 0.0, 1.0)

    # Alpha = intensity (so empty regions stay background).
    rgb = (color * 255.0).astype(np.uint8)
    alpha = (intensity * 255.0).astype(np.uint8)
    rgba = np.dstack([rgb, alpha])
    return rgba


def composite_on_background(rgba, bg):
    """Composite an RGBA image onto an RGB background of the same shape."""
    a = rgba[:, :, 3:4].astype(np.float32) / 255.0
    fg = rgba[:, :, :3].astype(np.float32)
    bgf = np.broadcast_to(np.array(bg, dtype=np.float32), fg.shape)
    out = a * fg + (1.0 - a) * bgf
    return np.clip(out, 0, 255).astype(np.uint8)


# --- Colormaps. Each is a (256, 3) array in [0,1]. Defined by a few stops, interpolated. ---


def make_cmap(stops):
    n = 256
    pos = np.array([s[0] for s in stops])
    cols = np.array([s[1] for s in stops])
    out = np.zeros((n, 3), dtype=np.float64)
    xs = np.linspace(0, 1, n)
    for c in range(3):
        out[:, c] = np.interp(xs, pos, cols[:, c])
    return out


COLORMAPS = {
    "ember": make_cmap([
        (0.00, [0.02, 0.00, 0.04]),
        (0.20, [0.20, 0.05, 0.10]),
        (0.50, [0.75, 0.18, 0.10]),
        (0.80, [0.98, 0.65, 0.20]),
        (1.00, [1.00, 0.95, 0.80]),
    ]),
    "ice": make_cmap([
        (0.00, [0.01, 0.02, 0.05]),
        (0.25, [0.05, 0.15, 0.35]),
        (0.55, [0.15, 0.55, 0.75]),
        (0.80, [0.55, 0.85, 0.95]),
        (1.00, [0.95, 0.99, 1.00]),
    ]),
    "verdigris": make_cmap([
        (0.00, [0.02, 0.04, 0.04]),
        (0.30, [0.05, 0.25, 0.22]),
        (0.60, [0.20, 0.60, 0.50]),
        (0.85, [0.65, 0.90, 0.70]),
        (1.00, [0.95, 1.00, 0.92]),
    ]),
    "violet": make_cmap([
        (0.00, [0.03, 0.01, 0.06]),
        (0.30, [0.20, 0.05, 0.30]),
        (0.55, [0.55, 0.15, 0.55]),
        (0.80, [0.85, 0.45, 0.85]),
        (1.00, [0.98, 0.85, 0.99]),
    ]),
    "amber": make_cmap([
        (0.00, [0.04, 0.02, 0.00]),
        (0.30, [0.30, 0.15, 0.02]),
        (0.60, [0.85, 0.45, 0.05]),
        (0.85, [0.98, 0.78, 0.30]),
        (1.00, [1.00, 0.97, 0.78]),
    ]),
    "ink": make_cmap([
        (0.00, [0.01, 0.01, 0.02]),
        (0.30, [0.10, 0.10, 0.20]),
        (0.60, [0.35, 0.30, 0.55]),
        (0.85, [0.75, 0.75, 0.90]),
        (1.00, [0.99, 0.99, 1.00]),
    ]),
}


BACKGROUND = (10, 11, 16)


# --- Configurations for each system ---


CONFIGS = [
    {
        "name": "lorenz",
        "field": lorenz,
        "x0": (0.1, 0.0, 0.0),
        "dt": 0.005,
        "n_steps": 600_000,
        "view": (math.radians(20), math.radians(15)),
        "cmap": "ember",
        "gamma": 0.40,
    },
    {
        "name": "rossler",
        "field": rossler,
        "x0": (0.1, 0.0, 0.0),
        "dt": 0.02,
        "n_steps": 500_000,
        "view": (math.radians(35), math.radians(50)),
        "cmap": "amber",
        "gamma": 0.40,
    },
    {
        "name": "aizawa",
        "field": aizawa,
        "x0": (0.1, 0.0, 0.0),
        "dt": 0.01,
        "n_steps": 800_000,
        "view": (math.radians(40), math.radians(70)),
        "cmap": "violet",
        "gamma": 0.45,
    },
    {
        "name": "halvorsen",
        "field": halvorsen,
        "x0": (-1.48, -1.51, 2.04),
        "dt": 0.005,
        "n_steps": 600_000,
        "view": (math.radians(30), math.radians(25)),
        "cmap": "verdigris",
        "gamma": 0.42,
    },
    {
        "name": "thomas",
        "field": thomas,
        "x0": (1.1, 1.1, -0.01),
        "dt": 0.05,
        "n_steps": 500_000,
        "view": (math.radians(25), math.radians(20)),
        "cmap": "ice",
        "gamma": 0.45,
    },
    {
        "name": "chen",
        "field": chen,
        "x0": (-10.0, 0.0, 37.0),
        "dt": 0.0015,
        "n_steps": 800_000,
        "view": (math.radians(35), math.radians(15)),
        "cmap": "ink",
        "gamma": 0.42,
    },
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)

    res = int(os.environ.get("ATTRACTOR_RES", "1400"))

    rendered = []
    for cfg in CONFIGS:
        print(f"[integrate] {cfg['name']}: dt={cfg['dt']}, steps={cfg['n_steps']}")
        sys.stdout.flush()
        t0 = _now()
        pts = integrate(cfg["field"], cfg["x0"], cfg["dt"], cfg["n_steps"])
        t1 = _now()
        print(f"  integrated in {t1 - t0:.1f}s")
        sys.stdout.flush()

        rgba = render_attractor(pts, cfg["view"], res=res,
                                gamma=cfg["gamma"], cmap_name=cfg["cmap"])
        rgb = composite_on_background(rgba, BACKGROUND)
        out_path = os.path.join(out_dir, f"{cfg['name']}.png")
        Image.fromarray(rgb).save(out_path)
        t2 = _now()
        print(f"  rendered in {t2 - t1:.1f}s -> {out_path}")
        sys.stdout.flush()
        rendered.append((cfg["name"], rgb))

    # Contact sheet: 2x3 grid.
    sheet = make_contact_sheet(rendered, cols=3)
    sheet_path = os.path.join(out_dir, "gallery.png")
    Image.fromarray(sheet).save(sheet_path)
    print(f"[gallery] -> {sheet_path}")


def make_contact_sheet(rendered, cols=3, gap=12, label_h=44):
    n = len(rendered)
    rows = (n + cols - 1) // cols
    h, w, _ = rendered[0][1].shape
    sheet_w = cols * w + (cols + 1) * gap
    sheet_h = rows * (h + label_h) + (rows + 1) * gap
    sheet = np.full((sheet_h, sheet_w, 3), BACKGROUND, dtype=np.uint8)
    for i, (name, img) in enumerate(rendered):
        r, c = divmod(i, cols)
        y = gap + r * (h + label_h + gap)
        x = gap + c * (w + gap)
        sheet[y:y + h, x:x + w] = img
        # Label band: leave dark, no rasterized text (keep dependencies minimal).
    return sheet


def _now():
    import time
    return time.time()


if __name__ == "__main__":
    main()
