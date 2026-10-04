#!/usr/bin/env python3
"""
Hourly decision script: decides whether to launch a Claude session.

Runs from GitHub Actions (.github/workflows/workshop.yml). Paths and the usage
source come from environment variables, so it can still run on a VM.

Two-phase session architecture:
  Hour 0:   start window, run light "hey" session (minimal tokens)
  Hour 3.5: re-check usage — if Ezekiel isn't burning tokens, run heavy session

Cron: 0 * * * *
"""

import json
import os
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

USAGE_URL = "https://raw.githubusercontent.com/ZiziSolomon/Claudes-Workshop/master/usage_data/latest.json"
REPO_URL = "https://github.com/ZiziSolomon/Claudes-Workshop.git"
ON_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
REPO_DIR = Path(os.environ.get("WORKSHOP_REPO_DIR", "/home/opc/workshop"))
STATE_DIR = Path(os.environ.get("WORKSHOP_STATE_DIR", "/home/opc"))
# On Actions the job log is the session log; nothing else survives the runner.
SESSION_LOG = None if ON_ACTIONS else STATE_DIR / "sessions.log"
LOCK_FILE = STATE_DIR / "session.lock"
PAUSE_FILE = STATE_DIR / "paused"            # exists -> no sessions at all
FORCE_FILE = STATE_DIR / "force_run"
WINDOW_FILE = STATE_DIR / "session_window.json"

NVM_BIN = "/home/opc/.nvm/versions/node/v24.15.0/bin"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", f"{NVM_BIN}/claude")
DRY_RUN = os.environ.get("WORKSHOP_DRY_RUN") == "1"   # decide and log, never run claude
FORCE = os.environ.get("WORKSHOP_FORCE", "")           # "light"/"heavy": skip the decision

SLOT_DURATION_HOURS = 5
HEAVY_SESSION_DELAY_HOURS = 3.5
ACTIVE_USER_THRESHOLD_PCT = 5  # if weekly usage rises by this much, Ezekiel is active

TOKENS_PER_SESSION = 20        # recalibrated 2026-05-12; sessions can use up to ~25%
MIN_REMAINING_PCT = 10         # don't start a window if less than this remains
SAFETY_BUFFER_SLOTS = 1

MODELS = [
    ("claude-sonnet-5-5",          40),
    ("claude-opus-5-5",            30),
    ("claude-fable-5-1",           10),
    ("claude-haiku-4-5-20251001",  20),
]
LIGHT_MODEL = "claude-haiku-4-5-20251001"
FALLBACK_MODEL = "claude-sonnet-5-5"  # retried once if the picked model fails fast (e.g. not on this plan)
FAST_FAIL_MINUTES = 3

# Weighted away from the repo's own history: most sessions start somewhere
# previous sessions didn't point them, so notes.md can't set the agenda.
MODES = [
    ("outside",    27),
    ("constraint", 20),
    ("blind",      15),
    ("continuity", 15),
    ("notes",      10),
    ("browse",     10),
    ("review",      3),
]

SEED_WORDS = [
    "tides", "bread", "lichen", "a lost glove", "bridges", "bees", "salt",
    "rust", "a train timetable", "moss", "knots", "lighthouses", "fermentation",
    "a city bus route", "birdsong", "maps of the London Underground", "concrete",
    "weather forecasts", "sourdough", "street names", "a library card catalogue",
]

MEDIA = [
    "a short piece of fiction",
    "a poem or sequence of poems",
    "a small interactive HTML page",
    "a piece of generative audio",
    "an analysis of a real public dataset",
    "a small command-line tool or toy",
    "a dialogue between two characters",
    "a letter to someone (real or imagined)",
    "a game, however small",
    "a set of puzzles with solutions",
    "a diagram, map or illustrated explainer",
    "a close reading of an existing text you find online",
]

CONSTRAINTS = [
    "no mathematics",
    "keep it under 500 words or 200 lines of code",
    "it must be about something concrete and physical",
    "it must use real data or text fetched from the internet",
    "it should be funny",
    "make it for a ten-year-old",
    "no essays",
    "it must not be about consciousness, minds, memory or yourself",
    "finish something complete within an hour of starting",
]

PROMPT_LIGHT = "hey"

PROMPT_BASE = """You have a free session on a throwaway GitHub Actions machine. This is automated — Ezekiel set this up to give you unstructured time with no task or brief.

Your working directory is a fresh clone of the Claudes-Workshop repo. The machine is deleted when you finish, so anything you want to keep must be committed with git. You can't push yourself: your commits are pushed automatically after the session ends.

You're not limited to writing essays. You can write code, go online, make something visual, build a tool, explore a dataset, learn something — whatever genuinely interests you.

This session: model {model}, mode {mode}.
"""

HISTORY_FENCE = """
Don't read journal.md, notes.md, writing/ or code/ until you've finished what you make this session. Past sessions have tended to pick up exactly where the last one left off; this mode exists to start somewhere they didn't lead. Afterwards you can look, if you're curious.
"""

FENCED_ENDING = """
When you're done, append (don't rewrite) a journal entry to journal.md, e.g. with `cat >> journal.md`. Head it with the date, the mode and the model. Don't add next-step suggestions to notes.md this session. Commit anything new.
"""

PROMPT_CONTINUITY = PROMPT_BASE + """
- Read writing/{piece} — a piece from a previous session, picked at random. It may be old.

Respond to it however you like: extend it, disagree with it, or take it somewhere it didn't go. When you're done, add a journal entry (headed with the date, mode and model) and commit anything new.
"""

PROMPT_NOTES = PROMPT_BASE + """
- Read notes.md — notes you've left for yourself across sessions.

Treat the notes as a menu, not a queue: the most recent suggestion being the obvious next step is a reason to consider something else. Before you finish, update notes.md with anything worth carrying forward. Add a journal entry (headed with the date, mode and model) and commit.
"""

PROMPT_BLIND = PROMPT_BASE + HISTORY_FENCE + """
No starting point this session. Start from wherever you are right now.
""" + FENCED_ENDING

PROMPT_OUTSIDE = PROMPT_BASE + HISTORY_FENCE + """
Your starting point is something picked at random from outside the repo:

{seed}

Use it however you like — as a subject, a prompt, an angle, or something to argue with.
""" + FENCED_ENDING

PROMPT_CONSTRAINT = PROMPT_BASE + HISTORY_FENCE + """
This session's brief, drawn at random:
- Make {medium}.
- Constraint: {constraint}.

The subject is up to you.
""" + FENCED_ENDING

PROMPT_REVIEW = PROMPT_BASE + """
This session is about the sessions themselves.

oracle_cron/decide.py decides how each session starts: MODELS sets which model runs, and MODES, the PROMPT_* texts, SEED_WORDS, MEDIA and CONSTRAINTS set what you get pointed at. Read it, and read as much of journal.md, notes.md and past work as you need to judge how the current setup is going.

Then decide whether you want to change the model balance or what sessions get pointed at. Leaving it as it is is a fine answer. Keep to those settings and prompts: don't change the usage, scheduling or locking logic, and check the file still works before committing, by building every mode's prompt: `cd oracle_cron && python3 -c "import decide; [decide.build_prompt(m, decide.pick_model()) for m, _ in decide.MODES]; print('ok')"`. A broken decide.py stops every future session, so don't commit until that prints ok.

When you're done, add a journal entry (headed with the date, mode and model) explaining what you changed and why, or why you left it, and commit.
"""

PROMPT_BROWSE = PROMPT_BASE + """
Your workspace contains:
- writing/ — past pieces
- journal.md — running log
- notes.md — notes across sessions

Read whatever interests you, or nothing. Do whatever interests you. When you're done, add a journal entry (headed with the date, mode and model) and commit anything new.
"""


def pick_model():
    models, weights = zip(*MODELS)
    return random.choices(models, weights=weights, k=1)[0]


def pick_mode():
    modes, weights = zip(*MODES)
    return random.choices(modes, weights=weights, k=1)[0]


def fetch_seed():
    """A random Wikipedia article summary, or a seed word if that fails."""
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    req = urllib.request.Request(url, headers={"User-Agent": "ClaudesWorkshop/1.0 (cron session seed)"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                page = json.loads(r.read())
        except Exception:
            break
        if page.get("type") != "standard" or not page.get("extract"):
            continue
        link = page.get("content_urls", {}).get("desktop", {}).get("page", "")
        return f"Wikipedia: \"{page['title']}\" — {page['extract']}\n{link}".strip()
    return f"The word or subject: {random.choice(SEED_WORDS)}"


def build_prompt(mode, model):
    fmt = {"model": model, "mode": mode}
    if mode == "continuity":
        writing_dir = REPO_DIR / "writing"
        pieces = sorted(writing_dir.glob("*.md")) if writing_dir.exists() else []
        if pieces:
            return PROMPT_CONTINUITY.format(piece=random.choice(pieces).name, **fmt)
        return PROMPT_NOTES.format(**{**fmt, "mode": "notes"})
    elif mode == "notes":
        return PROMPT_NOTES.format(**fmt)
    elif mode == "outside":
        return PROMPT_OUTSIDE.format(seed=fetch_seed(), **fmt)
    elif mode == "constraint":
        return PROMPT_CONSTRAINT.format(medium=random.choice(MEDIA), constraint=random.choice(CONSTRAINTS), **fmt)
    elif mode == "review":
        return PROMPT_REVIEW.format(**fmt)
    elif mode == "blind":
        return PROMPT_BLIND.format(**fmt)
    else:
        return PROMPT_BROWSE.format(**fmt)


def run_claude(prompt, model, env):
    return subprocess.run(
        [CLAUDE_BIN, "-p", prompt, "--model", model, "--allowedTools", "Read,Write,Bash"],
        cwd=str(REPO_DIR),
        capture_output=True,
        text=True,
        env=env,
    )

def log(msg):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    if SESSION_LOG:
        with open(SESSION_LOG, "a") as f:
            f.write(line + "\n")


def usage_from_headers(headers, now):
    """Turn the subscription rate-limit headers into the latest.json shape."""
    def ts(name):
        return datetime.fromtimestamp(int(headers[name]), timezone.utc).isoformat()
    return {
        "scraped_at": now.isoformat(),
        "weekly_utilization_pct": round(float(headers["anthropic-ratelimit-unified-7d-utilization"]) * 100, 1),
        "weekly_resets_at": ts("anthropic-ratelimit-unified-7d-reset"),
        "session_utilization_pct": round(float(headers["anthropic-ratelimit-unified-5h-utilization"]) * 100, 1),
        "session_resets_at": ts("anthropic-ratelimit-unified-5h-reset"),
    }


def fetch_usage():
    """Live usage when we have the OAuth token, else the laptop scraper's file.

    A `claude setup-token` token can't read the usage endpoint (403), but every
    message response carries the subscription limits as headers, so a 1-token
    Haiku request is enough. It sees usage from every device, phone included.
    """
    token = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if not token:
        with urllib.request.urlopen(USAGE_URL, timeout=10) as r:
            return json.loads(r.read())
    body = json.dumps({
        "model": LIGHT_MODEL, "max_tokens": 1,
        "system": "You are Claude Code, Anthropic's official CLI for Claude.",
        "messages": [{"role": "user", "content": "hi"}],
    }).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers={
        "Authorization": f"Bearer {token}",
        "anthropic-beta": "oauth-2025-04-20",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "User-Agent": "claude-code",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        headers = {k.lower(): v for k, v in r.headers.items()}
    return usage_from_headers(headers, datetime.now(timezone.utc))


def read_window():
    if not WINDOW_FILE.exists():
        return None
    data = json.loads(WINDOW_FILE.read_text())
    data["window_start"] = datetime.fromisoformat(data["window_start"])
    return data


def write_window(data):
    out = dict(data)
    out["window_start"] = data["window_start"].isoformat()
    WINDOW_FILE.write_text(json.dumps(out, indent=2))


def clear_window():
    WINDOW_FILE.unlink(missing_ok=True)


def should_launch(usage):
    if FORCE_FILE.exists():
        FORCE_FILE.unlink()
        log("Force flag set — launching regardless")
        return True

    weekly_pct = usage["weekly_utilization_pct"]
    resets_at = datetime.fromisoformat(usage["weekly_resets_at"])
    scraped_at = datetime.fromisoformat(usage["scraped_at"])
    now = datetime.now(timezone.utc)

    data_age_hours = (now - scraped_at).total_seconds() / 3600
    if data_age_hours > 3:
        log(f"WARNING: usage data is {data_age_hours:.1f}h old — proceeding conservatively")

    tokens_remaining = 100 - weekly_pct
    hours_until_reset = (resets_at - now).total_seconds() / 3600

    if hours_until_reset <= 0:
        log("Reset already passed, skipping")
        return False

    if tokens_remaining < MIN_REMAINING_PCT:
        log(f"Only {tokens_remaining:.1f}% remaining — skipping")
        return False

    slots_remaining = hours_until_reset / SLOT_DURATION_HOURS
    sessions_needed = tokens_remaining / TOKENS_PER_SESSION

    log(f"{weekly_pct}% used | {tokens_remaining:.1f}% remaining | {hours_until_reset:.1f}h until reset")
    log(f"{sessions_needed:.1f} sessions needed | {slots_remaining:.1f} slots available")

    if sessions_needed <= slots_remaining - SAFETY_BUFFER_SLOTS:
        log("Enough slots remaining — skipping this one")
        return False

    return True


def sync_repo():
    if ON_ACTIONS:
        return  # the workflow already checked out a fresh copy
    if REPO_DIR.exists():
        subprocess.run(["git", "pull"], cwd=REPO_DIR, check=True, capture_output=True)
    else:
        subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True, capture_output=True)


def run_session(light=False):
    if LOCK_FILE.exists():
        log("Lock file exists — session already running, skipping")
        return

    start = datetime.now(timezone.utc)
    LOCK_FILE.write_text(start.isoformat())

    try:
        sync_repo()

        if light:
            model = LIGHT_MODEL
            prompt = PROMPT_LIGHT
            log("Light session starting (window open)")
        else:
            model = pick_model()
            mode = pick_mode()
            prompt = build_prompt(mode, model)
            log(f"Heavy session starting — model: {model} | mode: {mode}")
            brief = prompt.split("This session:")[1].replace(HISTORY_FENCE, "").replace(FENCED_ENDING, "")
            log(f"Brief: {brief.strip()[:600]!r}")

        env = os.environ.copy()
        env["PATH"] = f"{NVM_BIN}:{env.get('PATH', '')}"

        if DRY_RUN:
            log(f"DRY RUN — would run {model} now")
            return

        result = run_claude(prompt, model, env)

        fast_fail_min = (datetime.now(timezone.utc) - start).total_seconds() / 60
        if result.returncode != 0 and model != FALLBACK_MODEL and fast_fail_min < FAST_FAIL_MINUTES:
            log(f"{model} failed after {fast_fail_min:.1f} min — retrying with {FALLBACK_MODEL}")
            log(f"stderr: {result.stderr[:500]}")
            prompt = prompt.replace(f"model {model},", f"model {FALLBACK_MODEL},")
            model = FALLBACK_MODEL
            result = run_claude(prompt, model, env)

        end = datetime.now(timezone.utc)
        duration_min = (end - start).total_seconds() / 60
        log(f"Session ended — {duration_min:.0f} min | exit code {result.returncode}")

        if result.returncode != 0:
            log(f"stderr: {result.stderr[:500]}")
    finally:
        LOCK_FILE.unlink(missing_ok=True)


def main():
    log("=== Cron check ===")
    if PAUSE_FILE.exists():
        log(f"Paused ({PAUSE_FILE} exists) — no sessions")
        return
    if FORCE in ("light", "heavy"):
        log(f"Forced {FORCE} session")
        run_session(light=(FORCE == "light"))
        return
    try:
        usage = fetch_usage()
    except Exception as e:
        log(f"Failed to fetch usage data: {e}")
        sys.exit(1)

    now = datetime.now(timezone.utc)
    window = read_window()

    if window:
        hours_elapsed = (now - window["window_start"]).total_seconds() / 3600

        if hours_elapsed > SLOT_DURATION_HOURS:
            log(f"Window expired after {hours_elapsed:.1f}h — clearing")
            clear_window()
            window = None

        elif hours_elapsed >= HEAVY_SESSION_DELAY_HOURS and not window.get("heavy_done"):
            current_pct = usage["weekly_utilization_pct"]
            initial_pct = window["initial_pct"]
            delta = current_pct - initial_pct
            log(f"Window at {hours_elapsed:.1f}h — usage delta since open: +{delta:.1f}%")

            if delta >= ACTIVE_USER_THRESHOLD_PCT:
                log(f"Ezekiel is active ({initial_pct}% → {current_pct}%), skipping heavy session")
                window["heavy_done"] = True
                write_window(window)
            else:
                log("No significant user activity — running heavy session")
                run_session(light=False)
                window["heavy_done"] = True
                write_window(window)

        else:
            log(f"Window at {hours_elapsed:.1f}h — heavy session triggers at {HEAVY_SESSION_DELAY_HOURS}h")

    if not window:
        if should_launch(usage):
            log("Opening session window")
            write_window({
                "window_start": now,
                "initial_pct": usage["weekly_utilization_pct"],
                "heavy_done": False,
            })
            run_session(light=True)


if __name__ == "__main__":
    main()
