# RHEL 9 Python 3.9 Network Automation Bundle

This repository includes a packaging workflow so you can build once, copy to a RHEL 9 host, and start automating quickly.

## What is included

- Curated package set for Cisco + Palo Alto automation in `requirements/network-automation-rhel9.txt`
- Bundle builder script: `scripts/build_rhel9_automation_bundle.sh`
- Output archive containing:
  - `venv/` (prebuilt virtual environment)
  - `wheelhouse/` (downloaded dependencies for offline install)
  - `requirements.txt` + `requirements.lock.txt`
  - `bootstrap_from_wheelhouse.sh` (rebuild venv on target host)

## Build the bundle

```bash
./scripts/build_rhel9_automation_bundle.sh
```

Optional overrides:

```bash
PYTHON_BIN=python3.9 \
REQ_FILE=requirements/network-automation-rhel9.txt \
DIST_DIR=dist \
./scripts/build_rhel9_automation_bundle.sh
```

## Copy and install on RHEL 9

1. Copy the generated archive from `dist/` to your RHEL host.
2. Extract and bootstrap from the included wheelhouse (recommended):

```bash
tar -xzf network-automation-rhel9-<timestamp>.tar.gz
cd network-automation-rhel9-<timestamp>
./bootstrap_from_wheelhouse.sh /opt/network-automation-venv
source /opt/network-automation-venv/bin/activate
```

## Why bootstrap instead of directly copying `venv/`?

Copying a virtualenv between hosts can fail due to:

- Absolute interpreter paths in venv scripts
- Host-level shared library differences
- Different OpenSSL/glibc/runtime paths

`bootstrap_from_wheelhouse.sh` recreates the venv locally while staying offline from the bundled wheelhouse.

## Included key packages

- Device access/orchestration: `netmiko`, `paramiko`, `scrapli`, `nornir`, `napalm`, `ncclient`
- Palo Alto: `pan-os-python`, `pan-python`, `pandevice`
- Cisco testing: `pyats[full]`, `unicon`, `genie`
- NetBox + utilities: `pynetbox`, `jinja2`, `pyyaml`, `requests`, `httpx`, `rich`

> Note: `json` and `pprint` are part of Python standard library and are not installed via pip.
