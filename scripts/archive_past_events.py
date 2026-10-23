"""Move past events with `library: true` to _library and delete past events with `library: false`.

An event is past once its last day (`end_date`, `date` or the date in the file name) is before today.
Talks (`tag: talk`) without a `library` flag are deleted, other events without the flag are kept.
A moved event gets a `redirect_from` entry for its old URL and `_events/...` link tags pointing to
it are updated. An event is not deleted while other files still link to it.
Run from the repository root.
"""

import argparse
import datetime
import re
import subprocess
from pathlib import Path

EVENTS_DIR = Path("_events")
LIBRARY_DIR = Path("_library")
FILENAME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})-(.+)\.(?:md|html)")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.S)


def field(front_matter, key):
    match = re.search(rf"^{key}:[ \t]*(.*?)[ \t]*$", front_matter, re.M)
    return match.group(1).strip("\"'") if match else None


def parse_date(value):
    return datetime.date.fromisoformat(value[:10]) if value else None


def add_redirect(front_matter, url):
    if re.search(r"^redirect_from:[ \t]*$", front_matter, re.M):
        return re.sub(
            r"^redirect_from:[ \t]*$",
            f"redirect_from:\n- {url}",
            front_matter,
            count=1,
            flags=re.M,
        )
    return front_matter + f"redirect_from:\n- {url}\n"


def references(path):
    result = subprocess.run(
        ["git", "grep", "-l", "--untracked", "--fixed-strings", path.as_posix()],
        capture_output=True,
        text=True,
    )
    return [name for name in result.stdout.split() if name != path.as_posix()]


def update_links(old_path, new_path):
    for name in references(old_path):
        path = Path(name)
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace(old_path.as_posix(), new_path.as_posix()), encoding="utf-8"
        )
        print(f"  updated link in {name}")


def delete(path):
    linked_from = references(path)
    if linked_from:
        print(f"skipped: {path} (still linked from {', '.join(linked_from)})")
        return
    path.unlink()
    print(f"deleted: {path}")


def move(path, text, front_matter_match, start, slug):
    if list(LIBRARY_DIR.glob(f"????-??-??-{slug}.*")):
        print(f"skipped: {path} (a library entry with slug '{slug}' already exists)")
        return
    event_url = f"/events/{start:%Y/%m/%d}/{slug}/"
    target = LIBRARY_DIR / path.name
    target.write_text(
        f"---\n{add_redirect(front_matter_match.group(1), event_url)}---\n"
        + text[front_matter_match.end() :],
        encoding="utf-8",
    )
    path.unlink()
    print(f"moved: {path} -> {target}")
    update_links(path, target)


def process(path, today):
    name_match = FILENAME_RE.fullmatch(path.name)
    if not name_match:
        return
    text = path.read_text(encoding="utf-8")
    front_matter_match = FRONT_MATTER_RE.match(text)
    if not front_matter_match:
        return
    front_matter = front_matter_match.group(1)
    flag = (field(front_matter, "library") or "").lower()
    if not flag and field(front_matter, "tag") == "talk":
        flag = "false"
    if flag not in ("true", "false"):
        return

    start = parse_date(field(front_matter, "date")) or parse_date(name_match.group(1))
    end = parse_date(field(front_matter, "end_date")) or start
    if end >= today:
        return

    if flag == "false":
        delete(path)
    else:
        slug = field(front_matter, "slug") or name_match.group(2)
        move(path, text, front_matter_match, start, slug)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--today",
        type=datetime.date.fromisoformat,
        default=datetime.date.today(),
        help="reference date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    for path in sorted(EVENTS_DIR.iterdir()):
        process(path, args.today)


if __name__ == "__main__":
    main()
