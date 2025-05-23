import frontmatter
import glob

all_redirects = dict()

for file in glob.glob("docs/**/*.md", recursive=True):
    with open(file, 'r') as doc_file:
        doc = frontmatter.load(doc_file)

    if "redirect_from" in doc:
        doc_redirects = doc["redirect_from"]
        for doc_redirect in doc_redirects:
            if file.startswith(doc_redirect[1:]):
                print(
                    f"{file} redirects to itself, removing redirect"
                )
                doc["redirect_from"] = None
                with open(file, 'w') as doc_file:
                    doc_file.write(frontmatter.dumps(doc))

            if doc_redirect in all_redirects:
                print(
                    f"{file}: {doc_redirect} already occurs in {all_redirects[doc_redirect]}"
                )
            else:
                all_redirects[doc_redirect] = file
