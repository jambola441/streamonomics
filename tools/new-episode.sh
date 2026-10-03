#!/usr/bin/env bash
# Create today's episode log from episodes/_template.
set -euo pipefail
title="${1:?usage: new-episode.sh \"<title>\"}"
root="$(cd "$(dirname "$0")/.." && pwd)"
today="$(date +%F)"
slug="$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g')"
dest="$root/episodes/$today-$slug.md"
[[ -e "$dest" ]] && { echo "episodes/$today-$slug.md already exists" >&2; exit 1; }
safe_title="$(printf '%s' "$title" | sed 's/[\/&]/\\&/g')"
sed -e "s/__TITLE__/$safe_title/g" -e "s/__DATE__/$today/g" "$root/episodes/_template/episode.md" > "$dest"
echo "created episodes/$today-$slug.md"
