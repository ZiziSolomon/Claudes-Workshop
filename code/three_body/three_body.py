"""
Three-body gravitational orbits.

Symplectic kick-drift-kick leapfrog on point masses under Newtonian
gravity (G=1). Renders trajectories as PNGs: each body gets its own
color; the trail is splatted into a 2D density buffer with bilinear
antialiasing, then log-tonemapped per body.

Catalog:
  - Chenciner-Montgomery figure-8 (Moore 1993, proven 2000): three equal
    masses chasing each other along a single planar lemniscate.
  - "Butterfly I", "Yin-Yang I", "Moth I" from the Šuvakov-Dmitrašinović
    2013 catalog of zero-angular-momentum periodic three-body orbits.
  - Pythagorean problem (Burrau 1913): masses 3, 4, 5 placed at the
    vertices of a 3-4-5 right triangle, opposite the corresponding side,
    all at rest. Famously chaotic; produces close encounters and an
    eventual ejection of one body around t ≈ 60.
"""

from __future__ import annotations

import math
import os
import struct
import zlib
from dataclasses import dataclass

import numpy as np


# ------------------------------- physics --------------------------------- #

EPS2 = 1e-12  # Plummer softening^2; near machine zero so periodic orbits
#               whose close approaches are part of the dynamics are preserved.


def accelerations(pos: np.ndarray, mass: np.ndarray) -> np.ndarray:
    """All-pairs Newtonian acceleration, fully vectorized."""
    diff = pos[None, :, :] - pos[:, None, :]            # (n, n, 2)
    r2 = (diff * diff).sum(axis=-1) + EPS2              # (n, n)
    inv_r3 = r2 ** -1.5                                 # (n, n)
    np.fill_diagonal(inv_r3, 0.0)
    return (mass[None, :, None] * diff * inv_r3[:, :, None]).sum(axis=1)


def total_energy(pos: np.ndarray, vel: np.ndarray, mass: np.ndarray) -> float:
    """KE + PE; the conserved Hamiltonian for an isolated N-body system."""
    ke = 0.5 * float(np.sum(mass * np.sum(vel * vel, axis=1)))
    diff = pos[None, :, :] - pos[:, None, :]
    r = np.sqrt((diff * diff).sum(axis=-1) + EPS2)
    iu = np.triu_indices(pos.shape[0], k=1)
    inv_r = 1.0 / r[iu]
    mm = (mass[:, None] * mass[None, :])[iu]
    pe = -float(np.sum(mm * inv_r))
    return ke + pe


def leapfrog(
    pos: np.ndarray,
    vel: np.ndarray,
    mass: np.ndarray,
    dt: float,
    steps: int,
) -> tuple[np.ndarray, float]:
    """
    Kick-drift-kick leapfrog. Returns (history, max_relative_E_drift).

    history has shape (steps + 1, n_bodies, 2).
    """
    n = pos.shape[0]
    history = np.empty((steps + 1, n, 2), dtype=np.float64)
    history[0] = pos
    e0 = total_energy(pos, vel, mass)
    max_drift = 0.0

    a = accelerations(pos, mass)
    check_every = max(1, steps // 20)
    for k in range(steps):
        vel += 0.5 * dt * a
        pos += dt * vel
        a = accelerations(pos, mass)
        vel += 0.5 * dt * a
        history[k + 1] = pos
        if (k + 1) % check_every == 0:
            e = total_energy(pos, vel, mass)
            drift = abs(e - e0) / abs(e0) if e0 != 0 else 0.0
            if drift > max_drift:
                max_drift = drift
    return history, max_drift


# -------------------------- initial conditions --------------------------- #


@dataclass
class System:
    name: str
    mass: np.ndarray
    pos: np.ndarray
    vel: np.ndarray
    dt: float
    steps: int
    palette: tuple[tuple[int, int, int], ...]
    bg: tuple[int, int, int]
    pad: float = 0.15
    crop_steps: int | None = None  # render only the first N+1 positions


# Chenciner-Montgomery figure-8. Period T ≈ 6.3259, run for ~2 cycles.
def figure8() -> System:
    p1 = np.array([-0.97000436, 0.24308753])
    p2 = np.array([0.97000436, -0.24308753])
    p3 = np.array([0.0, 0.0])
    v3 = np.array([-0.93240737, -0.86473146])
    v1 = -v3 / 2
    v2 = -v3 / 2
    return System(
        name="figure_8",
        mass=np.array([1.0, 1.0, 1.0]),
        pos=np.stack([p1, p2, p3]),
        vel=np.stack([v1, v2, v3]),
        dt=2.0e-4,
        steps=70_000,  # ~2.21 periods
        palette=(
            (255, 200, 120),
            (140, 220, 255),
            (255, 130, 180),
        ),
        bg=(8, 10, 18),
    )


# Šuvakov-Dmitrašinović catalog initializer:
#   r1 = (-1, 0),  r2 = (+1, 0),  r3 = (0, 0)
#   v1 = v2 = (p1, p2),  v3 = -2 (p1, p2)
#   masses all 1, G = 1.
def _suvakov(name, p1, p2, dt, steps, palette, bg, pad=0.15) -> System:
    pos = np.array([[-1.0, 0.0], [1.0, 0.0], [0.0, 0.0]])
    v = np.array([p1, p2])
    vel = np.stack([v, v, -2 * v])
    return System(
        name=name,
        mass=np.array([1.0, 1.0, 1.0]),
        pos=pos,
        vel=vel,
        dt=dt,
        steps=steps,
        palette=palette,
        bg=bg,
        pad=pad,
    )


def butterfly_I() -> System:
    # T ≈ 6.2356; integrate ~3 periods.
    return _suvakov(
        "butterfly_I",
        p1=0.30689,
        p2=0.12551,
        dt=5.0e-5,
        steps=380_000,
        palette=(
            (255, 180, 100),
            (120, 200, 255),
            (200, 255, 160),
        ),
        bg=(10, 8, 16),
    )


def yin_yang_I() -> System:
    # T ≈ 4.5759; integrate ~3 periods.
    return _suvakov(
        "yin_yang_I",
        p1=0.51394,
        p2=0.30474,
        dt=5.0e-5,
        steps=280_000,
        palette=(
            (240, 220, 255),
            (255, 160, 120),
            (140, 240, 200),
        ),
        bg=(6, 8, 14),
    )


def moth_I() -> System:
    # T ≈ 14.894; integrate ~2 periods (longer, but no extreme close approaches).
    return _suvakov(
        "moth_I",
        p1=0.46444,
        p2=0.39606,
        dt=1.0e-4,
        steps=300_000,
        palette=(
            (255, 210, 130),
            (180, 220, 255),
            (255, 150, 200),
        ),
        bg=(8, 6, 14),
        pad=0.10,
    )


# Pythagorean problem (Burrau 1913). Masses 3, 4, 5 at the vertices of a
# 3-4-5 right triangle, each opposite the side equal to its mass, at rest.
# Famously chaotic; the "Burrau orbit" goes through ~50 close approaches
# before a triple near-collision around t ≈ 15.83 sends m=5 escaping.
# We integrate just to t ≈ 25, before the final ejection sweeps the plot
# bounds wide — and crop the render to the first ~70% of the history so
# the central tangle reads cleanly.
def pythagorean() -> System:
    pos = np.array([
        [1.0, 3.0],     # m=3
        [-2.0, -1.0],   # m=4
        [1.0, -1.0],    # m=5
    ])
    vel = np.zeros_like(pos)
    return System(
        name="pythagorean",
        mass=np.array([3.0, 4.0, 5.0]),
        pos=pos,
        vel=vel,
        dt=2.0e-4,
        steps=80_000,        # to t = 16
        crop_steps=80_000,
        palette=(
            (255, 180, 90),
            (130, 200, 255),
            (220, 130, 255),
        ),
        bg=(6, 6, 12),
        pad=0.05,
    )


# ------------------------------ rendering -------------------------------- #


WIDTH, HEIGHT = 1200, 1200


def rasterize(history: np.ndarray, sys: System) -> np.ndarray:
    """
    Splat trajectory points into one float density buffer per body, with
    bilinear antialiasing. Tonemap log -> gamma per body, composite onto
    the background, then mark each body's final position.
    """
    if sys.crop_steps is not None:
        history = history[: sys.crop_steps + 1]
    n_bodies = history.shape[1]

    xs = history[:, :, 0]
    ys = history[:, :, 1]
    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()
    extent = max(xmax - xmin, ymax - ymin)
    cx, cy = (xmax + xmin) / 2, (ymax + ymin) / 2
    half = extent * (0.5 + sys.pad)
    xmin, xmax = cx - half, cx + half
    ymin, ymax = cy - half, cy + half

    sx = (WIDTH - 1) / (xmax - xmin)
    sy = (HEIGHT - 1) / (ymax - ymin)

    buffers = [np.zeros((HEIGHT, WIDTH), dtype=np.float32) for _ in range(n_bodies)]

    for b in range(n_bodies):
        buf = buffers[b]
        u = (history[:, b, 0] - xmin) * sx
        v = (ymax - history[:, b, 1]) * sy
        i0 = np.floor(u).astype(np.int32)
        j0 = np.floor(v).astype(np.int32)
        fu = (u - i0).astype(np.float32)
        fv = (v - j0).astype(np.float32)
        for di, fdi in ((0, 1 - fu), (1, fu)):
            for dj, fdj in ((0, 1 - fv), (1, fv)):
                ii = i0 + di
                jj = j0 + dj
                w = fdi * fdj
                mask = (ii >= 0) & (ii < WIDTH) & (jj >= 0) & (jj < HEIGHT)
                np.add.at(buf, (jj[mask], ii[mask]), w[mask])

    img = np.tile(np.array(sys.bg, dtype=np.float32), (HEIGHT, WIDTH, 1))
    for b in range(n_bodies):
        buf = buffers[b]
        peak = buf.max()
        if peak > 0:
            buf = np.log1p(buf * 4.0)
            buf /= buf.max()
            buf = buf ** 0.7
        color = np.array(sys.palette[b], dtype=np.float32)
        img += buf[:, :, None] * color

    for b in range(n_bodies):
        x = (history[-1, b, 0] - xmin) * sx
        y = (ymax - history[-1, b, 1]) * sy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            _draw_marker(img, x, y, sys.palette[b], r=6.0)

    np.clip(img, 0, 255, out=img)
    return img.astype(np.uint8)


def _draw_marker(img: np.ndarray, cx: float, cy: float, color, r: float) -> None:
    halo_r = r * 2.4
    x0 = max(0, int(cx - halo_r) - 1)
    x1 = min(WIDTH, int(cx + halo_r) + 2)
    y0 = max(0, int(cy - halo_r) - 1)
    y1 = min(HEIGHT, int(cy + halo_r) + 2)
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    core = np.clip(r + 0.5 - d, 0, 1)
    halo = np.exp(-((d / (halo_r * 0.45)) ** 2)) * 0.6
    alpha = np.clip(core + halo * (1 - core), 0, 1)
    c = np.array(color, dtype=np.float32)
    region = img[y0:y1, x0:x1]
    region[:] = region * (1 - alpha[:, :, None]) + c * alpha[:, :, None]


# -------------------------- minimal PNG writer --------------------------- #


def write_png(path: str, img: np.ndarray) -> None:
    h, w, _ = img.shape
    raw = bytearray()
    for row in img:
        raw.append(0)
        raw.extend(row.tobytes())
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", compressed))
        f.write(chunk(b"IEND", b""))


# ------------------------------ contact sheet ---------------------------- #


def contact_sheet(image_paths, out_path, cols=2, gap=24, bg=(6, 7, 12)):
    from PIL import Image
    imgs = [Image.open(p) for p in image_paths]
    w, h = imgs[0].size
    rows = (len(imgs) + cols - 1) // cols
    sheet_w = cols * w + (cols + 1) * gap
    sheet_h = rows * h + (rows + 1) * gap
    sheet = Image.new("RGB", (sheet_w, sheet_h), bg)
    for idx, im in enumerate(imgs):
        r, c = divmod(idx, cols)
        sheet.paste(im, (gap + c * (w + gap), gap + r * (h + gap)))
    sheet.save(out_path, optimize=True)


# ---------------------------------- main --------------------------------- #


def run_one(sys: System, out_dir: str) -> str:
    pos = sys.pos.copy()
    vel = sys.vel.copy()
    history, max_drift = leapfrog(pos, vel, sys.mass, sys.dt, sys.steps)
    img = rasterize(history, sys)
    out_path = os.path.join(out_dir, sys.name + ".png")
    write_png(out_path, img)
    print(
        f"  {sys.name:14s}  steps={sys.steps:7d}  dt={sys.dt:.1e}  "
        f"max |ΔE/E| = {max_drift:.2e}"
    )
    return out_path


def main() -> None:
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)

    systems = [figure8(), butterfly_I(), yin_yang_I(), moth_I(), pythagorean()]
    print("rendering three-body orbits")
    paths = [run_one(s, out_dir) for s in systems]

    sheet_path = os.path.join(out_dir, "gallery.png")
    contact_sheet(paths, sheet_path, cols=2)
    print(f"gallery -> {sheet_path}")


if __name__ == "__main__":
    main()
