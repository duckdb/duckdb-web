import sys
import os
import shutil
import frontmatter


# update new stable file based on old stable file
def update_new_preview_page(file):
    doc = frontmatter.load(file)
    if "redirect_from" in doc:
        del doc["redirect_from"]

    # replace link tags in the content
    doc.content = doc.content.replace(
        f"{{% link docs/stable/", f"{{% link docs/preview/"
    )
    return frontmatter.dumps(doc)


# copy docs/stable to docs/preview
def copy_docs():
    src = "docs/stable"
    dst = "docs/preview"

    shutil.rmtree(dst)
    os.makedirs(dst)

    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)

        dest_dir = os.path.join(dst, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)

            print(src_file)

            if src_file.endswith(".md"):
                new_content = update_new_preview_page(src_file)
                with open(dst_file, "w") as f:
                    f.write(new_content)
                    f.write("\n")
            else:
                shutil.copy2(src_file, dst_file)


shutil.copy("_data/menu_docs_stable.json", f"_data/menu_docs_preview.json")
copy_docs()
