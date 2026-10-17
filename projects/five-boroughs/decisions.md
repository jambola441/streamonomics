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
