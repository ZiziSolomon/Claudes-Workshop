#!/usr/bin/env python3
"""Fourier epicycle animator.

Decomposes a parametric curve into Fourier modes and renders each frequency
component as a rotating circle (epicycle). As the chain rotates, the tip
traces the original curve.

Output: animated GIF + contact-sheet PNG for each curve.
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

W, H = 520, 520
CX, CY = W // 2, H // 2

# ── Colour palette ─────────────────────────────────────────────────────────────

BG         = (10,  12,  20)
GRID_COL   = (22,  26,  40)
REF_COL    = (35,  55,  90)    # dim reference curve
CIRCLE_COL = (35,  48,  80)    # epicycle outlines
SPOKE_COL  = (65,  90, 150)    # spokes
TRAIL_BASE = (180,  70,  20)   # ember trail (dim end)
TRAIL_TIP  = (255, 220,  80)   # gold (bright end)
DOT_COL    = (255, 240, 100)   # current tip


# ── Curve definitions ──────────────────────────────────────────────────────────

def heart(N):
    t = np.linspace(0, 2 * math.pi, N, endpoint=False)
    x =  16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    return (x + 1j * y)


def trefoil(N):
    t = np.linspace(0, 2 * math.pi, N, endpoint=False)
    x = np.sin(t) + 2 * np.sin(2*t)
    y = np.cos(t) - 2 * np.cos(2*t)
    return x + 1j * y


def lissajous(N, a=3, b=5, delta=math.pi / 4):
    t = np.linspace(0, 2 * math.pi, N, endpoint=False)
    x = np.sin(a * t + delta)
    y = np.sin(b * t)
    return x + 1j * y


def butterfly(N):
    """Butterfly curve (Temple H. Fay, 1989)."""
    t = np.linspace(0, 12 * math.pi, N, endpoint=False)
    r = np.exp(np.cos(t)) - 2 * np.cos(4*t) - np.sin(t/12) ** 5
    x = r * np.sin(t)
    y = r * np.cos(t)
    return x + 1j * y


# ── Fourier decomposition ──────────────────────────────────────────────────────

def fourier_components(z, n_terms):
    """Return top n_terms Fourier components, sorted by amplitude descending."""
    N = len(z)
    Z = np.fft.fft(z) / N
    freqs = np.fft.fftfreq(N) * N   # integer frequencies

    idx = np.argsort(-np.abs(Z))[:n_terms]
    amps   = np.abs(Z[idx])
    phases = np.angle(Z[idx])
    freq_i = np.round(freqs[idx]).astype(int)
    return amps, freq_i, phases


def evaluate_chain(t_frac, amps, freqs, phases):
    """Evaluate the epicycle chain at t in [0, 1]. Returns tip position."""
    angle = 2 * math.pi * freqs * t_frac + phases
    return (amps * np.exp(1j * angle)).sum()


def evaluate_chain_steps(t_frac, amps, freqs, phases):
    """Return cumulative positions at each circle in the chain."""
    angle = 2 * math.pi * freqs * t_frac + phases
    contributions = amps * np.exp(1j * angle)
    return np.concatenate(([0j], np.cumsum(contributions)))


# ── Screen helpers ─────────────────────────────────────────────────────────────

def to_screen(z, scale):
    return (int(CX + z.real * scale), int(CY - z.imag * scale))


def lerp_color(c0, c1, t):
    return tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))


# ── Background: faint grid + reference curve ───────────────────────────────────

def make_background(curve_world, scale):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Light grid
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=GRID_COL)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=GRID_COL)

    # Reference curve (dim ice-blue)
    pts = [to_screen(z, scale) for z in curve_world]
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=REF_COL, width=1)
    draw.line([pts[-1], pts[0]], fill=REF_COL, width=1)   # close

    return img


# ── Frame renderer ─────────────────────────────────────────────────────────────

def render_frame(bg, trail, t_frac, amps, freqs, phases, scale, min_radius=1):
    img = bg.copy()
    draw = ImageDraw.Draw(img)

    # Trail: fade from dim to bright
    n = len(trail)
    if n > 1:
        for i in range(n - 1):
            t_fade = i / (n - 1)
            col = lerp_color(TRAIL_BASE, TRAIL_TIP, t_fade ** 0.6)
            p1 = to_screen(trail[i],   scale)
            p2 = to_screen(trail[i+1], scale)
            draw.line([p1, p2], fill=col, width=2)

    # Epicycle chain
    steps = evaluate_chain_steps(t_frac, amps, freqs, phases)
    for i in range(len(steps) - 1):
        old = steps[i]
        new = steps[i + 1]
        r_px = int(amps[i] * scale)
        if r_px >= min_radius:
            cx, cy = to_screen(old, scale)
            draw.ellipse([cx - r_px, cy - r_px, cx + r_px, cy + r_px],
                         outline=CIRCLE_COL, width=1)
        p1 = to_screen(old, scale)
        p2 = to_screen(new, scale)
        draw.line([p1, p2], fill=SPOKE_COL, width=1)

    # Tip dot
    tip = to_screen(steps[-1], scale)
    r = 4
    draw.ellipse([tip[0]-r, tip[1]-r, tip[0]+r, tip[1]+r], fill=DOT_COL)

    return img


# ── Full animation ─────────────────────────────────────────────────────────────

def animate(curve_fn, name, n_terms=60, n_frames=200, frame_ms=50, sample_N=1024):
    print(f"\n── {name} ──")

    # Sample and normalise curve
    z_raw = curve_fn(sample_N)
    z_raw = z_raw - z_raw.mean()
    max_r = np.max(np.abs(z_raw))
    z_norm = z_raw / max_r

    # Scale so curve fits with some margin
    scale = (W // 2 - 40)    # pixels per unit (curve is in [-1, 1])

    # Fourier decomposition
    amps, freqs, phases = fourier_components(z_norm, n_terms)

    # Reference curve (reconstructed from Fourier components)
    t_ref = np.linspace(0, 1, sample_N, endpoint=False)
    ref_world = np.array([evaluate_chain(t, amps, freqs, phases) for t in t_ref])

    # Background
    bg = make_background(ref_world, scale)

    # Generate frames
    frames = []
    trail  = []
    contact_frames = []
    contact_t = [0, n_frames // 4, n_frames // 2, 3 * n_frames // 4]

    for i in range(n_frames):
        t = i / n_frames
        tip = evaluate_chain(t, amps, freqs, phases)
        trail.append(tip)

        frame = render_frame(bg, trail, t, amps, freqs, phases, scale)
        frames.append(frame)

        if i in contact_t:
            contact_frames.append(frame)

        if i % 50 == 0:
            print(f"  frame {i}/{n_frames}")

    # Animated GIF
    gif_path = os.path.join(OUT, f"{name}.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
    )
    print(f"  → {gif_path}")

    # Contact sheet: 4 frames in a 2×2 grid
    cs = Image.new("RGB", (W * 2, H * 2), BG)
    for idx, fr in enumerate(contact_frames[:4]):
        row, col = divmod(idx, 2)
        cs.paste(fr, (col * W, row * H))

    cs_path = os.path.join(OUT, f"{name}_contact.png")
    cs.save(cs_path)
    print(f"  → {cs_path}")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    animate(heart,     "heart",      n_terms=60, n_frames=200, frame_ms=50)
    animate(trefoil,   "trefoil",    n_terms=40, n_frames=200, frame_ms=50)
    animate(lissajous, "lissajous",  n_terms=40, n_frames=200, frame_ms=50)
    animate(butterfly, "butterfly",  n_terms=80, n_frames=200, frame_ms=50)

    print("\nDone.")
