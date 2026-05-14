"""
Animated GIF of the baker map kneading.

The discrete iterates n = 0..10 are rendered as frames at a higher
resolution than the static strip. Each iteration holds for a beat so the
eye has time to recognise the rearrangement. The first frame (initial
4-quadrant condition) is held longer, and the last frame (essentially
horizontal stripes) is held a moment so the GIF visibly settles before
looping.

The interesting frames are the early ones (n = 1, 2, 3) where you can
still see the cut-and-stack happen as bands rearrange. By n = 6 the
information is in stripes whose order changes step-by-step in ways the
eye can no longer track. That asymmetry is exactly mixing.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from baker_doubling import baker_quadrant_after, load_fonts
from baker_doubling import BG, PANEL, TEXT, MUTED, AMBER, DIM


N = 320
FRAMES = 11   # n = 0 .. 10
PAD = 36
LABEL_H = 36
TITLE_H = 64


def render_frame(n: int, fonts) -> Image.Image:
    """Single GIF frame: square dough on a labelled canvas."""
    f_sm, f_md, f_lg = fonts["sm"], fonts["md"], fonts["lg"]

    W = N + 2 * PAD
    H = TITLE_H + N + LABEL_H + PAD

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((PAD, 14), "Baker map", fill=TEXT, font=f_lg)
    draw.text((PAD, 38),
              "B(x, y) = (2x mod 1,  (y + floor(2x)) / 2)",
              fill=MUTED, font=f_sm)

    arr = baker_quadrant_after(N, n)
    draw.rectangle([PAD - 1, TITLE_H - 1, PAD + N, TITLE_H + N], outline=DIM)
    img.paste(Image.fromarray(arr), (PAD, TITLE_H))

    # Bottom label: iteration count.
    label = f"n = {n}"
    draw.text((PAD, TITLE_H + N + 8), label, fill=AMBER, font=f_md)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)

    fonts = load_fonts()
    frames = [render_frame(n, fonts) for n in range(FRAMES)]

    # Hold the start frame for ~1 s, intermediate frames ~0.5 s,
    # the final-stripes frame for ~1 s before looping.
    durations = []
    for n in range(FRAMES):
        if n == 0:
            durations.append(900)
        elif n == FRAMES - 1:
            durations.append(900)
        else:
            durations.append(500)

    # Convert all frames to the same palette with NO dithering so that the
    # high-frequency stripes don't pick up phantom mid-tones from
    # Floyd-Steinberg error diffusion.
    pal_src = frames[0].convert("P", palette=Image.ADAPTIVE, colors=64,
                                dither=Image.Dither.NONE)
    p_frames = [pal_src] + [
        f.quantize(palette=pal_src, dither=Image.Dither.NONE)
        for f in frames[1:]
    ]

    out_path = os.path.join(out_dir, "baker.gif")
    p_frames[0].save(
        out_path,
        save_all=True,
        append_images=p_frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )
    size_kb = os.path.getsize(out_path) / 1024
    print(f"wrote {out_path}  ({size_kb:.0f} KB,  {FRAMES} frames)")


if __name__ == "__main__":
    main()
