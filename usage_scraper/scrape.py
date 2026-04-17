#!/usr/bin/env python3
"""
Usage scraper for claude.ai — captures weekly token usage and writes to
usage_data/latest.json in the repo root.

Modes:
  python scrape.py --setup      Headed browser: log in manually, saves auth state to auth.json
  python scrape.py --discover   Headless: logs all API responses to help locate usage endpoint
  python scrape.py              Normal headless scrape, writes usage_data/latest.json
"""

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
AUTH_FILE = SCRIPT_DIR / "auth.json"
OUTPUT_FILE = REPO_ROOT / "usage_data" / "latest.json"

# The claude.ai endpoint that returns usage data.
# Run --discover to find/confirm this if it stops working.
USAGE_ENDPOINT = "/api/account_usage"  # update if --discover reveals a different path

CLAUDE_URL = "https://claude.ai"
USAGE_URL = "https://claude.ai/settings/usage"


class AuthExpiredError(Exception):
    pass


CHROME_USER_DATA_DIR = r"C:\Users\Ezekiel\AppData\Local\Google\Chrome\User Data"
CHROME_ACCOUNT_EMAIL = "marthasolomon1991@gmail.com"


def _find_chrome_profile() -> str:
    """Find the Chrome profile directory for CHROME_ACCOUNT_EMAIL."""
    user_data = Path(CHROME_USER_DATA_DIR)
    candidates = [user_data / "Default"] + sorted(user_data.glob("Profile *"))
    for profile_dir in candidates:
        prefs_file = profile_dir / "Preferences"
        if not prefs_file.exists():
            continue
        try:
            prefs = json.loads(prefs_file.read_text(encoding="utf-8"))
            account_info = prefs.get("account_info", [])
            for account in account_info:
                if account.get("email", "").lower() == CHROME_ACCOUNT_EMAIL.lower():
                    return str(profile_dir)
        except Exception:
            continue
    raise RuntimeError(
        f"Could not find a Chrome profile for {CHROME_ACCOUNT_EMAIL}.\n"
        f"Profiles checked: {[str(c) for c in candidates]}"
    )


async def setup_auth():
    """
    Saves auth by launching Chrome with your real profile (already logged in).
    Chrome must be fully closed before running this.
    """
    profile_dir = _find_chrome_profile()
    print(f"Using Chrome profile: {profile_dir}")
    print("Make sure Chrome is fully closed, then press Enter to continue...")
    input()
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            profile_dir,
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(USAGE_URL, timeout=30_000)
        print("Page loaded. If you can see the usage page, press Enter to save auth.")
        input()
        await context.storage_state(path=str(AUTH_FILE))
        print(f"Auth saved to {AUTH_FILE}")
        await context.close()


async def discover_endpoints():
    """Navigate to claude.ai and log all API responses — helps identify the usage endpoint."""
    _check_auth_file()
    captured = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(AUTH_FILE))
        page = await context.new_page()

        async def handle_response(response):
            url = response.url
            if "claude.ai/api" in url:
                try:
                    body = await response.json()
                    captured.append({"url": url, "status": response.status, "body": body})
                except Exception:
                    captured.append({"url": url, "status": response.status, "body": None})

        page.on("response", handle_response)

        _check_for_redirect(await _navigate(page, USAGE_URL))

        # Brief wait to let background API calls settle
        await page.wait_for_timeout(3000)
        await browser.close()

    print(f"\nCaptured {len(captured)} API responses:\n")
    for entry in captured:
        print(f"  {entry['status']} {entry['url']}")
        if entry["body"] and isinstance(entry["body"], dict):
            keys = list(entry["body"].keys())
            print(f"       keys: {keys}")
    print("\nLook for an entry with keys like 'tokens_used', 'usage', 'limit', etc.")
    print(f"Then update USAGE_ENDPOINT in {__file__}")


async def scrape():
    """Main scrape — writes usage numbers to usage_data/latest.json."""
    _check_auth_file()

    usage = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(AUTH_FILE))
        page = await context.new_page()

        # Intercept the usage API response
        async def handle_response(response):
            nonlocal usage
            if USAGE_ENDPOINT in response.url and response.status == 200:
                try:
                    usage = await response.json()
                except Exception as e:
                    print(f"Warning: couldn't parse usage response: {e}")

        page.on("response", handle_response)

        _check_for_redirect(await _navigate(page, USAGE_URL))

        # Wait for the usage API call (up to 10s)
        deadline = 10_000
        step = 500
        elapsed = 0
        while usage is None and elapsed < deadline:
            await page.wait_for_timeout(step)
            elapsed += step

        await browser.close()

    if usage is None:
        raise RuntimeError(
            f"Usage data not found. The endpoint '{USAGE_ENDPOINT}' may have changed. "
            "Run with --discover to find the correct endpoint."
        )

    output = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "raw": usage,
    }

    # Try to extract the key numbers into a flat, easy-to-read structure.
    # Update these keys if --discover reveals different field names.
    output["summary"] = _extract_summary(usage)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2))
    print(f"Written to {OUTPUT_FILE}")
    print(f"Summary: {output['summary']}")


def _extract_summary(raw: dict) -> dict:
    """
    Pull key numbers out of the raw API response into a flat dict.
    Fields here are guesses — update after running --discover.
    """
    summary = {}
    # Common field names to probe; extend as needed
    for key in ("tokens_used", "usage", "used", "consumed"):
        if key in raw:
            summary["tokens_used"] = raw[key]
    for key in ("tokens_limit", "limit", "total", "allowance"):
        if key in raw:
            summary["tokens_limit"] = raw[key]
    for key in ("reset_at", "reset_date", "resets_at", "period_end"):
        if key in raw:
            summary["reset_at"] = raw[key]
    return summary


async def _navigate(page, url: str):
    try:
        await page.goto(url, wait_until="networkidle", timeout=30_000)
    except PlaywrightTimeout:
        pass  # networkidle can time out on SPAs; that's fine
    return page.url


def _check_for_redirect(current_url: str):
    if "login" in current_url or "signin" in current_url:
        raise AuthExpiredError(
            "Redirected to login page — auth has expired.\n"
            "Run: python scrape.py --setup"
        )


def _check_auth_file():
    if not AUTH_FILE.exists():
        print(f"No auth file found at {AUTH_FILE}")
        print("Run: python scrape.py --setup")
        sys.exit(1)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    if mode == "--setup":
        asyncio.run(setup_auth())
    elif mode == "--discover":
        asyncio.run(discover_endpoints())
    elif mode is None:
        asyncio.run(scrape())
    else:
        print(f"Unknown argument: {mode}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
