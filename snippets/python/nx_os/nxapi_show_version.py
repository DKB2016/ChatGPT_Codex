"""NX-OS NX-API: run show commands via JSON-RPC payload."""

from __future__ import annotations

import os
import requests

BASE_URL = os.environ["NXOS_BASE_URL"]
USER = os.environ["NXOS_USER"]
PASSWORD = os.environ["NXOS_PASSWORD"]

payload = {
    "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show version",
        "output_format": "json",
    }
}

response = requests.post(
    f"{BASE_URL}/ins",
    auth=(USER, PASSWORD),
    json=payload,
    headers={"content-type": "application/json"},
    timeout=20,
    verify=False,
)
response.raise_for_status()

body = response.json()["ins_api"]["outputs"]["output"]["body"]
print(body)
