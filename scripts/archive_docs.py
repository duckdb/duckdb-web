import sys
import os
import shutil
import frontmatter

if len(sys.argv) < 2:
    print("Usage: archive_docs VERSION")
    exit(1)

old_stable_version = sys.argv[1]


# update new stable file based on old stable file
def update_new_stable_page(new_stable_file, old_stable_dir):
    # if the old counterpart exists, parse YAML metadata and get the "redirect_from" field
    old_stable_file = new_stable_file.replace("docs/preview", "docs/stable")
    if os.path.exists(old_stable_file):
        old_stable_doc = frontmatter.load(old_stable_file)
        redirect_from_field = old_stable_doc.get("redirect_from")
    else:
        redirect_from_field = None

    new_stable_doc = frontmatter.load(new_stable_file)

    # overwrite the new stable doc's redirect_from field with the one from the old stable document
    new_stable_doc["redirect_from"] = redirect_from_field

    # replace link tags in the content
    new_stable_doc.content = new_stable_doc.content.replace(
        f"{{% link docs/preview/", f"{{% link docs/stable/"
    )
    return frontmatter.dumps(new_stable_doc)


# copy docs/preview to docs/stable, while keeping the redirects from docs/stable
def archive_preview():
    src = "docs/preview"
    dst = f"docs/stable_temp"
    old_stable = "docs/stable"

    os.makedirs(dst, exist_ok=True)

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dst, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)

            if src_file.endswith(".md"):
                new_content = update_new_stable_page(src_file, old_stable)
                with open(dst_file, "w") as f:
                    f.write(new_content)
                    f.write("\n")
            else:
                shutil.copy2(src_file, dst_file)

    shutil.rmtree("docs/stable")
    shutil.move("docs/stable_temp", "docs/stable")


def update_stable_page(src_file, old_stable_version):
    # parse YAML metadata and adjust the "redirect_from" field
    doc = frontmatter.load(src_file)

    # remove redirects
    if "redirect_from" in doc:
        del doc["redirect_from"]

    # replace link tags in the content
    doc.content = doc.content.replace(
        f"{{% link docs/stable/", f"{{% link docs/{old_stable_version}/"
    )
    return frontmatter.dumps(doc)


# copy docs/stable to docs/<old_stable_version>
# the directs should be expanded on with the version number
def archive_stable(old_stable_version):
    src = "docs/stable"
    dst = f"docs/{old_stable_version}"

    os.makedirs(dst, exist_ok=True)

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dst, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)

            if src_file.endswith(".md"):
                new_content = update_stable_page(src_file, old_stable_version)
                with open(dst_file, "w") as f:
                    f.write(new_content)
                    f.write("\n")
            else:
                shutil.copy2(src_file, dst_file)


old_stable_version_no_dots = old_stable_version.replace(".", "")

shutil.copy(
    "_data/menu_docs_stable.json", f"_data/menu_docs_{old_stable_version_no_dots}.json"
)
archive_stable(old_stable_version)

shutil.copy("_data/menu_docs_preview.json", f"_data/menu_docs_stable.json")
archive_preview()

shutil.move("js/stable", "js/{old_stable_version}")
shutil.copytree("js/preview", "js/stable")
