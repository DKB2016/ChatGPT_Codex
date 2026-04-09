"""Meraki dashboard API example."""

from __future__ import annotations

import os
import requests

API_KEY = os.environ["MERAKI_API_KEY"]
ORG_ID = os.environ["MERAKI_ORG_ID"]

response = requests.get(
    f"https://api.meraki.com/api/v1/organizations/{ORG_ID}/networks",
    headers={"X-Cisco-Meraki-API-Key": API_KEY, "Accept": "application/json"},
    timeout=30,
)
response.raise_for_status()

for network in response.json():
    print(f"{network['id']} {network['name']} ({network.get('productTypes', [])})")
