"""
MDL (Minimum Description Length) visualization.

Shows inference as compression: given data from a quadratic + noise, we fit
polynomial models of degrees 0..8. For each model:
  - model_bits: bits to encode the polynomial coefficients (model complexity)
  - residual_bits: bits to encode the residuals given the model (data|model)
  - total_bits (MDL) = model_bits + residual_bits

The optimal model degree minimizes total description length. Too simple =
large residuals (underfitting). Too complex = costly model (overfitting).
The minimum is where genuine structure ends and noise begins.

Three panels:
  Panel 1: The data and several polynomial fits (degrees 0, 2, 5, 8)
  Panel 2: The MDL decomposition — model bits, residual bits, total by degree
  Panel 3: Residual distributions for four key degrees (showing convergence
           to gaussian / randomness at the optimal degree)
"""

import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

rng = np.random.default_rng(42)

# --- Data generation ---
N = 40
x = np.linspace(-2.0, 2.0, N)
true_fn = lambda t: 0.8 * t**2 - 0.3 * t + 0.5
noise_std = 0.35
y = true_fn(x) + rng.normal(0, noise_std, N)

# --- Fit polynomials and compute MDL ---
max_deg = 8
degrees = list(range(max_deg + 1))

fits = {}
residuals = {}
model_bits = []
residual_bits = []
total_bits = []

# Bits to encode one coefficient: we use the log of its magnitude + sign.
# More principled: use a prior over coefficients, cost = -log p(coef).
# For simplicity, use floating-point quantization: each coefficient costs
# COEF_BITS bits to encode, and the model has (deg+1) coefficients.
# For residuals: assume gaussian, cost = N/2 * log2(2*pi*e*sigma^2) in bits.
COEF_BITS = 32  # standard float32

for deg in degrees:
    coeffs = np.polyfit(x, y, deg)
    y_hat = np.polyval(coeffs, x)
    res = y - y_hat
    fits[deg] = (coeffs, y_hat)
    residuals[deg] = res

    # Model complexity: number of coefficients * bits per coefficient
    m_bits = (deg + 1) * COEF_BITS
    model_bits.append(m_bits)

    # Residual complexity: gaussian coding cost in bits
    sigma2 = np.var(res) if np.var(res) > 1e-10 else 1e-10
    # Coding cost per sample: 0.5 * log2(2*pi*e*sigma2)
    r_bits = N * 0.5 * math.log2(2 * math.pi * math.e * sigma2)
    # r_bits can be negative (when sigma < 1/(sqrt(2*pi*e))); clamp to 0
    residual_bits.append(max(r_bits, 0.0))
    total_bits.append(m_bits + max(r_bits, 0.0))

model_bits = np.array(model_bits)
residual_bits = np.array(residual_bits)
total_bits = np.array(total_bits)
best_deg = int(np.argmin(total_bits))

# --- Palette and layout ---
BG       = (18, 20, 25)
GRID     = (40, 42, 50)
TEXT     = (210, 215, 225)
MUTED    = (110, 115, 130)
AMBER    = (255, 190,  60)
ICE      = (100, 200, 255)
EMBER    = (255,  90,  50)
VERDI    = ( 80, 210, 140)
GOLD     = (230, 175,  50)
VIOLET   = (170, 110, 240)

W, H = 1400, 520
PAD = 50
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

try:
    font_sm = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 13)
    font_md = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 15)
    font_lg = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 17)
    font_xl = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 20)
except OSError:
    font_sm = font_md = font_lg = font_xl = ImageFont.load_default()

PANEL_W = (W - 4 * PAD) // 3
PANEL_H = H - 2 * PAD

def panel_rect(i):
    x0 = PAD + i * (PANEL_W + PAD)
    y0 = PAD
    x1 = x0 + PANEL_W
    y1 = y0 + PANEL_H
    return x0, y0, x1, y1

def draw_panel_bg(i, title):
    x0, y0, x1, y1 = panel_rect(i)
    draw.rectangle([x0, y0, x1, y1], fill=(24, 27, 35))
    draw.rectangle([x0, y0, x1, y1], outline=GRID, width=1)
    tw = draw.textlength(title, font=font_lg)
    draw.text((x0 + (PANEL_W - tw) / 2, y0 + 10), title, fill=TEXT, font=font_lg)
    return x0, y0 + 40, x1, y1

# ── Panel 0: Data + fits ──────────────────────────────────────────────────────
px0, py0, px1, py1 = draw_panel_bg(0, "Polynomial Fits")
inner_h = py1 - py0 - 20
inner_w = px1 - px0 - 20

def data_to_px(xi, yi, x_range, y_range, ox, oy, w, h):
    fx = (xi - x_range[0]) / (x_range[1] - x_range[0])
    fy = (yi - y_range[0]) / (y_range[1] - y_range[0])
    return ox + fx * w, oy + (1 - fy) * h

x_range = (-2.1, 2.1)
y_margin = 0.5
y_range = (y.min() - y_margin, y.max() + y_margin)
ox, oy, pw, ph = px0 + 15, py0 + 10, inner_w, inner_h - 20

# Grid lines
for yi_val in np.linspace(y_range[0], y_range[1], 5):
    _, gy = data_to_px(0, yi_val, x_range, y_range, ox, oy, pw, ph)
    draw.line([(ox, int(gy)), (ox + pw, int(gy))], fill=GRID, width=1)
for xi_val in np.linspace(x_range[0], x_range[1], 5):
    gx, _ = data_to_px(xi_val, 0, x_range, y_range, ox, oy, pw, ph)
    draw.line([(int(gx), oy), (int(gx), oy + ph)], fill=GRID, width=1)

# True function (faint)
xs_dense = np.linspace(x_range[0], x_range[1], 200)
ys_true = true_fn(xs_dense)
pts_true = [data_to_px(xi_, yi_, x_range, y_range, ox, oy, pw, ph)
            for xi_, yi_ in zip(xs_dense, ys_true)]
for k in range(len(pts_true) - 1):
    draw.line([pts_true[k], pts_true[k+1]], fill=(60, 80, 60), width=1)

# Fits for select degrees
show_degs = [(0, EMBER, "deg 0"), (3, VIOLET, "deg 3"),
             (best_deg, VERDI, f"deg {best_deg} ★"), (8, ICE, "deg 8")]
for deg, color, label in show_degs:
    _, y_hat = fits[deg]
    # Smooth version
    c = fits[deg][0]
    ys_fit = np.polyval(c, xs_dense)
    pts = [data_to_px(xi_, yi_, x_range, y_range, ox, oy, pw, ph)
           for xi_, yi_ in zip(xs_dense, ys_fit)]
    lw = 2 if deg == best_deg else 1
    for k in range(len(pts) - 1):
        draw.line([pts[k], pts[k+1]], fill=color, width=lw)

# Data points
for xi_, yi_ in zip(x, y):
    px_, py_ = data_to_px(xi_, yi_, x_range, y_range, ox, oy, pw, ph)
    r = 3
    draw.ellipse([px_-r, py_-r, px_+r, py_+r], fill=AMBER)

# Legend
leg_x, leg_y = px0 + 15, py1 - 75
for deg, color, label in show_degs:
    draw.rectangle([leg_x, leg_y+3, leg_x+22, leg_y+9], fill=color)
    draw.text((leg_x + 28, leg_y - 1), label, fill=TEXT, font=font_sm)
    leg_y += 17

# ── Panel 1: MDL bars ─────────────────────────────────────────────────────────
px0, py0, px1, py1 = draw_panel_bg(1, "Description Length (MDL)")
inner_h = py1 - py0 - 30
inner_w = px1 - px0 - 30
ox, oy = px0 + 20, py0 + 15

# Normalize for display
max_bits = max(total_bits)
bar_area_h = inner_h - 35
bar_area_w = inner_w

bar_w = bar_area_w / (max_deg + 1)
gap = 4

for deg in degrees:
    bx0 = ox + deg * bar_w + gap
    bx1 = bx0 + bar_w - 2 * gap

    # Residual bits (bottom)
    rb = residual_bits[deg] / max_bits * bar_area_h
    by_res0 = oy + bar_area_h - rb
    by_res1 = oy + bar_area_h
    draw.rectangle([bx0, by_res0, bx1, by_res1],
                   fill=ICE if deg == best_deg else (50, 100, 130))

    # Model bits (stacked on top)
    mb = model_bits[deg] / max_bits * bar_area_h
    by_mod0 = by_res0 - mb
    by_mod1 = by_res0
    draw.rectangle([bx0, by_mod0, bx1, by_mod1],
                   fill=AMBER if deg == best_deg else (100, 80, 30))

    # Star for best
    lbl = f"{deg}★" if deg == best_deg else str(deg)
    tw = draw.textlength(lbl, font=font_sm)
    draw.text((bx0 + (bar_w - 2*gap - tw)/2, oy + bar_area_h + 5),
              lbl, fill=(VERDI if deg == best_deg else MUTED), font=font_sm)

# Total line
prev_pt = None
for deg in degrees:
    bx_mid = ox + deg * bar_w + bar_w / 2
    by = oy + bar_area_h - total_bits[deg] / max_bits * bar_area_h
    if prev_pt:
        draw.line([prev_pt, (bx_mid, by)], fill=EMBER, width=2)
    draw.ellipse([bx_mid-3, by-3, bx_mid+3, by+3], fill=EMBER)
    prev_pt = (bx_mid, by)

# Legend
leg_x, leg_y = px0 + 18, py1 - 58
draw.rectangle([leg_x, leg_y+3, leg_x+16, leg_y+11], fill=(50, 100, 130))
draw.text((leg_x + 22, leg_y), "residual bits", fill=TEXT, font=font_sm)
leg_y += 18
draw.rectangle([leg_x, leg_y+3, leg_x+16, leg_y+11], fill=(100, 80, 30))
draw.text((leg_x + 22, leg_y), "model bits", fill=TEXT, font=font_sm)
leg_y += 18
draw.line([(leg_x, leg_y+7), (leg_x+16, leg_y+7)], fill=EMBER, width=2)
draw.text((leg_x + 22, leg_y), "total (MDL)", fill=TEXT, font=font_sm)

draw.text((px0 + 15, py0 + inner_h - 8), "← degree →",
          fill=MUTED, font=font_sm)

# ── Panel 2: Residual distributions ──────────────────────────────────────────
px0, py0, px1, py1 = draw_panel_bg(2, "Residuals by Degree")
inner_h = py1 - py0 - 30
inner_w = px1 - px0 - 30
ox, oy = px0 + 15, py0 + 10

show_res = [(0, EMBER), (best_deg, VERDI), (5, VIOLET), (8, ICE)]
sub_h = (inner_h - 10) // len(show_res)

for idx, (deg, color) in enumerate(show_res):
    res = residuals[deg]
    sub_oy = oy + idx * sub_h

    # Mini histogram of residuals
    hist_w = inner_w - 80
    hist_h = sub_h - 12
    n_bins = 16
    hist_ox = ox + 65
    hist_oy = sub_oy + 6

    counts, bin_edges = np.histogram(res, bins=n_bins, range=(-2.0, 2.0))
    max_count = max(counts) if max(counts) > 0 else 1
    bin_w = hist_w / n_bins

    for b, cnt in enumerate(counts):
        bx0 = hist_ox + b * bin_w + 1
        bx1 = hist_ox + (b+1) * bin_w - 1
        bar_h = int(cnt / max_count * hist_h)
        by0 = hist_oy + hist_h - bar_h
        by1 = hist_oy + hist_h
        alpha = 200 if deg == best_deg else 140
        c = tuple(int(ci * alpha / 255) + int(BG[i] * (255 - alpha) / 255)
                  for i, ci in enumerate(color))
        draw.rectangle([bx0, by0, bx1, by1], fill=color)

    # Gaussian overlay
    sigma = np.std(res)
    xs_g = np.linspace(-2.0, 2.0, 100)
    norm = math.sqrt(2 * math.pi) * sigma if sigma > 0 else 1
    ys_g = np.exp(-0.5 * (xs_g / sigma)**2) / norm if sigma > 0 else xs_g * 0
    # Scale to histogram
    bin_size = 4.0 / n_bins
    ys_g_scaled = ys_g * max_count * bin_size
    pts_g = [(hist_ox + (xg + 2.0) / 4.0 * hist_w,
              hist_oy + hist_h - min(yg / max_count * hist_h, hist_h))
             for xg, yg in zip(xs_g, ys_g_scaled)]
    for k in range(len(pts_g) - 1):
        draw.line([pts_g[k], pts_g[k+1]], fill=(200, 200, 200), width=1)

    # Label
    sigma_r = np.std(res)
    label = f"deg {deg}★" if deg == best_deg else f"deg {deg}"
    label2 = f"σ={sigma_r:.3f}"
    draw.text((ox, sub_oy + 4), label, fill=color, font=font_sm)
    draw.text((ox, sub_oy + 20), label2, fill=MUTED, font=font_sm)

    # Zero line
    zero_x = hist_ox + hist_w / 2
    draw.line([(zero_x, hist_oy), (zero_x, hist_oy + hist_h)],
              fill=GRID, width=1)

# Caption at bottom
caption = (f"MDL minimum at degree {best_deg}  "
           f"(model {model_bits[best_deg]:.0f} bits + residual {residual_bits[best_deg]:.0f} bits"
           f" = {total_bits[best_deg]:.0f} bits total)")
draw.text((PAD, H - 22), caption, fill=MUTED, font=font_sm)

img.save("/home/opc/workshop/code/inference/out/mdl.png")
print(f"Saved. Best degree: {best_deg}")
print(f"MDL by degree: {[f'{t:.1f}' for t in total_bits]}")
print(f"Model bits:    {list(model_bits)}")
print(f"Residual bits: {[f'{r:.1f}' for r in residual_bits]}")
