"""IOS XR NETCONF: retrieve BGP config subtree."""

from __future__ import annotations

import os
from ncclient import manager

HOST = os.environ["IOSXR_HOST"]
USER = os.environ["IOSXR_USER"]
PASSWORD = os.environ["IOSXR_PASSWORD"]

FILTER = """
<filter>
  <bgp xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg\"/>
</filter>
"""

with manager.connect(host=HOST, port=830, username=USER, password=PASSWORD, hostkey_verify=False) as m:
    response = m.get_config(source="running", filter=FILTER)
    print(response.xml)
