import frontmatter
import sys
from glob import glob
from pathlib import Path
import re
import textwrap

if len(sys.argv) < 3:
    print(
        textwrap.dedent(
            """Expected usage: python3 scripts/redirect.py from_directory to_directory

       For example, to add a redirect from version '0.6.1' to '0.6',
       first move the directory manually from 'docs/archive/0.6.1' to 'docs/archive/0.6'.

       Then, run:

       python3 scripts/redirect.py docs/archive/0.6.1 docs/archive/0.6"
    """
        )
    )
    exit(1)

from_directory = sys.argv[1]
to_directory = sys.argv[2]

source = Path(to_directory)
for path in source.glob("**/*.md"):
    print(path)
    doc = frontmatter.load(path)

    new_redirect_entries = []

    # convert path to string and drop extension
    filename = str(path)
    filename = re.sub(r"\.md$", "", filename)

    if filename.endswith("overview"):
        new_redirect_entries = new_redirect_entries + [
            str(filename).replace(to_directory, from_directory)
        ]

    # drop overview from path
    filename = re.sub(r"/overview$", "", filename)

    new_redirect_entries = new_redirect_entries + [
        str(filename).replace(to_directory, from_directory)
    ]

    doc["redirect_from"] = doc.get("redirect_from", []) + new_redirect_entries

    with open(path, "w") as f:
        f.write(frontmatter.dumps(doc))
