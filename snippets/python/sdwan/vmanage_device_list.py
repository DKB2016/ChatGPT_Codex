"""Cisco SD-WAN vManage: authenticate and list devices."""

from __future__ import annotations

import os
import requests

BASE_URL = os.environ["VMANAGE_BASE_URL"]
USER = os.environ["VMANAGE_USER"]
PASSWORD = os.environ["VMANAGE_PASSWORD"]

session = requests.Session()
session.verify = False

login_resp = session.post(
    f"{BASE_URL}/j_security_check",
    data={"j_username": USER, "j_password": PASSWORD},
    timeout=20,
)
login_resp.raise_for_status()

csrf_resp = session.get(f"{BASE_URL}/dataservice/client/token", timeout=20)
if csrf_resp.ok:
    session.headers.update({"X-XSRF-TOKEN": csrf_resp.text})

devices_resp = session.get(f"{BASE_URL}/dataservice/device", timeout=20)
devices_resp.raise_for_status()

for device in devices_resp.json().get("data", []):
    print(f"{device.get('host-name')} | {device.get('device-model')} | {device.get('reachability')}")
