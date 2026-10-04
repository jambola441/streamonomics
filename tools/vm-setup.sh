#!/usr/bin/env bash
# Bootstrap the Streamonomics stage VM (STR-18). Run on the VM as the `stream` user:
#   curl -fsSL https://raw.githubusercontent.com/jambola441/streamonomics/claude/tender-goldberg-2m9ybu/tools/vm-setup.sh | bash
# or, from a clone:  bash tools/vm-setup.sh
# Safe to re-run: every step checks before it acts.
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/jambola441/streamonomics.git}"
REPO_DIR="${REPO_DIR:-$HOME/streamonomics}"
# Work lives on this branch until it is merged to main.
REPO_BRANCH="${REPO_BRANCH:-claude/tender-goldberg-2m9ybu}"

step() { printf '\n==> %s\n' "$*"; }

step "Base packages"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  build-essential git curl jq ripgrep tmux unzip ca-certificates \
  python3 python3-venv python3-pip fonts-jetbrains-mono

step "Node.js 22 (NodeSource)"
if ! command -v node >/dev/null || [[ "$(node -v)" != v22* ]]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt-get install -y -qq nodejs
fi
node -v

step "Browser (Firefox)"
command -v firefox >/dev/null || sudo snap install firefox || echo "firefox install skipped (no snapd?)"

step "Claude Code"
if ! command -v claude >/dev/null; then
  curl -fsSL https://claude.ai/install.sh | bash
fi
grep -q '.local/bin' "$HOME/.bashrc" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
export PATH="$HOME/.local/bin:$PATH"
claude --version || echo "claude installed; open a new shell, then run: claude  (log in once)"

step "This repo"
if [[ -d "$REPO_DIR/.git" ]]; then
  git -C "$REPO_DIR" pull --ff-only || echo "pull skipped (local changes?)"
else
  git clone -b "$REPO_BRANCH" "$REPO_URL" "$REPO_DIR"
fi

step "Host firewall: SSH only over Tailscale"
# Cloud firewall already blocks public 22; this makes the VM itself agree.
sudo ufw allow in on tailscale0 >/dev/null
sudo ufw delete allow 22/tcp >/dev/null 2>&1 || true
sudo ufw status | head -n 8

step "Done"
cat <<'EOF'
Next:
  1. New shell, then `claude` in ~/streamonomics and log in (do this off-stream).
  2. git identity: git config --global user.name "..." && git config --global user.email "..."
  3. Remote desktop (STR-17): install NoMachine from https://www.nomachine.com/download (Linux .deb, amd64).
EOF
