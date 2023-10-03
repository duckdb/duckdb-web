import frontmatter
import sys
from glob import glob
from pathlib import Path
import re

if len(sys.argv) < 3:
    print("Expected usage: python3 scripts/redirect.py from_directory to_directory")
    exit(1)


from_directory = sys.argv[1]
to_directory = sys.argv[2]


source = Path(from_directory)
for path in source.glob("**/*.md"):
    doc = frontmatter.load(path)

    filename = str(path)
    filename = re.sub(r"\.md$", "", filename)
    filename = re.sub(r"/overview$", "", filename)

    new_redirect_entry = str(filename).replace(from_directory, to_directory)

    doc["redirect_from"] = doc.get("redirect_from", []) + [new_redirect_entry]

    with open(path, "w") as f:
        f.write(frontmatter.dumps(doc))
