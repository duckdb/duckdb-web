import json
import os
import re
import yaml
import textwrap
from datetime import datetime, timezone
import argparse
import pathlib
import frontmatter


# Function to convert a path (a link from in a Markdown document) to a label.
# The conversion includes resolving the leading "../" navigation steps with the actual path, removing the ".md"
# extension from the filename and replacing slash characters ("/") with colons (":") for the label.
#
# For example, for the inputs:
# - doc_file_path="docs/sql/query_syntax/select.md"
# - link_path="../expressions/star"
#
# the function will compute:
# - resolved_path="docs/sql/expressions/star.md"
#
# which will turn into the LaTeX label:
# - label="docs:sql:expressions:star"
def path_to_label(doc_file_path, link_relative_path):
    doc_dir_path = f"{doc_file_path}/.."
    link_full_path = f"{doc_dir_path}/{link_relative_path}"
    resolved_path = os.path.relpath(link_full_path)
    label = re.sub(r"\.md$", "", str(resolved_path)).replace("/", ":")
    return label


def concat(of, header_level, docs_root_absolute_path, docs_root, doc_file_path):
    # skip index files
    if doc_file_path.endswith("index"):
        return
    
    doc_file_full_path = f"{docs_root}/{doc_file_path}.md"
    if not os.path.exists(doc_file_full_path):
        doc_file_full_path = f"{docs_root}/{doc_file_path}/index.md"

    with open(doc_file_full_path) as doc_file:
        # parse YAML header and add header to the beginning of the content based on the "title" attribute
        # with a corresponding label to allow cross-references to target this header
        doc = frontmatter.load(doc_file)
        doc_title = doc["title"]
        doc_body = doc.content

        of.write(f"""{"#" * header_level} {doc_title}""")

        # drop "Pages in this Section" and "More" sections
        doc_body = doc_body.replace("### Pages in this Section", "")
        doc_body = doc_body.replace("### More", "")

        # drop lines containing "---", pandoc interprets these as h2 headers
        doc_body = re.sub(r"^---$", "", doc_body, flags=re.MULTILINE)

        # add path labels to headers at the beginning of the file
        path_label = doc_file_full_path \
            .replace("../docs/", "") \
            .replace(".md", "") \
            .replace("../", "") \
            .replace("/", ":")
        
        of.write(f" {{#{path_label}}}\n")

        # move headers h2-h4 down by 3 levels (to h5-h7)
        extra_header_levels = 3*"#"
        doc_body = re.sub(r"^##", f"##{extra_header_levels}", doc_body, flags=re.MULTILINE)

        # replace blog post paths to the full URL
        doc_body = re.sub(
                r"\(/(20[0-9][0-9]/[0-9][0-9]/[0-9][0-9])/",
                r"(https://duckdb.org/\1/",
                doc_body
            )

        # use relative path for images
        doc_body = doc_body.replace(
                "](/images",
                "](../images"
            )

        # add labels to sections within documents
        # e.g., the sql/statements/copy.md file's "Copy To" section gets the label {#sql:statements:copy::copy-to}
        doc_body_with_new_headers = ""
        for line in doc_body.splitlines():
            matches = re.findall(r"^(#+)( ?)(.*)$", line)
            if matches:
                match = matches[0]
                header_title = match[2]
                header_label = header_title \
                    .lower() \
                    .replace(" ", "-")
                header_label = re.sub("[^-_0-9a-z]", "", header_label)

                new_header = f"{match[0]} {match[2]} {{#{path_label}::{header_label}}}"
                doc_body_with_new_headers += new_header + "\n"
            else:
                doc_body_with_new_headers += line + "\n"

        # change links to filenames to links to headers
        # do not match images (which have a '!' character) within the link
        matches = re.findall(r"([^!]\[[^]!]*\])\(([^)]*)\)", doc_body_with_new_headers)
        for match in matches:
            original_link = match[1]
            if original_link.startswith("http://") or original_link.startswith("https://"):
                continue
            link_parts = original_link.split("#")

            # we step up one level to navigate from the Markdown file to the directory,
            # then we concatenate the rest of the path
            link_path = link_parts[0]

            link_to_label = path_to_label(doc_file_path, link_path)
            # if there was an anchor target in the link (#some-item),
            # we append it using double colons as separator (::some-item)
            if len(link_parts) > 1:
                link_to_label = link_to_label + "::" + link_parts[1]

            old_link = f"{match[0]}({original_link})"
            new_link = f"{match[0]}(#{link_to_label})"
            doc_body_with_new_headers = doc_body_with_new_headers.replace(old_link, new_link)

        of.write(doc_body_with_new_headers)


def add_to_documentation(docs_root_absolute_path, data, of, chapter_title, verbose):
    of.write(f"# {chapter_title}\n\n")
    chapter_json = [x for x in data["docsmenu"] if x["page"] == chapter_title][0]
    chapter_slug = chapter_json["slug"]
    main_level_pages = chapter_json["mainfolderitems"]

    for main_level_page in main_level_pages:
        main_title = main_level_page["page"]
        main_url = main_level_page.get("url")
        main_slug = main_level_page.get("slug")

        if main_url:
            if verbose:
                print(f"- {main_url}")
            concat(of, 2, docs_root_absolute_path, docs_root, f"{chapter_slug}{main_url}")

        if main_slug:
            of.write(f"## {main_title} {{#{ path_to_label(docs_root_absolute_path, f'{chapter_slug}/{main_slug}') }}} \n\n")
        else:
            continue

        if verbose:
            print(f"- {main_slug}")
        for subfolder_page in main_level_page["subfolderitems"]:
            subfolder_page_title = subfolder_page["page"]
            subfolder_url = subfolder_page.get("url")
            subfolder_slug = subfolder_page.get("slug")

            if subfolder_url:
                if verbose:
                    print(f"  - {main_slug}/{subfolder_url}")
                concat(of, 3, docs_root_absolute_path, docs_root, f"{chapter_slug}{main_slug}/{subfolder_url}")

            if subfolder_slug:
                of.write(f"### {subfolder_page_title} {{#{ path_to_label(docs_root_absolute_path, f'{chapter_slug}/{main_slug}/{subfolder_slug}') }}} \n\n")
            else:
                continue

            if verbose:
                print(f"  - {main_slug}/{subfolder_slug}")
            for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                subsubfolder_url = subsubfolder_page.get("url")

                if verbose:
                    print(f"    - {main_slug}/{subfolder_slug}/{subsubfolder_url}")
                concat(of, 4, docs_root_absolute_path, docs_root, f"{chapter_slug}{main_slug}/{subfolder_slug}/{subsubfolder_url}")



parser = argparse.ArgumentParser()
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()
verbose = args.verbose


# get version number
with open("../_config.yml") as config_file, open("metadata/metadata.yaml", "w") as metadata_file:
    config = yaml.safe_load(config_file.read())
    metadata_file.write(textwrap.dedent(
        f"""
          ---
          title: DuckDB documentation
          subtitle: >-
            DuckDB version {config["currentsnapshotversion"]}\\newline
            Generated on {datetime.now(timezone.utc).strftime("%Y-%m-%d at %H:%M UTC")}
          ---
        """))

# concatenate documents
docs_root = "../docs"
docs_root_absolute_path = pathlib.Path(docs_root).resolve()

with open("../_data/menu_docs_dev.json") as menu_docs_file, open(f"duckdb-docs.md", "w") as of:
    data = json.load(menu_docs_file)

    add_to_documentation(docs_root_absolute_path, data, of, "Documentation", verbose)
    add_to_documentation(docs_root_absolute_path, data, of, "Guides", verbose)

    with open("acknowledgments.md") as acknowledgments_file:
        of.write(acknowledgments_file.read())
