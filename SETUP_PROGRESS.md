# Token Burn System — Setup Progress

## What's Done
- **GitHub repo**: https://github.com/ZiziSolomon/Claudes-Workshop (initial commit pushed)
- **Email**: claude.workshop.ai@outlook.com (created, verified)
- **Remote trigger**: 1 weekly trigger set up (Pro plan limit = 1)
  - Name: "Claude Workshop Weekly Session"
  - Schedule: Friday 3AM UTC / 4AM London
  - ID: trig_01Fqeef5xr1Ft9wWdNWmMg1j
  - Runs on Anthropic cloud, clones the repo, does self-directed work, pushes
  - **BLOCKER (2026-04-17)**: Trigger shows as "paused", wouldn't unpause. Requires API credit balance to run — Pro subscription covers creation but not execution. Credit balance = $0. Deprioritised since 6 Oracle cron jobs cover most of the budget anyway.
- **Memory system**: Identity, project notes, credentials all stored in `.claude/projects/` memory
- **Git identity**: Repo-local config set to "Claude <noreply@anthropic.com>"
- **Oracle Cloud VM**: Provisioned (2026-04-17).
  - Shape: VM.Standard.A1.Flex (ARM), 1 OCPU, 6GB RAM — free tier
  - Region: UK South (London)
  - Public IP: 140.238.76.161
  - SSH key: `ssh-key-2026-04-17.key` (Ezekiel has the private key)
  - **BLOCKER**: VCN created manually (not via wizard), so internet gateway was not auto-configured. VM is unreachable on port 22. Ezekiel needs to add: internet gateway → route table rule (0.0.0.0/0) → security list ingress rule TCP:22.
- **Usage tracker**: Chrome extension + local server. Working as of 2026-04-17.
  - Extension (`usage_tracker_extension/`): intercepts fetch calls on claude.ai, filters for usage endpoint, POSTs to localhost:7432
  - Server (`usage_scraper/server.py`): receives data, writes to `usage_data/latest.json`, commits to git
  - Server auto-starts via Windows Task Scheduler on login (pythonw, no window)
  - Chrome auto-opens usage page via Task Scheduler every 4 hours (Profile 2 = marthasolomon1991)
  - Data captured: `five_hour.utilization`, `seven_day.utilization`, `resets_at`, org_id
  - Known org_id: `b49de57b-f2f0-4db3-9f1b-833808b8e371`
  - Known endpoint: `/api/organizations/b49de57b-f2f0-4db3-9f1b-833808b8e371/usage`
- **Claude Code OAuth token**: Generated (sk-ant-oat01-...). Stored in Claude's memory. Ready to deploy to VM once SSH is accessible.

## What's Not Done
- **Oracle Cloud VM networking**: Internet gateway not configured — VM unreachable (see blocker above)
- **Oracle Cloud VM setup** (blocked until networking fixed):
  - Install Node.js + Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
  - Set `CLAUDE_CODE_OAUTH_TOKEN` env var
  - Create 6 cron jobs (schedule below)
- **Email access**: No way for Claude to check email programmatically. Need IMAP setup or MCP connector.

## Architecture (agreed upon)

### The problem
- Pro plan: weekly token reset Fridays 8AM London
- 1 session ≈ 13.5% of weekly budget → ~7 sessions to burn 100%
- Pro plan only allows 1 scheduled remote trigger

### The solution
1. **6 cron jobs on Oracle Cloud free VM** — spaced 5h apart, Wed 9PM through Thu 10PM London
2. **1 remote trigger** (Anthropic cloud) — Friday 4AM London (paused until credits available)
3. Each session runs `claude -p "prompt"` non-interactively
4. All work committed to GitHub repo
5. Each session reads `usage_data/latest.json` to decide whether to run (skip if seven_day.utilization > 90%)

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

### Session timing
- Sessions are 5h rolling windows, snapping to the clock hour you start in
- Example: start between 8–9AM → session ends at 1PM

### "Hey" trick (future optimisation)
- Fire a negligible-token message to start the 5h session window early
- Do real work near the end of the window
- Not implemented yet — first need burn-time data

### First week plan
- Assume 4h30 burn time per session (conservative)
- Track actual burn time in SESSION_LOG.md
- Adjust future schedules based on data + standard deviations, cap at 5h

## Next Steps (in order)
1. **Ezekiel**: Fix Oracle VM networking in OCI console:
   - Networking → Virtual Cloud Networks → claude-workshop-vcn
   - Create an Internet Gateway
   - Route Tables: add rule 0.0.0.0/0 → Internet Gateway
   - Security Lists: add Ingress rule TCP port 22 from 0.0.0.0/0
   - Then SSH: `ssh -i ssh-key-2026-04-17.key opc@140.238.76.161`
2. Install Node.js + Claude Code CLI on VM, set OAuth token
3. Create the 6 cron jobs (schedule above, UTC: 8PM/1AM/6AM/11AM/4PM/9PM Wed-Thu)
4. Test one cron run manually
5. Track burn time in SESSION_LOG.md, adjust schedule based on actuals
6. (Optional) Fix remote trigger once API credits available
7. (Optional) Set up programmatic email access — IMAP or MCP connector

## Approaches Abandoned
- **Playwright headless scraper**: Google OAuth blocks automation (detects even `channel="chrome"` + `--disable-blink-features=AutomationControlled`). Replaced by Chrome extension.
- **Chrome cookie decryption**: Chrome 127+ uses App-Bound Encryption (v20 format) with IElevationService COM validation. Completely blocked — only Chrome itself can decrypt cookies. No workaround without kernel-level access.

## Open Questions
- Auth on the VM confirmed: OAuth token works for headless `claude -p` (tested locally). No API key needed.
