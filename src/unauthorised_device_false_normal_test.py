#!/usr/bin/env python3
"""Controlled local-lab unauthorised-device test for MWS Assessment 2.

This script does not steal credentials. It uses deliberately provided lab
credentials to demonstrate blocked access, ACL enforcement and the operational
risk of credential misuse in a private lab.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


def getenv(name: str, default: str) -> str:
    return os.environ.get(name, default)


BROKER_HOST = getenv("MQTT_BROKER_HOST", "192.168.1.10")
BROKER_PORT = int(getenv("MQTT_BROKER_PORT", "1883"))
READONLY_USERNAME = getenv("READONLY_USERNAME", "lab_test")
READONLY_PASSWORD = getenv("READONLY_PASSWORD", "ChangeMe-LabTest-2026")
SIM_STOLEN_USERNAME = getenv("SIMULATED_STOLEN_USERNAME", "sensor01")
SIM_STOLEN_PASSWORD = getenv("SIMULATED_STOLEN_PASSWORD", "ChangeMe-Sensor01-2026")
CLIENT_ID = getenv("CLIENT_ID", "mws-lab-unauth01")
TARGET_TOPIC = getenv("TARGET_TOPIC", "mws/water/quality/sensor01/telemetry")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_client(client_id: str, username: str | None, password: str | None) -> mqtt.Client:
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    except AttributeError:
        client = mqtt.Client(client_id=client_id)
    if username is not None:
        client.username_pw_set(username, password)
    return client


def publish_once(username: str | None, password: str | None, label: str) -> bool:
    client = create_client(f"{CLIENT_ID}-{label}", username, password)
    payload = {
        "timestamp_utc": now_iso(),
        "source": "VM5 lab-only unauthorised-device test",
        "test_label": label,
        "simulation_marker": "FALSE_NORMAL_SIMULATION",
        "sensor_id": "sensor01",
        "status": "NORMAL",
        "measurements": {
            "ph": 7.20,
            "turbidity_ntu": 0.90,
            "free_chlorine_mg_l": 0.50,
        },
        "warning": "Controlled lab evidence message, not a real sensor reading.",
    }
    try:
        print(f"[TEST] Connecting as {username or 'anonymous'} for {label}", flush=True)
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=10)
        client.loop_start()
        time.sleep(1)
        result = client.publish(TARGET_TOPIC, json.dumps(payload, separators=(",", ":")), qos=1)
        result.wait_for_publish(timeout=5)
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
        print(f"[RESULT] Publish attempt completed for {label}; check broker logs/operator console for accepted or denied state.", flush=True)
        return True
    except Exception as exc:
        print(f"[RESULT] Publish attempt failed for {label}: {exc}", flush=True)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Controlled MWS local-lab unauthorised device test")
    parser.add_argument("--mode", choices=["invalid", "acl-denied", "simulated-stolen", "all"], default="all")
    parser.add_argument("--confirm-lab-only", action="store_true", help="Required acknowledgement for local lab use")
    args = parser.parse_args()

    if not args.confirm_lab_only:
        print("Refusing to run without --confirm-lab-only. This script is only for the private assessment lab.", file=sys.stderr)
        return 2

    if args.mode in {"invalid", "all"}:
        publish_once("intruder", "wrong-password", "invalid-credentials-blocked")

    if args.mode in {"acl-denied", "all"}:
        publish_once(READONLY_USERNAME, READONLY_PASSWORD, "read-only-acl-denied")

    if args.mode in {"simulated-stolen", "all"}:
        publish_once(SIM_STOLEN_USERNAME, SIM_STOLEN_PASSWORD, "simulated-stolen-credential-risk")

    print("[DONE] Controlled lab test completed. Review VM1 broker logs and VM4 IDS logs.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
