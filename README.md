# Streamonomics

> One person. A stack of AI tools. Real work, done live.

## The story

Everyone's arguing about whether AI can actually *do the work*. Streamonomics doesn't argue about it. It just shows it: live, unedited, on real projects that real people pay for.

Most coding streams are either polished tutorials or someone grinding through a side project alone. This is neither. It's a working session: **one operator running Claude and friends like a small team**, switching between whatever the business needs that day:

- **Build**: web apps, internal tools, automations, APIs. From idea to deployed URL.
- **Make**: physical stuff in Autodesk (Fusion/AutoCAD). Parts, enclosures, fixtures, things that get printed or cut.
- **Grow**: marketing for an actual business. Landing pages, copy, ads, emails, content calendars, analytics.

The hook is **"Claude-maxxing"**: how far can one person push AI leverage on real work? Every stream asks the same question: *what would this have cost a team, and how long did it take us?* That's the "-onomics." We track the time, the tool spend, and what got shipped, and we keep score in public.

### Why people watch
1. **It's real.** Real clients, real deadlines, real bugs. Failures stay in.
2. **It's useful.** Viewers see prompts, workflows, and tool setups they can steal for their own jobs.
3. **They can shape it.** Chat throws in ideas, votes on what to build next, and roasts bad prompts.
4. **It has stakes and a scoreboard.** A running ledger of hours saved, dollars spent, and things shipped.

### Recurring formats
| Format | What it is |
|---|---|
| **Ship It** | Take a project from zero to deployed in one stream. |
| **The Grind** | Long working session on an ongoing project. Chill and steady. |
| **Shop Floor** | Autodesk / physical build day. |
| **Growth Lab** | Marketing sprint for a business: copy, funnels, ads, numbers. |
| **Chat Builds It** | Chat pitches, votes, and we build the winner. |
| **The Ledger** | Weekly recap: what shipped, time and money spent, lessons learned. |

## This repo: the control station

Everything that runs the channel lives here.

```
streamonomics/
├── README.md          # this: the story / pitch
├── PLAN.md            # the roadmap to launch and beyond
├── CLAUDE.md          # how Claude should work inside this repo
├── stream/            # the broadcast itself
│   ├── obs/           #   scene layouts, profiles, settings notes
│   ├── overlays/      #   browser-source overlays (HTML/CSS)
│   ├── bot/           #   chat bot commands, alerts, integrations
│   ├── checklists/    #   pre-stream / post-stream run sheets
│   ├── branding.md    #   name, voice, colors, panels
│   └── schedule.md    #   when we're live and what format
├── projects/          # one folder per thing we build on stream
│   └── _template/
├── ideas/             # ideation: inbox → backlog → promoted to a project
├── episodes/          # one log per stream (what happened, clip timestamps)
│   └── _template/
├── content/           # repurposing: clips, shorts, posts, metrics
└── tools/             # scripts that run the station
```

### Quick commands
```bash
tools/new-project.sh my-cool-app                      # scaffold projects/my-cool-app
tools/new-episode.sh "Ship It: invoice app"           # create today's episode log
tools/new-idea.sh "AI quote generator for the shop"   # drop an idea in the inbox
```
