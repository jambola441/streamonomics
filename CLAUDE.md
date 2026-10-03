# CLAUDE.md: Streamonomics control station

This repo runs a live-streaming channel where the owner works on real projects with AI tools. Read `README.md` for the story and `PLAN.md` for the roadmap.

## Conventions
- New project → `tools/new-project.sh <slug>` (copies `projects/_template`). Keep `projects/<slug>/README.md` current: goal, status, stack, next steps.
- New stream → `tools/new-episode.sh "<title>"` creates `episodes/YYYY-MM-DD-<slug>.md`.
- Ideas go to `ideas/inbox.md` (one line each, newest at the bottom). Promote good ones with `tools/new-project.sh`.
- Small project code can live in `projects/<slug>/`. Bigger apps get their own repo, linked from the project README.

## On-stream rules for Claude
- Never print, echo, or cat secrets, `.env` files, tokens, or credentials. Assume the screen is public.
- Prefer short, readable output. Viewers are watching the terminal.
- When finishing a chunk of work, offer a one-line "ledger" summary: what shipped and roughly how long it took.
