"""Make SVG thumbnail strokes thinner when the image is shown large (e.g. in a blog post header).

Adds a <style id="thin-strokes"> block that scales every stroke-width found in the file by a factor,
applied only when the rendered image is at least --min-width pixels wide. The original stroke-width
attributes are never changed, so the script can be re-run with different settings at any time.
"""

import argparse
import re
from pathlib import Path

STYLE_ID = "thin-strokes"
BLOCK_RE = re.compile(r'\n?<style id="' + STYLE_ID + r'">.*?</style>', re.S)
LEGACY_RE = re.compile(
    r"\n?<style>\s*@media \(min-width: \d+px\) \{\s*\[stroke-width\] \{ stroke-width: [\d.]+; \}\s*\}\s*</style>",
    re.S,
)
SVG_TAG_RE = re.compile(r"<svg\b[^>]*>")
STROKE_RE = re.compile(r'stroke-width="([^"]+)"')


def format_number(value):
    return f"{value:.3f}".rstrip("0").rstrip(".")


def build_block(widths, factor, min_width):
    rules = " ".join(
        f'[stroke-width="{w}"] {{ stroke-width: {format_number(float(w) * factor)}; }}'
        for w in widths
    )
    return f'<style id="{STYLE_ID}">@media (min-width: {min_width}px) {{ {rules} }}</style>'


def process(path, factor, min_width):
    original = path.read_text(encoding="utf-8")
    text = LEGACY_RE.sub("", BLOCK_RE.sub("", original))
    widths = sorted(
        {w for w in STROKE_RE.findall(text) if re.fullmatch(r"[\d.]+", w)}, key=float
    )
    tag = SVG_TAG_RE.search(text)
    if not tag:
        return "no-svg"
    if widths:
        text = (
            text[: tag.end()]
            + "\n"
            + build_block(widths, factor, min_width)
            + text[tag.end() :]
        )
    if text == original:
        return "unchanged"
    path.write_text(text, encoding="utf-8")
    if not widths:
        return "removed"
    return "updated" if f'<style id="{STYLE_ID}">' in original else "added"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths",
        nargs="*",
        default=["images/blog/thumbs"],
        help="SVG files or folders (default: images/blog/thumbs)",
    )
    parser.add_argument(
        "--factor",
        type=float,
        default=0.625,
        help="stroke-width multiplier (default: 0.625, i.e. 3.2 -> 2)",
    )
    parser.add_argument(
        "--min-width",
        type=int,
        default=500,
        help="rendered image width in px from which thin strokes apply (default: 500)",
    )
    args = parser.parse_args()

    files = []
    for p in map(Path, args.paths):
        files.extend(sorted(p.glob("*.svg")) if p.is_dir() else [p])

    results = {}
    for f in files:
        results.setdefault(process(f, args.factor, args.min_width), []).append(f.name)

    for status in ("added", "updated", "removed", "unchanged", "no-svg"):
        names = results.get(status, [])
        if not names:
            continue
        print(f"{status}: {len(names)}")
        if status in ("added", "removed", "no-svg"):
            for name in names:
                print(f"  {name}")


if __name__ == "__main__":
    main()
