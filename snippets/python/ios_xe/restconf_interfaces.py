"""IOS XE RESTCONF: read interface operational data."""

from __future__ import annotations

import os
import requests

BASE_URL = os.environ["IOSXE_BASE_URL"]
USER = os.environ["IOSXE_USER"]
PASSWORD = os.environ["IOSXE_PASSWORD"]


def get_interfaces() -> dict:
    endpoint = f"{BASE_URL}/restconf/data/ietf-interfaces:interfaces-state"
    headers = {"Accept": "application/yang-data+json"}

    response = requests.get(
        endpoint,
        auth=(USER, PASSWORD),
        headers=headers,
        timeout=20,
        verify=False,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    payload = get_interfaces()
    for item in payload.get("ietf-interfaces:interfaces-state", {}).get("interface", []):
        print(f"{item['name']:<20} admin={item.get('admin-status')} oper={item.get('oper-status')}")
