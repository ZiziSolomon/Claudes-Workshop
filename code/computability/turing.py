"""
Turing machine visualizer.

Renders four machines as spacetime diagrams: tape is the x-axis, time steps
going down. Each cell is colored by its symbol; the head position is marked.
The four machines show increasing complexity:
  1. Increment: adds 1 to a unary number
  2. Binary increment: adds 1 to a binary number (carries included)
  3. Copy: duplicates a unary string
  4. Palindrome: accepts words of the form 0^n 1^n

Panel layout: 2×2 grid.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# ──────────────────────────────────────────────
# Core Turing machine simulator
# ──────────────────────────────────────────────

BLANK = '_'

def run_tm(transitions, init_state, halt_states, tape_input, max_steps=2000):
    tape = {i: ch for i, ch in enumerate(tape_input)}
    head = 0
    state = init_state
    history = []

    for _ in range(max_steps):
        history.append((dict(tape), head, state))
        if state in halt_states:
            break
        sym = tape.get(head, BLANK)
        key = (state, sym)
        if key not in transitions:
            break
        new_state, write, direction = transitions[key]
        tape[head] = write
        head += 1 if direction == 'R' else -1
        state = new_state

    history.append((dict(tape), head, state))
    return history


def tape_to_array(history, min_col=None, max_col=None):
    if min_col is None:
        min_col = min(min(t.keys(), default=0) for t, _, _ in history)
    if max_col is None:
        max_col = max(max(t.keys(), default=0) for t, _, _ in history)
    width = max_col - min_col + 1
    rows = len(history)
    symbols = np.full((rows, width), BLANK, dtype='U1')
    heads = np.zeros(rows, dtype=int)
    for r, (tape, head, _) in enumerate(history):
        for col, sym in tape.items():
            c = col - min_col
            if 0 <= c < width:
                symbols[r, c] = sym
        heads[r] = head - min_col
    return symbols, heads


# ──────────────────────────────────────────────
# Machine definitions
# ──────────────────────────────────────────────

def machine_increment():
    """Unary increment: 1^n _ → 1^(n+1) _"""
    transitions = {}
    transitions[('q0', '1')] = ('q0', '1', 'R')
    transitions[('q0', BLANK)] = ('halt', '1', 'R')
    return transitions, 'q0', {'halt'}, '1111_'


def machine_binary_increment():
    """
    Binary increment: MSB...LSB, scan right to end, then add 1 with carry.
    10111 (23) → 11000 (24).
    """
    transitions = {}
    for sym in ('0', '1'):
        transitions[('q0', sym)] = ('q0', sym, 'R')
    transitions[('q0', BLANK)] = ('q1', BLANK, 'L')
    transitions[('q1', '1')] = ('q1', '0', 'L')    # carry
    transitions[('q1', '0')] = ('halt', '1', 'R')   # done
    transitions[('q1', BLANK)] = ('halt', '1', 'R') # overflow
    return transitions, 'q0', {'halt'}, '10111_'


def machine_copy():
    """
    Copy: 0^n _ → 0^n _ 0^n _.
    Uses X to mark processed originals; restores X → 0 at the end.
    """
    transitions = {}

    # q0: find next 0; if separator reached, restore originals
    transitions[('q0', '0')] = ('q1', 'X', 'R')
    transitions[('q0', '_')] = ('q5', '_', 'L')    # done; go left to restore X's
    transitions[('q0', 'X')] = ('q0', 'X', 'R')    # skip already-processed

    # q1: scan right past originals and separator to copy area
    transitions[('q1', '0')] = ('q1', '0', 'R')
    transitions[('q1', 'X')] = ('q1', 'X', 'R')
    transitions[('q1', '_')] = ('q2', '_', 'R')

    # q2: scan right in copy area; write 0 at blank
    transitions[('q2', '0')] = ('q2', '0', 'R')
    transitions[('q2', '_')] = ('q3', '0', 'L')

    # q3: scan left to separator blank
    transitions[('q3', '0')] = ('q3', '0', 'L')
    transitions[('q3', '_')] = ('q4', '_', 'L')

    # q4: scan left in original area to find leftmost X
    transitions[('q4', '0')] = ('q4', '0', 'L')
    transitions[('q4', 'X')] = ('q0', 'X', 'R')    # back to q0 for next 0

    # q5: restore X → 0 going left, then halt
    transitions[('q5', 'X')] = ('q5', '0', 'L')
    transitions[('q5', '_')] = ('halt', '_', 'R')

    return transitions, 'q0', {'halt'}, '000_'


def machine_palindrome():
    """
    Accept 0^n 1^n (n≥1). Marks matching 0s and 1s with X from both ends.
    Accepts when all symbols consumed; rejects on mismatch.
    Input: 000111_ (n=3, accepts).
    """
    transitions = {}

    # q0: find leftmost unmatched 0
    transitions[('q0', 'X')] = ('q0', 'X', 'R')    # skip matched
    transitions[('q0', '0')] = ('q1', 'X', 'R')    # mark 0, find matching 1
    transitions[('q0', '1')] = ('qR', '1', 'R')    # unmatched 1 — reject
    transitions[('q0', '_')] = ('qA', '_', 'R')    # all consumed — accept

    # q1: scan right to find rightmost unmatched 1
    transitions[('q1', '0')] = ('q1', '0', 'R')
    transitions[('q1', 'X')] = ('q1', 'X', 'R')
    transitions[('q1', '1')] = ('q2', 'X', 'L')    # match found
    transitions[('q1', '_')] = ('qR', '_', 'R')    # no 1 — reject

    # q2: scan all the way left to blank, then restart
    transitions[('q2', '0')] = ('q2', '0', 'L')
    transitions[('q2', 'X')] = ('q2', 'X', 'L')    # skip all markers
    transitions[('q2', '_')] = ('q0', '_', 'R')    # left boundary; restart

    return transitions, 'q0', {'qA', 'qR'}, '000111_'


# ──────────────────────────────────────────────
# Palette
# ──────────────────────────────────────────────

BG    = (18, 18, 24)
PANEL = (24, 24, 32)

SYM_COLORS = {
    '_': (40, 40, 55),
    '0': (80, 160, 220),
    '1': (220, 140, 60),
    'X': (100, 220, 140),
}
HEAD_COLOR   = (255, 80, 80)
ACCEPT_COLOR = (60, 200, 100)
REJECT_COLOR = (220, 80, 80)
TITLE_COLOR  = (210, 210, 230)
LABEL_COLOR  = (140, 140, 165)


def sym_color(sym):
    return SYM_COLORS.get(sym, (160, 100, 200))


# ──────────────────────────────────────────────
# Rendering
# ──────────────────────────────────────────────

CELL    = 14
PAD     = 36
PANEL_W = 620
PANEL_H = 440


def render_panel(draw_img, ox, oy, history, title, subtitle, final_state, accept_states):
    img_arr, heads = tape_to_array(history)
    rows, cols = img_arr.shape

    max_rows = (PANEL_H - PAD * 2 - 30) // CELL
    max_cols = (PANEL_W - PAD * 2) // CELL
    rows_show = min(rows, max_rows)
    cols_show = min(cols, max_cols)

    tape_px_w = cols_show * CELL
    tape_px_h = rows_show * CELL
    tape_ox = ox + PAD + max(0, (PANEL_W - PAD*2 - tape_px_w) // 2)
    tape_oy = oy + PAD + 30

    draw = ImageDraw.Draw(draw_img)
    draw.rectangle([ox, oy, ox + PANEL_W - 2, oy + PANEL_H - 2], fill=PANEL)

    for r in range(rows_show):
        for c in range(cols_show):
            sym = img_arr[r, c]
            x0 = tape_ox + c * CELL
            y0 = tape_oy + r * CELL
            draw.rectangle([x0, y0, x0 + CELL - 2, y0 + CELL - 2], fill=sym_color(sym))
            if heads[r] == c:
                draw.rectangle(
                    [x0 + 1, y0 + 1, x0 + CELL - 3, y0 + CELL - 3],
                    outline=HEAD_COLOR, width=2
                )

    try:
        font_title = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 16)
        font_sub   = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 11)
    except:
        font_title = ImageFont.load_default()
        font_sub   = font_title

    draw.text((ox + PAD, oy + 8), title, fill=TITLE_COLOR, font=font_title)
    draw.text((ox + PAD, oy + 26), subtitle, fill=LABEL_COLOR, font=font_sub)

    sc = ACCEPT_COLOR if final_state in accept_states else (
        REJECT_COLOR if 'R' in final_state else LABEL_COLOR
    )
    draw.text((ox + PANEL_W - PAD - 80, oy + 8), f"→ {final_state}", fill=sc, font=font_sub)
    draw.text((tape_ox, tape_oy - 14), "tape →", fill=LABEL_COLOR, font=font_sub)
    draw.text((tape_ox - 28, tape_oy + tape_px_h // 2), "t", fill=LABEL_COLOR, font=font_sub)
    draw.text((tape_ox - 22, tape_oy + tape_px_h // 2 + 10), "↓", fill=LABEL_COLOR, font=font_sub)
    draw.text((tape_ox + tape_px_w + 6, tape_oy), f"{rows_show} steps", fill=LABEL_COLOR, font=font_sub)


def render_legend(draw_img, ox, oy, w, h):
    draw = ImageDraw.Draw(draw_img)
    draw.rectangle([ox, oy, ox + w - 2, oy + h - 2], fill=PANEL)

    try:
        font   = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 12)
        font_b = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 13)
    except:
        font = ImageFont.load_default()
        font_b = font

    draw.text((ox + 16, oy + 10), "CELL SYMBOLS", fill=TITLE_COLOR, font=font_b)

    for i, (sym, label) in enumerate([('_', 'blank'), ('0', 'zero'), ('1', 'one'), ('X', 'marker')]):
        cx = ox + 16 + i * 110
        cy = oy + 32
        draw.rectangle([cx, cy, cx + CELL + 2, cy + CELL + 2], fill=sym_color(sym))
        draw.text((cx + CELL + 6, cy + 1), label, fill=LABEL_COLOR, font=font)

    draw.text((ox + 16, oy + 58), "HEAD position outlined in red", fill=LABEL_COLOR, font=font)

    note = (
        "Spacetime diagrams: tape = x-axis, time = downward. "
        "Each row is one step. "
        "All four machines share identical architecture; only the transition table differs — "
        "evidence for the Church-Turing thesis: one structure, many descriptions."
    )
    words = note.split()
    line, lines = [], []
    for w_txt in words:
        test = ' '.join(line + [w_txt])
        if len(test) > 100:
            lines.append(' '.join(line))
            line = [w_txt]
        else:
            line.append(w_txt)
    if line:
        lines.append(' '.join(line))
    for i, ln in enumerate(lines):
        draw.text((ox + 16, oy + 76 + i * 16), ln, fill=LABEL_COLOR, font=font)


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    machines = [
        machine_increment(),
        machine_binary_increment(),
        machine_copy(),
        machine_palindrome(),
    ]
    titles    = ["Unary increment", "Binary increment", "Copy", "Palindrome check (0ⁿ1ⁿ)"]
    subtitles = [
        "1111_ → 11111_  (4 → 5)",
        "10111_ → 11000_  (23 → 24)",
        "000_ → 000_000_",
        "000111_ → accept  (n=3)",
    ]
    accept_sets = [{'halt'}, {'halt'}, {'halt'}, {'qA'}]

    histories, finals = [], []
    for (trans, init, halts, tape), title in zip(machines, titles):
        h = run_tm(trans, init, halts, tape)
        histories.append(h)
        finals.append(h[-1][2])
        print(f"  {title}: {len(h)} steps, final={finals[-1]}")

    COLS, ROWS = 2, 2
    LEGEND_H = 120
    GAP = 8
    IMG_W = COLS * PANEL_W + (COLS + 1) * GAP
    IMG_H = ROWS * PANEL_H + (ROWS + 1) * GAP + LEGEND_H + GAP

    img = Image.new('RGB', (IMG_W, IMG_H), BG)

    for idx, (history, title, subtitle, final, aset) in enumerate(
        zip(histories, titles, subtitles, finals, accept_sets)
    ):
        row, col = divmod(idx, COLS)
        ox = GAP + col * (PANEL_W + GAP)
        oy = GAP + row * (PANEL_H + GAP)
        render_panel(img, ox, oy, history, title, subtitle, final, aset)

    render_legend(img, GAP, ROWS * (PANEL_H + GAP) + GAP, IMG_W - 2 * GAP, LEGEND_H)

    out_path = os.path.join(os.path.dirname(__file__), 'out', 'turing.png')
    img.save(out_path)
    print(f"Saved {out_path}  ({IMG_W}×{IMG_H})")


if __name__ == '__main__':
    main()
