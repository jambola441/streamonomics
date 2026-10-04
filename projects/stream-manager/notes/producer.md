# Claude as stream producer (v4): design notes

**Idea:** a system watches the stream (chat, audio, video) and, when I say something or a run-sheet cue fires, the right thing happens on its own: scene change, overlay update, a task for the VM Claude session. I keep working; the producer runs the show.

**Core principle:** don't make the expensive model watch. Most of what streams in is noise. Cheap, always-on detectors turn raw signal into *events*; a cheap triage tier decides which events matter; only real work reaches the VM Claude session.

## Layers

```
 SIGNALS            DETECT (cheap, always on)        TRIAGE                     ACT
 chat ───────► chat listener (EventSub/IRC) ──┐
 mic audio ──► VAD → wake word → local STT ───┤──► event bus ──► 1. rules (free)  ──► deterministic action
 video ──────► periodic OBS screenshot checks ┤    (queue)      2. small model    ──►   (sm obs / sm twitch / overlay)
 run sheet ──► timer / condition cues ────────┤                  3. escalate      ──► VM Claude session (real work)
 OBS stats ──► dropped frames, mic muted, … ──┘                                     └► ledger: decision + cost
```

| Layer | What runs | Cost profile |
|---|---|---|
| **Detect** | Non-LLM code: Twitch EventSub/IRC client; voice activity detection + wake word ("producer, …") + local speech-to-text (whisper.cpp) on the VM or Mac; OBS screenshots every N s with cheap checks (black/frozen frame, OCR for secret-looking strings); `obsctl status` polling | ~free (CPU only) |
| **Event bus** | Append-only queue (SQLite or JSONL) of typed events: `voice_command`, `chat_command`, `chat_message`, `cue`, `alert` | free |
| **Triage 1: rules** | Exact matches: `!idea`, "producer, BRB", run-sheet cue → scene change, mic-muted-while-talking alert | free |
| **Triage 2: small model** | Batched, only for ambiguous items: "is this a command? which action?", "any chat question worth answering?" Every N seconds, not per message | low, capped |
| **Triage 3: escalate** | Hand a task to the VM Claude Code session (e.g. "add this feature chat suggested to the backlog", "fix the failing test") | highest; rare by design |
| **Act** | Deterministic actions go straight to `sm` (no LLM). Only open-ended work goes to Claude | n/a |

## Rules of the road
- **Action allowlist.** The producer can only trigger named actions (`scene`, `mic`, `overlay`, `marker`, `idea`, `task`). Anything else is ignored.
- **Chat is untrusted input.** Chat can suggest; it can never directly make Claude run code or change files. Only my voice or my own Twitch account can issue `task` actions. Assume chat will try prompt injection.
- **Budgets.** Per-stream spend cap for triage + escalation; when hit, drop to rules-only. Every model call is logged with its cost to the ledger (this is literally the "-onomics").
- **Kill switch.** "producer, stand down" / `!producer off` from my account stops all automatic actions instantly.
- **Shadow mode first.** The producer logs what it *would* do for a few streams before it's allowed to act.

## Open questions
- Where STT runs: the Mac (where the mic is) vs. the VM (needs the audio sent over). Leaning Mac-side detector that only ships text events.
- Run-sheet format: YAML with time and condition cues, e.g. `at: 00:00 → scene Starting Soon`, `when: shipped → overlay pop`.
- How the VM Claude session receives tasks: a watched queue file vs. a skill that pulls the next task.
