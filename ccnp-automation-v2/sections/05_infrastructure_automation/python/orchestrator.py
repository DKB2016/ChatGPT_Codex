"""Section 05 - Infrastructure automation orchestrator.

Run provisioning then validation in a single Python entrypoint.
"""

from __future__ import annotations

import subprocess


def run_command(cmd: list[str]) -> int:
    print(f"running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    run_command(["echo", "TODO: call terraform/ansible pipelines"])
