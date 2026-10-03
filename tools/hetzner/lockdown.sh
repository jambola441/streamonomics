#!/usr/bin/env bash
# After `sudo tailscale up` works on the stage: close public SSH so the VM is reachable only over Tailscale.
set -euo pipefail
hcloud firewall delete-rule stage-fw --direction in --protocol tcp --port 22 --source-ips 0.0.0.0/0 --source-ips ::/0 --description ssh-bootstrap
echo "public SSH closed; use: ssh stream@stage (Tailscale MagicDNS)"
