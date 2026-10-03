# The Rig

Decision and reasoning: `projects/stream-manager/decisions.md` (2026-10-03: Broadcast rig).

```
 Hetzner VM nbg1 (Ubuntu + XFCE) — the stage MacBook (Apple Silicon) — A/V + encoder
 ├─ Claude Code + this repo + `sm` CLI        ├─ OBS ───────── stream ─────────► Twitch
 ├─ editor, terminal, browser       ─────►    │   ├─ window capture: remote desktop into VM
 ├─ `sm serve` overlays :7777  ◄── Tailscale ─┤   ├─ browser sources: http://<vm>:7777/...
 ├─ `.env` (Twitch app creds)                 │   ├─ webcam + mic (native devices)
 └─ `sm obs` ─────────────── Tailscale ────►  │   └─ obs-websocket :4455 (password)
                                               └─ "stream" macOS user for Fusion days
```

## Pieces
| Piece | Where | Notes |
|---|---|---|
| Stage VM | Hetzner, Nuremberg (`nbg1`), `cx43` | 8 vCPU / 16 GB, ~$18/mo. Ubuntu 24.04 + XFCE. Created by `tools/hetzner/create-stage.sh` + `cloud-init.yaml`. US (`ash`) is ~4x the price; the ~100 ms typing lag only affects the remote desktop, not viewers. |
| Remote desktop | VM → Mac | NoMachine (good quality on CPU-only VMs); xrdp as fallback. Capture its window in OBS. |
| Private network | VM ↔ Mac | Tailscale on both. Nothing exposed publicly: overlays and OBS WebSocket only on the tailnet. |
| OBS | Mac | Apple VT hardware encoder. Scenes per `stream/obs/README.md`. WebSocket on, password set. |
| Cam + mic | Mac | Native devices into OBS; audio filters (noise suppression, compressor, limiter). |
| Secrets | VM `.env` | Twitch app creds + OBS WebSocket password. Never opened on stream. Stream key stays in OBS on the Mac. |
| Autodesk | Mac, "stream" user | Fusion/AutoCAD don't run on Linux. Dedicated macOS user keeps personal stuff out of frame. |

## Cost notes
- Hetzner bills stopped servers. Only delete stops billing (snapshot → delete → recreate is possible but not worth it at ~$18/mo).

## Upgrade path
If home upload is the bottleneck: move OBS to a GPU cloud box and send cam/mic from the Mac via VDO.Ninja (browser source).
