import frontmatter
import sys

if len(sys.argv) < 2:
    print("Usage: add-redirect-to-dev.py path")
    print()
    print(
        "For example, the path should be 'sql/query_syntax/prepared_statements' to add a redirect"
    )
    print("from: /docs/sql/query_syntax/prepared_statements")
    print("to:   /docs/dev/sql/query_syntax/prepared_statements")
    exit(1)


path = sys.argv[1]

with open(f"docs/dev/{path}.md", "r") as f:
    doc = frontmatter.load(f)

with open(f"docs/dev/{path}.md", "w+") as of:
    redirect_from_field = doc.get("redirect_from")
    doc["redirect_from"] = [f"/docs/{path}"] + (redirect_from_field or [])
    of.write(frontmatter.dumps(doc))
    of.write('\n')
