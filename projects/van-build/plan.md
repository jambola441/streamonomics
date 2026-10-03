---
name: Van Build-Out
slug: van-build
status: active          # idea | active | paused | shipped | archived
slot: weekend           # tue | thu | weekend | any
linear:
  team: Streamonomics
  project: Van Build-Out
  project_id:           # written by /sync-plan
---
# Van Build-Out: Plan

## Goal
TODO: define done. Weekend-trip ready, or full-time livable?

## Transit notes
The van is a **Ford Transit**, so Transit-specific considerations apply to every milestone below:
- **Roof height** (low / medium / high) sets standing room, upper cabinets, and how much insulation you can afford to lose.
- **Wheelbase / length** (130" / 148" / 148" EL) sets the floor plan, bed orientation, and tank placement.
- **Factory mounting points** (rib and pillar threaded holes, floor tie-downs): design furniture and the electrical bay around them instead of drilling the body.

## Milestones

### Design <!-- linear-milestone: -->
- [ ] Confirm the Transit config and current state
  - model year, roof height, wheelbase
  - what's already done (and what's staying)
- [ ] Floor plan / layout in AutoCAD or Fusion
  - drawn on the real interior dimensions for this roof + wheelbase
  - export to `assets/`
- [ ] Electrical system design: battery, solar, inverter, load budget
  - load budget table, battery and solar sizing math
  - wiring diagram exported to `assets/`
- [ ] Running BOM + spend ledger
  - tracked against a shop quote for the same build

### Systems <!-- linear-milestone: -->
- [ ] Electrical install
  - follows the wiring diagram from Design
  - mounted to factory points where possible

### Build <!-- linear-milestone: -->
- [ ] Insulation, walls, floor
- [ ] Furniture and cabinetry: Fusion models + cut lists
  - designed around factory mounting points
- [ ] Furniture and cabinetry: build and install

## Parking lot
<!-- not synced to Linear -->
- IRL build-day streams (needs a mobile / second-camera setup)
