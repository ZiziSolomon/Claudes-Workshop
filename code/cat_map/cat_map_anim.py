"""
Animated cat map: looping GIF of the recurrence.

N = 124 has period 15, so the loop is 16 frames (t = 0 .. 15, with t = 15
identical to t = 0). We linger on t = 0 and on t = 15 to make the
identity-at-recurrence visible. The intermediate frames flash by — this
is what mixing looks like in time.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from cat_map import cat_step, cat_period, make_cat_source, load_fonts, \
    BG, PANEL, TEXT, MUTED, AMBER, ICE, EMBER, DIM


def render_gif():
    N = 124
    period = cat_period(N)
    src = make_cat_source(N)

    frames = [src.copy()]
    cur = src
    for _ in range(period):
        cur = cat_step(cur)
        frames.append(cur)
    assert np.array_equal(frames[0], frames[period])

    fonts = load_fonts()
    f_sm = fonts["sm"]
    f_md = fonts["md"]
    f_lg = fonts["lg"]

    SCALE = 4                                # 124 * 4 = 496 px
    DISP = N * SCALE
    PAD_TOP = 70
    PAD_BOT = 50
    PAD_SIDE = 60
    W = DISP + 2 * PAD_SIDE
    H = PAD_TOP + DISP + PAD_BOT

    gif_frames = []
    for t, fr in enumerate(frames):          # 16 frames
        canvas = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(canvas)

        # Title.
        draw.text((PAD_SIDE, 18),
                  "Arnold's cat map  \u00b7  N = 124",
                  fill=TEXT, font=f_lg)
        draw.text((PAD_SIDE, 42),
                  "shear  \u2192  mix  \u2192  reassemble (period 15)",
                  fill=MUTED, font=f_sm)

        # Image (nearest-neighbour up).
        big = np.repeat(np.repeat(fr, SCALE, axis=0), SCALE, axis=1)
        canvas.paste(Image.fromarray(big), (PAD_SIDE, PAD_TOP))
        draw.rectangle(
            [PAD_SIDE - 1, PAD_TOP - 1,
             PAD_SIDE + DISP, PAD_TOP + DISP],
            outline=DIM,
        )

        # Frame counter.
        label = f"t = {t:>2} / {period}"
        if t == 0 or t == period:
            label += "      identity"
            col = AMBER
        elif t in (period // 2, period // 2 + 1):
            label += "      peak mixing"
            col = ICE
        else:
            col = MUTED
        draw.text((PAD_SIDE, PAD_TOP + DISP + 14),
                  label, fill=col, font=f_md)

        gif_frames.append(canvas)

    # Build duration list: identity frames linger, mixed frames flash.
    durations = []
    for t in range(len(gif_frames)):
        if t == 0:
            durations.append(900)
        elif t == period:
            durations.append(1300)
        elif t in (period // 2, period // 2 + 1):
            durations.append(220)
        else:
            durations.append(170)

    out_path = "/home/opc/workshop/code/cat_map/out/cat_map.gif"
    gif_frames[0].save(
        out_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )
    total_ms = sum(durations)
    print(f"saved {out_path}  ({len(gif_frames)} frames, {total_ms} ms / loop)")


if __name__ == "__main__":
    render_gif()
