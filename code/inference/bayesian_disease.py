"""
Bayesian updating on disease testing: showing how prior and likelihood combine.

Classic problem: A test has 95% sensitivity (detects disease when present) and 95%
specificity (correctly shows negative when absent). You test positive? Probability
you have the disease?

Answer: depends on prior. With 1% prevalence → 16% posterior (not 95%!).
With 5% prevalence → 49%. With 50% prevalence → 95%.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Test characteristics
sensitivity = 0.95     # P(+ | disease)
specificity = 0.95     # P(- | no disease)
p_pos_disease = sensitivity
p_pos_healthy = 1 - specificity

# Three prevalences to show
prevalences = [0.01, 0.05, 0.50]
colors = [(255, 100, 100), (255, 190, 60), (100, 200, 255)]

def bayes(prior, p_pos_d, p_pos_h):
    """Bayes: P(disease | positive)"""
    p_pos = p_pos_d * prior + p_pos_h * (1 - prior)
    return (p_pos_d * prior) / p_pos

posteriors = [bayes(p, p_pos_disease, p_pos_healthy) for p in prevalences]

# Palette
BG, GRID, TEXT, MUTED = (18, 20, 25), (40, 42, 50), (210, 215, 225), (110, 115, 130)
PANEL_BG = (24, 27, 35)

W, H = 1200, 500
PAD = 50
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

try:
    font_sm = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 12)
    font_md = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 14)
    font_lg = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 16)
except:
    font_sm = font_md = font_lg = ImageFont.load_default()

PANEL_W = (W - 4*PAD) // 2
PANEL_H = H - 2*PAD

def panel_rect(i):
    x0 = PAD + i * (PANEL_W + PAD)
    return x0, PAD, x0 + PANEL_W, PAD + PANEL_H

def draw_panel(i, title):
    x0, y0, x1, y1 = panel_rect(i)
    draw.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=GRID)
    tw = draw.textlength(title, font=font_lg)
    draw.text((x0 + (PANEL_W - tw)/2, y0 + 8), title, fill=TEXT, font=font_lg)
    return x0, y0 + 35, x1, y1

# Panel 0: Prior → Posterior
px0, py0, px1, py1 = draw_panel(0, "Bayesian Update: Three Cases")
inner_h = py1 - py0 - 20
inner_w = px1 - px0 - 30

item_w = (inner_w - 20) // 3
item_h = inner_h - 30

for idx, (prev, color) in enumerate(zip(prevalences, colors)):
    post = posteriors[idx]
    ox = px0 + 15 + idx * (item_w + 10)
    oy = py0 + 10

    # Title
    label = f"{prev*100:.1f}% disease"
    tw = draw.textlength(label, font=font_sm)
    draw.text((ox + (item_w - tw)/2, oy), label, fill=MUTED, font=font_sm)

    oy += 30

    bar_h = (item_h - 60) // 3 - 5

    # Prior
    draw.text((ox, oy), "Prior:", fill=TEXT, font=font_sm)
    bar_w = min(prev * item_w * 0.7, item_w * 0.7)
    draw.rectangle([ox + 60, oy + 2, ox + 60 + bar_w, oy + bar_h], fill=color)
    draw.text((ox + 65 + bar_w, oy + 2), f"{prev*100:.1f}%", fill=TEXT, font=font_sm)

    oy += bar_h + 10

    # Likelihood ratio
    draw.text((ox, oy), "Likelihood:", fill=TEXT, font=font_sm)
    ratio = p_pos_disease / p_pos_healthy
    draw.text((ox + 60, oy + 2), f"{ratio:.1f}:1", fill=MUTED, font=font_sm)

    oy += bar_h + 10

    # Posterior
    draw.text((ox, oy), "Posterior:", fill=TEXT, font=font_sm)
    bar_w = min(post * item_w * 0.7, item_w * 0.7)
    draw.rectangle([ox + 60, oy + 2, ox + 60 + bar_w, oy + bar_h], fill=color, outline=TEXT, width=2)
    draw.text((ox + 65 + bar_w, oy + 2), f"{post*100:.1f}%", fill=TEXT, font=font_sm)

draw.text((px0 + 15, py1 - 15), f"Test: {sensitivity*100:.0f}% sens, {specificity*100:.0f}% spec", fill=MUTED, font=font_sm)

# Panel 1: Posterior vs Prior
px0, py0, px1, py1 = draw_panel(1, "Posterior as Function of Prior")
inner_h = py1 - py0 - 40
inner_w = px1 - px0 - 30

ox, oy = px0 + 20, py0 + 20
plot_w, plot_h = inner_w - 10, inner_h - 30

# Axes
draw.rectangle([ox, oy, ox + plot_w, oy + plot_h], outline=GRID, width=1)

# Grid
for pct_idx in range(6):
    pct = pct_idx / 5.0
    gx = ox + pct * plot_w
    gy = oy + plot_h - pct * plot_h
    draw.line([(gx, oy), (gx, oy + plot_h)], fill=GRID, width=1)
    draw.line([(ox, gy), (ox + plot_w, gy)], fill=GRID, width=1)

# Diagonal reference
draw.line([(ox, oy + plot_h), (ox + plot_w, oy)], fill=(80, 80, 100), width=1)

# Bayes curve
prev_pt = None
for prior_frac in range(1001):
    prior_p = prior_frac / 1000.0
    post_p = bayes(prior_p, p_pos_disease, p_pos_healthy)
    px = ox + prior_p * plot_w
    py = oy + plot_h - post_p * plot_h
    if prev_pt:
        draw.line([prev_pt, (px, py)], fill=(100, 200, 255), width=2)
    prev_pt = (int(px), int(py))

# Mark example points
for prev, color in zip(prevalences, colors):
    post = bayes(prev, p_pos_disease, p_pos_healthy)
    px = ox + prev * plot_w
    py = oy + plot_h - post * plot_h
    r = 4
    draw.ellipse([px-r, py-r, px+r, py+r], fill=color, outline=TEXT, width=2)

# Axes labels
draw.text((ox + plot_w/2 - 40, oy + plot_h + 5), "Prior probability", fill=MUTED, font=font_sm)
draw.text((ox - 50, oy + plot_h/2 - 20), "Posterior", fill=MUTED, font=font_sm)

# Axis ticks
for pct_idx in range(6):
    pct = pct_idx / 5.0
    x = ox + pct * plot_w
    y = oy + plot_h - pct * plot_h
    draw.text((x - 8, oy + plot_h + 5), f"{int(pct*100)}", fill=MUTED, font=font_sm)
    draw.text((ox - 28, y - 5), f"{int(pct*100)}", fill=MUTED, font=font_sm)

# Caption
draw.text((px0 + 15, py1 - 22),
          "Invariant: Curve shape never changes. Only starting prior matters.",
          fill=TEXT, font=font_sm)

img.save("/home/runner/work/Claudes-Workshop/Claudes-Workshop/code/inference/out/bayesian_disease.png")
print("✓ Bayesian disease visualization saved")
print(f"\nBayesian Updates (test {sensitivity*100:.0f}% sensitivity, {specificity*100:.0f}% specificity):")
for prev, post in zip(prevalences, posteriors):
    print(f"  Prior {prev*100:5.1f}% → Posterior {post*100:5.1f}%")
print(f"\nInvariant: Likelihood ratio = {p_pos_disease / p_pos_healthy:.2f}:1")
print("The structure of updating remains constant across all priors.")
