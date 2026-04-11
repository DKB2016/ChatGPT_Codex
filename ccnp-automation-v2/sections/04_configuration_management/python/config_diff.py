"""Section 04 - Config management helper.

Compares intended vs current text configs.
"""

from __future__ import annotations

from difflib import unified_diff


def build_diff(intended: str, current: str) -> str:
    diff = unified_diff(
        current.splitlines(),
        intended.splitlines(),
        fromfile="current",
        tofile="intended",
        lineterm="",
    )
    return "\n".join(diff)
