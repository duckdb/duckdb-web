import json
import os
import re
import yaml
import textwrap
from datetime import datetime, timezone
import argparse


def concat(of, header_level, docs_root, doc_path):
    full_path = f"{docs_root}/{doc_path}.md"
    if not os.path.exists(full_path):
        full_path = f"{docs_root}/{doc_path}/index.md"

    with open(full_path) as doc_file:
        doc_text = doc_file.read()

        # drop "Pages in this Section"
        doc_text = doc_text.replace("### Pages in this Section", "")

        # parse YAML header and add header to the beginning of the content based on the "title" attribute
        doc_groups = doc_text.split("---\n")
        header = yaml.safe_load(doc_groups[1])
        of.write(f"""{"#" * header_level} {header["title"]}""")

        # the rest of the string (after the second horizontal bar) is the main body of the document
        doc_text = "\n".join(doc_groups[2:])

        # add path labels to headers at the beginning of the file
        path_label = full_path \
            .replace("../docs/", "") \
            .replace(".md", "") \
            .replace("../", "") \
            .replace("/", ":")
        of.write(f" {{#{path_label}}}\n")

        # increase indentation of headers in the document -- they should be at least level 5 (i.e. ##### Title)
        # - for top-level (header_level = 2), increase indentation by 3
        # - for mid-level (header_level = 3), increase indentation by 2
        # - for the lowest-level (header_level = 4), increase indentation by 1
        extra_header_levels = "#" * (5 - header_level)
        doc_text = re.sub(r"^### ", f"###{extra_header_levels} ", doc_text, flags=re.MULTILINE)

        # replace blog post paths to the full URL
        doc_text = re.sub(
                r"\(/(20[0-9][0-9]/[0-9][0-9]/[0-9][0-9])/",
                r"(https://duckdb.org/\1/",
                doc_text
            )

        # use relative path for images
        doc_text = doc_text.replace(
                "](/images",
                "](../images"
            )

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


def add_to_documentation(data, of, chapter_title, verbose):
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
            concat(of, 2, docs_root, f"{chapter_slug}{main_url}")

        if main_slug:
            of.write(f"## {main_title}\n\n")
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
                concat(of, 3, docs_root, f"{chapter_slug}{main_slug}/{subfolder_url}")

            if subfolder_slug:
                of.write(f"### {subfolder_page_title}\n\n")
            else:
                continue

            if verbose:
                print(f"  - {main_slug}/{subfolder_slug}")
            for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                subsubfolder_url = subsubfolder_page.get("url")

                if verbose:
                    print(f"    - {main_slug}/{subfolder_slug}/{subsubfolder_url}")
                concat(of, 4, docs_root, f"{chapter_slug}{main_slug}/{subfolder_slug}/{subsubfolder_url}")



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

with open("../_data/menu_docs_dev.json") as menu_docs_file, open(f"duckdb-docs.md", "w") as of:
    data = json.load(menu_docs_file)

    add_to_documentation(data, of, "Documentation", verbose)
    add_to_documentation(data, of, "Guides", verbose)

    with open("acknowledgments.md") as acknowledgments_file:
        of.write(acknowledgments_file.read())
