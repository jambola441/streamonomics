# Five Boroughs: Log

One `## YYYY-MM-DD` heading per day, freeform bullets, newest at the bottom. Issue IDs optional.

## 2026-10-17
- Project created.
- Named it Five Boroughs (no "GTA" in the name). Goal: max-scale stress test of the new model. M1 = streets + walking + car + cops.
- Building approach decided: data shells + features pulled from photos by Haiku → generated 3D models. Added M2 survey pipeline.
- Same recipes + per-object scripts approach extended to streets, parks, plazas (M3). Builder library + render-and-compare loop added to M2.
- Re-sequenced: M1 whole Manhattan grid (empty blocks), M2 One WTC, M3 buildings, M4 streetscape.
- Parked until next week: too big for the first stream. Plan, brief, and the 3-screen stream layout idea are ready to pick back up.

## 2026-10-30
- Unpaused. Starting with the WTC area: a peer session in Chrome researches buildings via Google Maps (text notes only), and the five-boroughs session builds in Three.js.
- Citywide tiles built by peer session. Next: tier-1 detail for every building = PLUTO style archetype + facade shader. Photo survey stays M3.

## 2026-10-31
- Citywide tiles live on Supabase; flyer with address search at generic.tech/five-boroughs. Plan restructured around the detail ladder L0–L5 with per-building accuracy + cost.
- L2 v1 live in the flyer: per-style facade shader (window grid, floor bands, storefronts, curtain walls from the style sheets) + color-by-accuracy view (reads v2 when uploaded). Builder session inactive, so L2 was built directly in the flyer.
- L3 pilot live: Dean St 100-199 (Boerum Hill) has 72 facade recipes (59 Mapillary via Sonnet/Haiku, 13 Street View text). The flyer renders real 3D windows, doors, stoops, cornices and wall colours per house. Mapillary coverage is thin (Brooklyn 5.5% at 5+ images), so the plan is archetype recipes calibrated on photo samples plus per-building overrides.
- Flyer: click-to-pin + street view walk mode, NYC Planimetric sidewalks/roadbed with curbs, street trees (NYC Parks Forestry, snapped to curbs), road markings (centerline/lanes/crosswalks/stop bars/bike lanes), log depth buffer fixed ground flicker. Owner corrections on 156/158/160 Dean. W 109th St tenement pilot read (21 faces). L4 rounds 1-2 done on Dean St (mean score 0.55 -> 0.60).
