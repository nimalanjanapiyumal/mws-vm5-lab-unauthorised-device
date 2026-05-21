# VM5 - MWS Lab-only Unauthorised Device Test Repository

This repository configures VM5 as the controlled lab-only unauthorised-device test VM.

## VM details

- Hostname: `mws-lab-unauth01`
- Static IP: `192.168.1.50/24`
- Target broker: `192.168.1.10:1883`

## Safety note

This repository does not steal credentials. It only uses lab credentials deliberately configured by the assessment owner. Run it only in the private MWS assessment lab.

## Single setup command

```bash
sudo bash setup.sh
```

## Run controlled evidence test

```bash
bash scripts/run_lab_unauthorised_test.sh
```

The test performs three local-lab demonstrations:

1. Invalid credentials are blocked.
2. Read-only `lab_test` credentials cannot publish to the protected telemetry topic.
3. Simulated stolen `sensor01` credentials can publish a false-normal message, demonstrating the risk of credential misuse and the need for stronger device identity controls.

Collect VM1 broker logs and VM4 IDS alerts as supporting evidence.
