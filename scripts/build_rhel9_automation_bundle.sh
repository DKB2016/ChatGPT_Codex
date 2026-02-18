#!/usr/bin/env bash
set -euo pipefail

# Build a transferable Python automation bundle for RHEL 9 / Python 3.9.
# Produces:
#   dist/network-automation-rhel9-<timestamp>.tar.gz
# Bundle contains:
#   - venv/ (preinstalled environment)
#   - wheelhouse/ (all downloaded wheels/sdists)
#   - requirements.txt
#   - bootstrap_from_wheelhouse.sh (recreate venv locally, preferred)

PYTHON_BIN="${PYTHON_BIN:-python3.9}"
REQ_FILE="${REQ_FILE:-requirements/network-automation-rhel9.txt}"
DIST_DIR="${DIST_DIR:-dist}"
BUILD_ROOT="${BUILD_ROOT:-.build/rhel9-bundle}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BUNDLE_DIR="${BUILD_ROOT}/network-automation-rhel9-${TIMESTAMP}"
WHEELHOUSE_DIR="${BUNDLE_DIR}/wheelhouse"
VENV_DIR="${BUNDLE_DIR}/venv"
ARCHIVE_PATH="${DIST_DIR}/network-automation-rhel9-${TIMESTAMP}.tar.gz"

command -v "${PYTHON_BIN}" >/dev/null 2>&1 || {
  echo "ERROR: ${PYTHON_BIN} not found. Install Python 3.9 first." >&2
  exit 1
}

mkdir -p "${DIST_DIR}" "${WHEELHOUSE_DIR}"

"${PYTHON_BIN}" -m pip install --upgrade pip setuptools wheel

# Download dependencies first, so installs can be done offline on target.
"${PYTHON_BIN}" -m pip download -r "${REQ_FILE}" -d "${WHEELHOUSE_DIR}"

"${PYTHON_BIN}" -m venv "${VENV_DIR}"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-index --find-links "${WHEELHOUSE_DIR}" -r "${REQ_FILE}"
python -m pip freeze > "${BUNDLE_DIR}/requirements.lock.txt"
cp "${REQ_FILE}" "${BUNDLE_DIR}/requirements.txt"

cat > "${BUNDLE_DIR}/bootstrap_from_wheelhouse.sh" <<'BOOTSTRAP'
#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3.9}"
TARGET_DIR="${1:-./venv}"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

command -v "${PYTHON_BIN}" >/dev/null 2>&1 || {
  echo "ERROR: ${PYTHON_BIN} not found on target host." >&2
  exit 1
}

"${PYTHON_BIN}" -m venv "${TARGET_DIR}"
# shellcheck disable=SC1091
source "${TARGET_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-index --find-links "${BASE_DIR}/wheelhouse" -r "${BASE_DIR}/requirements.txt"

cat <<MSG
Done.
Activate with:
  source ${TARGET_DIR}/bin/activate
MSG
BOOTSTRAP
chmod +x "${BUNDLE_DIR}/bootstrap_from_wheelhouse.sh"

# Helpful metadata
cat > "${BUNDLE_DIR}/README.txt" <<README
Network Automation Bundle (RHEL9/Python3.9)

Created: ${TIMESTAMP}
Python: ${PYTHON_BIN}
Requirements source: ${REQ_FILE}

Important portability note:
- Copying a venv between hosts can fail due to absolute paths/system library differences.
- Preferred method on target host: run ./bootstrap_from_wheelhouse.sh

Quick start on target host:
  tar -xzf $(basename "${ARCHIVE_PATH}")
  cd network-automation-rhel9-${TIMESTAMP}
  ./bootstrap_from_wheelhouse.sh /opt/network-automation-venv
  source /opt/network-automation-venv/bin/activate
README

tar -czf "${ARCHIVE_PATH}" -C "${BUILD_ROOT}" "network-automation-rhel9-${TIMESTAMP}"

echo "Bundle created: ${ARCHIVE_PATH}"
echo "Contents folder: ${BUNDLE_DIR}"
