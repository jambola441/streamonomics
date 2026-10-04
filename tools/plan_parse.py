#!/usr/bin/env python3
"""Parse a project plan.md into JSON so /sync-plan works from a deterministic view.

usage:
  plan_parse.py <path/to/plan.md>   # one plan -> JSON object
  plan_parse.py --all               # every projects/*/plan.md (skips _template) -> JSON list

Every issue found lands in `warnings` as {line, level, message}. level "error"
means the structure is broken (or unsafe to sync) and the exit code is 1.
level "warning" is informational. Exit 2 = usage / file problems.

Stdlib only. The format is documented in projects/README.md.
"""
import json
import re
import sys
from pathlib import Path

STATUSES = {"idea", "active", "paused", "shipped", "archived"}
SLOTS = {"tue", "thu", "weekend", "any"}
REQUIRED_FM = ["name", "slug", "status", "slot", "linear.team", "linear.project"]

CHECKBOX_RE = re.compile(r"^- \[( |x|X)\] (.*)$")
# Near-misses of a top-level checkbox: "-[ ]", "* [ ]", "- []", "- [x]no-space", ...
LOOSE_CHECKBOX_RE = re.compile(r"^[-*+]\s*\[[^\]]?\]")
NESTED_CHECKBOX_RE = re.compile(r"^\s+[-*+]\s*\[[ xX]?\]")
ID_RE = re.compile(r"\[([A-Z][A-Z0-9]*-\d+)\](?!\()")
ID_LIKE_RE = re.compile(r"\[([A-Za-z][A-Za-z0-9]*-[^\]\s]*)\](?!\()")
CODE_SPAN_RE = re.compile(r"`([^`]*)`")
TAG_KEY_RE = re.compile(r"^(est|slot):(.*)$")
EST_RE = re.compile(r"^\d+(\.\d+)?$")
MILESTONE_COMMENT_RE = re.compile(r"\s*<!--\s*linear-milestone:\s*([^\s>]*)\s*-->\s*$")
PLACEHOLDER_RE = re.compile(r"^TODO:")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


class Plan:
    def __init__(self, path):
        self.path = str(path)
        self.warnings = []

    def warn(self, line, message, level="warning"):
        self.warnings.append({"line": line, "level": level, "message": message})

    def error(self, line, message):
        self.warn(line, message, "error")


# --------------------------------------------------------------------------- #
# Frontmatter: a tiny YAML subset. `key: value`, nested maps by indentation,
# `# comments`, optional quotes. Empty / null / ~ values become None.
# --------------------------------------------------------------------------- #
FM_LINE_RE = re.compile(r"^( *)([A-Za-z0-9_.-]+):(?:\s+(.*))?$")


def _scalar(raw):
    raw = raw.strip()
    if raw[:1] in ("'", '"'):
        q = raw[0]
        end = raw.find(q, 1)
        if end != -1:
            return raw[1:end]
    raw = re.sub(r"(^|\s)#.*$", "", raw).strip()
    if raw in ("", "~", "null"):
        return None
    return raw


def parse_frontmatter(lines, plan):
    """lines: list of (lineno, text). Returns (dict, {dotted.key: lineno})."""
    root = {}
    key_lines = {}
    # frame: [indent, dict, child_indent, dotted_prefix]
    stack = [[-1, root, None, ""]]
    placeholders = []  # (parent, key, dict) for keys whose value was empty
    for lineno, text in lines:
        if not text.strip() or text.lstrip().startswith("#"):
            continue
        if "\t" in text[: len(text) - len(text.lstrip())]:
            plan.error(lineno, "frontmatter: tabs in indentation")
            continue
        m = FM_LINE_RE.match(text)
        if not m:
            plan.error(lineno, f"frontmatter: can't parse line: {text.strip()!r}")
            continue
        indent, key, raw = len(m.group(1)), m.group(2), m.group(3) or ""
        while stack[-1][0] >= indent:
            stack.pop()
        frame = stack[-1]
        if frame[2] is None:
            frame[2] = indent
        elif frame[2] != indent:
            plan.error(lineno, "frontmatter: inconsistent indentation")
            continue
        parent, dotted = frame[1], frame[3] + key
        if key in parent:
            plan.error(lineno, f"frontmatter: duplicate key {dotted!r}")
        key_lines[dotted] = lineno
        value = _scalar(raw) if raw.strip() else None
        if value is None:
            child = {}
            parent[key] = child
            placeholders.append((parent, key, child))
            stack.append([indent, child, None, dotted + "."])
        else:
            parent[key] = value
    for parent, key, child in placeholders:
        if not child:
            parent[key] = None
    return root, key_lines


def _get(d, dotted):
    for part in dotted.split("."):
        if not isinstance(d, dict) or part not in d:
            return None
        d = d[part]
    return d


# --------------------------------------------------------------------------- #
# Deliverable line: "- [ ] Title [ABC-1] `est:3` `slot:tue`"
# --------------------------------------------------------------------------- #
def parse_item_text(text, lineno, plan, check_tags=True):
    ids = ID_RE.findall(text)
    for m in ID_LIKE_RE.finditer(text):
        if not ID_RE.fullmatch(m.group(0)):
            plan.error(lineno, f"malformed issue ID {m.group(0)!r} (expected like [ABC-123])")
    if len(ids) > 1:
        plan.error(lineno, f"more than one issue ID on a line: {ids}")
    est = slot = None
    tag_spans = []
    for m in CODE_SPAN_RE.finditer(text):
        tm = TAG_KEY_RE.match(m.group(1))
        if not tm:
            continue  # ordinary code span, part of the title
        key, val = tm.group(1), tm.group(2).strip()
        tag_spans.append(m.span())
        if not check_tags:
            continue
        if key == "est":
            if not EST_RE.match(val):
                plan.error(lineno, f"bad tag `est:{val}` (expected a number of points)")
            elif est is not None:
                plan.error(lineno, "duplicate `est:` tag")
            else:
                est = float(val) if "." in val else int(val)
        else:
            if val not in SLOTS:
                plan.error(lineno, f"bad tag `slot:{val}` (expected one of {sorted(SLOTS)})")
            elif slot is not None:
                plan.error(lineno, "duplicate `slot:` tag")
            else:
                slot = val
    # Title = text minus tag spans and the ID, whitespace collapsed.
    title = text
    for start, end in sorted(tag_spans, reverse=True):
        title = title[:start] + title[end:]
    title = ID_RE.sub("", title)
    title = re.sub(r"\s+", " ", title).strip()
    return {"title": title, "id": ids[0] if ids else None, "est": est, "slot": slot}


def _dedent(desc):
    while desc and not desc[-1].strip():
        desc.pop()
    indents = [len(l) - len(l.lstrip()) for l in desc if l.strip()]
    cut = min(indents) if indents else 0
    return [l[cut:] if l.strip() else "" for l in desc]


# --------------------------------------------------------------------------- #
# Body
# --------------------------------------------------------------------------- #
def parse(path):
    plan = Plan(path)
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    out = {
        "path": plan.path,
        "frontmatter": {},
        "frontmatter_lines": {},
        "title": None,
        "goal": "",
        "milestones": [],
        "parking_lot": [],
        "counts": {},
        "warnings": plan.warnings,
    }

    # ---- frontmatter
    body_start = 0
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            plan.error(1, "frontmatter: no closing '---'")
            end = 0
        else:
            fm, fm_lines = parse_frontmatter(
                [(i + 1, lines[i]) for i in range(1, end)], plan
            )
            out["frontmatter"], out["frontmatter_lines"] = fm, fm_lines
        body_start = end + 1
    else:
        plan.error(1, "missing frontmatter (file must start with '---')")

    fm = out["frontmatter"]
    for key in REQUIRED_FM:
        if not _get(fm, key):
            plan.error(1, f"frontmatter: missing {key!r}")
    status, fslot = _get(fm, "status"), _get(fm, "slot")
    if status and status not in STATUSES:
        plan.error(out["frontmatter_lines"].get("status", 1),
                   f"frontmatter: status {status!r} not in {sorted(STATUSES)}")
    if fslot and fslot not in SLOTS:
        plan.error(out["frontmatter_lines"].get("slot", 1),
                   f"frontmatter: slot {fslot!r} not in {sorted(SLOTS)}")
    slug = _get(fm, "slug")
    parent_dir = Path(path).resolve().parent.name
    if slug and parent_dir != "_template" and slug != parent_dir:
        plan.warn(out["frontmatter_lines"].get("slug", 1),
                  f"frontmatter: slug {slug!r} doesn't match folder {parent_dir!r}")

    # ---- body
    section = None          # lowercased text of the current "## " heading
    milestone = None        # current milestone dict
    item = None             # current deliverable / parking-lot item (collects sub-bullets)
    goal_lines = []
    in_fence = False
    seen_milestones_section = False

    def close_item():
        nonlocal item
        if item is not None:
            item["description"] = _dedent(item["description"])
            item = None

    for idx in range(body_start, len(lines)):
        lineno, line = idx + 1, lines[idx]

        if FENCE_RE.match(line):
            in_fence = not in_fence
            if section == "goal":
                goal_lines.append(line)
            continue
        if in_fence:
            if section == "goal":
                goal_lines.append(line)
            elif item is not None:
                item["description"].append(line)
            continue

        if line.startswith("# ") and not line.startswith("## "):
            close_item()
            if out["title"] is None:
                out["title"] = line[2:].strip()
            continue

        if line.startswith("## "):
            close_item()
            milestone = None
            section = line[3:].strip().lower()
            if section == "milestones":
                if seen_milestones_section:
                    plan.error(lineno, "more than one '## Milestones' section")
                seen_milestones_section = True
            continue

        if section == "goal":
            goal_lines.append(line)
            continue

        if line.startswith("### "):
            close_item()
            if section != "milestones":
                milestone = None
                continue
            heading = line[4:]
            cm = MILESTONE_COMMENT_RE.search(heading)
            if cm:
                mid = cm.group(1) or None
                heading = heading[: cm.start()]
            else:
                mid = None
                plan.warn(lineno, "milestone heading has no <!-- linear-milestone: --> comment "
                                  "(sync will add one)")
            milestone = {
                "title": heading.strip(),
                "linear_milestone_id": mid,
                "has_comment": bool(cm),
                "line": lineno,
                "deliverables": [],
            }
            out["milestones"].append(milestone)
            continue

        # Indented continuation of the current item (sub-bullets / description)
        if item is not None and (line.startswith((" ", "\t")) or not line.strip()):
            if NESTED_CHECKBOX_RE.match(line) and section == "milestones":
                plan.warn(lineno, "nested checkbox is treated as description text, not an issue")
            item["description"].append(line)
            continue
        close_item()

        if not line.strip() or line.lstrip().startswith("<!--"):
            continue

        cb = CHECKBOX_RE.match(line)
        if section == "parking lot":
            pm = re.match(r"^[-*+] (?:\[[ xX]\] )?(.*)$", line)
            if pm:
                parsed = parse_item_text(pm.group(1), lineno, plan, check_tags=False)
                item = {"text": pm.group(1).strip(), "id": parsed["id"],
                        "line": lineno, "description": []}
                out["parking_lot"].append(item)
            continue

        if not cb:
            if LOOSE_CHECKBOX_RE.match(line):
                plan.error(lineno, f"malformed checkbox: {line.strip()!r} (use '- [ ] ' or '- [x] ')")
            elif section == "milestones" and line.startswith(("- ", "* ", "+ ")):
                plan.warn(lineno, "plain bullet under a milestone is ignored (not a checkbox)")
            continue

        if section != "milestones":
            where = f"section '## {section}'" if section else "before any '##' section"
            plan.warn(lineno, f"checkbox {where} is not synced")
            continue
        if milestone is None:
            plan.error(lineno, "checkbox under '## Milestones' but before any '### ' milestone")
            continue

        parsed = parse_item_text(cb.group(2), lineno, plan)
        if not parsed["title"]:
            plan.error(lineno, "deliverable has no title")
        elif PLACEHOLDER_RE.match(parsed["title"]):
            plan.error(lineno, "placeholder deliverable (starts with 'TODO:'); "
                               "write the real one before syncing")
        item = {
            "title": parsed["title"],
            "done": cb.group(1) in "xX",
            "id": parsed["id"],
            "est": parsed["est"],
            "slot": parsed["slot"],
            "description": [],
            "line": lineno,
            "raw": line,
        }
        milestone["deliverables"].append(item)

    close_item()
    if in_fence:
        plan.error(len(lines), "unclosed code fence")

    out["goal"] = "\n".join(goal_lines).strip()
    if not seen_milestones_section:
        plan.warn(1, "no '## Milestones' section")

    # ---- cross checks
    seen_ids = {}
    for m in out["milestones"]:
        for d in m["deliverables"]:
            if d["id"]:
                if d["id"] in seen_ids:
                    plan.error(d["line"], f"duplicate issue ID {d['id']} "
                                          f"(also on line {seen_ids[d['id']]})")
                else:
                    seen_ids[d["id"]] = d["line"]
    for p in out["parking_lot"]:
        if p["id"] and p["id"] in seen_ids:
            plan.error(p["line"], f"issue ID {p['id']} is in both the parking lot "
                                  f"and line {seen_ids[p['id']]}")
    seen_titles, seen_mids = {}, {}
    for m in out["milestones"]:
        if not m["title"]:
            plan.error(m["line"], "milestone has no title")
        key = m["title"].lower()
        if key in seen_titles:
            plan.error(m["line"], f"duplicate milestone title {m['title']!r} "
                                  f"(also line {seen_titles[key]})")
        seen_titles.setdefault(key, m["line"])
        if m["linear_milestone_id"]:
            if m["linear_milestone_id"] in seen_mids:
                plan.error(m["line"], "duplicate linear-milestone ID")
            seen_mids.setdefault(m["linear_milestone_id"], m["line"])

    ds = [d for m in out["milestones"] for d in m["deliverables"]]
    out["counts"] = {
        "milestones": len(out["milestones"]),
        "deliverables": len(ds),
        "done": sum(d["done"] for d in ds),
        "unsynced": sum(1 for d in ds if not d["id"]),
        "parking_lot": len(out["parking_lot"]),
    }
    out["warnings"].sort(key=lambda w: w["line"])
    return out


def has_errors(result):
    return any(w["level"] == "error" for w in result["warnings"])


def main(argv):
    if len(argv) != 1 or argv[0] in ("-h", "--help"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    if argv[0] == "--all":
        root = Path(__file__).resolve().parent.parent / "projects"
        paths = sorted(p for p in root.glob("*/plan.md") if not p.parent.name.startswith("_"))
        results = [parse(p) for p in paths]
        for r in results:
            r["path"] = str(Path(r["path"]).resolve().relative_to(root.parent))
        print(json.dumps(results, indent=2))
        return 1 if any(has_errors(r) for r in results) else 0
    path = Path(argv[0])
    if not path.is_file():
        print(f"plan_parse: no such file: {path}", file=sys.stderr)
        return 2
    result = parse(path)
    print(json.dumps(result, indent=2))
    return 1 if has_errors(result) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
