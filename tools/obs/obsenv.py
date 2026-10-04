"""Shared helpers for the tools/obs scripts: read .env and open an obs-websocket client."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                v = v.split(" #", 1)[0]
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    missing = [k for k in ("OBS_HOST", "OBS_PASSWORD") if not os.environ.get(k)]
    if missing:
        sys.exit(f"missing {', '.join(missing)} in .env (see .env.example)")


def client():
    import obsws_python as obs
    load_env()
    return obs.ReqClient(host=os.environ["OBS_HOST"], port=int(os.environ.get("OBS_PORT", 4455)),
                         password=os.environ["OBS_PASSWORD"], timeout=10)
