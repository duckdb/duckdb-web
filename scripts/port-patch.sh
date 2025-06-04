#!/usr/bin/env bash

set -euo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

STABLE_DIR="docs/stable"
PREVIEW_DIR="docs/preview"
PATCH_FILE="/tmp/commit.patch"

if [ $# -lt 1 ]; then
    echo "Usage: scripts/apply_patch.sh COMMIT_HASH"
    exit 1
fi

COMMIT_HASH=$1

cd "${STABLE_DIR}"
git format-patch -1 ${COMMIT_HASH} --stdout > "${PATCH_FILE}"

# change stable to preview, both in filenames and in file content
sed -i.bkp "s#${STABLE_DIR}#${PREVIEW_DIR}#g" ${PATCH_FILE}

git apply "${PATCH_FILE}" && echo "Patch applied to ${PREVIEW_DIR}." || {
  echo "Failed to apply patch."
  exit 1
}
