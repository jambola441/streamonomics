# The Rig

Decision and reasoning: `projects/stream-manager/decisions.md` (2026-10-03: Broadcast rig).

```
 Hetzner VM fsn1 (Ubuntu + XFCE) — the stage MacBook (Apple Silicon) — A/V + encoder
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
| Stage VM | Hetzner, Falkenstein (`fsn1`), `cx43`, server name `stage` | 8 vCPU / 16 GB, ~$18/mo. Ubuntu 24.04 + XFCE. Created by `tools/hetzner/create-stage.sh` + `cloud-init.yaml`. US (`ash`) is ~4x the price; the ~100 ms typing lag only affects the remote desktop, not viewers. |
| Remote desktop | VM → Mac | NoMachine (good quality on CPU-only VMs); xrdp as fallback. Capture its window in OBS. |
| Private network | VM ↔ Mac | Tailscale on both. Nothing exposed publicly: overlays and OBS WebSocket only on the tailnet. |
| OBS | Mac | Apple VT hardware encoder. Scenes per `stream/obs/README.md`. WebSocket on, password set. |
| Cam + mic | Mac | Native devices into OBS; audio filters (noise suppression, compressor, limiter). |
| Secrets | VM `.env` | Twitch app creds + OBS WebSocket password. Never opened on stream. Stream key stays in OBS on the Mac. |
| Autodesk | Mac, "stream" user | Fusion/AutoCAD don't run on Linux. Dedicated macOS user keeps personal stuff out of frame. |

## Remote desktop (STR-17): NoMachine
On the VM (`ssh stream@stage`):
1. `sudo passwd stream`: NoMachine logs in with a password. SSH passwords stay disabled, and port 4000 is only reachable over Tailscale.
2. Download the **Linux DEB amd64** link from https://www.nomachine.com/download, then `sudo apt install ./nomachine_*_amd64.deb`.
3. `sudo systemctl set-default multi-user.target && sudo reboot`: no local display, so NoMachine creates a virtual XFCE desktop.

On the Mac: install NoMachine, add a connection to host `stage`, port `4000`, protocol NX, user `stream`.
Check: text is readable at 1080p, and typing latency is tolerable. If NoMachine misbehaves, fall back to `xrdp` + Microsoft's "Windows App".

## Cost notes
- Hetzner bills stopped servers. Only delete stops billing (snapshot → delete → recreate is possible but not worth it at ~$18/mo).

## Upgrade path
If home upload is the bottleneck: move OBS to a GPU cloud box and send cam/mic from the Mac via VDO.Ninja (browser source).
