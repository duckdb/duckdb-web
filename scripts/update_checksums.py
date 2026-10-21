#!/usr/bin/env python3
"""Update the SHA-256 hashes in _data/checksums_XY.yml from a DuckDB GitHub release.

Usage: python scripts/update_checksums.py 1.5.6

For version X.Y.Z, the default file is _data/checksums_XY.yml (e.g., checksums_15.yml for 1.5.6).
Artifacts that are not published in the duckdb/duckdb release (e.g., the JDBC and ODBC drivers)
are left unchanged and reported.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "_data"


def default_file(version):
    major, minor = version.split(".")[:2]
    return DATA_DIR / f"checksums_{major}{minor}.yml"


def fetch_digests(version):
    url = f"https://api.github.com/repos/duckdb/duckdb/releases/tags/v{version}"
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request) as response:
        release = json.load(response)

    digests = {}
    for asset in release["assets"]:
        digest = asset.get("digest") or ""
        if digest.startswith("sha256:"):
            digests[asset["name"]] = digest.removeprefix("sha256:")
    return digests


def update_file(path, digests):
    # Edit line by line to preserve the file's comments and formatting
    lines = path.read_text().splitlines(keepends=True)
    filename = None
    updated, missing = [], []
    for i, line in enumerate(lines):
        if m := re.match(r'\s*filename:\s*"?([^"\s]+)"?', line):
            filename = m.group(1)
        elif filename and (m := re.match(r'(\s*sha256:\s*)"?[0-9a-fA-F]*"?\s*$', line)):
            if filename in digests:
                lines[i] = f'{m.group(1)}"{digests[filename]}"\n'
                updated.append(filename)
            else:
                missing.append(filename)
            filename = None
    path.write_text("".join(lines))
    return updated, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("version", help="DuckDB version, e.g., 1.5.6")
    parser.add_argument(
        "--file",
        type=Path,
        help="checksums YAML file to update (default: _data/checksums_XY.yml)",
    )
    args = parser.parse_args()

    version = args.version.removeprefix("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"Invalid version {version}, expected X.Y.Z")
    path = args.file or default_file(version)
    if not path.exists():
        sys.exit(f"Checksums file {path} does not exist")
    try:
        digests = fetch_digests(version)
    except urllib.error.HTTPError as e:
        sys.exit(f"Failed to fetch release v{version}: {e}")
    if not digests:
        sys.exit(f"Release v{version} has no SHA-256 digests")

    updated, missing = update_file(path, digests)
    print(f"Updated {len(updated)} hashes in {path}")
    for filename in sorted(set(missing)):
        print(f"Not found in release v{version}, left unchanged: {filename}")


if __name__ == "__main__":
    main()
