# The Plan

Phases are ordered. Check items off as you go. Claude can update this file on request.

## Phase 0: Foundation (this week)
- [x] Control-station repo scaffolded
- [ ] Lock the name and handle (Twitch, YouTube, X, TikTok). Check availability for `streamonomics`
- [ ] Write `stream/branding.md`: tagline, voice, 2–3 colors, font
- [ ] Decide what's **off-limits on stream**: client names, API keys, private dashboards (see Safety below)
- [x] Pick the first projects: **stream-manager** (#1), **turonomics**, **terpenomics**, **van-build** (see `projects/`)
- [x] Set the slots: Tue evening, Thu evening, one weekend day (see `stream/schedule.md`)
- [ ] Lock exact times. The weekend slot floats: Saturday or Sunday, whichever works that week
- [ ] Authorize Linear connector, create 'Streamonomics' team, run /sync-plan all

## Project #1: Stream Manager
Claude runs the stream through custom Claude Code skills. Overlays, the chat bot, and OBS/Twitch control from Phases 1–2 are **built as part of this project**. Spec: `projects/stream-manager/README.md`. Roadmap: `projects/stream-manager/plan.md`.

## Phase 1: Broadcast setup (weeks 1–2)
- [ ] Install OBS. Create scenes: `Starting Soon`, `Main (screen + cam)`, `Full Screen Code`, `Just Chatting`, `BRB`, `Ending`
- [ ] Export the scene collection to `stream/obs/` so it's versioned
- [ ] Mic and camera check; set audio filters (noise suppression, compressor, limiter)
- [ ] Build browser-source overlays in `stream/overlays/`:
  - [ ] "Now building" ticker (current project + goal)
  - [ ] **Ledger widget**: session timer, items shipped, AI spend
  - [ ] Starting-soon / BRB screens
- [ ] Set up a privacy layer: a separate browser profile and desktop for streaming, hidden notifications, an `.env` that never touches the screen
- [ ] Do a private test stream, then review the recording

## Phase 2: Chat and interactivity (weeks 2–3)
- [ ] Chat bot (Streamer.bot, Nightbot, or a custom one built on stream as episode #1 content)
- [ ] Commands: `!project`, `!stack`, `!ledger`, `!idea <text>` (writes to `ideas/inbox.md`), `!schedule`
- [ ] Channel point redeems: "Pick the next feature", "Roast my prompt", "Make Claude rewrite it"
- [ ] Twitch panels: About, Stack, Schedule, Socials

## Phase 3: Launch (weeks 3–4)
- [ ] Publish `stream/schedule.md`. Consistency beats volume: start with 3 fixed slots a week
- [ ] Launch stream = **Ship It**: build something small, finish it, deploy it, show the URL
- [ ] After every stream, run `stream/checklists/post-stream.md`

## Phase 4: Content flywheel (ongoing)
- [ ] Every stream → 2–3 short clips (TikTok / Shorts / Reels) + 1 X post
- [ ] Weekly **Ledger** recap (YouTube long-form or a thread)
- [ ] Claude drafts titles, descriptions, and thread text from each episode log into `content/`
- [ ] Track growth in `content/metrics.md`

## Phase 5: Leverage (later)
- [ ] Turn recurring workflows into reusable Claude skills and commands, and open-source them
- [ ] Templates and starter kits people can grab (monetizable)
- [ ] Guest streams / co-op builds
- [ ] Affiliate and sponsor slots for tools actually used on stream

## Safety rules for streaming work
1. **Never show secrets.** Keys live in `.env` files and password managers, and never get opened on stream. Rotate anything that leaks.
2. **Client work:** get permission or anonymize (rename the business, blur dashboards).
3. **Separate accounts** for streaming where possible (browser profile, email, cloud console).
4. **Delay:** consider a 10–30s stream delay on days involving sensitive dashboards.
