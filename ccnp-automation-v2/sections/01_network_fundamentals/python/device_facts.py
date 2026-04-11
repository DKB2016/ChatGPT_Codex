"""Section 01 - Network fundamentals automation task.

Goal: collect and normalize basic device facts for exam prep.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone


def collect_facts() -> dict:
    """Replace this mock payload with real API/CLI collection logic."""
    return {
        "hostname": "lab-r1",
        "os_version": "17.x",
        "interfaces_up": 12,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    print(json.dumps(collect_facts(), indent=2))
