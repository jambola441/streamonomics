---
name: Stream Manager
slug: stream-manager
status: active          # idea | active | paused | shipped | archived
slot: weekend           # tue | thu | weekend | any
linear:
  team: Streamonomics
  project: Stream Manager
  project_id: 7d9132c0-8c3f-4b16-b44a-3182c2aab281  # written by /sync-plan
---
# Stream Manager: Plan

## Goal
Claude is the stream manager: I type slash commands, Claude runs the show (episode prep, OBS scenes, overlays, Twitch title, clip markers, ledger, recap). I just work.

**Done (v0) looks like:** a full stream run end to end with `/prep`, `/golive`, `/now`, `/ship`, `/clip`, and `/wrap`, with overlays updating live and no manual note-taking. Target: the first weekend stream.

## Milestones

### Rig: broadcast setup <!-- linear-milestone: 3ec64763-7905-40c5-8ee4-494d5f0d3209 -->
- [x] Provision Hetzner stage VM (Ubuntu 24.04 + XFCE, Germany) [STR-15]
  - Falkenstein `cx43` (8 vCPU / 16 GB, ~$18/mo); SSH keys only; firewall closed except Tailscale
  - `tools/hetzner/create-stage.sh` + `cloud-init.yaml`; `lockdown.sh` closes public SSH after Tailscale
- [x] Tailscale on the VM and the Mac [STR-16]
- [x] Remote desktop into the VM (NoMachine, xrdp fallback) [STR-17]
  - readable at stream resolution; test latency while typing
- [x] VM bootstrap: Claude Code, git, Python, Node, this repo [STR-18]
  - scripted as `tools/vm-setup.sh` so the VM is rebuildable
- [x] OBS on the Mac: scenes, audio filters, WebSocket with password [STR-19]
  - window-capture the remote desktop; export scene collection to `stream/obs/`
- [ ] "stream" macOS user for Fusion/AutoCAD days [STR-20]
- [ ] Private test stream end to end, then review the recording [STR-21]

### v0: Local only, no API keys <!-- linear-milestone: f7ea7a49-daf7-47f2-8198-bd652e56809e -->
- [ ] `tools/sm` CLI: state and session commands [STR-1]
  - `state get/set`, `session start/stop`, `ship`, `clip`, `serve`
  - all writes go through `stream/state.json`
- [ ] `stream/state.json` schema [STR-2]
  - `live`, `session_started_at`, `episode`, `project`, `goal`, `now`, `ledger` (`shipped[]`, `ai_spend`, `markers[]`), `scene`
- [ ] Overlays: `now-building.html` and `ledger.html` [STR-3]
  - ledger shows session timer, shipped count, latest ship
  - served by `sm serve` on `localhost:7777`, polling `/state.json`
- [ ] Skills: `/prep`, `/golive`, `/now`, `/ship`, `/clip`, `/idea`, `/wrap` [STR-4]
  - `/prep` picks the goal from the project's next open `plan.md` deliverables
  - `/wrap` appends today's `## YYYY-MM-DD` entry to `projects/<slug>/log.md` (creates the heading if missing)
  - `/wrap` checks off shipped deliverables in `plan.md` and offers to run `/sync-plan <slug>`
- [ ] Dry run: fake stream, end to end [STR-5]

### v1: OBS control <!-- linear-milestone: 1ae4fa49-034f-4dbc-adac-f8c3c44a2b98 -->
- [ ] `sm obs`: scenes, stream/record start-stop, chapter markers [STR-6]
  - obs-websocket v5
- [ ] `/scene` and `/brb`; `/golive` and `/wrap` drive scenes [STR-7]

### v2: Twitch <!-- linear-milestone: dc7c713d-735f-4744-878b-11f6a2517b62 -->
- [ ] Twitch app + OAuth token in `.env` (set up off-stream) [STR-8]
- [ ] `sm twitch`: title, category, stream markers, send chat message [STR-9]
- [ ] Chat bot: `!idea` → inbox, `!project`, `!ledger`, `!schedule` [STR-10]
- [ ] `/chat` skill [STR-11]

### v3: Content flywheel <!-- linear-milestone: 4c2a2ac0-d002-40f6-ab2d-c6c86f85511b -->
- [ ] `/recap` weekly Ledger [STR-12]
- [ ] Clip captions and post drafts → `content/` [STR-13]
- [ ] Metrics pull into `content/metrics.md` [STR-14]

### v4: Producer (watch → triage → act) <!-- linear-milestone: 67cb85a1-2b95-4d37-95be-5c2205a41134 -->
- [ ] Producer design + decision record [STR-22]
  - layered: cheap detectors → event bus → rules / small model / escalate to VM Claude; see `notes/producer.md`
- [ ] Event bus + action allowlist [STR-23]
  - typed events queue; producer can only trigger named actions (`scene`, `mic`, `overlay`, `marker`, `idea`, `task`)
- [ ] Chat listener → events [STR-24]
  - Twitch EventSub/IRC; only the owner's account can issue `task` actions; chat treated as untrusted (prompt-injection safe)
- [ ] Voice commands → events [STR-25]
  - voice activity detection + wake word + local speech-to-text; ships text events only
- [ ] Run sheets: scripted cues [STR-26]
  - YAML time/condition cues (e.g. start → Starting Soon, shipped → overlay pop)
- [ ] Video + health watcher [STR-27]
  - periodic OBS screenshots: black/frozen frame, secret-looking text on screen; mic muted while talking; dropped frames
- [ ] Triage tiers + budget caps [STR-28]
  - rules first, batched small model for ambiguous items, escalate real work to the VM Claude session; per-stream spend cap; costs logged to the ledger
- [ ] Kill switch + shadow mode [STR-29]
  - "producer, stand down" / `!producer off`; log-only mode for a few streams before it acts

## Parking lot
<!-- not synced to Linear -->
- Live push (SSE) for overlays instead of polling
