"""Section 02 - API/protocol workflow skeleton.

Implement REST/RESTCONF/NETCONF calls with retries and auth.
"""

from __future__ import annotations

import os
import requests


def get_health() -> dict:
    base_url = os.environ.get("LAB_API_BASE", "https://example.local")
    token = os.environ.get("LAB_API_TOKEN", "replace-me")
    response = requests.get(
        f"{base_url}/health",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
        verify=False,
    )
    return {"status_code": response.status_code, "ok": response.ok}
