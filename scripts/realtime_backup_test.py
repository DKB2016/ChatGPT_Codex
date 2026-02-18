#!/usr/bin/env python3
"""Real-time backup workflow test against PAN-OS XML API (or mock server)."""

from __future__ import annotations

import argparse
import hashlib
import os
import ssl
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test backup workflow against PAN-OS API")
    parser.add_argument("--host", default="127.0.0.1:8080", help="Firewall host:port")
    parser.add_argument("--scheme", default="http", choices=["http", "https"])
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="admin")
    parser.add_argument("--backup-dir", default="artifacts/backups")
    parser.add_argument("--include-device-state", action="store_true")
    parser.add_argument("--verify-tls", action="store_true")
    return parser.parse_args()


def build_url(scheme: str, host: str) -> str:
    return f"{scheme}://{host}/api/"


def http_get(url: str, params: dict[str, str], verify_tls: bool) -> bytes:
    query = urlencode(params)
    full_url = f"{url}?{query}"
    req = Request(full_url, method="GET")

    context = None
    if full_url.startswith("https://") and not verify_tls:
        context = ssl._create_unverified_context()

    with urlopen(req, timeout=60, context=context) as response:  # noqa: S310
        return response.read()


def get_api_key(url: str, username: str, password: str, verify_tls: bool) -> str:
    payload = http_get(
        url,
        {"type": "keygen", "user": username, "password": password},
        verify_tls,
    )

    root = ET.fromstring(payload.decode("utf-8"))
    key = root.findtext("./result/key")
    if not key:
        raise RuntimeError(f"No API key returned: {payload!r}")
    return key


def export_file(url: str, api_key: str, category: str, destination: Path, verify_tls: bool) -> None:
    payload = http_get(
        url,
        {"type": "export", "category": category, "key": api_key},
        verify_tls,
    )

    destination.write_bytes(payload)
    if destination.stat().st_size <= 0:
        raise RuntimeError(f"Exported file is empty: {destination}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    args = parse_args()
    backup_dir = Path(args.backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    file_prefix = f"{args.host.replace(':', '_')}-{timestamp}"

    url = build_url(args.scheme, args.host)
    api_key = get_api_key(url, args.username, args.password, args.verify_tls)

    generated_files: list[Path] = []

    config_path = backup_dir / f"{file_prefix}-running-config.xml"
    export_file(url, api_key, "configuration", config_path, args.verify_tls)
    generated_files.append(config_path)

    if args.include_device_state:
        state_path = backup_dir / f"{file_prefix}-device-state.tgz"
        export_file(url, api_key, "device-state", state_path, args.verify_tls)
        generated_files.append(state_path)

    manifest_path = backup_dir / f"{file_prefix}-sha256sum.txt"
    with manifest_path.open("w", encoding="utf-8") as manifest:
        for file_path in generated_files:
            manifest.write(f"{sha256_file(file_path)}  {file_path.name}\n")

    print("Backup workflow complete")
    print(f"API endpoint: {url}")
    print(f"Artifacts: {os.fspath(backup_dir)}")
    for artifact in generated_files:
        print(f" - {artifact} ({artifact.stat().st_size} bytes)")
    print(f"Checksum manifest: {manifest_path}")


if __name__ == "__main__":
    main()
