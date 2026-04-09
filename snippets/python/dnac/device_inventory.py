"""Catalyst Center (DNA Center) inventory retrieval."""

from __future__ import annotations

import os
import requests

BASE_URL = os.environ["DNAC_BASE_URL"]
USER = os.environ["DNAC_USER"]
PASSWORD = os.environ["DNAC_PASSWORD"]


def get_token() -> str:
    response = requests.post(
        f"{BASE_URL}/dna/system/api/v1/auth/token",
        auth=(USER, PASSWORD),
        timeout=20,
        verify=False,
    )
    response.raise_for_status()
    return response.json()["Token"]


def get_devices(token: str) -> list[dict]:
    response = requests.get(
        f"{BASE_URL}/dna/intent/api/v1/network-device",
        headers={"X-Auth-Token": token},
        timeout=20,
        verify=False,
    )
    response.raise_for_status()
    return response.json().get("response", [])


if __name__ == "__main__":
    token = get_token()
    devices = get_devices(token)
    for device in devices:
        print(f"{device.get('hostname')} | {device.get('managementIpAddress')} | {device.get('platformId')}")
