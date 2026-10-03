# Stream Manager: Decisions

ADR-lite, newest at the bottom. `**Decision:** open` = still undecided.

## 2026-10-03: Skills are thin, the CLI is dumb
**Context:** Claude needs to drive OBS, Twitch, overlays, and logs without leaking secrets or behaving differently every time.
**Decision:** Skills hold the judgment; a Python `sm` CLI does every side effect and is the only thing that reads `.env`.
**Why:** Deterministic, testable without Claude, and secrets never pass through the terminal.

## 2026-10-03: Build v0 live or pre-build it off-stream?
**Context:** v0 has to exist before the stream can run itself.
**Decision:** open. Leaning live: it's the perfect launch episode.
**Why:** _tbd_

## 2026-10-03: Custom chat bot vs. Streamer.bot
**Context:** v2 needs `!idea`, `!project`, `!ledger`, `!schedule`.
**Decision:** open. Custom fits the brand and becomes content; Streamer.bot is faster.
**Why:** _tbd_

## 2026-10-03: How to track AI spend
**Context:** The ledger shows AI spend per session.
**Decision:** open. Manual `/ship --cost`, or pull from the Anthropic usage console?
**Why:** _tbd_

## 2026-10-03: Broadcast rig: cloud stage VM + Mac as A/V and encoder
**Context:** The MacBook (Apple Silicon, 16GB+) shouldn't be the "stage" (personal desktop, notifications, accounts), but camera and mic are physically on it.
**Decision:** A Hetzner cloud VM (Linux desktop, US East) runs Claude Code, the repo, `sm`, and the dev workspace. The Mac runs only OBS + cam + mic + the hardware encoder, and captures a remote-desktop window into the VM. Tailscale links them: OBS browser sources load overlays from the VM's `sm serve`, and `sm obs` drives OBS's WebSocket on the Mac. Autodesk days run Fusion natively on the Mac under a dedicated "stream" macOS user.
**Why:** Only the VM window ever hits the stream; A/V stays native (no sync drift); Apple Silicon encodes nearly free; stream secrets live on the VM, not the laptop; ~$30–80/mo. Full-cloud OBS (VDO.Ninja for cam/mic) stays as an upgrade path if laptop upload becomes the bottleneck.
