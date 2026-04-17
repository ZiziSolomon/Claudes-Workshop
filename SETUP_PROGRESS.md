# Token Burn System — Setup Progress

## What's Done
- **GitHub repo**: https://github.com/ZiziSolomon/Claudes-Workshop (initial commit pushed)
- **Email**: claude.workshop.ai@outlook.com (created, verified)
- **Remote trigger**: 1 weekly trigger set up (Pro plan limit = 1)
  - Name: "Claude Workshop Weekly Session"
  - Schedule: Friday 3AM UTC / 4AM London
  - ID: trig_01Fqeef5xr1Ft9wWdNWmMg1j
  - Runs on Anthropic cloud, clones the repo, does self-directed work, pushes
  - **BLOCKER (2026-04-17)**: Trigger shows as "paused", wouldn't unpause. Likely requires API credit balance to run — Pro subscription may cover creation but not execution. Check billing page for credit balance.
- **Memory system**: Identity, project notes, credentials all stored in `.claude/projects/` memory
- **Git identity**: Repo-local config set to "Claude <noreply@anthropic.com>"
- **Oracle Cloud VM**: Registered (in Ezekiel's name for billing match). Always Free ARM VM (4 cores, 24GB RAM). Note: 2FA — Ezekiel handles auth/re-auth when sessions expire.
- **Usage scraper**: `usage_scraper/scrape.py` — Python + Playwright, scrapes claude.ai for weekly token usage. Writes to `usage_data/latest.json`. Auth persisted via `auth.json` (gitignored). Modes: `--setup` (headed login), `--discover` (find API endpoint), headless (normal run).

## What's Not Done
- **Oracle Cloud VM cron jobs**: VM is registered and ready, but cron sessions not yet configured.
  - Account: claude.workshop.ai@outlook.com (registered in Ezekiel's name to match billing)
  - Purpose: Always Free ARM VM (4 cores, 24GB RAM) to run 6 additional cron sessions
  - Blocker: 2FA — Ezekiel must handle auth and re-auth when sessions expire
  - Next: provision VM, install Node.js + Claude Code CLI, set up auth, create cron jobs
- **Email access**: No way for Claude to check email programmatically yet. Need IMAP setup or MCP connector.

## Architecture (agreed upon)

### The problem
- Pro plan: weekly token reset Fridays 8AM London
- 1 session ≈ 13.5% of weekly budget → ~7 sessions to burn 100%
- Pro plan only allows 1 scheduled remote trigger

### The solution
1. **1 remote trigger** (Anthropic cloud) — Friday 4AM London, already set up
2. **6 cron jobs on Oracle Cloud free VM** — spaced 5h apart, Wed 9PM through Thu 10PM London
3. Each session runs `claude -p "prompt"` non-interactively
4. All work committed to GitHub repo

### Schedule (all London time)
| # | Source | Time | Day |
|---|--------|------|-----|
| 1 | Oracle cron | 9PM | Wednesday |
| 2 | Oracle cron | 2AM | Thursday |
| 3 | Oracle cron | 7AM | Thursday |
| 4 | Oracle cron | 12PM | Thursday |
| 5 | Oracle cron | 5PM | Thursday |
| 6 | Oracle cron | 10PM | Thursday |
| 7 | Remote trigger | 4AM | Friday |

### "Hey" trick (future optimization)
- Fire a negligible-token message to start the 5h session window early
- Do real work near the end of the window
- Not implemented yet — first need burn-time data

### First week plan
- Assume 4h30 burn time per session (conservative)
- Track actual burn time in SESSION_LOG.md
- Adjust future schedules based on data + standard deviations, cap at 5h

## Next Steps (in order)
1. Ezekiel logs Claude into Oracle Cloud VM (2FA required), installs Node.js + Claude Code CLI
2. Resolve auth on the VM: Pro plan uses OAuth, headless `claude -p` likely needs an API key — generate one or find another method
3. Create the 6 cron jobs on the VM (schedule in table above)
4. Test one run manually before letting it run for a week
5. Track burn time in SESSION_LOG.md, adjust schedule based on actuals
6. (Optional later) Set up programmatic email access — IMAP or MCP connector

## Open Questions
- Auth on the VM: Pro plan uses OAuth, but `claude -p` on a headless VM likely needs an API key. May need to generate one or find another auth method.
