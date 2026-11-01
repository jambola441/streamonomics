# Dean Street pilot: results and checklist for the next block

Block: Dean St 100-199, Hoyt St to Bond St, Boerum Hill, Brooklyn (72 street faces, 58 of them rowhouses). Dates: 2026-10-31 to 11-01. Pipeline: Mapillary coverage (L3 prep), facade recipes read by Claude Code subagents (L3, two passes), render-and-compare against the flyer's renders (L4, three rounds), owner street checks folded in between rounds. All reader work ran as subagents on the plan: no API spend, no paid imagery. Mapillary photos stay local (CC BY-SA 4.0, attribution in scratch `shared:five-boroughs/recipes/dean100/index.json`).

## 1. Imagery
- 72 faces (north 36, south 36). 59 have usable Mapillary frames (49 with 5+, median 26 usable per face). 13 have none (100-122 even, 174) and were read from Street View as text.
- Newest capture 2024-04, from two panorama drives (2016 and 2024).
- Heading fix: per-frame yaw calibration against projected party walls. compass_angle scatters several degrees, which is a bay or more at 12 m.
- PLUTO addresses on the north side are one house off (door plate 169 is BIN 3001117, PLUTO 167). Key by BIN; treat the address as a label.

## 2. Cost per house by pass (tokens = subagent totals incl. images)
| Pass | Reader | Houses | Reads | Tokens | Per house | Notes |
|---|---|---|---|---|---|---|
| L3 pass 1 | Sonnet (Haiku tried on 6) | 59 | 68 | 5.6 M | ~95 k | Haiku too weak at picking the house, dropped |
| L3 pass 2 | Sonnet | 59 | 59 | 5.0 M | ~85 k | yaw-calibrated rectified views; changed 23 bay counts and 28 door positions |
| L3 gap fill | Street View text reads | 13 | 13 | — | — | mean confidence 0.71 |
| L4 round 1 | Sonnet | 10 | 10 | 0.86 M | ~86 k | 16 patches |
| L4 round 2 | Sonnet | 10 | 10 | 0.84 M | ~84 k | 30 patches (parapet, stoop direction) |
| L4 round 3 | Sonnet | 10 | 10 | 0.85 M | ~85 k | 4 patches, all parapet |
| Retries | Sonnet + Haiku | | ~20 | ~1.9 M | | |

Whole block: about 14.5 M tokens. That's roughly 200 k per house for a photo recipe, plus about 255 k for each house that went through three compare rounds. To save next time: one L3 pass on calibrated views, no Haiku, and L4 only on houses the owner can check or that have a frontal frame.

## 3. Recipe confidence (L3)
Block today, 72 faces: mean 0.60, median 0.60, 52 at 0.6+, 10 under 0.5. On the 47 faces with real coverage, pass 2 averaged 0.63. Confidence is a usefulness signal, not a quality score.

## 4. L4 score progression (rounds 1 / 2 / 3)
150 Dean 0.72/0.75/0.75 · 154 0.55/0.62/0.70 · 156 0.60/0.60/0.70 · 160 0.72/0.72/0.62 · 167 0.72/0.62/0.80 · 182 0.60/0.70/0.62 · 189 0.30/0.45/0.60 · 195 0.60/0.60/0.72 · 197 0.30/0.30/0.40 (bad poses) · 199 0.35/0.60/0.72. **Mean 0.55 → 0.60 → 0.66.** Patch volume went 16 → 30 → 4. Renderer fixes between rounds moved scores as much as the recipe patches did: window heads, door hoods, full-flight stoops, areaway fences, fire escapes.

## 5. Owner-corrected houses
- 156 Dean: 3 bays (third hidden by a tree), door left, entablature hood on consoles, straight stoop.
- 158 Dean: 3 bays, door left.
- 160 Dean: door left, straight stoop.
- 187 Dean: 3 bays, door left with stoop.
- 189 Dean: 3 bays, 4 floors above the garden level, door left at garden level with no stoop, iron areaway fence, plain arched stucco openings.
- 191 Dean: 3 bays, stoop and door left.

Six houses needed a street check. In nearly all of them the readers got the ground floor wrong (door side, stoop, bays hidden by trees). Everything above the parlor floor mostly held up.

## 6. Recurring reader errors
1. **Door side behind trees.** Readers pick the nearest visible door, often the neighbour's. A door read where a tree covers the target's ground floor is a guess; send it to the owner list.
2. **Garden level counted as a storey.** A leading ~1.2–2.6 m entry in floor_heights_m is the garden level; `floors` counts the parlor floor and above.
3. **Neighbour mix-ups at party walls.** About 3 m of GPS lateral error. Anything within one bay of a party wall needs a second frame from the other side.
4. **Parapet versus cornice top.** City height includes the parapet. Default parapet_m 0.5 for brownstones, 0 where the cornice is the roof edge.
5. **Pose problems read as recipe problems** (197 Dean). No compare loop without a frame showing sidewalk and cornice together.
6. **Pane pattern** (2/2 vs 1/1) is noise unless the frame is frontal and within 15 m.

## 7. Checklist for the next block
- **Before reading:** pick a block with 5+ usable frames per face and a drive newer than 2020. Yaw-calibrate first and read once, on rectified views. Reject poses without sidewalk and cornice together. Note any PLUTO address offset. Key by BIN.
- **Reading:** Sonnet only, with the target marked. Use two frames from opposite directions for houses at party walls. Prompt rules: the garden level is not a storey; a tree over the ground floor makes the door side a guess; describe only what lies between the red lines. Confidence under 0.5 goes to the owner list.
- **Compare loop:** two rounds, not three. Round 1 covers structure (bays, door, stoop, materials); round 2 covers sizes (parapet, cornice, stoop direction). Owner facts go in as fixed fields. Withhold door side and bay count when target identity is in doubt.
- **Budget:** about 85 k tokens per read and per compare round. A 70-face block with one read and two rounds on ten houses is about 7.7 M tokens, half of Dean St.
