"""Generic RESTCONF PATCH for loopback interface intent."""

from __future__ import annotations

import os
import requests

BASE_URL = os.environ["RESTCONF_BASE_URL"]
USER = os.environ["RESTCONF_USER"]
PASSWORD = os.environ["RESTCONF_PASSWORD"]

payload = {
    "ietf-interfaces:interface": [
        {
            "name": "Loopback123",
            "description": "created-by-restconf",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [{"ip": "10.123.123.1", "netmask": "255.255.255.255"}]
            },
        }
    ]
}

response = requests.patch(
    f"{BASE_URL}/restconf/data/ietf-interfaces:interfaces",
    auth=(USER, PASSWORD),
    headers={
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
    },
    json=payload,
    timeout=20,
    verify=False,
)
response.raise_for_status()
print("Loopback PATCH succeeded")
