import sys
import os
import shutil
import frontmatter


# copy **the redirects** from docs/lts to docs/current
def copy_redirects():
    src = "docs/lts"
    dst = "docs/current"

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        for file in files:
            if not file.endswith(".md"):
                continue
            src_file = os.path.join(root, file)
            dest_dir = os.path.join(dst, rel_path)
            dst_file = os.path.join(dest_dir, file)

            if not os.path.exists(dst_file):
                continue

            print(f"{src_file} -> {dst_file}")

            src_doc_frontmatter = frontmatter.load(src_file)
            dst_doc_frontmatter = frontmatter.load(dst_file)

            if "redirect_from" in src_doc_frontmatter:
                src_redirect_from = src_doc_frontmatter["redirect_from"]
                dst_redirect_from = dst_doc_frontmatter.get("redirect_from", [])
                dst_doc_frontmatter["redirect_from"] = sorted(
                    dst_redirect_from + src_redirect_from
                )
                del src_doc_frontmatter["redirect_from"]

            with open(src_file, "w") as f:
                f.write(frontmatter.dumps(src_doc_frontmatter))
                f.write("\n")

            with open(dst_file, "w") as f:
                f.write(frontmatter.dumps(dst_doc_frontmatter))
                f.write("\n")


def add_stable_redirects():
    src = "docs/current"

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        for file in files:
            if not file.endswith(".md"):
                continue
            src_file = os.path.join(root, file)

            doc = frontmatter.load(src_file)
            redirect_from = doc.get("redirect_from", [])
            stable_path = "/" + os.path.join(
                "docs/stable", rel_path, file
            ).removesuffix(".md")
            if stable_path not in redirect_from:
                redirect_from.append(stable_path)
            doc["redirect_from"] = sorted(redirect_from)

            with open(src_file, "w") as f:
                f.write(frontmatter.dumps(doc))
                f.write("\n")


copy_redirects()
add_stable_redirects()
