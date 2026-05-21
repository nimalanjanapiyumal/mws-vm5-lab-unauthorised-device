# Evidence Notes - VM5 Lab-only Unauthorised Device Test

## What to capture

- Hostname: `mws-lab-unauth01`
- Static IP: `192.168.1.75/24`
- Setup command: `sudo bash setup.sh`
- Verification command: `bash verify.sh`
- Role: Controlled local-lab test VM for blocked login, ACL-denied publish and simulated credential misuse evidence

## Suggested screenshot commands

```bash
hostnamectl --static
ip -4 addr
bash verify.sh
```
