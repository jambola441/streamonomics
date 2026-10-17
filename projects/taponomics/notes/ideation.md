# Ideation recap (ChatGPT, 2026-10-17)

How we got here. The full YapTap spec is in [yaptap-prd.md](yaptap-prd.md).

## MapTap economics (the "-onomics" baseline)
- MapTap.gg: daily geography guessing game. ~13k App Store ratings (4.9★), 10k+ Android installs. MapTap+ is $14.99/yr or $2.99/mo. No ads.
- ChatGPT's estimate of owner operating profit: **$75k–$150k/yr, ~$100k working number**, low confidence (scenarios ran from $12k to $292k depending on MAU and conversion).
- If MapTap ran ads: ~$45k–$240k/yr more at 75k–400k MAU (10 impressions/user/mo, $5 eCPM). The YapTap PRD plans for 1.5 impressions per DAU at a $3 eCPM, which is ~$16k/yr per 10k DAU.

## The Tap ideas
| Game | Mechanic | Notes |
|---|---|---|
| **YapTap** | Hear speech, guess the country on a map | Strongest standalone. Spec done. **First.** |
| **SoundTap** | Hear a sound, type a free-form guess, score = calibrated embedding similarity (+ CLAP audio-text) | Owner's idea. Most novel mechanic. Return only the score, never the nearest label. |
| **3D ScaleTap** | Resize a 3D object next to a fixed one until the sizes match | 2D version exists; 3D is the upgrade. Log-error scoring, silhouette mode, AR later. |
| **CrapTap** | Guess the animal from a photo of its poop | Cheap, very shareable. |
| **NapTap** | Guess where Neema is napping; each miss zooms out | Personal and charming, needs a big photo library. |
| CountTap | Estimate how many objects are in a container | Already exists. Skip. |
| PriceTap | Guess an odd item's real auction price | ChatGPT's addition. |

## Product choices made in that chat
- Daily-only (no practice mode), ads-only (no subs), network brand (own domain per game, shared backend and accounts).
- Shared engine: daily seeded puzzle, server-side scoring, streaks, share card, analytics; each game plugs in its own scoring.
- SoundTap scoring sketch: S = 0.7·semantic + 0.3·audio, exact synonyms = 100, calibrate against unrelated guesses instead of trusting raw cosine.
- ScaleTap scoring sketch: E = |ln(guess/true)|, S = 100·e^(−2E) (2× or ½× → 25 pts).

## ChatGPT's closing advice
The real question is whether people want to come back every day, not whether it can be built. A small prototype with ~10 good recordings answers that before any platform work.
