# Five Boroughs: Decisions

ADR-lite, newest at the bottom. Undecided? Write `**Decision:** open` and come back to it.

<!--
## YYYY-MM-DD: <title>
**Context:** what forced the choice
**Decision:** what we picked
**Why:** the reasoning, and what we gave up
-->

## 2026-10-17: Code-only public repo, accept IP risk on characters/assets
**Context:** Want movie characters and Google Earth-style real NYC visuals, in a public repo.
**Decision:** Repo holds code only; character likenesses and third-party assets stay out of git. Google 3D Tiles get streamed live through the API, never extracted. Owner accepts takedown risk on characters.
**Why:** Keeps the code shareable and the takedown surface small. Gave up a fully self-contained repo.

## 2026-10-17: Buildings = real data shells + features pulled from photos, not photogrammetry
**Context:** Want buildings that match real life without paying for Google 3D Tiles, which also look melted at street level and can't be cached or edited under Google's terms.
**Decision:** Building shapes come from the NYC 3D Building Model + PLUTO. Facade features get pulled from street photos (Mapillary) by Haiku vision as structured recipes, voted across angles, then a procedural generator builds the 3D model.
**Why:** Free and open data, game-ready meshes, and the pipeline itself is good stream content. Gave up photoreal textures; accuracy depends on photo coverage and how well photos get matched to buildings.

## 2026-10-17: One pipeline for everything: recipes + per-object scripts on a builder library
**Context:** Buildings, streets, parks, and plazas all need to match real NYC.
**Decision:** Open data gives placement and shape. Photos give features. A builder library holds standard recipes. Haiku/Sonnet write sandboxed per-object scripts that only call the library. A render-and-compare loop checks output against photos. Results get baked to glTF.
**Why:** One pipeline to build and debug, safe to run generated code, instanced and fast to render. Gave up full freedom in the generated code.

## 2026-10-17: Start with the whole Manhattan grid, empty blocks, then One WTC
**Context:** Could start with one detailed neighborhood or the whole island rough.
**Decision:** M1 is every Manhattan street with empty blocks. M2 is One WTC as the first landmark. Individual buildings come after.
**Why:** The whole island playable from day one is a better hook, and it forces chunked streaming early. One landmark shakes out the builder library before we scale it to 43k buildings.

## 2026-10-31: Detail ladder with per-building accuracy
**Context:** The first run put every building at the right place, height and shape. Now the goal is to get each building as close to real as possible.
**Decision:** Climb levels L0–L5 (box → real shape → right look → real 3D facade → that exact building → landmarks). Pilot each level small, then scale. Score accuracy and cost per building.
**Why:** Every step stays visible, and we only spend on detail where the pilot shows it pays. Gave up a single big-bang build.

## 2026-10-31: Street View as a fallback source, open sources primary
**Context:** Mapillary reaches only ~5% of Brooklyn buildings with 5+ photos, and fewer recent ones. Street View covers almost every building but Google's terms forbid building derived data from it.
**Decision:** Open sources stay primary: Mapillary, KartaView, NYC tax photos, calibrated archetype recipes. Street View fills gaps only, read by the Chrome research session. Only the text recipe is kept; no images are saved, cached, published or shown on stream. Requests stay slow and bounded. Each recipe records its source, so Street-View-derived ones can be pulled if needed.
**Why:** The owner accepted the terms risk for better per-building accuracy, while keeping exposure small and reversible. What we gave up: a fully clean data lineage.

## 2026-10-31: Five Boroughs is non-commercial
**Context:** Some data sources (Municipal Archives tax photos) license differently for commercial vs non-commercial use.
**Decision:** The project is non-commercial, made for the public. No paid game, ads or sponsorship deals tied to it.
**Why:** It's a public-interest project. This keeps the Archives photos license-exempt with a credit line, and fits CC BY-SA sources.
