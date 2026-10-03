# Stream Manager

- **Pillar:** Build
- **Status:** active, project #1
- **Started:** 2026-10-03
- **Stack / tools:** Claude Code (custom skills), Python 3 CLI, HTML/CSS overlays, OBS WebSocket, Twitch Helix API
- **Repo / link:** this repo (`.claude/skills/`, `tools/`, `stream/`)

## Goal
Claude is the stream manager. During a stream I type slash commands in Claude Code. Claude preps the episode, flips OBS scenes, updates overlays, sets the Twitch title, drops clip markers, logs what shipped, and writes the recap afterwards. I just work.

**Done (v0) looks like:** a full stream run end to end with `/prep`, `/golive`, `/now`, `/ship`, `/clip`, and `/wrap`, with overlays updating live and no manual note-taking.

## Architecture

```
          you (Claude Code terminal)              chat (Twitch)
                    │ /slash skills                    │ !idea !project !ledger
                    ▼                                  ▼
  ┌───────────── .claude/skills/ ─────────────┐   chat bot (v2)
  │ judgment + workflow: what to do and when  │        │
  └──────────────────┬────────────────────────┘        │
                     │ calls                           │
                     ▼                                 ▼
          tools/sm  (Python CLI): deterministic actions
          ├── state   → stream/state.json  (single source of truth)
          ├── serve   → localhost overlay server (OBS browser sources)
          ├── obs     → OBS WebSocket: scenes, record, markers   (v1)
          ├── twitch  → Helix API: title, category, markers, chat (v2)
          └── log     → episodes/*.md, projects/*/log.md, ledger
```

**Key design rule:** skills are thin and the CLI is dumb.
- **Skills** hold the judgment: what goal to set, how to phrase a title, what counts as "shipped".
- **The `sm` CLI** does the actual side effects, the same way every time. It's testable without Claude, and it's the only thing that touches secrets (read from `.env`, never printed).

**State** (`stream/state.json`): `live`, `session_started_at`, `episode` (path), `project`, `goal`, `now` (current task), `ledger` (`shipped[]`, `ai_spend`, `markers[]`), `scene`. Overlays poll it from the local server, so the CLI writes the state and the overlays read it. Nothing else.

**Why a local server instead of `file://`:** OBS browser sources block `fetch()` on local files. `sm serve` serves `stream/overlays/` plus `/state.json` on `localhost:7777`. Live push (SSE) can come later.

## Skills (slash commands)

| Skill | When | What it does |
|---|---|---|
| `/prep [slot]` | before stream | Reads `schedule.md`, the project README and log, and the backlog. Proposes the goal, title, and go-live post. Creates the episode log and sets state. |
| `/golive` | going live | Runs the pre-stream checklist, sets state `live`, starts the session timer, switches to the Starting Soon scene (v1), sets the Twitch title and category (v2). |
| `/now "<task>"` | during | Updates the "now building" ticker. |
| `/ship "<thing>"` | during | Adds to the ledger, logs to the episode, shows the overlay "shipped" pop, drops a Twitch marker (v2). |
| `/clip "<moment>"` | during | Drops a marker and writes a timestamp into the episode log's clip table. |
| `/scene <name>` / `/brb` | during | Scene control (v1). |
| `/idea "<text>"` | anytime | Appends to `ideas/inbox.md`. |
| `/wrap` | ending | Fills in the episode log, updates the project log and status, totals the ledger, drafts 2–3 clip captions and the post-stream post, switches to the Ending scene, commits. |
| `/recap` | weekly | Builds the Ledger recap from the week's episodes and drafts it for YouTube or as a thread. |
| `/chat` | during (v2) | Summarizes recent chat and surfaces questions and ideas worth answering. |

## Roadmap
- **v0: local only, no API keys** (target: first weekend stream)
  - [ ] `tools/sm` CLI: `state get/set`, `session start/stop`, `ship`, `clip`, `serve`
  - [ ] `stream/state.json` schema
  - [ ] Overlays: `now-building.html`, `ledger.html` (timer, shipped count, latest ship)
  - [ ] Skills: `/prep`, `/golive`, `/now`, `/ship`, `/clip`, `/idea`, `/wrap`
  - [ ] Dry run: fake stream, end to end
- **v1: OBS control**
  - [ ] `sm obs`: scene switch, start/stop stream and recording, recording chapter markers (obs-websocket v5)
  - [ ] `/scene`, `/brb`; `/golive` and `/wrap` drive scenes
- **v2: Twitch**
  - [ ] Twitch app + OAuth token in `.env` (set up off-stream)
  - [ ] `sm twitch`: title, category, stream markers, send chat message
  - [ ] Chat bot: `!idea` → inbox, `!project`, `!ledger`, `!schedule`
  - [ ] `/chat` skill
- **v3: content flywheel**
  - [ ] `/recap` weekly Ledger
  - [ ] Clip captions and post drafts → `content/`
  - [ ] Metrics pull into `content/metrics.md`

## Open questions
- Build v0 live on stream (recommended: it's the perfect launch episode) or pre-build it off-stream?
- Custom bot vs. Streamer.bot for chat. Custom fits the brand and becomes content.
- AI spend tracking: manual `/ship --cost`, or pull from the Anthropic usage console?
