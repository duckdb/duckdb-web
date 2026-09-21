#!/usr/bin/env python3
"""Remove redirect_from entries starting with /docs/preview from Markdown front matter.

Edits the front matter line by line to preserve the existing formatting.
If a redirect_from list becomes empty, the redirect_from key is removed.
"""

import argparse
import re
from pathlib import Path

PREFIX = "/docs/preview"
LIST_ITEM = re.compile(r"^\s*-\s*['\"]?(?P<value>[^'\"]*)['\"]?\s*$")


def process_front_matter(lines):
    """Return (new_lines, removed_entries) for the front matter lines (without the --- delimiters)."""
    result = []
    removed = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("redirect_from:"):
            result.append(line)
            i += 1
            continue

        # collect the list items belonging to redirect_from
        i += 1
        kept = []
        while i < len(lines) and LIST_ITEM.match(lines[i]):
            value = LIST_ITEM.match(lines[i]).group("value")
            if value.startswith(PREFIX):
                removed.append(value)
            else:
                kept.append(lines[i])
            i += 1

        if kept:
            result.append(line)
            result.extend(kept)
    return result, removed


def process_file(path, dry_run):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return []

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---")
    except StopIteration:
        return []

    new_front_matter, removed = process_front_matter(lines[1:end])
    if removed and not dry_run:
        path.write_text(
            "".join([lines[0], *new_front_matter, *lines[end:]]), encoding="utf-8"
        )
    return removed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory", nargs="?", default=".", help="directory to process (default: .)"
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="report changes without writing"
    )
    args = parser.parse_args()

    changed_files = 0
    removed_entries = 0
    for path in sorted(Path(args.directory).rglob("*.md")):
        removed = process_file(path, args.dry_run)
        if removed:
            changed_files += 1
            removed_entries += len(removed)
            print(f"{path}: removed {', '.join(removed)}")

    action = "Would remove" if args.dry_run else "Removed"
    print(f"{action} {removed_entries} entries from {changed_files} files")


if __name__ == "__main__":
    main()
