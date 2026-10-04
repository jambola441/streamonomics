# OBS

Export scene collections and profiles here (OBS → Scene Collection → Export) so the layout is versioned.

Planned scenes: `Starting Soon`, `Main (screen + cam)`, `Full Screen Code`, `Just Chatting`, `BRB`, `Ending`.

Once encoder and bitrate settings are tuned, write them down in `settings.md`.

## Let Claude build the scenes
After building **Main** by hand (VM window capture + camera + mic) and enabling **Tools → WebSocket Server Settings** on the Mac:

On the VM:
```bash
cd ~/streamonomics && cp .env.example .env && nano .env      # OBS_HOST = the Mac's Tailscale name, OBS_PASSWORD
python3 -m venv ~/.venvs/obs && ~/.venvs/obs/bin/pip install obsws-python
~/.venvs/obs/bin/python tools/obs/setup_scenes.py            # dry run
~/.venvs/obs/bin/python tools/obs/setup_scenes.py --apply    # builds Code, Chatting, Starting Soon, BRB, Ending
```
Safe to re-run; existing scenes are left alone.
