# Taponomics

- **Pillar:** Build (Grow once ads go live)
- **Started:** 2026-10-17
- **Stack / tools:** Vite + React + TypeScript SPA, small Node API, Render (web service + Postgres), Google FLEURS speech clips (CC-BY-4.0), Natural Earth country map, Claude Code on the Max $200 plan
- **Repo / link:** public repo TBD (link here once created)

Status, slot, goal, and milestones live in [plan.md](plan.md). Work log: [log.md](log.md). Decisions: [decisions.md](decisions.md). Source spec: [notes/yaptap-prd.md](notes/yaptap-prd.md). Ideation recap: [notes/ideation.md](notes/ideation.md).

## What it is
A network of one-minute daily guessing games in the MapTap mold, each with its own name and one shared engine (daily puzzle, server-side scoring, streaks, share card). First game: **YapTap**. You hear someone speaking and guess the country on a world map, with 5 guesses and distance and direction feedback. Next up: **SoundTap** (free-form guesses scored by embedding distance), **3D ScaleTap** (resize 3D objects to their true size), and **CrapTap** (guess the animal from its droppings).

## Stream angle
Clone-a-business speedrun. ChatGPT puts MapTap's owner profit at about $100k/yr (low confidence: ~13k App Store ratings, a $14.99/yr sub, no ads). How many Taps can a $200/mo plan ship, and what would they earn on ads? Each stream tracks hours per game shipped, infra $/mo, and later DAU and ad revenue against that $100k. Chat plays the daily live and votes on which Tap gets built next.

## On-stream safety
- **Answers are spoilers.** Puzzles built on stream are burned for viewers. The public launch set gets curated off stream, and the schedule and answers are never put on screen after launch.
- Render API key, database URL, and any ad-account pages stay off screen. Secrets live in `.env` only, never committed.
- The answer never ships in the client bundle or in API responses before the round ends (also the core anti-cheat rule).
- FLEURS is CC-BY-4.0: credit it on the site. Never show or store speaker IDs. Don't try to identify speakers.
- NapTap (if it happens): strip EXIF/GPS from Neema photos, and no shots that give away where anyone lives.
