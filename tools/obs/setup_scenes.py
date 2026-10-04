#!/usr/bin/env python3
"""Build the standard Streamonomics scenes in OBS over obs-websocket v5.

Run on the stage VM (it reaches OBS on the Mac over Tailscale):
    python3 -m venv ~/.venvs/obs && ~/.venvs/obs/bin/pip install obsws-python
    ~/.venvs/obs/bin/python tools/obs/setup_scenes.py            # dry run: prints the plan
    ~/.venvs/obs/bin/python tools/obs/setup_scenes.py --apply    # builds it

Needs OBS_HOST, OBS_PORT, OBS_PASSWORD in the repo's .env (see .env.example).
Expects a scene named "Main" that already has the VM screen capture and the camera.
Idempotent: existing scenes and sources are left alone, so re-running is safe.
"""
import os
import sys
from pathlib import Path

import obsws_python as obs

ROOT = Path(__file__).resolve().parents[2]
BG_COLOR = 0xFF14110F          # OBS colors are ABGR: opaque, near-black
TEXT_FONT = {"face": "Helvetica", "size": 96, "style": "Bold"}

# Scene name -> headline text for the card scenes.
CARDS = {
    "Starting Soon": "Starting soon\ngeneric_tech",
    "BRB": "Be right back",
    "Ending": "Thanks for watching\nTue & Thu evenings + weekends",
}


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    missing = [k for k in ("OBS_HOST", "OBS_PASSWORD") if not os.environ.get(k)]
    if missing:
        sys.exit(f"missing {', '.join(missing)} in .env (see .env.example)")


def find_sources(cl):
    """Find the screen-capture and camera inputs already used in Main."""
    items = cl.get_scene_item_list("Main").scene_items
    screen = camera = None
    for it in items:
        kind = (it.get("inputKind") or "").lower()
        name = it["sourceName"]
        if "screen_capture" in kind or "window_capture" in kind or "display_capture" in kind:
            screen = screen or name
        elif "av_capture" in kind or "avcapture" in kind or "camera" in kind or "video_capture" in kind:
            camera = camera or name
    return screen, camera


def fit(cl, scene, source, x, y, w, h):
    """Scale a source to fit inside the box (x, y, w, h), keeping aspect ratio."""
    item_id = cl.get_scene_item_id(scene, source).scene_item_id
    cl.set_scene_item_transform(scene, item_id, {
        "positionX": x, "positionY": y,
        "boundsType": "OBS_BOUNDS_SCALE_INNER",
        "boundsWidth": w, "boundsHeight": h,
        "boundsAlignment": 0,
    })


def main():
    apply = "--apply" in sys.argv
    load_env()
    cl = obs.ReqClient(host=os.environ["OBS_HOST"], port=int(os.environ.get("OBS_PORT", 4455)),
                       password=os.environ["OBS_PASSWORD"], timeout=10)
    vs = cl.get_video_settings()
    W, H = vs.base_width, vs.base_height
    scenes = {s["sceneName"] for s in cl.get_scene_list().scenes}
    inputs = {i["inputName"]: i["inputKind"] for i in cl.get_input_list().inputs}
    if "Main" not in scenes:
        sys.exit('no "Main" scene found; build Main (screen capture + camera) first')
    screen, camera = find_sources(cl)
    print(f"canvas {W}x{H} | screen source: {screen!r} | camera source: {camera!r}")
    if not screen or not camera:
        sys.exit("couldn't identify the screen-capture and camera sources in Main")

    # Pick the text source kind this OBS build supports.
    kinds = set(cl.get_input_kind_list(False).input_kinds)
    text_kind = next(k for k in ("text_ft2_source_v2", "text_gdiplus_v3", "text_gdiplus_v2") if k in kinds)

    plan = []
    if "Code" not in scenes:
        plan.append(("Code", [("ref", screen, (0, 0, W, H))]))
    if "Chatting" not in scenes:
        plan.append(("Chatting", [
            ("ref", camera, (W * 0.05, H * 0.08, W * 0.9, H * 0.84)),
        ]))
    for scene, text in CARDS.items():
        if scene not in scenes:
            plan.append((scene, [("bg",), ("text", f"{scene} text", text)]))

    if not plan:
        print("all scenes already exist; nothing to do")
        return
    for scene, parts in plan:
        print(f"+ scene {scene!r}: " + ", ".join(p[1] if len(p) > 1 else "background" for p in parts))
    if not apply:
        print("\ndry run; re-run with --apply to build")
        return

    for scene, parts in plan:
        cl.create_scene(scene)
        for part in parts:
            if part[0] == "ref":
                _, src, (x, y, w, h) = part
                cl.create_scene_item(scene, src, True)
                fit(cl, scene, src, x, y, w, h)
            elif part[0] == "bg":
                name = "Card background"
                if name not in inputs:
                    cl.create_input(scene, name, "color_source_v3",
                                    {"color": BG_COLOR, "width": W, "height": H}, True)
                    inputs[name] = "color_source_v3"
                else:
                    cl.create_scene_item(scene, name, True)
            elif part[0] == "text":
                _, name, text = part
                if name not in inputs:
                    cl.create_input(scene, name, text_kind,
                                    {"text": text, "font": TEXT_FONT, "color1": 0xFFFFFFFF, "color2": 0xFFFFFFFF},
                                    True)
                    inputs[name] = text_kind
                else:
                    cl.create_scene_item(scene, name, True)
                fit(cl, scene, name, W * 0.1, H * 0.35, W * 0.8, H * 0.3)
        print(f"built {scene!r}")
    print("done. BRB mic muting is handled by `sm obs` when it switches scenes (v1).")


if __name__ == "__main__":
    main()
