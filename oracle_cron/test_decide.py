"""Tests for decide.py's scheduling logic. Run: python -m unittest oracle_cron/test_decide.py"""
import importlib
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))

# Real headers from the usage probe run on 2026-10-04.
HEADERS = {
    "anthropic-ratelimit-unified-5h-reset": "1791121200",
    "anthropic-ratelimit-unified-5h-utilization": "0.29",
    "anthropic-ratelimit-unified-7d-reset": "1791471600",
    "anthropic-ratelimit-unified-7d-utilization": "0.04",
}


def usage(weekly_pct, hours_to_reset):
    now = datetime.now(timezone.utc)
    return {
        "scraped_at": now.isoformat(),
        "weekly_utilization_pct": weekly_pct,
        "weekly_resets_at": (now + timedelta(hours=hours_to_reset)).isoformat(),
    }


class DecideTest(unittest.TestCase):
    def setUp(self):
        self.state = tempfile.TemporaryDirectory()
        env = {"GITHUB_ACTIONS": "true", "WORKSHOP_STATE_DIR": self.state.name,
               "WORKSHOP_REPO_DIR": self.state.name, "WORKSHOP_DRY_RUN": "1",
               "WORKSHOP_FORCE": ""}
        self.env = mock.patch.dict(os.environ, env)
        self.env.start()
        import decide
        self.d = importlib.reload(decide)  # module reads env at import time
        # Never call the real API or claude from tests.
        self.run_claude = mock.patch.object(self.d, "run_claude").start()

    def tearDown(self):
        mock.patch.stopall()
        self.env.stop()
        self.state.cleanup()

    def test_headers_become_latest_json_shape(self):
        u = self.d.usage_from_headers(HEADERS, datetime(2026, 10, 4, tzinfo=timezone.utc))
        self.assertEqual(u["weekly_utilization_pct"], 4.0)
        self.assertEqual(u["session_utilization_pct"], 29.0)
        self.assertEqual(u["weekly_resets_at"], "2026-10-08T15:00:00+00:00")
        self.assertEqual(u["session_resets_at"], "2026-10-04T13:40:00+00:00")

    def test_pause_file_stops_everything_before_fetching_usage(self):
        Path(self.state.name, "paused").touch()
        with mock.patch.object(self.d, "fetch_usage") as fetch:
            self.d.main()
        fetch.assert_not_called()

    def test_skips_when_plenty_of_slots_left(self):
        self.assertFalse(self.d.should_launch(usage(4, 96)))

    def test_launches_when_behind_schedule(self):
        self.assertTrue(self.d.should_launch(usage(4, 10)))

    def test_skips_when_almost_nothing_left(self):
        self.assertFalse(self.d.should_launch(usage(95, 10)))

    def test_dry_run_never_runs_claude(self):
        with mock.patch.dict(os.environ, {"WORKSHOP_FORCE": "heavy"}):
            importlib.reload(self.d)
            run_claude = mock.patch.object(self.d, "run_claude").start()
            self.d.main()
        run_claude.assert_not_called()

    def test_window_opens_then_heavy_runs_if_user_idle(self):
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(4, 10)):
            self.d.main()
        window = json.loads(Path(self.state.name, "session_window.json").read_text())
        self.assertFalse(window["heavy_done"])

        # 3.6h later, usage barely moved -> heavy session, window marked done.
        window["window_start"] = (datetime.now(timezone.utc) - timedelta(hours=3.6)).isoformat()
        Path(self.state.name, "session_window.json").write_text(json.dumps(window))
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(5, 6.4)), \
             mock.patch.object(self.d, "run_session") as run:
            self.d.main()
        run.assert_called_once_with(light=False)
        window = json.loads(Path(self.state.name, "session_window.json").read_text())
        self.assertTrue(window["heavy_done"])

    def test_heavy_skipped_if_user_active(self):
        start = datetime.now(timezone.utc) - timedelta(hours=3.6)
        Path(self.state.name, "session_window.json").write_text(json.dumps(
            {"window_start": start.isoformat(), "initial_pct": 4, "heavy_done": False}))
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(12, 6.4)), \
             mock.patch.object(self.d, "run_session") as run:
            self.d.main()
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
