# Five Boroughs

- **Pillar:** Build
- **Started:** 2026-10-17
- **Stack / tools:** Three.js + Vite (browser), OpenStreetMap / NYC Open Data geometry, Google Photorealistic 3D Tiles (streamed live, never committed), Claude Code on the Max $200 plan
- **Repo / link:** public repo, TBD (link here once created)

Status, slot, goal, and milestones live in [plan.md](plan.md). Work log: [log.md](log.md). Decisions: [decisions.md](decisions.md).

## What it is
An open-world crime sandbox set in a real-geometry New York City, built in the browser. Walk, steal cars, get chased by cops, run missions. Movie-inspired characters, real streets. It's also a benchmark: how far can a new frontier model get on a "make GTA" prompt over N streams.

## Stream angle
Model-maxxing stress test. The -onomics: $200/mo plan vs. what a studio spends; track hours on stream, tokens/limits hit, and features shipped per stream. "How much game does $200 buy?"

## On-stream safety
- Google Maps / 3D Tiles API key lives in `.env` only: never on screen, never committed. Restrict the key by HTTP referrer and set a billing cap.
- Third-party assets (character likenesses, tile caches, ripped models) stay out of the repo (`.gitignore`d); repo holds code only.
- 9/11 Memorial stays a respectful, non-destructible space: no violence or mission content there.
- No real addresses of private people (own home, friends) used as mission locations.
