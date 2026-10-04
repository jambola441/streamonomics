# Stream Manager: Log

One `## YYYY-MM-DD` heading per day, freeform bullets, newest at the bottom. Issue IDs optional.

## 2026-10-03
- Did: architecture and skill list drafted (off-stream)
- Next: decide build-live vs. pre-build; start v0 `sm` CLI + state.json

## 2026-10-04
- Stage VM `stage` live on Hetzner fsn1 (cx43). Tailscale joined on VM + Mac.
- Public SSH closed (`tools/hetzner/lockdown.sh`); VM reachable only via `ssh stream@stage` over Tailscale.
- STR-15, STR-16 done.
- `tools/vm-setup.sh` run on the VM; Claude Code installed and logged in (STR-18 done).
- Merged everything to `main` ([jambola441/streamonomics#1](https://github.com/jambola441/streamonomics/pull/1)).
- NoMachine (paid subscription) working: XFCE desktop on `stage` from the Mac. Fix needed: `DefaultDesktopCommand "/usr/bin/startxfce4"` in `/usr/NX/etc/node.cfg` (STR-17 done).
- OBS on the Mac: Main built by hand (NoMachine window + camera + mic with RNNoise/compressor/limiter); WebSocket on; the VM Claude built Code, Chatting, Starting Soon, BRB, Ending with `tools/obs/setup_scenes.py` (STR-19 done). First time Claude drove OBS.
