# Projects

One folder per thing built on stream. Create one with `tools/new-project.sh <slug> ["Display Name"] [slot]`.

| Project | Pillar | Status | Slot | Link |
|---|---|---|---|---|
| [stream-manager](stream-manager/) | Build | active (project #1) | Weekend | this repo |
| [turonomics](turonomics/) | Build | active | Tuesday | [jambola441/turonomics](https://github.com/jambola441/turonomics) |
| [terpenomics](terpenomics/) | Build / Grow | active | Thursday | [jambola441/terpenomics](https://github.com/jambola441/terpenomics) |
| [van-build](van-build/) | Make | active | Weekend (Shop Floor) | n/a |

## What's in a project folder

```
projects/<slug>/
├── README.md      # overview: what it is, repo link, stack, stream angle, on-stream safety
├── plan.md        # goal + milestones + deliverables. THE source of truth, synced to Linear
├── log.md         # what happened, per day
├── decisions.md   # ADR-lite: why we picked X over Y
├── notes/         # freeform research and scratch
└── assets/        # screenshots, CAD exports, diagrams
```

The README changes rarely. `plan.md` changes every stream. `log.md` grows every stream.

## Linear

Linear is the board view; `plan.md` is the truth. Edit the plan, then run `/sync-plan <slug>` (or `/sync-plan all`) in Claude Code.

| Here | Linear |
|---|---|
| (the whole channel) | Team **Streamonomics** |
| `projects/<slug>/` | Project |
| `### ` milestone in plan.md | Project Milestone |
| `- [ ]` deliverable line | Issue |
| sub-bullets under a deliverable | Issue description |
| `[x]` | Issue moved to Done on the next sync |
| deliverable line deleted | Sync proposes Canceled and asks first |

The sync runs through the Linear connector (authorize it once in claude.ai connector settings). No API keys on disk. It always shows a dry run and waits for a yes before touching Linear, then writes the IDs back into plan.md. Details: [`.claude/skills/sync-plan/SKILL.md`](../.claude/skills/sync-plan/SKILL.md).

## plan.md format

```markdown
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
<what done looks like>

## Milestones

### v0: Local only <!-- linear-milestone: -->
- [ ] Build `sm` CLI state commands `est:3` `slot:weekend`
  - state get/set, session start/stop
  - writes stream/state.json
- [x] Some finished thing [STR-12]

### v1: OBS control <!-- linear-milestone: -->
- [ ] ...

## Parking lot
<!-- not synced to Linear -->
- maybe-someday ideas
```

Rules:
- A **deliverable** is a top-level `- [ ] ` or `- [x] ` line under a `### ` milestone inside `## Milestones`. One line, one issue.
- **Linear ID** goes in brackets right after the title: `[STR-12]`. No ID = not synced yet. Never type one in by hand; `/sync-plan` writes them.
- **Tags** are optional inline code spans: `est:<points>` and `slot:<tue|thu|weekend|any>`. Other code spans are just part of the title.
- **Indented sub-bullets** under a deliverable become the issue description (acceptance criteria, notes).
- **Milestone headings** carry `<!-- linear-milestone: <id> -->`, empty until synced.
- **`## Parking lot`** is never synced. Park ideas there freely.
- Other `## ` sections (e.g. van-build's `## Transit notes`) are fine and ignored by the sync.
- Lines starting with `TODO:` are placeholders. The parser refuses to sync them, so write the real thing first.

Check a plan any time (no Linear needed):

```bash
python3 tools/plan_parse.py projects/stream-manager/plan.md   # JSON + warnings, exit 1 on errors
python3 tools/plan_parse.py --all
python3 tools/test_plan_parse.py                              # parser tests
```

## log.md format

Per day, freeform. Newest at the bottom. Issue IDs optional. Logs never get posted to Linear.

```markdown
# Stream Manager: Log

## 2026-10-03
- got `sm state` working [STR-12]
- OBS websocket fought back, lost
```

## decisions.md format

ADR-lite, newest at the bottom. `**Decision:** open` is allowed for questions still in the air.

```markdown
## 2026-10-03: Custom chat bot vs. Streamer.bot
**Context:** v2 needs `!idea`, `!project`, `!ledger`.
**Decision:** Custom bot.
**Why:** Fits the brand and the build is content. Costs a weekend.
```
