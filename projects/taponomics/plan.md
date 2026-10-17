---
name: Taponomics
slug: taponomics
status: active          # idea | active | paused | shipped | archived
slot: weekend          # tue | thu | weekend | any
linear:
  team: Streamonomics
  project: Taponomics
  project_id:           # written by /sync-plan
---
# Taponomics: Plan

## Goal
A network of daily one-minute guessing games on one shared engine, built on stream. YapTap ships first as a playable daily game at a public link. Each later stream ships or levels up one Tap. Track hours, infra $, and (once ads are live) revenue against MapTap's estimated ~$100k/yr.

## Milestones

### M1: YapTap playable + daily loop <!-- linear-milestone: -->
- [ ] Create public repo with Vite + React + TS SPA and a small Node API, one Render web service
  - API serves `/api/*` and the built SPA from one origin
  - `.env` for secrets; raw audio and dataset downloads gitignored
- [ ] Pull 20 FLEURS clips from single-country languages as the first puzzle set
  - trim to 8–15s, loudness-normalize, opaque asset IDs (no language or country in filenames)
  - per puzzle: country code, ISO 639-3 language, 4 progressive hints, FLEURS CC-BY credit
  - no speaker IDs kept; no same country or language family back to back
- [ ] World map country picker with search fallback
  - SVG from Natural Earth; tap or search selects, confirm button submits
  - previous guesses stay on the map, numbered
- [ ] Scoring module with tests
  - haversine between country reference points; best guess × attempt multiplier (1, .85, .7, .55, .4); max 5000
  - solved ranks above unsolved; tests prove exact beats miss, score falls with distance, earlier solve beats later
- [ ] Server-authoritative guess API: start or resume session, guess, result
  - 5 guesses max, no repeats, idempotency key
  - each guess returns distance, bearing, and the unlocked hint only; answer revealed only when the round ends
- [ ] Results screen with answer reveal, language fact, score, and emoji share string
- [ ] Deploy to Render and post the playable link to chat
- [ ] Daily loop: puzzle by UTC date, anonymous player token, sessions survive refresh
  - Render Postgres for players, sessions, guesses
- [ ] Streaks and archive: server-side UTC streaks, past results viewable, no replays
- [ ] Daily stats on results: solve rate and guess distribution

### M2: Network shell + launch set <!-- linear-milestone: -->
- [ ] Shared game-client package: daily scheduling, sessions, streaks, share card, per-game scoring contract
- [ ] Network hub page that links every Tap without breaking today's session
- [ ] 45 reviewed puzzles off stream for a 30-day runway, plus a CLI to schedule them
- [ ] Analytics: start, complete, share, D1 and D7 retention, per-puzzle solve rate
- [ ] Results-screen display ad with consent banner, no interstitials between guesses
- [ ] Custom domain and FLEURS credit on an about page

### M3: SoundTap <!-- linear-milestone: -->
- [ ] Pull 30 CC0 sound clips with exact answers, synonyms, and reference descriptions
- [ ] Free-form guess scoring: text embeddings calibrated against unrelated guesses, synonyms score 100
- [ ] Blend in audio-text similarity (CLAP), starting at 0.7 semantic / 0.3 audio
- [ ] Return only the score per guess, never the closest label
- [ ] Ship SoundTap on the shared engine and the hub

### M4: 3D ScaleTap <!-- linear-milestone: -->
- [ ] Object library: 30 glTF models normalized to real-world dimensions
- [ ] Two-object scene with orbit camera and a size slider (React Three Fiber)
- [ ] Log-error scoring: 100·e^(−2·|ln(guess/true)|), so 2× and ½× score the same
- [ ] Silhouette mode so textures don't give the size away
- [ ] Ship ScaleTap on the shared engine and the hub

## Parking lot
<!-- not synced to Linear -->
- CrapTap: guess the animal from its droppings (cheapest, most viral)
- NapTap: guess where Neema is napping, zooms out each wrong guess
- PriceTap: guess the real auction price of a weird item
- YapTap region- and city-level puzzles; multi-country languages by verified speaker origin
- Verified accounts (OIDC) and a global leaderboard; one identity across all Tap domains
- AR mode for ScaleTap on iPhone
- Practice mode, subscriptions (decided against for now: daily-only, ads-only)
- Per-stream "how much Tap does $200 buy" scoreboard overlay
