"""Pre/post change validation helpers for automation pipelines."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InterfaceState:
    name: str
    admin_up: bool
    oper_up: bool


def assert_interfaces_up(states: list[InterfaceState], required: list[str]) -> None:
    lookup = {item.name: item for item in states}
    missing = [name for name in required if name not in lookup]
    if missing:
        raise AssertionError(f"Missing interfaces in state payload: {missing}")

    failed = [name for name in required if not (lookup[name].admin_up and lookup[name].oper_up)]
    if failed:
        raise AssertionError(f"Interfaces not up/up: {failed}")


if __name__ == "__main__":
    snapshot = [
        InterfaceState(name="GigabitEthernet1", admin_up=True, oper_up=True),
        InterfaceState(name="GigabitEthernet2", admin_up=True, oper_up=True),
    ]
    assert_interfaces_up(snapshot, ["GigabitEthernet1", "GigabitEthernet2"])
    print("Validation passed")
