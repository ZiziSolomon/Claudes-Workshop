#!/usr/bin/env python3
"""
Local HTTP server that receives usage data POSTed by the Chrome extension
and writes it to usage_data/latest.json, then commits + pushes to GitHub.

Run this on login via Task Scheduler. It stays alive indefinitely.
Usage: python server.py
"""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Suppress console windows for subprocesses on Windows
_NO_WINDOW = {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}

LOG_FILE = Path(__file__).parent / "server.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


def _run(cmd):
    subprocess.run(cmd, cwd=REPO_ROOT, check=True, capture_output=True, **_NO_WINDOW)

PORT = 7432
REPO_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = REPO_ROOT / "usage_data" / "latest.json"


class Handler(BaseHTTPRequestHandler):
    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "https://claude.ai")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path != "/usage":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError as e:
            log.error(f"Bad JSON: {e}")
            self.send_response(400)
            self.end_headers()
            return

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
        log.info(f"Usage data written to {OUTPUT_FILE}")

        _git_commit_and_push()

        self.send_response(200)
        self._cors_headers()
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format, *args):
        pass  # suppress default access log noise


def _git_commit_and_push():
    try:
        _run(["git", "add", str(OUTPUT_FILE)])
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO_ROOT, capture_output=True, **_NO_WINDOW
        )
        if result.returncode == 0:
            log.info("No changes to commit.")
            return
        _run(["git", "commit", "-m", f"Update usage data {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"])
        _run(["git", "push"])
        log.info("Committed and pushed.")
    except subprocess.CalledProcessError as e:
        log.error(f"Git error: {e.stderr.decode().strip()}")


if __name__ == "__main__":
    log.info(f"Starting — listening on http://localhost:{PORT}")
    log.info(f"Writing to: {OUTPUT_FILE}")
    try:
        HTTPServer(("localhost", PORT), Handler).serve_forever()
    except Exception as e:
        log.exception(f"Server crashed: {e}")
