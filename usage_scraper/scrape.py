#!/usr/bin/env python3
"""
Usage scraper for claude.ai — reads Firefox cookies, calls usage API,
writes usage_data/latest.json, commits and pushes to GitHub.

Run on a schedule via Task Scheduler. No browser automation needed.

Usage: python scrape.py
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import browser_cookie3
from curl_cffi import requests

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_FILE = REPO_ROOT / "usage_data" / "latest.json"

USAGE_URL = "https://claude.ai/api/organizations/b49de57b-f2f0-4db3-9f1b-833808b8e371/usage"

_NO_WINDOW = {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}


def scrape():
    cookies = browser_cookie3.firefox(domain_name=".claude.ai")
    cookie_dict = {c.name: c.value for c in cookies}

    response = requests.get(
        USAGE_URL,
        cookies=cookie_dict,
        impersonate="firefox",
        headers={"Referer": "https://claude.ai/"},
    )
    response.raise_for_status()
    raw = response.json()

    seven_day = raw.get("seven_day") or {}
    five_hour = raw.get("five_hour") or {}
    output = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "weekly_utilization_pct": seven_day.get("utilization"),
        "weekly_resets_at": seven_day.get("resets_at"),
        "session_utilization_pct": five_hour.get("utilization"),
        "session_resets_at": five_hour.get("resets_at"),
        "raw": raw,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2))

    _git_commit_and_push()


def _git_commit_and_push():
    def run(cmd):
        subprocess.run(cmd, cwd=REPO_ROOT, check=True, capture_output=True, **_NO_WINDOW)

    run(["git", "add", str(OUTPUT_FILE)])
    changed = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=REPO_ROOT, capture_output=True, **_NO_WINDOW
    ).returncode != 0

    if not changed:
        return

    run(["git", "commit", "-m", f"Update usage data {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"])
    run(["git", "push"])


if __name__ == "__main__":
    scrape()
