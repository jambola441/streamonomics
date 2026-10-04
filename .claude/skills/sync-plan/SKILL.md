---
name: sync-plan
description: Sync a project's plan.md to Linear (team "Streamonomics"). Use when the user runs `/sync-plan <slug>` or `/sync-plan all`, asks to push a plan to Linear, update the Linear board, or after plan.md deliverables were added, edited, or checked off. plan.md is the source of truth; Linear is the board view.
---

# /sync-plan

Push `projects/<slug>/plan.md` to Linear and write the Linear IDs back into plan.md.

**Mapping:** team `Streamonomics` · `projects/<slug>/` = Linear Project · `### ` milestone = Project Milestone · `- [ ]` deliverable = Issue. Format spec: `projects/README.md`.

**Arguments:** `<slug>` syncs one project. `all` syncs every `projects/*/plan.md` except `_template` and projects with `status: archived` (sync an archived one by naming it explicitly). No argument: ask which.

## On-stream rules (the screen is public)
- Never print tokens, keys, OAuth URLs with codes, or raw API responses. Linear IDs and titles are fine.
- Keep output short: the dry-run table, one confirm, a final summary. No JSON dumps.

## 1. Parse

```bash
python3 tools/plan_parse.py projects/<slug>/plan.md   # or: python3 tools/plan_parse.py --all
```

- Exit 2: bad path. Tell the user, stop.
- Exit 1 (any `level: "error"` warning): list the errors as `plan.md:<line>  <message>`, and stop for that project. Don't guess around broken structure. With `all`, skip broken projects, sync the rest, and list the skipped ones at the end. Placeholder deliverables (`TODO: ...`) are errors on purpose, so templates never become junk issues.
- `level: "warning"` entries: mention them in one line each in the dry run; they don't block.

Work from the parser's JSON, not your own reading of the markdown. Use each deliverable's `line` and `raw` to edit the file later.

## 2. Connect to Linear

- Load the Linear MCP tools: `ToolSearch` with query `linear` (try `+linear` if needed). Read the returned schemas; use the tools that list/get/create/update teams, projects, project milestones, issues, issue statuses (workflow states), and labels. Don't assume tool names; discover them.
- If no Linear tools come back, or a call fails with an auth/permission error: stop and tell the user to **authorize the Linear connector in claude.ai connector settings**, then re-run `/sync-plan`. Don't try API keys or scripts.

## 3. Resolve the team and project

1. **Team:** find the team named in `frontmatter.linear.team` (default `Streamonomics`). If it doesn't exist, stop: "Create a Linear team named Streamonomics, then re-run." Never create teams. Note the team's issue prefix (e.g. `STR`) and its workflow states; find the Done state = the state of type `completed` (prefer the one named "Done") and the Canceled state = type `canceled`.
2. **Project:** if `linear.project_id` is set, fetch that project. Otherwise search the team's projects by exact name `linear.project`. If found by name, plan to write its ID back. If not found, plan to **create** it (name = `linear.project`, team, description = the plan's Goal). Creation is automatic (step 6).
   - If `project_id` is set but the project is gone (deleted/inaccessible): stop and ask. Don't silently create a duplicate.
3. **Labels:** if any deliverable has a `slot` tag, look up team labels named `slot:<value>` (e.g. `slot:tue`). Plan to create missing ones if the label tool allows it; otherwise skip labels and say so once.
4. **Estimates:** if any deliverable has `est`, the issue tool must accept an estimate. If the team has estimates off (the call rejects it, or the team settings say so), skip estimates and say so once.

## 4. Fetch what Linear has

- The project's milestones (id, name).
- **All** issues in the project (paginate; include completed and canceled): identifier (`STR-12`), title, description, state + state type, milestone, estimate, labels.

## 5. Diff (plan.md wins)

Collect every ID referenced in plan.md: all deliverable `id`s plus parking-lot `id`s.

**Milestones** (in plan order):
- Has `linear_milestone_id` and it exists in Linear → rename in Linear if the title differs.
- Has an ID that Linear doesn't know → error for that milestone; ask the user (it was probably deleted in Linear).
- No ID → match an existing Linear milestone by exact name (case-insensitive), else **create**. Either way, write the ID into the heading comment.
- Linear milestones not in plan.md: list them as info. Never delete milestones.

**Deliverables:**
- **No ID** → **create** issue: title, description = the `description` lines joined with `\n` (markdown sub-bullets, as-is; omit if empty), team, project, milestone, estimate from `est`, label `slot:<value>` from `slot`. If `done` is true, create it directly in the Done state.
  - Duplicate guard: if an *unreferenced* issue in the project has the exact same title, propose **linking** to it (write its ID back) instead of creating a twin. This recovers cleanly from a half-finished earlier sync.
- **Has ID** but not in this Linear project → error for that line (wrong ID, or the issue moved). Ask; don't change it.
- **Has ID** → **update** whatever differs: title, milestone, estimate, slot label. Description: if plan.md has sub-bullets and they differ, overwrite; if plan.md has none, leave Linear's description alone.
- `[x]` and the Linear state type is not `completed` → set to the Done state (**done**). If Linear says `canceled`, report it instead of reviving it.
- `[ ]` but Linear says `completed` → **mismatch**: report it ("STR-12 is Done in Linear but unchecked in plan.md: check it off, or reopen it in Linear?"). Don't flip either side.
- `[ ]` and Linear says `canceled` → report as a mismatch too.

**Orphans:** issues in the Linear project whose identifier is not referenced anywhere in plan.md (deliverables or parking lot) and that aren't already completed/canceled → propose **cancel**. These always need an explicit yes, listed by ID and title. Completed/canceled orphans: ignore.

**Parking lot:** never synced. Nothing under `## Parking lot` creates or updates anything.

## 6. Summary, then apply (auto-save)

The owner has pre-approved issue saves: **creating projects, milestones, and issues, updating them, and marking them Done happen without asking.** Show one compact summary per project, then go straight to step 7:

```
stream-manager → Linear project "Stream Manager" (create)
  milestones: 2 create, 1 rename
  issues:     5 create, 1 update, 1 done, 1 cancel?
  + v0: Local only  (milestone)
  + L19  Build `sm` CLI state commands  est:3 slot:weekend
  ~ L24  STR-13  title: "Scene switch" → "Scene switching"
  ✓ L22  STR-12  → Done
  ? STR-31 "Old idea" not in plan.md → Cancel? (needs a yes)
  ! STR-14 is Done in Linear but unchecked on L26
  plan.md: 1 project_id, 2 milestone IDs, 5 issue IDs to write back
```

Rules:
- Creates, updates, and Done transitions apply automatically. If there are no changes, say "in sync" and stop.
- **Still ask first** (only this): orphan cancels, opt-in per item, listed by ID and title. Apply everything else, then ask about cancels at the end.
- Mismatches (`!` lines) are reported, never auto-resolved.

## 7. Apply

Order: project → labels → milestones → issues (creates, then updates, then done) → cancels the user approved.

Write IDs back **as you go** (right after each create succeeds), so an interrupted run never loses an ID:

- **project_id:** fill the value of the `project_id:` line (line number in `frontmatter_lines["linear.project_id"]`), keeping its trailing comment, e.g. `  project_id: 6f1c…           # written by /sync-plan`.
- **Milestone:** fill the comment on the heading line: `### v0: Local only <!-- linear-milestone: <id> -->`. If the heading had no comment, append ` <!-- linear-milestone: <id> -->`.
- **Issue:** insert ` [STR-12]` into the deliverable's `raw` line right after the title text: before the first `est:`/`slot:` tag span, or at the end of the line if there are no tags. Example: ``- [ ] Build `sm` CLI `est:3` `` → ``- [ ] Build `sm` CLI [STR-12] `est:3` ``.

Editing rules: use the Edit tool with the exact `raw` line (or heading line) as `old_string`. Change only those lines; every other byte of plan.md stays as-is (no reformatting, no reflowing, no trailing-newline changes). Never write an ID you didn't get back from Linear, and never invent one.

If a Linear call fails mid-run: stop, keep what's already written back, report what did and didn't apply. Re-running is safe (IDs in plan.md + the duplicate guard).

Afterwards, re-run `python3 tools/plan_parse.py projects/<slug>/plan.md` and confirm `unsynced` is 0 and there are no errors.

## 8. Summary

Two or three lines, stream-friendly:

```
synced stream-manager: +5 issues, ~1 updated, 1 done, 1 canceled · plan.md updated
mismatch: STR-14 (Done in Linear, unchecked in plan.md)
```

Then offer to commit `plan.md` (`Sync <slug> plan to Linear`). Don't commit unasked.

## Don'ts
- Don't create teams, delete anything, or touch issues outside the project.
- Don't post comments to Linear from log.md or anywhere else.
- Don't sync the parking lot, and don't sync placeholder `TODO:` deliverables.
- Don't put Linear URLs, tokens, or user emails into plan.md. IDs only.
