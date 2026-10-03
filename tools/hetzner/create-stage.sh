#!/usr/bin/env bash
# Create the Streamonomics stage VM on Hetzner. Needs HCLOUD_TOKEN and an SSH key already uploaded to Hetzner.
# usage: tools/hetzner/create-stage.sh <hetzner-ssh-key-name> [server-type] [location]
set -euo pipefail
key="${1:?usage: create-stage.sh <ssh-key-name> [type] [location]}"
type="${2:-cx43}"
loc="${3:-nbg1}"
name="stage"
here="$(cd "$(dirname "$0")" && pwd)"

hcloud firewall describe stage-fw >/dev/null 2>&1 || {
  hcloud firewall create --name stage-fw
  # SSH only until Tailscale is up; then tools/hetzner/lockdown.sh removes it.
  hcloud firewall add-rule stage-fw --direction in --protocol tcp --port 22 --source-ips 0.0.0.0/0 --source-ips ::/0 --description ssh-bootstrap
  hcloud firewall add-rule stage-fw --direction in --protocol udp --port 41641 --source-ips 0.0.0.0/0 --source-ips ::/0 --description tailscale-direct
}

hcloud server create --name "$name" --type "$type" --location "$loc" --image ubuntu-24.04 \
  --ssh-key "$key" --firewall stage-fw --user-data-from-file "$here/cloud-init.yaml" \
  --label app=streamonomics --label role=stage
hcloud server ip "$name"
