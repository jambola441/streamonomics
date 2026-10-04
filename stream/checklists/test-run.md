# Hands-free test run (STR-21)

Goal: a full practice recording where the only input is talking to Claude, including from your phone.

## Setup (once)
On the VM:
```bash
tmux new -s claude                      # keeps Claude alive when you disconnect
cd ~/streamonomics && claude remote-control
```
Detach with `Ctrl-b d`; reattach later with `tmux attach -t claude`. The session shows up in the Claude app on your phone.
On the Mac: OBS open (WebSocket on), NoMachine connected to `stage`, camera and mic plugged in.

## The prompt (send from your phone)
> Run the STR-21 test run using `stream/checklists/test-run.md` and `tools/obs/obsctl.py`:
> check status, switch to Starting Soon, start recording, wait 20s, switch to Main, then narrate
> what you're doing for ~3 minutes while you summarize `projects/stream-manager/plan.md` in a
> terminal on the stage desktop. Then go Code (30s), Chatting (30s), BRB (20s, confirm the mic is muted),
> Main (30s), Ending (15s), and stop recording. Take a screenshot of each scene, look at them,
> and report: readability, framing, anything private on screen, dropped frames.

## What to check afterwards (on the Mac recording)
- Terminal text readable at normal size
- Voice clear, in sync, silent during BRB
- No notifications, personal tabs, or secrets on screen
