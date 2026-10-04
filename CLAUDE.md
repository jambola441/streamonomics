# CLAUDE.md: Streamonomics control station

This repo runs a live-streaming channel where the owner works on real projects with AI tools. Read `README.md` for the story and `PLAN.md` for the roadmap.

## Conventions
- New project → `/new-project` skill (interviews, scaffolds via `tools/new-project.sh`, fills README + plan.md, adds the index row, offers `/sync-plan`). The bare script is fine for a quick empty scaffold.
- Each project folder: `README.md` (overview, stream angle, safety), `plan.md`, `log.md`, `decisions.md`, `notes/`, `assets/`. Format details: `projects/README.md`.
- **`plan.md` is the source of truth** for goals, milestones, and deliverables. Linear is just the board. After editing a plan, run `/sync-plan <slug>` (or offer to). Never invent Linear IDs; only `/sync-plan` writes them.
- `log.md` is per day: one `## YYYY-MM-DD` heading, freeform bullets underneath, newest at the bottom. Append to today's heading if it exists.
- Decisions go in `decisions.md` (`## YYYY-MM-DD: <title>` + **Context** / **Decision** / **Why**), not buried in logs.
- New stream → `tools/new-episode.sh "<title>"` creates `episodes/YYYY-MM-DD-<slug>.md`.
- Ideas go to `ideas/inbox.md` (one line each, newest at the bottom). Promote good ones with `/new-project <idea>`.
- Small project code can live in `projects/<slug>/`. Bigger apps get their own repo, linked from the project README.

## On-stream rules for Claude
- Never print, echo, or cat secrets, `.env` files, tokens, or credentials. Assume the screen is public.
- Prefer short, readable output. Viewers are watching the terminal.
- When finishing a chunk of work, offer a one-line "ledger" summary: what shipped and roughly how long it took.
