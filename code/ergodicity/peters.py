"""
Ergodicity visualization: the Peters coin flip.

Each trajectory starts with wealth 1.0. Every step, a fair coin is flipped:
  heads (p=0.5): wealth *= 1.5  (a 50% gain)
  tails (p=0.5): wealth *= 0.6  (a 40% loss)

Per-flip ensemble expectation: E[r] = 0.5*1.5 + 0.5*0.6 = 1.05  (5% gain).
Per-flip time-average growth:   exp(E[log r]) = sqrt(1.5*0.6) = sqrt(0.9)
                                              ≈ 0.9487      (5% loss).

The two diverge by ten orders of magnitude over a few hundred flips.
A typical trajectory loses everything; the ensemble mean is dominated by
exceedingly rare massive winners. This is the canonical non-ergodic
process: the time average along any trajectory disagrees, in the long run,
with the average across the ensemble at a fixed time.

Three panels:
  Panel 1: 300 sample trajectories on a log-y axis.
  Panel 2: Theoretical ensemble mean (1.05^t) vs theoretical typical wealth
           (0.9487^t), with the empirical median overlaid for sanity.
  Panel 3: Histogram of log-wealth at the final time.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

rng = np.random.default_rng(7)

# --- Simulation ---
N_TRAJ = 5000
T = 300                 # 300 flips: ~13 orders of magnitude divergence
UP = 1.5
DN = 0.6

flips = rng.random((N_TRAJ, T)) < 0.5
mults = np.where(flips, UP, DN)
log_mults = np.log(mults)
log_w = np.concatenate(
    [np.zeros((N_TRAJ, 1)), np.cumsum(log_mults, axis=1)], axis=1
)

t_axis = np.arange(T + 1)
theory_mean    = (0.5 * UP + 0.5 * DN) ** t_axis        # 1.05^t
theory_typical = (math.sqrt(UP * DN)) ** t_axis         # 0.9487^t

empirical_median = np.exp(np.median(log_w, axis=0))

final_log = log_w[:, -1]
frac_below_start = float(np.mean(final_log < 0))
frac_lost_99pct  = float(np.mean(final_log < math.log(0.01)))
frac_won = 1 - frac_below_start

# --- Palette ---
BG     = (18, 20, 25)
PANEL  = (24, 27, 35)
GRID   = (40, 42, 50)
TEXT   = (210, 215, 225)
MUTED  = (110, 115, 130)
DIM    = (75, 80, 92)

AMBER  = (255, 190,  60)    # ensemble mean
EMBER  = (255,  90,  50)    # typical / time-average
ICE    = (100, 200, 255)    # median / reference
VERDI  = ( 80, 210, 140)
VIOLET = (170, 110, 240)

W, H = 1500, 580
PAD = 50
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

try:
    font_xs = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 11)
    font_sm = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 13)
    font_md = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 15)
    font_lg = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 17)
    font_xl = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 22)
except OSError:
    font_xs = font_sm = font_md = font_lg = font_xl = ImageFont.load_default()

PANEL_W = (W - 4 * PAD) // 3
PANEL_H = H - 2 * PAD

def panel_rect(i):
    x0 = PAD + i * (PANEL_W + PAD)
    y0 = PAD
    return x0, y0, x0 + PANEL_W, y0 + PANEL_H

def draw_panel_bg(i, title, subtitle=None):
    x0, y0, x1, y1 = panel_rect(i)
    draw.rectangle([x0, y0, x1, y1], fill=PANEL)
    draw.rectangle([x0, y0, x1, y1], outline=GRID, width=1)
    tw = draw.textlength(title, font=font_lg)
    draw.text((x0 + (PANEL_W - tw) / 2, y0 + 10), title, fill=TEXT, font=font_lg)
    if subtitle:
        sw = draw.textlength(subtitle, font=font_xs)
        draw.text((x0 + (PANEL_W - sw) / 2, y0 + 32), subtitle, fill=MUTED, font=font_xs)
    return x0 + 50, y0 + 56, x1 - 14, y1 - 14

# ----------------------------------------------------------------------------
# Panel 1: trajectories on log-y
# ----------------------------------------------------------------------------
ox, oy, ex, ey = draw_panel_bg(0, "Trajectories",
                               "5000 simulated coin-flippers, 300 plotted")
inner_w = ex - ox
inner_h = ey - oy

log10_w = log_w / math.log(10.0)
y_min = math.floor(np.percentile(log10_w, 0.5)) - 1
y_max = math.ceil(np.percentile(log10_w, 99.5)) + 1

def to_px1(t, y_log10):
    fx = t / T
    fy = (y_log10 - y_min) / (y_max - y_min)
    return ox + fx * inner_w, oy + (1 - fy) * inner_h

step = max(1, (y_max - y_min) // 14)
for yval in range(y_min, y_max + 1, step):
    yy = oy + (1 - (yval - y_min) / (y_max - y_min)) * inner_h
    draw.line([(ox, yy), (ox + inner_w, yy)], fill=GRID, width=1)
    label = f"10^{yval}" if yval != 0 else "1"
    draw.text((ox - 44, yy - 7), label, fill=MUTED, font=font_xs)

for ti in range(0, T + 1, 50):
    fx = ti / T
    xx = ox + fx * inner_w
    draw.line([(xx, oy), (xx, oy + inner_h)], fill=GRID, width=1)
    draw.text((xx - 8, oy + inner_h + 4), str(ti), fill=MUTED, font=font_xs)
draw.text((ox + inner_w / 2 - 14, oy + inner_h + 18), "flips", fill=MUTED, font=font_sm)

sample_idx = rng.choice(N_TRAJ, size=300, replace=False)
for i in sample_idx:
    pts = []
    for t in range(0, T + 1, 2):
        pts.append(to_px1(t, log10_w[i, t]))
    draw.line(pts, fill=DIM, width=1)

# Reference line at wealth = 1
yy0 = oy + (1 - (0 - y_min) / (y_max - y_min)) * inner_h
draw.line([(ox, yy0), (ox + inner_w, yy0)], fill=ICE, width=1)
draw.text((ox + inner_w - 110, yy0 - 14), "starting wealth = 1",
          fill=ICE, font=font_xs)

# ----------------------------------------------------------------------------
# Panel 2: time average vs ensemble average (theoretical)
# ----------------------------------------------------------------------------
ox, oy, ex, ey = draw_panel_bg(1, "Time average vs ensemble average",
                               "theoretical curves; empirical median in blue")
inner_w = ex - ox
inner_h = ey - oy

em_log10 = np.log10(theory_mean)
ty_log10 = np.log10(theory_typical)
md_log10 = np.log10(np.maximum(empirical_median, 1e-30))

y_min2 = math.floor(min(ty_log10.min(), md_log10.min()) - 1)
y_max2 = math.ceil(em_log10.max() + 1)

def to_px2(t, y_log10):
    fx = t / T
    fy = (y_log10 - y_min2) / (y_max2 - y_min2)
    return ox + fx * inner_w, oy + (1 - fy) * inner_h

step2 = max(1, (y_max2 - y_min2) // 14)
for yval in range(y_min2, y_max2 + 1, step2):
    yy = oy + (1 - (yval - y_min2) / (y_max2 - y_min2)) * inner_h
    draw.line([(ox, yy), (ox + inner_w, yy)], fill=GRID, width=1)
    label = f"10^{yval}" if yval != 0 else "1"
    draw.text((ox - 44, yy - 7), label, fill=MUTED, font=font_xs)

for ti in range(0, T + 1, 50):
    fx = ti / T
    xx = ox + fx * inner_w
    draw.line([(xx, oy), (xx, oy + inner_h)], fill=GRID, width=1)
    draw.text((xx - 8, oy + inner_h + 4), str(ti), fill=MUTED, font=font_xs)
draw.text((ox + inner_w / 2 - 14, oy + inner_h + 18), "flips", fill=MUTED, font=font_sm)

# Plot: median first (so it sits underneath), then theoretical curves
draw.line([to_px2(t, md_log10[t]) for t in range(T + 1)], fill=ICE, width=2)
draw.line([to_px2(t, ty_log10[t]) for t in range(T + 1)], fill=EMBER, width=3)
draw.line([to_px2(t, em_log10[t]) for t in range(T + 1)], fill=AMBER, width=3)

# Legend (lower-left to avoid the curves)
lx, ly = ox + 10, oy + inner_h - 80
draw.rectangle([lx - 6, ly - 6, lx + 270, ly + 64], fill=(30, 33, 42), outline=GRID)
draw.line([(lx, ly + 6), (lx + 22, ly + 6)], fill=AMBER, width=3)
draw.text((lx + 30, ly), "ensemble mean   (1.05)^t", fill=TEXT, font=font_sm)
draw.line([(lx, ly + 26), (lx + 22, ly + 26)], fill=EMBER, width=3)
draw.text((lx + 30, ly + 20), "typical wealth   (0.9487)^t", fill=TEXT, font=font_sm)
draw.line([(lx, ly + 46), (lx + 22, ly + 46)], fill=ICE, width=2)
draw.text((lx + 30, ly + 40), "empirical median (n=5000)", fill=TEXT, font=font_sm)

# Annotate the divergence at t=T
gap = em_log10[-1] - ty_log10[-1]
note = f"divergence at t={T}:  ~10^{gap:.0f}"
draw.text((ox + 12, oy + 8), note, fill=TEXT, font=font_md)

# ----------------------------------------------------------------------------
# Panel 3: final-time distribution of log-wealth
# ----------------------------------------------------------------------------
ox, oy, ex, ey = draw_panel_bg(2, f"Distribution of log-wealth at t = {T}",
                               "red = lost money,  green = gained money")
inner_w = ex - ox
inner_h = ey - oy

final_log10 = final_log / math.log(10.0)

hmin = math.floor(np.percentile(final_log10, 0.1)) - 2
hmax = math.ceil(np.percentile(final_log10, 99.9)) + 2
nbins = 60
counts, edges = np.histogram(final_log10, bins=nbins, range=(hmin, hmax))
max_count = counts.max()

for bi, c in enumerate(counts):
    if c <= 0:
        continue
    x_left = edges[bi]
    x_right = edges[bi + 1]
    fx0 = (x_left - hmin) / (hmax - hmin)
    fx1 = (x_right - hmin) / (hmax - hmin)
    xL = ox + fx0 * inner_w
    xR = ox + fx1 * inner_w
    yT = oy + (1 - c / max_count) * inner_h
    yB = oy + inner_h
    center = 0.5 * (x_left + x_right)
    color = EMBER if center < 0 else VERDI
    draw.rectangle([xL + 1, yT, xR - 1, yB], fill=color)

# x labels: choose tick step so labels do not crowd
tick_step = max(1, (hmax - hmin) // 6)
if tick_step >= 4:
    tick_step = ((tick_step + 1) // 2) * 2  # round up to even
for xv in range(hmin, hmax + 1, tick_step):
    fx = (xv - hmin) / (hmax - hmin)
    xx = ox + fx * inner_w
    draw.line([(xx, oy), (xx, oy + inner_h)], fill=GRID, width=1)
    label = f"10^{xv}" if xv != 0 else "1"
    tw = draw.textlength(label, font=font_xs)
    draw.text((xx - tw / 2, oy + inner_h + 4), label, fill=MUTED, font=font_xs)

# initial wealth marker
fx0 = (0 - hmin) / (hmax - hmin)
xx0 = ox + fx0 * inner_w
draw.line([(xx0, oy), (xx0, oy + inner_h)], fill=ICE, width=2)
draw.text((xx0 - 50, oy + 4), "start = 1", fill=ICE, font=font_xs)

# theoretical mean marker
mean_log10 = math.log10(theory_mean[-1])
fxM = (mean_log10 - hmin) / (hmax - hmin)
if 0 <= fxM <= 1:
    xxM = ox + fxM * inner_w
    draw.line([(xxM, oy), (xxM, oy + inner_h)], fill=AMBER, width=2)
    tw = draw.textlength("ensemble mean", font=font_xs)
    draw.text((xxM - tw - 6, oy + 22), "ensemble mean →", fill=AMBER, font=font_xs)

# stats panel
stats_y = oy + 60
stats_x = ox + 12
draw.rectangle([stats_x - 6, stats_y - 6, stats_x + 280, stats_y + 96],
               fill=(30, 33, 42), outline=GRID)
draw.text((stats_x, stats_y),
          f"trajectories: {N_TRAJ}", fill=TEXT, font=font_sm)
draw.text((stats_x, stats_y + 18),
          f"below starting wealth:  {100*frac_below_start:.1f}%",
          fill=EMBER, font=font_sm)
draw.text((stats_x, stats_y + 36),
          f"lost ≥99% of wealth:    {100*frac_lost_99pct:.1f}%",
          fill=EMBER, font=font_sm)
draw.text((stats_x, stats_y + 54),
          f"above starting wealth:  {100*frac_won:.1f}%",
          fill=VERDI, font=font_sm)
draw.text((stats_x, stats_y + 72),
          f"max sampled wealth:     10^{final_log10.max():.1f}",
          fill=VERDI, font=font_sm)

draw.text((ox + inner_w / 2 - 50, oy + inner_h + 18),
          "log10(final wealth)", fill=MUTED, font=font_sm)

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
footer = ("Each step: heads × 1.5,  tails × 0.6.   "
          "Ensemble grows at +5%/step; typical trajectory shrinks at -5%/step.   "
          "The two averages are not the same number.")
fw = draw.textlength(footer, font=font_sm)
draw.text(((W - fw) / 2, H - 28), footer, fill=MUTED, font=font_sm)

OUT = "/home/opc/workshop/code/ergodicity/out/peters.png"
img.save(OUT)
print(f"wrote {OUT}")
print(f"  theoretical ensemble mean at t={T}: 10^{em_log10[-1]:.2f}")
print(f"  theoretical typical at t={T}:       10^{ty_log10[-1]:.2f}")
print(f"  empirical median at t={T}:          10^{md_log10[-1]:.2f}")
print(f"  fraction below start:                {frac_below_start:.3f}")
print(f"  fraction lost ≥99%:                  {frac_lost_99pct:.3f}")
print(f"  max sampled final wealth:            10^{final_log10.max():.2f}")
