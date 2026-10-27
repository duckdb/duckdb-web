"""Set `latest_duckdb_r_version` in _config.yml if CRAN has a newer DuckDB R package.

The CRAN version is compared to `latest_duckdb_r_version` or, if that is empty, to
`maintained_duckdb_r_version`. Run from the repository root.
"""

import re
import sys
import urllib.request
from pathlib import Path

CONFIG = Path("_config.yml")
CRAN_URL = "https://cran.r-project.org/web/packages/duckdb/index.html"


def config_value(text, key):
    return re.search(rf'^{key}: "(.*)"$', text, re.M).group(1)


def version_key(version):
    return tuple(int(part) for part in re.split(r"[.-]", version))


def main():
    with urllib.request.urlopen(CRAN_URL, timeout=60) as response:
        page = response.read().decode("utf-8")
    match = re.search(r"<td>Version:</td>\s*<td>([\d.-]+)</td>", page)
    if not match:
        sys.exit(f"Could not find the package version on {CRAN_URL}")
    cran_version = match.group(1)

    text = CONFIG.read_text(encoding="utf-8")
    current = config_value(text, "latest_duckdb_r_version") or config_value(
        text, "maintained_duckdb_r_version"
    )
    if version_key(cran_version) <= version_key(current):
        print(f"R package on CRAN is {cran_version}, not newer than {current}")
        return
    text = re.sub(
        r'^latest_duckdb_r_version: ".*"$',
        f'latest_duckdb_r_version: "{cran_version}"',
        text,
        count=1,
        flags=re.M,
    )
    CONFIG.write_text(text, encoding="utf-8")
    print(f"updated latest_duckdb_r_version: {current} -> {cran_version}")


if __name__ == "__main__":
    main()
