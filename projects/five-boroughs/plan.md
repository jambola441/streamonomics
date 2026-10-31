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
Rebuild every NYC building as close to the real one as the data allows, in the browser, and climb the detail ladder level by level. Each level ships something visible in the flyer (generic.tech/five-boroughs) and reports per-building accuracy plus cost per building. Pilot, then scale: block, neighborhood, Manhattan, city. Open data first; Google is reference only.

## Milestones

### L0–L1: Shape baseline (done) <!-- linear-milestone: -->
- [x] Citywide footprint tiles (1.08M buildings, 3,231 tiles, Columbus Circle origin)
- [x] LOD2 roofs/walls from DOITT 2014 CityGML (94.6% of buildings)
- [x] LiDAR 2017 refine for 2014–17 buildings + bad-height fixes
- [x] Researched massing for post-2014 towers (92)
- [x] Hosted on Supabase Storage (v1, all boroughs)
- [x] Password-locked flyer with address search at generic.tech/five-boroughs

### L2: Right look from data <!-- linear-milestone: -->
- [ ] Accuracy score per building (level, confidence, sources) in the feature table
- [ ] Flyer: "color by accuracy" mode
- [ ] Facade generators for the top Manhattan styles (tenement, pre-war elevator, brownstone) from the style sheets
- [ ] Remaining 11 styles + fallbacks, citywide
- [ ] Tune styles.json rules on stream from spot checks

### L3: Real 3D facades from photos <!-- linear-milestone: -->
- [ ] Mapillary photo pull + photo-to-building-face matching for a one-block pilot
- [ ] Haiku facade recipe per building (JSON), voted across photos
- [ ] Builder library: recessed windows, cornices, stoops, storefronts, fire escapes as instanced geometry, baked glb LOD0–2
- [ ] Pilot report: cost/building, coverage, accuracy, then neighborhood run

### L4: That exact building <!-- linear-milestone: -->
- [ ] Render-and-compare loop against photos, max 3 rounds, score saved
- [ ] Sonnet escalation for low-confidence buildings
- [ ] Manhattan run with live cost-per-building ledger

### L5: Landmarks <!-- linear-milestone: -->
- [ ] Empire State Building hand-built generator (replace placeholder)
- [ ] Top ~150 landmarks from survey docs, reviewed on stream

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
- Streetscape (streets, parks, plazas) on the same pipeline
- Game layer: walk, drive, cops, missions
