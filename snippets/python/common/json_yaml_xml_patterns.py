"""Common serialization patterns seen in automation workflows."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any



def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_yaml(path: str, data: dict[str, Any]) -> None:
    import yaml

    Path(path).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def read_yaml(path: str) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def parse_interfaces_xml(xml_payload: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_payload)
    interfaces: list[dict[str, str]] = []

    for iface in root.findall(".//interface"):
        interfaces.append(
            {
                "name": iface.findtext("name", default=""),
                "admin_status": iface.findtext("enabled", default=""),
                "description": iface.findtext("description", default=""),
            }
        )

    return interfaces
