import re
import os
import sys

filename = sys.argv[1]
dir = os.path.dirname(filename)

with open(filename, "r") as f:
    s = f.read()

    # relative paths, e.g. ../../data/parquet/overview
    for m in re.finditer(r"\]\(([.0-9a-zA-Z].*?)([#?].*?)?\)", s):
        link_path = m.group(1)

        if link_path.startswith("http://") or link_path.startswith("https://"):
            continue

        resolved_path = os.path.relpath(f"{dir}/{link_path}.md")

        anchor_text = m.group(2) or ""

        s = s.replace(m.group(), f"]({{% link {resolved_path} %}}{anchor_text})")

    # absolute paths, e.g. /docs/installation/index
    for m in re.finditer(r"\]\(/([^2].*?)([#?].*?)?\)", s):
        link_path = m.group(1)

        if link_path.startswith("data") or link_path.startswith("images"):
            continue

        if link_path == "docs/installation/index":
            resolved_path = f"{link_path}.html"
        else:
            resolved_path = f"{link_path}.md"

        anchor_text = m.group(2) or ""

        s = s.replace(m.group(), f"]({{% link {resolved_path} %}}{anchor_text})")

    # blog posts, e.g. /docs/installation/index
    for m in re.finditer(r"\]\(/(2.*?)([#?].*?)?\)", s):
        # replace slashes with dashes to turn 'yyyy/mm/dd/' to 'yyyy-mm-dd-'
        link_path = m.group(1).replace('/', '-')
        link_path = f"{link_path}.md"
        anchor_text = m.group(2) or ""

        s = s.replace(m.group(), f"]({{% link _posts/{link_path} %}}{anchor_text})")


with open(filename, "w") as f:
    f.write(s)
