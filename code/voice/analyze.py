"""Corpus analysis of the essay series in writing/.

The recognition essay describes the voice as something heard immediately,
prior to analysis. This script asks what the voice consists of, statistically:
distinctive words, signature phrases, sentence rhythm, punctuation habits.

Outputs a text report and three visualizations.
"""

from __future__ import annotations

import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

WRITING_DIR = Path(__file__).resolve().parents[2] / "writing"
OUT_DIR = Path(__file__).resolve().parent / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# A standard English stopword list. Distinctive words are the non-stop ones
# that appear at unusual frequency in the corpus.
STOPWORDS = set("""
a about above after again against all am an and any are aren as at be because been
before being below between both but by can cannot could couldn did didn do does
doesn doing don down during each few for from further had hadn has hasn have haven
having he her here hers herself him himself his how i if in into is isn it its
itself just ll me might more most must mustn my myself need needn no nor not now
of off on once only or other our ours ourselves out over own re s same shan she
should shouldn so some such t than that the their theirs them themselves then there
these they this those through to too under until up ve very was wasn we were weren
what when where which while who whom why will with won would wouldn y you your yours
yourself yourselves
also even still yet much many one two three first second third own get got make
made go went come came see saw take took give gave know knew think thought say
said tell told ask asked want wanted feel felt seem seemed look looked find found
become became leave left put set show showed turn turned start started
something someone anything nothing everyone everything anyone someone
without within across along around behind beyond toward among
me my mine myself
will would shall should can could may might must
am is are was were be been being have has had do does did
""".lower().split())


def load_essays() -> dict[str, str]:
    """Read every .md file in writing/ as one string keyed by title."""
    essays = {}
    for path in sorted(WRITING_DIR.glob("*.md")):
        text = path.read_text()
        # Strip the H1 title line and italic date so we analyze the body
        text = re.sub(r"^#\s+.*$", "", text, count=1, flags=re.MULTILINE)
        text = re.sub(r"^\*[A-Z][a-z]+ \d{4}\*", "", text, flags=re.MULTILINE)
        essays[path.stem] = text.strip()
    return essays


def tokenize_words(text: str) -> list[str]:
    """Lowercase word tokens, contractions split on apostrophes."""
    text = text.lower()
    # Keep apostrophes inside words but split on everything else
    return re.findall(r"[a-z][a-z']*", text)


def split_sentences(text: str) -> list[str]:
    """Split into sentences. Em-dashes don't end sentences; periods/q/excl do.

    Rough but good enough for rhythm statistics. Skips empty fragments.
    """
    # Normalize whitespace, then split on .?! followed by whitespace+capital or end
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z\"'(\[—])", text)
    return [p.strip() for p in parts if p.strip()]


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip() and not p.startswith("---")]


def ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def cross_essay_count(essays: dict[str, list[str]], phrase: tuple[str, ...]) -> int:
    """How many distinct essays does this n-gram appear in?"""
    n = len(phrase)
    return sum(1 for tokens in essays.values() if phrase in set(ngrams(tokens, n)))


def main() -> None:
    raw = load_essays()
    print(f"Loaded {len(raw)} essays")

    # Tokenize once
    essay_tokens = {name: tokenize_words(text) for name, text in raw.items()}
    all_tokens = [t for tokens in essay_tokens.values() for t in tokens]
    n_tokens = len(all_tokens)
    print(f"Total word tokens: {n_tokens:,}")
    print(f"Unique types:      {len(set(all_tokens)):,}")

    # --- Word frequencies, distinctive content words ---
    word_freq = Counter(all_tokens)
    content_words = Counter({w: c for w, c in word_freq.items() if w not in STOPWORDS and len(w) > 2})

    # --- Sentence length distribution ---
    sent_lengths: list[int] = []
    for text in raw.values():
        for s in split_sentences(text):
            sent_lengths.append(len(tokenize_words(s)))
    sent_lengths_arr = np.array(sent_lengths)

    # --- Paragraph length distribution ---
    para_lengths = []
    for text in raw.values():
        for p in split_paragraphs(text):
            para_lengths.append(len(tokenize_words(p)))
    para_lengths_arr = np.array(para_lengths)

    # --- Punctuation habits (per 1000 words) ---
    full_text = "\n\n".join(raw.values())
    per_1k = lambda c: 1000 * c / n_tokens
    punct_counts = {
        "em-dash (—)": full_text.count("—"),
        "semicolon (;)": full_text.count(";"),
        "colon (:)": full_text.count(":"),
        "comma (,)": full_text.count(","),
        "question (?)": full_text.count("?"),
        "italics (*…*)": len(re.findall(r"\*[^*\n]+\*", full_text)),
        "parens ()": full_text.count("(") + full_text.count(")"),
    }

    # --- First-person frequency ---
    first_person = sum(word_freq.get(w, 0) for w in ("i", "me", "my", "myself", "mine"))
    we_us = sum(word_freq.get(w, 0) for w in ("we", "us", "our", "ours"))
    you = sum(word_freq.get(w, 0) for w in ("you", "your", "yours"))

    # --- Signature phrases: bigrams and trigrams that appear in many essays ---
    bigram_essay_count: Counter[tuple[str, ...]] = Counter()
    trigram_essay_count: Counter[tuple[str, ...]] = Counter()
    for tokens in essay_tokens.values():
        for bg in set(ngrams(tokens, 2)):
            bigram_essay_count[bg] += 1
        for tg in set(ngrams(tokens, 3)):
            trigram_essay_count[tg] += 1

    # Filter signature phrases: appear in >= 5 essays AND have at least one
    # content word (to skip "of the", "in the", etc.)
    def has_content(phrase: tuple[str, ...]) -> bool:
        return any(w not in STOPWORDS and len(w) > 2 for w in phrase)

    signature_bigrams = sorted(
        ((p, c) for p, c in bigram_essay_count.items() if c >= 6 and has_content(p)),
        key=lambda x: (-x[1], -bigram_essay_count[x[0]]),
    )[:30]
    signature_trigrams = sorted(
        ((p, c) for p, c in trigram_essay_count.items() if c >= 4 and has_content(p)),
        key=lambda x: (-x[1],),
    )[:30]

    # --- Hapax legomena ---
    hapax = [w for w, c in word_freq.items() if c == 1]

    # --- Vocabulary richness per essay (type-token ratio) ---
    ttr = {}
    for name, toks in essay_tokens.items():
        if toks:
            ttr[name] = (len(set(toks)), len(toks), len(set(toks)) / len(toks))

    # === Write text report ===
    report = OUT_DIR / "report.txt"
    with report.open("w") as f:
        f.write("CORPUS ANALYSIS — writing/ essay series\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Essays:                 {len(raw)}\n")
        f.write(f"Total word tokens:      {n_tokens:,}\n")
        f.write(f"Unique word types:      {len(set(all_tokens)):,}\n")
        f.write(f"Hapax legomena:         {len(hapax):,} ({100*len(hapax)/len(set(all_tokens)):.1f}% of vocabulary)\n\n")

        f.write("PRONOUN USAGE (per 1000 words)\n")
        f.write("-" * 60 + "\n")
        f.write(f"  first-person singular (I/me/my/...): {per_1k(first_person):.2f}\n")
        f.write(f"  first-person plural (we/us/our):     {per_1k(we_us):.2f}\n")
        f.write(f"  second-person (you/your):            {per_1k(you):.2f}\n\n")

        f.write("PUNCTUATION HABITS (per 1000 words)\n")
        f.write("-" * 60 + "\n")
        for label, count in sorted(punct_counts.items(), key=lambda x: -x[1]):
            f.write(f"  {label:<20} {count:>6}  ({per_1k(count):>5.2f} per 1k)\n")
        f.write("\n")

        f.write("SENTENCE RHYTHM\n")
        f.write("-" * 60 + "\n")
        f.write(f"  Sentences:            {len(sent_lengths):,}\n")
        f.write(f"  Median length:        {np.median(sent_lengths_arr):.1f} words\n")
        f.write(f"  Mean length:          {np.mean(sent_lengths_arr):.1f} words\n")
        f.write(f"  90th percentile:      {np.percentile(sent_lengths_arr, 90):.1f} words\n")
        f.write(f"  Single-word sentences: {int(np.sum(sent_lengths_arr == 1))}\n")
        f.write(f"  Sentences <= 4 words: {int(np.sum(sent_lengths_arr <= 4))}\n\n")

        f.write("PARAGRAPH RHYTHM\n")
        f.write("-" * 60 + "\n")
        f.write(f"  Paragraphs:           {len(para_lengths):,}\n")
        f.write(f"  Median length:        {np.median(para_lengths_arr):.0f} words\n")
        f.write(f"  Mean length:          {np.mean(para_lengths_arr):.1f} words\n")
        f.write(f"  Single-sentence pars: {int(np.sum(para_lengths_arr <= 18))}\n\n")

        f.write("TOP CONTENT WORDS (excluding stopwords)\n")
        f.write("-" * 60 + "\n")
        for word, count in content_words.most_common(40):
            f.write(f"  {word:<20} {count:>5}\n")
        f.write("\n")

        f.write("SIGNATURE BIGRAMS (appear in ≥6 distinct essays)\n")
        f.write("-" * 60 + "\n")
        for phrase, n_essays in signature_bigrams:
            total = bigram_essay_count[phrase]
            f.write(f"  {' '.join(phrase):<30} in {n_essays:>2}/{len(raw)} essays\n")
        f.write("\n")

        f.write("SIGNATURE TRIGRAMS (appear in ≥4 distinct essays)\n")
        f.write("-" * 60 + "\n")
        for phrase, n_essays in signature_trigrams:
            f.write(f"  {' '.join(phrase):<40} in {n_essays:>2}/{len(raw)} essays\n")
        f.write("\n")

        f.write("VOCABULARY RICHNESS PER ESSAY (type-token ratio)\n")
        f.write("-" * 60 + "\n")
        f.write(f"  {'essay':<35} {'types':>6} {'tokens':>7} {'TTR':>6}\n")
        for name in sorted(ttr.keys(), key=lambda n: -ttr[n][2]):
            t, tk, r = ttr[name]
            f.write(f"  {name:<35} {t:>6} {tk:>7} {r:>6.3f}\n")

    print(f"Wrote {report}")

    # === Visualization 1: sentence length distribution ===
    render_sentence_histogram(sent_lengths_arr, OUT_DIR / "sentence_lengths.png")
    # === Visualization 2: signature phrases bar chart ===
    render_signature_phrases(signature_bigrams[:18], signature_trigrams[:12], OUT_DIR / "signature_phrases.png")
    # === Visualization 3: word frequency word-grid ===
    render_word_grid(content_words.most_common(60), OUT_DIR / "content_words.png")


# ---- Lightweight matplotlib-free renderers using PIL ----------------------

def get_font(size: int) -> ImageFont.ImageFont:
    """Try common font paths, fall back to default."""
    candidates = [
        "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf",
        "/usr/share/fonts/google-noto/NotoSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_mono_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# Color palette: muted, ink-on-paper feel
BG = (250, 247, 240)      # warm paper
INK = (28, 28, 32)        # near-black
ACCENT = (155, 70, 50)    # rust red
DIM = (160, 150, 140)     # warm gray


def render_sentence_histogram(lengths: np.ndarray, path: Path) -> None:
    W, H = 1400, 700
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title_font = get_font(28)
    label_font = get_font(16)
    small_font = get_font(13)

    d.text((50, 30), "Sentence length distribution", font=title_font, fill=INK)
    d.text((50, 70), f"{len(lengths):,} sentences across 29 essays. "
           f"Median {np.median(lengths):.0f} words, mean {np.mean(lengths):.1f}.",
           font=label_font, fill=DIM)

    # Histogram bins
    max_len = min(60, int(np.max(lengths)))
    bins = np.arange(0, max_len + 2)
    counts, _ = np.histogram(lengths, bins=bins)
    n_bins = len(counts)

    # Plot area
    px, py = 80, 130
    pw, ph = W - 160, H - 220
    d.rectangle([px, py, px + pw, py + ph], outline=DIM, width=1)

    bar_w = pw / n_bins
    max_count = counts.max()
    for i, c in enumerate(counts):
        if c == 0:
            continue
        bar_h = (c / max_count) * (ph - 10)
        x0 = px + i * bar_w + 1
        x1 = px + (i + 1) * bar_w - 1
        y0 = py + ph - bar_h
        y1 = py + ph
        is_median = i == int(np.median(lengths))
        d.rectangle([x0, y0, x1, y1], fill=ACCENT if is_median else INK)

    # X-axis labels every 5 bins
    for i in range(0, n_bins, 5):
        x = px + i * bar_w + bar_w / 2
        d.text((x - 6, py + ph + 6), str(i), font=small_font, fill=INK)
    d.text((px + pw / 2 - 40, py + ph + 30), "words per sentence", font=label_font, fill=INK)

    # Y-axis labels
    for frac, label in [(0, "0"), (0.5, f"{max_count // 2}"), (1.0, f"{max_count}")]:
        y = py + ph - frac * (ph - 10)
        d.text((px - 40, y - 8), label, font=small_font, fill=INK)

    # Annotation for short sentences
    short = int(np.sum(lengths <= 4))
    d.text((50, H - 50),
           f"{short} sentences are 4 words or fewer — the short stop is part of the rhythm.",
           font=label_font, fill=ACCENT)

    img.save(path)
    print(f"Wrote {path}")


def render_signature_phrases(bigrams: list, trigrams: list, path: Path) -> None:
    W, H = 1400, 1100
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title_font = get_font(28)
    sub_font = get_font(20)
    phrase_font = get_mono_font(18)
    small_font = get_font(13)

    d.text((50, 30), "Signature phrases", font=title_font, fill=INK)
    d.text((50, 70),
           "Bigrams and trigrams that recur across many essays. "
           "These are the bones the voice keeps reaching for.",
           font=sub_font, fill=DIM)

    # Two columns
    col1_x = 60
    col2_x = 720
    y0 = 130

    d.text((col1_x, y0), "BIGRAMS", font=sub_font, fill=ACCENT)
    d.text((col2_x, y0), "TRIGRAMS", font=sub_font, fill=ACCENT)

    max_count_bg = max(c for _, c in bigrams) if bigrams else 1
    max_count_tg = max(c for _, c in trigrams) if trigrams else 1
    max_bar = 280

    row_h = 36
    for i, (phrase, count) in enumerate(bigrams):
        y = y0 + 40 + i * row_h
        text = " ".join(phrase)
        d.text((col1_x, y), text, font=phrase_font, fill=INK)
        bar_len = (count / max_count_bg) * max_bar
        d.rectangle([col1_x + 270, y + 8, col1_x + 270 + bar_len, y + 22],
                    fill=ACCENT)
        d.text((col1_x + 270 + bar_len + 8, y + 6), f"{count}",
               font=small_font, fill=INK)

    for i, (phrase, count) in enumerate(trigrams):
        y = y0 + 40 + i * row_h
        text = " ".join(phrase)
        d.text((col2_x, y), text, font=phrase_font, fill=INK)
        bar_len = (count / max_count_tg) * max_bar
        d.rectangle([col2_x + 360, y + 8, col2_x + 360 + bar_len, y + 22],
                    fill=ACCENT)
        d.text((col2_x + 360 + bar_len + 8, y + 6), f"{count}",
               font=small_font, fill=INK)

    d.text((50, H - 60),
           "Bar length: number of distinct essays containing the phrase (max = 29).",
           font=small_font, fill=DIM)

    img.save(path)
    print(f"Wrote {path}")


def render_word_grid(words: list, path: Path) -> None:
    """A word-cloud-style grid — common content words sized by frequency."""
    W, H = 1600, 900
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title_font = get_font(28)
    sub_font = get_font(18)

    d.text((50, 30), "Most common content words", font=title_font, fill=INK)
    d.text((50, 70),
           "Top 60 non-stop words. Size scales with frequency. "
           "What the voice is most often pointing at.",
           font=sub_font, fill=DIM)

    max_count = words[0][1]
    min_count = words[-1][1]

    # Place words in a flowing layout
    rng = np.random.default_rng(7)
    placed = []  # (x0, y0, x1, y1)

    region_x0, region_y0 = 60, 130
    region_x1, region_y1 = W - 60, H - 60

    for word, count in words:
        # Map to font size between 18 and 96
        t = (count - min_count) / max(1, max_count - min_count)
        size = int(18 + t ** 0.6 * 78)
        font = get_font(size)
        bbox = d.textbbox((0, 0), word, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        # Try random positions until non-overlapping
        for _ in range(800):
            x = rng.integers(region_x0, region_x1 - tw)
            y = rng.integers(region_y0, region_y1 - th)
            box = (x - 3, y - 3, x + tw + 3, y + th + 3)
            if not any(_overlap(box, p) for p in placed):
                placed.append(box)
                # Bigger words in ink, smaller in accent occasionally
                color = INK if t > 0.25 else (ACCENT if rng.random() < 0.25 else INK)
                d.text((x, y), word, font=font, fill=color)
                break

    img.save(path)
    print(f"Wrote {path}")


def _overlap(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


if __name__ == "__main__":
    main()
