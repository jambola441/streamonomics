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
