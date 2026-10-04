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
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import urllib.request

USAGE_URL = "https://raw.githubusercontent.com/ZiziSolomon/Claudes-Workshop/master/usage_data/latest.json"
REPO_URL = "https://github.com/ZiziSolomon/Claudes-Workshop.git"
ON_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
REPO_DIR = Path(os.environ.get("WORKSHOP_REPO_DIR", "/home/opc/workshop"))
STATE_DIR = Path(os.environ.get("WORKSHOP_STATE_DIR", "/home/opc"))
# On Actions the job log is the session log; nothing else survives the runner.
SESSION_LOG = None if ON_ACTIONS else STATE_DIR / "sessions.log"
PAUSE_FILE = STATE_DIR / "paused"            # exists -> no sessions at all
WINDOW_FILE = STATE_DIR / "session_window.json"
CALIBRATION_FILE = STATE_DIR / "calibration.json"

NVM_BIN = "/home/opc/.nvm/versions/node/v24.15.0/bin"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", f"{NVM_BIN}/claude")
DRY_RUN = os.environ.get("WORKSHOP_DRY_RUN") == "1"   # decide and log, never run claude
FORCE = os.environ.get("WORKSHOP_FORCE", "")           # "light"/"heavy": skip the decision
FORCE_MINUTES = int(os.environ.get("WORKSHOP_FORCE_MINUTES", "10"))  # cap on a forced heavy session

# Flow: when the week is heading for waste, "hey" opens a 5h window. Work starts
# late in the window, timed by calibration so the window's allowance runs out
# just before it resets, and Claude is re-prompted whenever it stops until a
# hard cutoff. Ezekiel's own use gets first claim on every window.
SLOT_DURATION_HOURS = 5
CHECK_INTERVAL_MINUTES = 60    # how often the workflow runs this script
ACTIVE_USER_JUMP_PCT = 5       # 5h usage up this much since the last check = Ezekiel is active
MIN_REMAINING_PCT = 10         # don't open a window if less than this remains of the week
SAFETY_BUFFER_SLOTS = 1
WEEKLY_RESERVE_PCT = 5         # stop re-prompting once weekly usage reaches 100 minus this
CUTOFF_SECONDS = 60            # hard stop this long before the window resets
START_MARGIN = 1.2             # start a little earlier than calibration says
CALIBRATION_N = 5              # recent sessions averaged per rate
DEFAULT_RATE_PCT_PER_MIN = 100 / 120   # until calibrated: a whole window takes ~2h of work
DEFAULT_WEEKLY_PER_WINDOW = 11.0       # weekly % a whole window costs: median of 55 windows, Apr-Sep 2026
MIN_CALL_SECONDS = 30          # failed prompts shorter than this count as "quick"...
MAX_QUICK_CALLS = 3            # ...and this many in a row ends the loop (a broken loop, not a fast model)

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

DEADLINE_NOTE = """
Timing: you have until {deadline} UTC (about {minutes} minutes). Whenever you stop, you'll get a follow-up prompt, so there's no need to wrap up early. At {deadline} the session is cut off without warning, so commit as you go.
"""

CONTINUE_PROMPT = """There's still time: until {deadline} UTC, about {minutes} minutes. Carry on with what you were doing, take it further, or start something new. Your choice. Commit as you go, and add to your journal entry when you finish something."""

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


def run_claude(prompt, model, env, resume=False, timeout=None):
    """One `claude -p` call. resume=True continues the previous conversation.

    On timeout, subprocess.run kills claude and raises TimeoutExpired.
    """
    cmd = [CLAUDE_BIN, "-p", prompt, "--model", model, "--allowedTools", "Read,Write,Bash"]
    if resume:
        cmd.insert(1, "--continue")
    return subprocess.run(cmd, cwd=str(REPO_DIR), capture_output=True, text=True, env=env, timeout=timeout)

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


def to_dt(value):
    return value if isinstance(value, datetime) else datetime.fromisoformat(value)


def read_window():
    if not WINDOW_FILE.exists():
        return None
    data = json.loads(WINDOW_FILE.read_text())
    for key in ("window_start", "window_end"):
        data[key] = to_dt(data[key])
    return data


def write_window(data):
    out = {k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in data.items()}
    WINDOW_FILE.write_text(json.dumps(out, indent=2))


def clear_window():
    WINDOW_FILE.unlink(missing_ok=True)


# ── Calibration ──────────────────────────────────────────────────────────────
# Each heavy session records how many points of the 5h allowance (d5h) and of
# the weekly allowance (d7d) it used, over how many minutes. Rates come from the
# last CALIBRATION_N usable records, so they follow whatever models and prompts
# currently do instead of a hand-set constant going stale.

def load_calibration():
    if not CALIBRATION_FILE.exists():
        return []
    return json.loads(CALIBRATION_FILE.read_text())


def record_calibration(record):
    records = load_calibration() + [record]
    CALIBRATION_FILE.write_text(json.dumps(records[-50:], indent=2))


def rate_for(model, records):
    """Points of the 5h allowance this model uses per minute of work."""
    recs = [r for r in records if r["model"] == model and r["minutes"] >= 5 and r["d5h"] > 0]
    recs = recs[-CALIBRATION_N:]
    if not recs:
        return DEFAULT_RATE_PCT_PER_MIN
    return sum(r["d5h"] for r in recs) / sum(r["minutes"] for r in recs)


def weekly_per_window(records):
    """Weekly % that burning a whole 5h window costs."""
    recs = [r for r in records if r["d5h"] >= 10 and r["d7d"] > 0][-CALIBRATION_N:]
    if not recs:
        return DEFAULT_WEEKLY_PER_WINDOW
    return sum(r["d7d"] for r in recs) / sum(r["d5h"] for r in recs) * 100


# ── Decisions ────────────────────────────────────────────────────────────────

def should_launch(usage, records):
    """Open a window only if the week is heading for waste."""
    weekly_pct = usage["weekly_utilization_pct"]
    resets_at = to_dt(usage["weekly_resets_at"])
    now = datetime.now(timezone.utc)

    tokens_remaining = 100 - weekly_pct
    hours_until_reset = (resets_at - now).total_seconds() / 3600

    if hours_until_reset <= 0:
        log("Reset already passed, skipping")
        return False

    if tokens_remaining < MIN_REMAINING_PCT:
        log(f"Only {tokens_remaining:.1f}% remaining — skipping")
        return False

    per_window = weekly_per_window(records)
    slots_remaining = hours_until_reset / SLOT_DURATION_HOURS
    sessions_needed = tokens_remaining / per_window

    log(f"{weekly_pct}% used | {tokens_remaining:.1f}% remaining | {hours_until_reset:.1f}h until reset")
    log(f"{sessions_needed:.1f} windows needed at {per_window:.1f}%/window | {slots_remaining:.1f} slots available")

    if sessions_needed <= slots_remaining - SAFETY_BUFFER_SLOTS:
        log("Enough slots remaining — skipping this one")
        return False

    return True


def work_start(window, usage, records):
    """When to start prompting so the window's allowance runs out at the cutoff."""
    remaining_5h = max(0.0, 100 - usage["session_utilization_pct"])
    minutes = remaining_5h / rate_for(window["model"], records) * START_MARGIN
    deadline = window["window_end"] - timedelta(seconds=CUTOFF_SECONDS)
    return deadline - timedelta(minutes=minutes), minutes


def sync_repo():
    if ON_ACTIONS:
        return  # the workflow already checked out a fresh copy
    if REPO_DIR.exists():
        subprocess.run(["git", "pull"], cwd=REPO_DIR, check=True, capture_output=True)
    else:
        subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True, capture_output=True)


def claude_env():
    env = os.environ.copy()
    env["PATH"] = f"{NVM_BIN}:{env.get('PATH', '')}"
    return env


def run_light():
    """Send "hey" so the 5h window starts now; costs next to nothing."""
    log("Light session starting (opens the 5h window)")
    if DRY_RUN:
        log(f"DRY RUN — would run {LIGHT_MODEL} now")
        return
    result = run_claude(PROMPT_LIGHT, LIGHT_MODEL, claude_env())
    log(f"Light session exit code {result.returncode}")


def commit_leftovers():
    """The cutoff can land mid-task: keep whatever the session hadn't committed."""
    subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, capture_output=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_DIR).returncode != 0
    if staged:
        subprocess.run(["git", "commit", "-q", "-m", "Session cut off: work left uncommitted at the deadline"],
                       cwd=REPO_DIR, capture_output=True)
        log("Committed work the session left uncommitted")


def hit_limit(result):
    text = (result.stdout + result.stderr).lower()
    return result.returncode != 0 and "limit" in text


def work_loop(window, deadline):
    """Prompt, and re-prompt whenever Claude stops, until the deadline or a limit."""
    model = window["model"]
    mode = pick_mode()
    sync_repo()
    env = claude_env()

    def timing():
        mins = max(0, int((deadline - datetime.now(timezone.utc)).total_seconds() / 60))
        return {"deadline": deadline.strftime("%H:%M"), "minutes": mins}

    first_prompt = build_prompt(mode, model) + DEADLINE_NOTE.format(**timing())
    log(f"Work loop starting — model: {model} | mode: {mode} | deadline {deadline:%H:%M} UTC")
    brief = first_prompt.split("This session:")[1].replace(HISTORY_FENCE, "").replace(FENCED_ENDING, "")
    log(f"Brief: {brief.strip()[:600]!r}")
    if DRY_RUN:
        log(f"DRY RUN — would run {model} until {deadline:%H:%M} UTC")
        return

    before = fetch_usage()
    start = datetime.now(timezone.utc)
    first, quick_calls, prompts = True, 0, 0

    while True:
        seconds_left = (deadline - datetime.now(timezone.utc)).total_seconds()
        if seconds_left < 60:
            log("Deadline reached")
            break
        if not first:
            now_usage = fetch_usage()
            if now_usage["weekly_utilization_pct"] >= 100 - WEEKLY_RESERVE_PCT:
                log(f"Weekly at {now_usage['weekly_utilization_pct']}% — keeping the reserve, stopping")
                break
            if now_usage["session_utilization_pct"] >= 99.5:
                log("5h allowance used up — stopping")
                break

        prompt = first_prompt if first else CONTINUE_PROMPT.format(**timing())
        call_start = datetime.now(timezone.utc)
        try:
            result = run_claude(prompt, model, env, resume=not first, timeout=seconds_left)
        except subprocess.TimeoutExpired:
            log("Cut off at the deadline")
            break
        prompts += 1
        call_secs = (datetime.now(timezone.utc) - call_start).total_seconds()
        log(f"Prompt {prompts} done in {call_secs / 60:.1f} min | exit {result.returncode} | "
            f"reply: {result.stdout[-500:]!r}")

        if first and result.returncode != 0 and model != FALLBACK_MODEL and call_secs < FAST_FAIL_MINUTES * 60:
            log(f"{model} failed fast — retrying with {FALLBACK_MODEL}. stderr: {result.stderr[:300]}")
            first_prompt = first_prompt.replace(f"model {model},", f"model {FALLBACK_MODEL},")
            model = FALLBACK_MODEL
            continue
        if hit_limit(result):
            log("Usage limit reached — stopping")
            break

        # Guard against a broken loop (e.g. every call erroring instantly).
        # Successful quick replies are fine (Opus often finishes a step in 20s).
        failed_fast = result.returncode != 0 and call_secs < MIN_CALL_SECONDS
        quick_calls = quick_calls + 1 if failed_fast else 0
        if quick_calls >= MAX_QUICK_CALLS:
            log(f"{MAX_QUICK_CALLS} prompts in a row failed within {MIN_CALL_SECONDS}s — stopping")
            break
        first = False

    commit_leftovers()
    after = fetch_usage()
    minutes = (datetime.now(timezone.utc) - start).total_seconds() / 60
    record = {
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "model": model, "mode": mode, "prompts": prompts, "minutes": round(minutes, 1),
        "d5h": round(after["session_utilization_pct"] - before["session_utilization_pct"], 1),
        "d7d": round(after["weekly_utilization_pct"] - before["weekly_utilization_pct"], 1),
    }
    record_calibration(record)
    log(f"Work loop ended: {record}")


def handle_window(window, usage, records):
    now = datetime.now(timezone.utc)
    jump = usage["session_utilization_pct"] - window.get("last_session_pct", usage["session_utilization_pct"])
    window["last_session_pct"] = usage["session_utilization_pct"]
    if jump >= ACTIVE_USER_JUMP_PCT:
        log(f"5h usage rose {jump:.1f} points in the last hour — Ezekiel is active, leaving this window alone")
        window["heavy_done"] = True
        write_window(window)
        return

    start, minutes = work_start(window, usage, records)
    log(f"Window ends {window['window_end']:%H:%M} UTC | {usage['session_utilization_pct']}% of 5h used | "
        f"{window['model']} needs ~{minutes:.0f} min | work starts {start:%H:%M} UTC")
    if start > now + timedelta(minutes=CHECK_INTERVAL_MINUTES):
        write_window(window)
        return  # a later hourly check will catch it

    wait = (start - now).total_seconds()
    window["heavy_done"] = True  # saved first, so a crash can't make the next run repeat it
    write_window(window)
    if wait > 0:
        log(f"Waiting {wait / 60:.0f} min until the start time")
        if not DRY_RUN:
            time.sleep(wait)
    work_loop(window, window["window_end"] - timedelta(seconds=CUTOFF_SECONDS))


def main():
    log("=== Check ===")
    if PAUSE_FILE.exists():
        log(f"Paused ({PAUSE_FILE} exists) — no sessions")
        return

    usage = fetch_usage()
    records = load_calibration()
    now = datetime.now(timezone.utc)

    if FORCE == "light":
        run_light()
        return
    if FORCE == "heavy":
        # Test the work loop now, capped at FORCE_MINUTES, inside the current 5h window.
        window = {"model": pick_model(), "window_start": now,
                  "window_end": to_dt(usage["session_resets_at"])}
        deadline = min(window["window_end"] - timedelta(seconds=CUTOFF_SECONDS),
                       now + timedelta(minutes=FORCE_MINUTES))
        log(f"Forced heavy session, capped at {FORCE_MINUTES} min")
        work_loop(window, deadline)
        return

    window = read_window()
    if window and now >= window["window_end"]:
        log("Window over — clearing")
        clear_window()
        window = None

    if window:
        if window.get("heavy_done"):
            log(f"Window open until {window['window_end']:%H:%M} UTC; its work is done")
        else:
            handle_window(window, usage, records)
        return

    if should_launch(usage, records):
        run_light()
        usage = fetch_usage()
        window = {
            "window_start": now,
            "window_end": to_dt(usage["session_resets_at"]),
            "model": pick_model(),
            "heavy_done": False,
            "last_session_pct": usage["session_utilization_pct"],
        }
        write_window(window)
        log(f"Window open until {window['window_end']:%H:%M} UTC; model {window['model']}")
        handle_window(window, usage, records)


if __name__ == "__main__":
    main()
