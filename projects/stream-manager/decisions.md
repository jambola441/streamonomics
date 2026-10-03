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
