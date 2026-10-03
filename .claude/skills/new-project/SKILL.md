---
name: new-project
description: Create a new Streamonomics project folder (README, plan.md, log.md, decisions.md, notes/, assets/) by interviewing the user, then optionally push it to Linear. Use when the user runs `/new-project [slug or idea]`, says "start a new project", "add a project for X", or wants to promote an idea from ideas/inbox.md or ideas/backlog.md into a project.
---

# /new-project

Turn an idea into a real project folder with a filled-in README and plan.md. Then optionally run `/sync-plan` so it shows up in Linear.

Structure and plan.md format: `projects/README.md`. The scaffold script is `tools/new-project.sh`, so don't create the files by hand.

## 1. Gather context (before asking anything)
- If an argument was given, look for it in `ideas/inbox.md` and `ideas/backlog.md`. If it matches, use that text as the starting point.
- If the user mentions a GitHub repo, read its README (and CLAUDE.md, top-level layout) so you can propose a grounded stack, goal, and milestones instead of asking blank questions.
- Read `projects/README.md` so the new slug doesn't collide and the pillar/slot mix makes sense.

## 2. Interview (one round, AskUserQuestion, up to 4 questions)
Propose answers; don't ask open-ended questions you could draft yourself. Cover:
1. **Name + slug.** Suggest both (slug: lowercase-hyphens).
2. **Pillar and slot.** Pillar: Build / Make / Grow. Slot: `tue` / `thu` / `weekend` / `any` (see `stream/schedule.md`).
3. **Goal.** Offer 2–3 concrete "done looks like" options.
4. **First milestone.** Offer a drafted milestone with 3–6 deliverables. Let the user pick or edit.

Ask a second round only if something essential is still unknown (repo link, what must never be on screen). Skip anything already answered in the conversation.

## 3. Scaffold
```bash
tools/new-project.sh <slug> "<Display Name>" <slot>
```
If the slug exists, stop and ask. Don't overwrite.

## 4. Fill in the files
- **README.md:** pillar, stack, repo link, "What it is", "Stream angle" (include the "-onomics": time, money, or leverage you can put a number on), and **On-stream safety** (keys, customer data, accounts, locations relevant to *this* project).
- **plan.md:** set `status` (`active` if starting now, else `idea`), write the Goal, and replace the template milestone with the agreed milestones and deliverables. No `TODO:` deliverables may remain if the user wants it synced (the parser rejects them). Put maybe-later items in `## Parking lot`.
- **log.md:** today's entry: `- Project created` plus anything decided.
- **decisions.md:** one entry if a real choice was made in the interview (e.g. stack, scope cut).
- **projects/README.md:** add a row to the index table (project, pillar, status, slot, link).
- If it came from `ideas/`, strike it through there and note `→ projects/<slug>`.

## 5. Validate
```bash
python3 tools/plan_parse.py projects/<slug>/plan.md
```
Fix any `error` warnings before going further.

## 6. Linear (ask first)
Ask: "Push to Linear now?" If yes, run the `/sync-plan <slug>` workflow (`.claude/skills/sync-plan/SKILL.md`), which has its own dry-run and confirmation.

## 7. Finish
- Commit: `Add <name> project` (follow repo commit conventions).
- Reply in 3–5 lines: folder path, goal, first milestone, Linear status. Keep it short; this may be on stream.

## Rules
- Never write secrets, tokens, or private customer data into project files. This repo is public.
- Don't invent product facts about an existing codebase. Read it or ask.
