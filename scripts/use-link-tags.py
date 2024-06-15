import re
import os
import sys

filename = sys.argv[1]
dir = os.path.dirname(filename)

with open(filename, "r") as f:
    s = f.read()
    
    for m in re.finditer(r"\]\(([.0-9a-zA-Z].*?)(#.*?)?\)", s):
        link_path = m.group(1)

        if link_path.startswith("http://") or link_path.startswith("https://"):
            continue
        
        resolved_path = os.path.relpath(dir + "/" + link_path + ".md")
        anchor_text = m.group(2) or ""

        s = s.replace(m.group(), f"]({{% link {resolved_path} %}}{anchor_text})")

with open(filename, "w") as f:
    f.write(s)
