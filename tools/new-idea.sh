#!/usr/bin/env bash
# Append an idea to ideas/inbox.md.
set -euo pipefail
[[ $# -gt 0 ]] || { echo "usage: new-idea.sh <idea text>" >&2; exit 1; }
root="$(cd "$(dirname "$0")/.." && pwd)"
echo "- $* _($(date +%F))_" >> "$root/ideas/inbox.md"
echo "added to ideas/inbox.md"
