---
name: Stream Manager
slug: stream-manager
status: active          # idea | active | paused | shipped | archived
slot: weekend           # tue | thu | weekend | any
linear:
  team: Streamonomics
  project: Stream Manager
  project_id:           # written by /sync-plan
---
# Stream Manager: Plan

## Goal
Claude is the stream manager: I type slash commands, Claude runs the show (episode prep, OBS scenes, overlays, Twitch title, clip markers, ledger, recap). I just work.

**Done (v0) looks like:** a full stream run end to end with `/prep`, `/golive`, `/now`, `/ship`, `/clip`, and `/wrap`, with overlays updating live and no manual note-taking. Target: the first weekend stream.

## Milestones

### v0: Local only, no API keys <!-- linear-milestone: -->
- [ ] `tools/sm` CLI: state and session commands
  - `state get/set`, `session start/stop`, `ship`, `clip`, `serve`
  - all writes go through `stream/state.json`
- [ ] `stream/state.json` schema
  - `live`, `session_started_at`, `episode`, `project`, `goal`, `now`, `ledger` (`shipped[]`, `ai_spend`, `markers[]`), `scene`
- [ ] Overlays: `now-building.html` and `ledger.html`
  - ledger shows session timer, shipped count, latest ship
  - served by `sm serve` on `localhost:7777`, polling `/state.json`
- [ ] Skills: `/prep`, `/golive`, `/now`, `/ship`, `/clip`, `/idea`, `/wrap`
  - `/prep` picks the goal from the project's next open `plan.md` deliverables
  - `/wrap` appends today's `## YYYY-MM-DD` entry to `projects/<slug>/log.md` (creates the heading if missing)
  - `/wrap` checks off shipped deliverables in `plan.md` and offers to run `/sync-plan <slug>`
- [ ] Dry run: fake stream, end to end

### v1: OBS control <!-- linear-milestone: -->
- [ ] `sm obs`: scenes, stream/record start-stop, chapter markers
  - obs-websocket v5
- [ ] `/scene` and `/brb`; `/golive` and `/wrap` drive scenes

### v2: Twitch <!-- linear-milestone: -->
- [ ] Twitch app + OAuth token in `.env` (set up off-stream)
- [ ] `sm twitch`: title, category, stream markers, send chat message
- [ ] Chat bot: `!idea` → inbox, `!project`, `!ledger`, `!schedule`
- [ ] `/chat` skill

### v3: Content flywheel <!-- linear-milestone: -->
- [ ] `/recap` weekly Ledger
- [ ] Clip captions and post drafts → `content/`
- [ ] Metrics pull into `content/metrics.md`

## Parking lot
<!-- not synced to Linear -->
- Live push (SSE) for overlays instead of polling
