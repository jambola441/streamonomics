#!/usr/bin/env bash
# Scaffold a new project from projects/_template.
set -euo pipefail
slug="${1:?usage: new-project.sh <slug>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$root/projects/$slug"
[[ -e "$dest" ]] && { echo "projects/$slug already exists" >&2; exit 1; }
mkdir -p "$dest"
today="$(date +%F)"
for f in "$root"/projects/_template/*.md; do
  sed -e "s/__NAME__/$slug/g" -e "s/__DATE__/$today/g" "$f" > "$dest/$(basename "$f")"
done
echo "created projects/$slug (add it to projects/README.md)"
