"""Tests for decide.py's scheduling logic. Run: python -m unittest oracle_cron/test_decide.py"""
import importlib
import json
import os
import subprocess
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


def now():
    return datetime.now(timezone.utc)


def usage(weekly=4, hours_to_reset=96, session=0, window_mins_left=300):
    return {
        "scraped_at": now().isoformat(),
        "weekly_utilization_pct": weekly,
        "weekly_resets_at": (now() + timedelta(hours=hours_to_reset)).isoformat(),
        "session_utilization_pct": session,
        "session_resets_at": (now() + timedelta(minutes=window_mins_left)).isoformat(),
    }


def done(returncode=0, stdout="ok", stderr=""):
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


class Base(unittest.TestCase):
    extra_env = {}

    def setUp(self):
        self.state = tempfile.TemporaryDirectory()
        self.dir = Path(self.state.name)
        env = {"GITHUB_ACTIONS": "true", "WORKSHOP_STATE_DIR": self.state.name,
               "WORKSHOP_REPO_DIR": self.state.name, "WORKSHOP_DRY_RUN": "",
               "WORKSHOP_FORCE": "", **self.extra_env}
        self.env = mock.patch.dict(os.environ, env)
        self.env.start()
        import decide
        self.d = importlib.reload(decide)  # module reads env at import time
        # Never touch the real API, claude, git or the clock's sleep from tests.
        self.run_claude = mock.patch.object(self.d, "run_claude", return_value=done()).start()
        self.sleep = mock.patch.object(self.d.time, "sleep").start()
        mock.patch.object(self.d, "commit_leftovers").start()
        mock.patch.object(self.d, "fetch_seed", return_value="seed").start()

    def tearDown(self):
        mock.patch.stopall()
        self.env.stop()
        self.state.cleanup()

    def window(self, mins_left=300, model="claude-sonnet-5-5", **kw):
        w = {"window_start": now(), "window_end": now() + timedelta(minutes=mins_left),
             "model": model, "heavy_done": False, "last_session_pct": 0, **kw}
        self.d.write_window(w)
        return self.d.read_window()


class Headers(Base):
    def test_headers_become_usage_shape(self):
        u = self.d.usage_from_headers(HEADERS, datetime(2026, 10, 4, tzinfo=timezone.utc))
        self.assertEqual(u["weekly_utilization_pct"], 4.0)
        self.assertEqual(u["session_utilization_pct"], 29.0)
        self.assertEqual(u["weekly_resets_at"], "2026-10-08T15:00:00+00:00")
        self.assertEqual(u["session_resets_at"], "2026-10-04T13:40:00+00:00")


class Calibration(Base):
    def test_defaults_without_data(self):
        self.assertAlmostEqual(self.d.rate_for("m", []), 100 / 120)
        self.assertEqual(self.d.weekly_per_window([]), 13.5)

    def test_rate_is_per_model_and_uses_recent_sessions(self):
        recs = [{"model": "a", "minutes": 60, "d5h": 30, "d7d": 4},
                {"model": "a", "minutes": 60, "d5h": 50, "d7d": 6},
                {"model": "b", "minutes": 10, "d5h": 50, "d7d": 6},
                {"model": "a", "minutes": 2, "d5h": 40, "d7d": 5}]   # too short to trust
        self.assertAlmostEqual(self.d.rate_for("a", recs), 80 / 120)
        self.assertAlmostEqual(self.d.rate_for("b", recs), 5.0)
        self.assertAlmostEqual(self.d.weekly_per_window(recs), 21 / 170 * 100)

    def test_work_start_leaves_time_to_burn_the_rest(self):
        w = self.window(mins_left=300)
        start, minutes = self.d.work_start(w, usage(session=40), [])
        self.assertAlmostEqual(minutes, 60 / (100 / 120) * 1.2)       # 86.4
        expected = w["window_end"] - timedelta(seconds=60) - timedelta(minutes=minutes)
        self.assertEqual(start, expected)


class Decisions(Base):
    def test_pause_stops_before_fetching_usage(self):
        (self.dir / "paused").touch()
        with mock.patch.object(self.d, "fetch_usage") as fetch:
            self.d.main()
        fetch.assert_not_called()

    def test_should_launch(self):
        self.assertFalse(self.d.should_launch(usage(weekly=4, hours_to_reset=96), []))
        self.assertTrue(self.d.should_launch(usage(weekly=4, hours_to_reset=10), []))
        self.assertFalse(self.d.should_launch(usage(weekly=95, hours_to_reset=10), []))

    def test_opens_window_with_light_session_and_stored_model(self):
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(hours_to_reset=10)):
            self.d.main()
        self.run_claude.assert_called_once()
        self.assertEqual(self.run_claude.call_args.args[0], "hey")
        w = self.d.read_window()
        self.assertIn(w["model"], [m for m, _ in self.d.MODELS])
        self.assertFalse(w["heavy_done"])   # 5h left, ~2.4h needed: not yet

    def test_window_waits_when_start_is_far_off(self):
        self.window(mins_left=290)
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(window_mins_left=290)), \
             mock.patch.object(self.d, "work_loop") as loop:
            self.d.main()
        loop.assert_not_called()

    def test_window_sleeps_to_exact_start_then_works(self):
        w = self.window(mins_left=180)    # needs ~144 min: start is ~35 min away
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(window_mins_left=180)), \
             mock.patch.object(self.d, "work_loop") as loop:
            self.d.main()
        loop.assert_called_once()
        slept = self.sleep.call_args.args[0]
        self.assertAlmostEqual(slept / 60, 180 - 1 - 144, delta=1)
        self.assertTrue(self.d.read_window()["heavy_done"])
        deadline = loop.call_args.args[1]
        self.assertEqual(deadline, w["window_end"] - timedelta(seconds=60))

    def test_skips_window_if_ezekiel_is_active(self):
        self.window(mins_left=180, last_session_pct=10)
        with mock.patch.object(self.d, "fetch_usage", return_value=usage(session=20, window_mins_left=180)), \
             mock.patch.object(self.d, "work_loop") as loop:
            self.d.main()
        loop.assert_not_called()
        self.assertTrue(self.d.read_window()["heavy_done"])

    def test_expired_window_is_cleared(self):
        self.window(mins_left=-1)
        with mock.patch.object(self.d, "fetch_usage", return_value=usage()):
            self.d.main()
        self.assertIsNone(self.d.read_window())


class WorkLoop(Base):
    def loop(self, results, mins=30, usages=None, model="claude-sonnet-5-5"):
        self.run_claude.side_effect = results
        fetch = mock.patch.object(self.d, "fetch_usage",
                                  side_effect=usages or [usage(session=s) for s in range(0, 200, 5)]).start()
        w = {"model": model}
        clock = [now()]
        # Each claude call "takes" 10 minutes of fake time.
        def fake_now(tz=None):
            return clock[0]
        def advance(*a, **k):
            clock[0] += timedelta(minutes=10)
            r = results.pop(0)
            if isinstance(r, Exception):
                raise r
            return r
        self.run_claude.side_effect = advance
        dt = mock.patch.object(self.d, "datetime", wraps=datetime).start()
        dt.now.side_effect = fake_now
        self.d.work_loop(w, clock[0] + timedelta(minutes=mins))
        return fetch

    def test_reprompts_with_continue_until_cutoff(self):
        self.loop([done(), done(), subprocess.TimeoutExpired("claude", 1)], mins=30)
        calls = self.run_claude.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertFalse(calls[0].kwargs["resume"])
        self.assertTrue(calls[1].kwargs["resume"])
        self.assertIn("There's still time", calls[1].args[0])
        recs = self.d.load_calibration()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["prompts"], 2)

    def test_stops_when_usage_limit_hit(self):
        self.loop([done(), done(1, "", "Claude usage limit reached")] + [done()] * 5, mins=200)
        self.assertEqual(self.run_claude.call_count, 2)

    def test_keeps_weekly_reserve(self):
        us = [usage(weekly=50), usage(weekly=96)] + [usage(weekly=96)] * 5
        self.loop([done()] * 5, mins=200, usages=us)
        self.assertEqual(self.run_claude.call_count, 1)

    def test_fast_failure_falls_back_once(self):
        results = [done(1, "", "model not available"), done(), subprocess.TimeoutExpired("c", 1)]
        # Fake calls take 10 min; widen the fast-fail window so this one counts as fast.
        mock.patch.object(self.d, "FAST_FAIL_MINUTES", 20).start()
        self.loop(results, mins=25, model="claude-opus-5-5")  # not the fallback itself
        models = [c.args[1] for c in self.run_claude.call_args_list]
        self.assertEqual(models[1], self.d.FALLBACK_MODEL)
        self.assertFalse(self.run_claude.call_args_list[1].kwargs["resume"])  # fresh start, not --continue


class DryRun(Base):
    extra_env = {"WORKSHOP_DRY_RUN": "1", "WORKSHOP_FORCE": "heavy"}

    def test_dry_run_never_runs_claude(self):
        with mock.patch.object(self.d, "fetch_usage", return_value=usage()):
            self.d.main()
        self.run_claude.assert_not_called()


if __name__ == "__main__":
    unittest.main()
