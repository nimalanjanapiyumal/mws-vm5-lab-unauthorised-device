#!/usr/bin/env bash
set -euo pipefail

echo "[CHECK] Hostname and IP"
hostnamectl --static
ip -4 addr | grep -E '192\.168\.1\.50|inet ' || true

echo "[CHECK] Broker reachability"
ping -c 2 192.168.1.10 || true
nc -zv 192.168.1.10 1883 || true

echo "[CHECK] Test script available"
python3 /opt/mws-lab-test/unauthorised_device_false_normal_test.py --help | head

echo "[DONE] VM5 verification complete."
