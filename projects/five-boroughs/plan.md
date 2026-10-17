---
name: Five Boroughs
slug: five-boroughs
status: active          # idea | active | paused | shipped | archived
slot: weekend          # tue | thu | weekend | any
linear:
  team: Streamonomics
  project: Five Boroughs
  project_id:           # written by /sync-plan
---
# Five Boroughs: Plan

## Goal
Max-scale stress test: see how far the new model can push a browser open-world NYC crime game across streams. Each stream ships a playable build; track features shipped, hours, and plan-limit hits per stream.

## Milestones

### M1: Streets and cops <!-- linear-milestone: -->
- [ ] Create public repo with Vite + Three.js scaffold and asset gitignore
  - `.env` for API keys, assets/ and tile caches ignored
- [ ] Load real lower Manhattan geometry (~1km) from OSM roads + buildings
- [ ] Third-person walk controller with camera
- [ ] One drivable car with enter/exit
- [ ] Wanted level + one cop car that chases the player
- [ ] Deploy a playable link and post it to chat

## Parking lot
<!-- not synced to Linear -->
- Google Photorealistic 3D Tiles streamed live for the skyline
- Movie-inspired character roster and missions
- All five boroughs, subway, bridges
- AI-generated assets / NPC dialogue
- Per-stream "how much game does $200 buy" scoreboard
