"""Assemble the gallery into a single 3x2 contact sheet."""

from PIL import Image, ImageDraw, ImageFont
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(THIS_DIR, "out")

ORDER = [
    ("ember_wing.png",    "a=-1.4  b=1.6   c=1.0   d=0.7"),
    ("ice_lattice.png",   "a=1.7   b=1.7   c=0.6   d=1.2"),
    ("viridis_petal.png", "a=-1.7  b=1.3   c=-0.1  d=-1.21"),
    ("ember_storm.png",   "a=-1.8  b=-2.0  c=-0.5  d=-0.9"),
    ("ice_currents.png",  "a=1.5   b=-1.8  c=1.6   d=0.9"),
    ("ink_braid.png",     "a=-2.0  b=-2.0  c=-1.2  d=2.0"),
]

CELL = 600
PAD = 16
LABEL_H = 36
COLS, ROWS = 3, 2
W = COLS * CELL + (COLS + 1) * PAD
H = ROWS * (CELL + LABEL_H) + (ROWS + 1) * PAD

sheet = Image.new("RGB", (W, H), (10, 10, 12))
draw = ImageDraw.Draw(sheet)

try:
    font = ImageFont.truetype("/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf", 16)
except Exception:
    font = ImageFont.load_default()

for idx, (fname, label) in enumerate(ORDER):
    r, c = divmod(idx, COLS)
    img = Image.open(os.path.join(OUT_DIR, fname)).resize((CELL, CELL), Image.LANCZOS)
    x = PAD + c * (CELL + PAD)
    y = PAD + r * (CELL + LABEL_H + PAD)
    sheet.paste(img, (x, y))
    draw.text((x + 6, y + CELL + 8), label, fill=(200, 200, 210), font=font)

out_path = os.path.join(OUT_DIR, "_contact_sheet.png")
sheet.save(out_path)
print(out_path)
