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

    # convert path to string and drop extension
    filename = str(path)
    filename = re.sub(r"\.md$", "", filename)

    new_redirect_entries = [
        "/" + str(filename).replace(to_directory, from_directory)
    ]

    doc["redirect_from"] = doc.get("redirect_from", []) + new_redirect_entries

    with open(path, "w") as f:
        f.write(frontmatter.dumps(doc))
