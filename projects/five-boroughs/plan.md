---
name: Five Boroughs
slug: five-boroughs
status: paused          # idea | active | paused | shipped | archived
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

### M1: The grid <!-- linear-milestone: -->
- [ ] Create public repo with Vite + Three.js scaffold and asset gitignore
  - `.env` for API keys, assets/ and tile caches ignored
- [ ] All of Manhattan's streets from LION/OSM: lanes, widths, real layout
- [ ] Every block as an empty raised lot from planimetric curbs + sidewalks
- [ ] Ground height from LiDAR terrain, water around the island
- [ ] Chunked streaming so the whole island runs in a browser
- [ ] Third-person walk controller with camera
- [ ] One drivable car with enter/exit
- [ ] Wanted level + one cop car that chases the player
- [ ] Deploy a playable link and post it to chat

### M2: First landmark, One World Trade Center <!-- linear-milestone: -->
- [ ] Builder library v0: core API (extrude, setback, taper, curtain wall, instanced parts, LODs)
- [ ] Sonnet-written bespoke generator for One WTC on the library
- [ ] Render-and-compare loop against reference photos, max 3 rounds
- [ ] 9/11 Memorial pools and plaza as a respectful, non-destructible space
- [ ] Bake to glTF and place at real position in the grid

### M3: Building survey pipeline <!-- linear-milestone: -->
- [ ] Pull Mapillary street photos for one pilot neighborhood (~500 buildings)
- [ ] Match each photo to the building face it sees (camera pose vs footprints)
- [ ] Haiku extracts a facade recipe per photo as structured JSON
  - material, color, floors, window grid, cornice, fire escapes, storefront, roof, confidence
- [ ] Vote across photos into one recipe per building, PLUTO fallback when unsure
- [ ] Add 5 building recipes to the builder library (brownstone, pre-war tenement, glass tower, cast-iron, art deco setback)
  - instanced parts, LODs, outputs a JSON op list
- [ ] Sandboxed per-building scripts: Haiku/Sonnet write code that only calls the builder library
- [ ] Render-and-compare loop: render from photo's camera pose, model critiques, fix, max 3 rounds, score saved
- [ ] Bake each building to glTF with LODs
- [ ] Cost and coverage report for the pilot (spend, % buildings covered, accuracy spot-check)

### M4: Streetscape survey <!-- linear-milestone: -->
- [ ] Load open street data for the pilot area
  - planimetrics (curbs, sidewalks, medians), LION lanes/widths, Street Tree Census, hydrants, bike lanes, subway entrances, Citi Bike docks, Parks + POPS boundaries
- [ ] Import Mapillary map-feature detections (signs, poles, lights, benches) as placements
- [ ] Street recipes in builder library: lane markings, crosswalks, curb cuts, bus stops, bike lanes
- [ ] Plaza and park recipes: paving, planters, benches, fountains, lawns, paths, playgrounds
- [ ] Per-space scripts + render-and-compare loop, same pipeline as buildings
- [ ] Bake street tiles and spaces to glTF; pilot report

## Parking lot
<!-- not synced to Linear -->
- Google Photorealistic 3D Tiles streamed live for the far skyline only
- Classic CV window counting on rectified facades
- NYC 1980s tax photos as fallback imagery (check license)
- More bespoke landmarks (Empire State, Flatiron, Chrysler, Brooklyn Bridge)
- Scale survey to all of Manhattan, then outer boroughs
- Movie-inspired character roster and missions
- All five boroughs, subway, bridges
- AI-generated assets / NPC dialogue
- Per-stream "how much game does $200 buy" scoreboard
