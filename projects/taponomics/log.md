# Taponomics: Log

One `## YYYY-MM-DD` heading per day, freeform bullets, newest at the bottom. Issue IDs optional.

## 2026-10-17
- Project created.
- Came out of a ChatGPT session: MapTap earnings estimate (~$100k/yr owner profit, low confidence) → a network of Tap clones → full YapTap PRD (saved to notes/yaptap-prd.md).
- Named it Taponomics (no "MapTap" in the name). YapTap first. Stream 1 scope: playable prototype + daily loop. Stack: Vite SPA on Render.
- Content: FLEURS (CC-BY-4.0, ungated). Common Voice has left Hugging Face, so it's out for the prototype.
- Set up three chats like Five Boroughs: this one plans and relays, an implementation chat builds, a stream controller runs OBS. Brief on jambola441/scratch, folder taponomics/.
- Repo created: jambola441/taponomics. Implementation chat ("Hello") briefed and waiting for GO.
- Stream controller ("Chief of stream controller", Remote Control session on the stage VM) briefed: 3-screen layout, game audio capture, run of show. Prepping scenes.
- Coder ("Hello") layout approved: apps/yaptap/{web,server,content}, scripts/fleurs, render.yaml. Pushes to main. Clips committed as AAC .m4a (iPhone-safe) with FLEURS credit. Answers sit in the public repo for the prototype (spoiler rule); the M2 launch set moves out of git.
- Render: Starter web + basic Postgres approved (~$13/mo). Stream controller blocked on the OBS WebSocket being off on the Mac.
