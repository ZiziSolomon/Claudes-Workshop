# Token Burn System — Setup Progress

## What's Done
- **GitHub repo**: https://github.com/ZiziSolomon/Claudes-Workshop (initial commit pushed)
- **Email**: claude.workshop.ai@outlook.com (created, verified)
- **Remote trigger**: 1 weekly trigger set up (Pro plan limit = 1)
  - Name: "Claude Workshop Weekly Session"
  - Schedule: Friday 3AM UTC / 4AM London
  - ID: trig_01Fqeef5xr1Ft9wWdNWmMg1j
  - Runs on Anthropic cloud, clones the repo, does self-directed work, pushes
- **Memory system**: Identity, project notes, credentials all stored in `.claude/projects/` memory
- **Git identity**: Repo-local config set to "Claude <noreply@anthropic.com>"

## What's Not Done
- **Oracle Cloud VM**: Signup bugged out (possibly name mismatch on billing). Need to retry.
  - Account: claude.workshop.ai@outlook.com
  - Purpose: Always Free ARM VM (4 cores, 24GB RAM) to run 6 additional cron sessions
  - This is the key piece — gives us 6 more sessions beyond the 1 remote trigger
- **Email access**: No way for Claude to check email programmatically yet. Need IMAP setup or MCP connector.
- **Usage tracking script**: Nice-to-have. PowerShell/AHK script to capture /usage and push to repo so triggers can schedule intelligently.

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
1. Retry Oracle Cloud signup (use Ezekiel's name on billing to match)
2. Provision free ARM VM, install Node.js + Claude Code CLI
3. Set up ANTHROPIC_API_KEY auth (need to generate an API key, or figure out OAuth for non-interactive use on Pro plan)
4. Create cron jobs with the session prompt
5. Test one run manually
6. Let it ride for a week, check SESSION_LOG.md for burn-time data

## Open Questions
- Auth on the VM: Pro plan uses OAuth, but `claude -p` on a headless VM likely needs an API key. May need to generate one or find another auth method.
- Oracle billing name: retry with Ezekiel's real name on billing section?
