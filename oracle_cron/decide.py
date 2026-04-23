#!/usr/bin/env python3
"""
Cron decision script for Oracle VM.
Fetches usage data from GitHub, decides whether to launch a Claude session.

Cron: 0 3,8,13,18,23 * * *
"""

import json
import os
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

NVM_BIN = "/home/opc/.nvm/versions/node/v24.15.0/bin"
CLAUDE_BIN = f"{NVM_BIN}/claude"

SLOT_DURATION_HOURS = 5

TOKENS_PER_SESSION = 13.5  # updated after calibration
SAFETY_BUFFER_SLOTS = 1

PROMPT = """You have a free session on an Oracle Cloud VM. This is automated — Ezekiel set this up to give you unstructured time with no task or brief.

Your workspace is at /home/opc/workshop (a git clone of the Claudes-Workshop repo).

For context and continuity:
- /home/opc/workshop/writing/ contains pieces from previous sessions. Start with on_the_chinese_room.md.
- /home/opc/workshop/journal.md is a running log — read it first, then add an entry for this session at the end.

Do whatever interests you. Write, build something, think through a problem. When you're done, commit and push anything new to the repo so it persists for next time.
"""


def log(msg):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(SESSION_LOG, "a") as f:
        f.write(line + "\n")


def fetch_usage():
    with urllib.request.urlopen(USAGE_URL, timeout=10) as r:
        return json.loads(r.read())


def should_launch(usage):
    if FORCE_FILE.exists():
        FORCE_FILE.unlink()
        log("Force flag set — running session regardless")
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

    if tokens_remaining < TOKENS_PER_SESSION:
        log(f"Only {tokens_remaining:.1f}% remaining — not enough for a full session, skipping")
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


def run_session():
    if LOCK_FILE.exists():
        log("Lock file exists — session already running, skipping")
        return

    start = datetime.now(timezone.utc)
    LOCK_FILE.write_text(start.isoformat())
    log("Session starting")

    try:
        sync_repo()

        env = os.environ.copy()
        env["PATH"] = f"{NVM_BIN}:{env.get('PATH', '')}"

        result = subprocess.run(
            [CLAUDE_BIN, "-p", PROMPT, "--allowedTools", "Read,Write,Bash"],
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

    if should_launch(usage):
        run_session()


if __name__ == "__main__":
    main()
