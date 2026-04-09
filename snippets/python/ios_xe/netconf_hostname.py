"""IOS XE NETCONF: set hostname using ncclient."""

from __future__ import annotations

import os
from ncclient import manager

HOST = os.environ["IOSXE_HOST"]
USER = os.environ["IOSXE_USER"]
PASSWORD = os.environ["IOSXE_PASSWORD"]
NEW_HOSTNAME = os.getenv("IOSXE_NEW_HOSTNAME", "ccnp-iosxe-lab")

CONFIG = f"""
<config>
  <native xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\">
    <hostname>{NEW_HOSTNAME}</hostname>
  </native>
</config>
"""

with manager.connect(host=HOST, port=830, username=USER, password=PASSWORD, hostkey_verify=False) as m:
    m.edit_config(target="running", config=CONFIG)
    print(m.get_config(source="running").xml)
