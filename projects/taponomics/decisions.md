# Taponomics: Decisions

ADR-lite, newest at the bottom. Undecided? Write `**Decision:** open` and come back to it.

<!--
## YYYY-MM-DD: <title>
**Context:** what forced the choice
**Decision:** what we picked
**Why:** the reasoning, and what we gave up
-->

## 2026-10-17: One network brand, YapTap first
**Context:** ChatGPT pitched YapTap, SoundTap, 3D ScaleTap, CrapTap, and NapTap. 2D ScaleTap and CountTap already exist.
**Decision:** The network is Taponomics. Each game keeps its own name and shares one engine. YapTap ships first, then SoundTap, then 3D ScaleTap. CrapTap and NapTap wait in the parking lot.
**Why:** YapTap already has a full spec and openly licensed audio, and it fits one weekend stream. SoundTap and 3D ScaleTap are the novel mechanics, so they're worth more once the engine exists. We gave up opening with the flashiest visuals (3D ScaleTap).

## 2026-10-17: Vite SPA on Render, not the PRD's Next.js + FastAPI + Cloud Run
**Context:** The PRD proposes Next.js, FastAPI, Postgres, and Cloud Run. The owner wants a Vite SPA on Render.
**Decision:** A Vite + React + TS SPA plus a small Node API, served from one Render web service, with Render Postgres once the daily loop lands.
**Why:** The fewest moving parts that still keep the server authoritative. The answer can't sit in a static bundle, or anyone (or anyone watching the stream) could read it. We gave up SSR/SEO and the Python scoring service. Revisit if SoundTap's embedding scoring needs Python.

## 2026-10-17: YapTap scoring = best guess × attempt multiplier, solved first
**Context:** The PRD's first formula summed per-guess points, but a correct guess ends the round, so 5000 points could never be reached.
**Decision:** Score = round(5000 · e^(−d_min/2000) · m(n)), with m = 1, .85, .7, .55, .4 for guesses 1–5. Leaderboards sort solved above unsolved, then by score.
**Why:** It's simple, it reaches 5000, and an exact answer always beats a close miss. Tests have to prove the ordering rules.

## 2026-10-17: Daily-only, ads-only, network of domains
**Context:** Choices made in the ChatGPT session. MapTap runs subscriptions and no ads.
**Decision:** One puzzle a day, no practice mode. Display ads on the results screen only. No subscriptions. Each game gets its own domain later, with a shared backend.
**Why:** Daily-only makes people come back. Ads-only keeps it free and tests the ad model MapTap skipped. We gave up subscription revenue and more impressions per visit.

## 2026-10-17: Prototype audio from FLEURS, single-country languages only
**Context:** We need speech clips with a trustworthy origin and a license that allows a public game. Common Voice is no longer on Hugging Face. FLEURS is CC-BY-4.0, ungated, and covers 102 languages, each tagged with a country (ka_ge, mn_mn, lo_la…).
**Decision:** Prototype puzzles use FLEURS languages spoken mainly in one country (e.g. Georgian, Mongolian, Lao, Icelandic, Maltese, Khmer). The answer is set editorially from the locale and never from AI accent detection.
**Why:** It's legal, fast to pull on stream, and gives clear answers. We gave up multi-country languages like Spanish and Arabic until we have verified speaker-origin data.
