#!/usr/bin/env bash
set -euo pipefail

if [ -f /etc/mws-lab-test/lab_test.env ]; then
  set -a
  # shellcheck disable=SC1091
  source /etc/mws-lab-test/lab_test.env
  set +a
fi

python3 /opt/mws-lab-test/unauthorised_device_false_normal_test.py --mode all --confirm-lab-only
