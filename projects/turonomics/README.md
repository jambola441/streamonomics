# Turonomics

- **Pillar:** Build (+ Grow later: selling it to other Turo hosts)
- **Stack / tools:** Chrome extension (Manifest V3, TypeScript), FastAPI (Python 3.12)
- **Repo / link:** [jambola441/turonomics](https://github.com/jambola441/turonomics)

Tuesday evening slot. Goal, milestones, and status: [plan.md](plan.md). Work log: [log.md](log.md). Decisions: [decisions.md](decisions.md).

## What it is
Tooling for Turo hosts to reconcile NY EZPass toll charges against individual rental trips. The extension exports trips from the Turo host dashboard. The API matches toll transactions to trips and returns a per-trip breakdown, including multiple transponders and plates per owner.

## Stream angle
A real small-business pain point: hosts lose money on unbilled tolls. Good "-onomics" story because you can put a dollar figure on recovered tolls.

## On-stream safety
- **Use only `examples/` / synthetic data on screen.** Real trip CSVs, plates, and toll accounts are personal and customer data.
- Don't log into the Turo host dashboard or the EZPass account on stream.
