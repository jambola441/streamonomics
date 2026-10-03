# Stream Manager

- **Pillar:** Build
- **Started:** 2026-10-03
- **Stack / tools:** Claude Code (custom skills), Python 3 CLI, HTML/CSS overlays, OBS WebSocket, Twitch Helix API
- **Repo / link:** this repo (`.claude/skills/`, `tools/`, `stream/`)

Project #1. Goal, milestones, and status: [plan.md](plan.md). Work log: [log.md](log.md). Decisions and open questions: [decisions.md](decisions.md).

## What it is
Claude is the stream manager. During a stream I type slash commands in Claude Code. Claude preps the episode, flips OBS scenes, updates overlays, sets the Twitch title, drops clip markers, logs what shipped, and writes the recap afterwards. I just work.

## Stream angle
The channel building its own control room, on stream. Every feature is immediately visible (the overlay it adds is on screen the same night), and it's the purest Claude-maxxing demo: the AI runs the show it's starring in.

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
| `/prep [slot]` | before stream | Reads `schedule.md`, the project's `plan.md` (next open deliverables) and `log.md`, and the backlog. Proposes the goal, title, and go-live post. Creates the episode log and sets state. |
| `/golive` | going live | Runs the pre-stream checklist, sets state `live`, starts the session timer, switches to the Starting Soon scene (v1), sets the Twitch title and category (v2). |
| `/now "<task>"` | during | Updates the "now building" ticker. |
| `/ship "<thing>"` | during | Adds to the ledger, logs to the episode, shows the overlay "shipped" pop, drops a Twitch marker (v2). |
| `/clip "<moment>"` | during | Drops a marker and writes a timestamp into the episode log's clip table. |
| `/scene <name>` / `/brb` | during | Scene control (v1). |
| `/idea "<text>"` | anytime | Appends to `ideas/inbox.md`. |
| `/wrap` | ending | Fills in the episode log, appends today's `## YYYY-MM-DD` entry to the project's `log.md` (creates the heading if missing), checks off shipped deliverables in `plan.md`, optionally runs `/sync-plan <slug>`, totals the ledger, drafts 2–3 clip captions and the post-stream post, switches to the Ending scene, commits. |
| `/sync-plan <slug\|all>` | after editing a plan | Pushes `plan.md` to Linear and writes issue IDs back. **Already built:** `.claude/skills/sync-plan/`. |
| `/recap` | weekly | Builds the Ledger recap from the week's episodes and drafts it for YouTube or as a thread. |
| `/chat` | during (v2) | Summarizes recent chat and surfaces questions and ideas worth answering. |

## On-stream safety
- The `sm` CLI is the only thing that reads secrets (`.env`), and it never prints them. Skills never `cat` or echo config.
- Twitch OAuth and OBS WebSocket passwords get set up **off-stream**.
- `stream/state.json` holds nothing secret; it's what the overlays show anyway.
