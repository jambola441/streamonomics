#!/usr/bin/env bash
# Scaffold a new project from projects/_template.
# usage: new-project.sh <slug> ["Display Name"] [slot]
#   slug: lowercase-with-hyphens; name defaults to the slug title-cased; slot: tue | thu | weekend | any (default any)
set -euo pipefail
usage='usage: new-project.sh <slug> ["Display Name"] [tue|thu|weekend|any]'
slug="${1:?$usage}"
name="${2:-}"
slot="${3:-any}"
[[ "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "slug must be lowercase letters, digits, hyphens" >&2; exit 1; }
case "$slot" in tue|thu|weekend|any) ;; *) echo "slot must be tue, thu, weekend, or any" >&2; exit 1 ;; esac
[[ -n "$name" ]] || name="$(printf '%s' "$slug" | awk -F- '{for (i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1' OFS=' ')"

root="$(cd "$(dirname "$0")/.." && pwd)"
tpl="$root/projects/_template"
dest="$root/projects/$slug"
[[ -e "$dest" ]] && { echo "projects/$slug already exists" >&2; exit 1; }

today="$(date +%F)"
esc() { printf '%s' "$1" | sed 's/[\/&|\\]/\\&/g'; }
s_name="$(esc "$name")"

mkdir -p "$dest"
(cd "$tpl" && find . -mindepth 1 -print) | while IFS= read -r rel; do
  rel="${rel#./}"
  if [[ -d "$tpl/$rel" ]]; then
    mkdir -p "$dest/$rel"
  elif [[ "$rel" == *.md ]]; then
    sed -e "s/__NAME__/$s_name/g" -e "s/__SLUG__/$slug/g" \
        -e "s/__DATE__/$today/g" -e "s/__SLOT__/$slot/g" "$tpl/$rel" > "$dest/$rel"
  else
    cp "$tpl/$rel" "$dest/$rel"
  fi
done
echo "created projects/$slug ($name, slot: $slot)"
echo "next: fill in plan.md, add a row to projects/README.md, then /sync-plan $slug"
