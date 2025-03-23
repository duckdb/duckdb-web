import json
import os
import frontmatter
import glob

all_redirects = set()

for file in glob.glob("docs/**/*.md", recursive=True):
    with open(file) as doc_file:
        doc = frontmatter.load(doc_file)
        if "redirect_from" in doc.metadata:
            doc_redirects = doc.metadata["redirect_from"]
            for doc_redirect in doc_redirects:
                if doc_redirect in all_redirects:
                    print(f"- {doc_redirect}")
                else:
                    all_redirects.add(doc_redirect)
