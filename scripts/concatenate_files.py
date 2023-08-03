import json
import os
import re
import yaml


def concat(of, level, docs_root, doc_path):
    full_path = f"{docs_root}/{doc_path}.md"
    if not os.path.exists(full_path):
        full_path = f"{docs_root}/{doc_path}/index.md"

    with open(full_path) as doc_file:
        doc_text = doc_file.read()
        # parse YAML header
        yaml_match = re.match("^---$((.|\n)*?)^---$", doc_text, flags=re.MULTILINE).groups(1)
        if yaml_match:
            header = yaml.safe_load(yaml_match[0])
            of.write(f"""{"#"*level} {header["title"]}""")
            # strip the YAML header
            doc_text = re.sub("^---$((.|\n)*)?^---$", "", doc_text, flags=re.MULTILINE)
        # use relative path for images
        doc_text = doc_text.replace("](/images", "](images")

        # add path labels to headers (one per file for now)
        path_label = full_path \
            .replace("./docs/", "") \
            .replace(".md", "") \
            .replace("../", "") \
            .replace("/", ":")

        of.write(f" {{#{path_label}}}")

        # add labels to sections within documents
        # e.g., the sql/statements/copy.md file's "Copy To" section gets the label {#sql:statements:copy::copy-to}
        doc_text_with_new_headers = ""
        for line in doc_text.splitlines():
            matches = re.findall(r"^(#+)( ?)(.*)$", line)
            if matches:
                match = matches[0]
                header_title = match[2]
                header_label = header_title \
                    .lower() \
                    .replace(" ", "-")
                header_label = re.sub("[^-_0-9a-z]", "", header_label)

                new_header = f"{match[0]} {match[2]} {{#{path_label}::{header_label}}}"
                doc_text_with_new_headers += new_header + "\n"
            else:
                doc_text_with_new_headers += line + "\n"
        
        # change links to filenames to links to headers
        # do not match images (which have a '!' character) within the link
        matches = re.findall(r"([^!]\[[^]!]*\])\(([^)]*)\)", doc_text_with_new_headers)
        for match in matches:
            original_link = match[1]
            if original_link.startswith("http://") or original_link.startswith("https://"):
                continue
            link_to_label = original_link \
                .replace("../", "") \
                .replace("/", ":") \
                .replace("#", "::")
            old_link = f"{match[0]}({original_link})"
            new_link = f"{match[0]}(#{link_to_label})"
            doc_text_with_new_headers = doc_text_with_new_headers.replace(old_link, new_link)

        of.write(doc_text_with_new_headers)


docs_root = "./docs"

with open("./_data/menu_docs_dev.json") as f, open("duckdb-docs.md", "w") as of:
    data = json.load(f)
    documentation_main_level_pages = [x for x in data["docsmenu"] if x["page"] == "Documentation"][0]["mainfolderitems"]

    for main_level_page in documentation_main_level_pages:
        main_title = main_level_page["page"]
        main_url = main_level_page.get("url")
        main_slug = main_level_page.get("slug")

        if main_url:
            print(f"- {main_url}")
            concat(of, 1, docs_root, f"{main_url}")

        if main_slug:
            of.write(f"# {main_title}\n\n")
        else:
            continue

        print(f"- {main_slug}")
        for subfolder_page in main_level_page["subfolderitems"]:
            subfolder_page_title = subfolder_page["page"]
            subfolder_url = subfolder_page.get("url")
            subfolder_slug = subfolder_page.get("slug")

            if subfolder_url:
                print(f"  - {main_slug}/{subfolder_url}")
                concat(of, 2, docs_root, f"{main_slug}/{subfolder_url}")

            if subfolder_slug:
                of.write(f"## {subfolder_page_title}\n\n")
            else:
                continue

            print(f"  - {main_slug}/{subfolder_slug}")
            for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                subsubfolder_url = subsubfolder_page.get("url")

                print(f"    - {main_slug}/{subfolder_slug}/{subsubfolder_url}")
                concat(of, 3, docs_root, f"{main_slug}/{subfolder_slug}/{subsubfolder_url}")
