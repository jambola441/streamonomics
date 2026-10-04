#!/usr/bin/env python3
"""Small OBS remote control for Claude on the stage VM (seed of `sm obs`, STR-6).

    obsctl.py status                 current scene, recording/streaming state, fps, dropped frames
    obsctl.py scenes                 list scenes
    obsctl.py scene "<name>"         switch scene (mutes the mic on card scenes, unmutes elsewhere)
    obsctl.py record start|stop      start/stop local recording (stop prints the file path on the Mac)
    obsctl.py shot [out.png]         screenshot of the live program output, saved on the VM
    obsctl.py mic on|off             unmute/mute the mic

Run with the venv that has obsws-python:  ~/.venvs/obs/bin/python tools/obs/obsctl.py status
Never prints the WebSocket password.
"""
import base64
import os
import sys
import time
from pathlib import Path

from obsenv import client

CARD_SCENES = {"Starting Soon", "BRB", "Ending"}   # mic muted on these


def mic_name(cl):
    if os.environ.get("OBS_MIC"):
        return os.environ["OBS_MIC"]
    for i in cl.get_input_list(None).inputs:
        if "coreaudio_input" in i["inputKind"] or "input_capture" in i["inputKind"]:
            return i["inputName"]
    return None


def current_scene(cl):
    r = cl.get_current_program_scene()
    return getattr(r, "scene_name", None) or r.current_program_scene_name


def cmd_status(cl):
    rec, stream, st = cl.get_record_status(), cl.get_stream_status(), cl.get_stats()
    print(f"scene: {current_scene(cl)}")
    print(f"recording: {'ON ' + rec.output_timecode if rec.output_active else 'off'}")
    print(f"streaming: {'ON ' + stream.output_timecode if stream.output_active else 'off'}")
    print(f"fps: {st.active_fps:.1f}  cpu: {st.cpu_usage:.1f}%  "
          f"skipped render/output frames: {st.render_skipped_frames}/{st.output_skipped_frames}")
    mic = mic_name(cl)
    if mic:
        print(f"mic ({mic}): {'MUTED' if cl.get_input_mute(mic).input_muted else 'live'}")


def cmd_scene(cl, name):
    names = [s["sceneName"] for s in cl.get_scene_list().scenes]
    if name not in names:
        sys.exit(f"no scene {name!r}; have: {', '.join(names)}")
    cl.set_current_program_scene(name)
    mic = mic_name(cl)
    if mic:
        cl.set_input_mute(mic, name in CARD_SCENES)
    print(f"scene -> {name}" + (f" (mic {'muted' if name in CARD_SCENES else 'live'})" if mic else ""))


def cmd_shot(cl, out):
    data = cl.get_source_screenshot(current_scene(cl), "png", 1920, 1080, -1).image_data
    Path(out).write_bytes(base64.b64decode(data.split(",", 1)[1]))
    print(f"saved {out}")


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cl, cmd, args = client(), argv[0], argv[1:]
    if cmd == "status":
        cmd_status(cl)
    elif cmd == "scenes":
        print("\n".join(s["sceneName"] for s in reversed(cl.get_scene_list().scenes)))
    elif cmd == "scene" and args:
        cmd_scene(cl, " ".join(args))
    elif cmd == "record" and args[:1] == ["start"]:
        cl.start_record(); print("recording started")
    elif cmd == "record" and args[:1] == ["stop"]:
        print(f"recording saved on the Mac: {cl.stop_record().output_path}")
    elif cmd == "shot":
        cmd_shot(cl, args[0] if args else f"/tmp/obs-shot-{int(time.time())}.png")
    elif cmd == "mic" and args[:1] in (["on"], ["off"]):
        mic = mic_name(cl) or sys.exit("no mic input found (set OBS_MIC in .env)")
        cl.set_input_mute(mic, args[0] == "off"); print(f"mic {args[0]}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
