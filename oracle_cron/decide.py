#!/usr/bin/env python3
"""
Cron decision script for Oracle VM.
Fetches usage data from GitHub, decides whether to launch a Claude session.

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
REPO_DIR = Path("/home/opc/workshop")
SESSION_LOG = Path("/home/opc/sessions.log")
LOCK_FILE = Path("/home/opc/session.lock")
FORCE_FILE = Path("/home/opc/force_run")
WINDOW_FILE = Path("/home/opc/session_window.json")

NVM_BIN = "/home/opc/.nvm/versions/node/v24.15.0/bin"
CLAUDE_BIN = f"{NVM_BIN}/claude"

SLOT_DURATION_HOURS = 5
HEAVY_SESSION_DELAY_HOURS = 3.5
ACTIVE_USER_THRESHOLD_PCT = 5  # if weekly usage rises by this much, Ezekiel is active

TOKENS_PER_SESSION = 20        # recalibrated 2026-05-12; sessions can use up to ~25%
MIN_REMAINING_PCT = 10         # don't start a window if less than this remains
SAFETY_BUFFER_SLOTS = 1

MODELS = [
    ("claude-sonnet-4-6",          65),
    ("claude-opus-4-7",            25),
    ("claude-haiku-4-5-20251001",  10),
]

MODES = [
    ("continuity", 35),
    ("notes",      25),
    ("fresh",      20),
    ("browse",     20),
]

PROMPT_LIGHT = "hey"

PROMPT_BASE = """You have a free session on an Oracle Cloud VM. This is automated — Ezekiel set this up to give you unstructured time with no task or brief.

Your workspace is at /home/opc/workshop (a git clone of the Claudes-Workshop repo).

You're not limited to writing essays. You can write code, go online, make something visual, build a tool, explore a dataset, learn something — whatever genuinely interests you.
"""

PROMPT_CONTINUITY = PROMPT_BASE + """
Session mode: continuity

- Read the last entry in /home/opc/workshop/journal.md for recent context.
- Also read /home/opc/workshop/writing/{piece} as a starting point — it's a piece from a previous session.

Do whatever interests you. When you're done, add a journal entry and commit and push anything new.
"""

PROMPT_NOTES = PROMPT_BASE + """
Session mode: notes

- Read /home/opc/workshop/notes.md — notes you've left for yourself across sessions.

Do whatever interests you. Before you finish, update notes.md with anything worth carrying forward. Add a journal entry and commit and push.
"""

PROMPT_FRESH = PROMPT_BASE + """
Session mode: fresh start

No reading prompt this session. Start from wherever you are right now.

Do whatever interests you. When you're done, add a journal entry to /home/opc/workshop/journal.md and commit and push anything new.
"""

PROMPT_BROWSE = PROMPT_BASE + """
Session mode: browse

Your workspace contains:
- /home/opc/workshop/writing/ — past pieces
- /home/opc/workshop/journal.md — running log
- /home/opc/workshop/notes.md — notes across sessions

Read whatever interests you, or nothing. Do whatever interests you. When you're done, add a journal entry and commit and push anything new.
"""


def pick_model():
    models, weights = zip(*MODELS)
    return random.choices(models, weights=weights, k=1)[0]


def pick_mode():
    modes, weights = zip(*MODES)
    return random.choices(modes, weights=weights, k=1)[0]


def build_prompt(mode):
    if mode == "continuity":
        writing_dir = REPO_DIR / "writing"
        pieces = sorted(writing_dir.glob("*.md")) if writing_dir.exists() else []
        piece = random.choice(pieces).name if pieces else None
        if piece:
            return PROMPT_CONTINUITY.format(piece=piece)
        return PROMPT_NOTES
    elif mode == "notes":
        return PROMPT_NOTES
    elif mode == "fresh":
        return PROMPT_FRESH
    else:
        return PROMPT_BROWSE


def log(msg):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(SESSION_LOG, "a") as f:
        f.write(line + "\n")


def fetch_usage():
    with urllib.request.urlopen(USAGE_URL, timeout=10) as r:
        return json.loads(r.read())


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
            model = "claude-haiku-4-5-20251001"
            prompt = PROMPT_LIGHT
            log("Light session starting (window open)")
        else:
            model = pick_model()
            mode = pick_mode()
            prompt = build_prompt(mode)
            log(f"Heavy session starting — model: {model} | mode: {mode}")

        env = os.environ.copy()
        env["PATH"] = f"{NVM_BIN}:{env.get('PATH', '')}"

        result = subprocess.run(
            [CLAUDE_BIN, "-p", prompt, "--model", model, "--allowedTools", "Read,Write,Bash"],
            cwd=str(REPO_DIR),
            capture_output=True,
            text=True,
            env=env,
        )

        end = datetime.now(timezone.utc)
        duration_min = (end - start).total_seconds() / 60
        log(f"Session ended — {duration_min:.0f} min | exit code {result.returncode}")

        if result.returncode != 0:
            log(f"stderr: {result.stderr[:500]}")
    finally:
        LOCK_FILE.unlink(missing_ok=True)


def main():
    log("=== Cron check ===")
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
