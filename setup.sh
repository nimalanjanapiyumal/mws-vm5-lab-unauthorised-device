#!/usr/bin/env bash
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Run as root: sudo bash setup.sh"
  exit 1
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPLY_STATIC_IP="${APPLY_STATIC_IP:-yes}"

if [ "$APPLY_STATIC_IP" = "yes" ]; then
  bash "$REPO_DIR/scripts/apply_static_ip.sh"
else
  hostnamectl set-hostname mws-lab-unauth01
fi

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-paho-mqtt mosquitto-clients netcat-openbsd

mkdir -p /opt/mws-lab-test /etc/mws-lab-test
cp "$REPO_DIR/src/unauthorised_device_false_normal_test.py" /opt/mws-lab-test/unauthorised_device_false_normal_test.py
chmod +x /opt/mws-lab-test/unauthorised_device_false_normal_test.py

if [ ! -f /etc/mws-lab-test/lab_test.env ]; then
  cp "$REPO_DIR/config/lab_test.env.example" /etc/mws-lab-test/lab_test.env
  chmod 640 /etc/mws-lab-test/lab_test.env
fi

echo "[DONE] VM5 lab-only unauthorised-device test setup complete."
echo "Run controlled test with: bash scripts/run_lab_unauthorised_test.sh"
