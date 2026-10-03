# CLAUDE.md: Streamonomics control station

This repo runs a live-streaming channel where the owner works on real projects with AI tools. Read `README.md` for the story and `PLAN.md` for the roadmap.

## Conventions
- New project → `tools/new-project.sh <slug> ["Display Name"] [slot]` (copies `projects/_template`), then add it to the table in `projects/README.md`.
- Each project folder: `README.md` (overview, stream angle, safety), `plan.md`, `log.md`, `decisions.md`, `notes/`, `assets/`. Format details: `projects/README.md`.
- **`plan.md` is the source of truth** for goals, milestones, and deliverables. Linear is just the board. After editing a plan, run `/sync-plan <slug>` (or offer to). Never invent Linear IDs; only `/sync-plan` writes them.
- `log.md` is per day: one `## YYYY-MM-DD` heading, freeform bullets underneath, newest at the bottom. Append to today's heading if it exists.
- Decisions go in `decisions.md` (`## YYYY-MM-DD: <title>` + **Context** / **Decision** / **Why**), not buried in logs.
- New stream → `tools/new-episode.sh "<title>"` creates `episodes/YYYY-MM-DD-<slug>.md`.
- Ideas go to `ideas/inbox.md` (one line each, newest at the bottom). Promote good ones with `tools/new-project.sh`.
- Small project code can live in `projects/<slug>/`. Bigger apps get their own repo, linked from the project README.

## On-stream rules for Claude
- Never print, echo, or cat secrets, `.env` files, tokens, or credentials. Assume the screen is public.
- Prefer short, readable output. Viewers are watching the terminal.
- When finishing a chunk of work, offer a one-line "ledger" summary: what shipped and roughly how long it took.
