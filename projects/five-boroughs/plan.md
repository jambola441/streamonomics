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
- [ ] Load real lower Manhattan (~1km): NYC 3D Building Model shells + OSM streets
  - PLUTO attributes (year built, floors, building class) joined per building
  - Facade v0: style guessed from PLUTO only
- [ ] Third-person walk controller with camera
- [ ] One drivable car with enter/exit
- [ ] Wanted level + one cop car that chases the player
- [ ] Deploy a playable link and post it to chat

### M2: Building survey pipeline <!-- linear-milestone: -->
- [ ] Pull Mapillary street photos for one pilot neighborhood (~500 buildings)
- [ ] Match each photo to the building face it sees (camera pose vs footprints)
- [ ] Haiku extracts a facade recipe per photo as structured JSON
  - material, color, floors, window grid, cornice, fire escapes, storefront, roof, confidence
- [ ] Vote across photos into one recipe per building, PLUTO fallback when unsure
- [ ] Facade generator v1: recipe + building shell → game-ready 3D model
- [ ] Cost and coverage report for the pilot (spend, % buildings covered, accuracy spot-check)

## Parking lot
<!-- not synced to Linear -->
- Google Photorealistic 3D Tiles streamed live for the far skyline only
- Classic CV window counting on rectified facades
- NYC 1980s tax photos as fallback imagery (check license)
- Scale survey to all of Manhattan, then outer boroughs
- Movie-inspired character roster and missions
- All five boroughs, subway, bridges
- AI-generated assets / NPC dialogue
- Per-stream "how much game does $200 buy" scoreboard
