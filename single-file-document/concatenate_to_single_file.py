import json
import os
import re
import yaml
import textwrap
from datetime import datetime, timezone
import argparse
import pathlib
import frontmatter
import logging


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
def linked_path_to_label(doc_file_path, link_relative_path):
    # ensure that the path is relative
    if link_relative_path.startswith('/'):
        link_relative_path = link_relative_path[1:]

    # for links pointing within the same document - [example](#section_header) -
    # we set the document's filename to the link path
    if link_relative_path == "":
        link_relative_path = doc_file_path.split("/")[-1]

    # find the containing directory
    doc_dir_path = f"{doc_file_path}/.."
    # compose the full path and get the relative path
    link_full_path = f"{doc_dir_path}/{link_relative_path}"
    resolved_path = os.path.relpath(link_full_path)
    # cleanup extension, use colons (as labels cannot use slashes)
    label = re.sub(r"\.md$", "", str(resolved_path)).replace("/", ":")
    return label


def reduce_clutter_in_doc(doc_body):
    # drop "Pages in This Section" sections which are only used in HTML
    doc_body = doc_body.replace("## Pages in This Section", "")

    # drop lines containing "---", pandoc interprets these as h2 headers
    doc_body = re.sub(r"^---$", "", doc_body, flags=re.MULTILINE)
    return doc_body


def move_headers_down(doc_body):
    # move headers h2-h4 down by 3 levels (to h5-h7)
    extra_header_levels = 3*"#"
    return re.sub(r"^##", f"##{extra_header_levels}", doc_body, flags=re.MULTILINE)


def replace_html_code_blocks(doc_body):
    matches = re.findall('(<div class="language-c highlighter-rouge">[^§]*?</code></pre></div></div>)', doc_body, flags=re.MULTILINE)
    for match in matches:
        # strip html elements
        code_without_html_elements = re.sub("<[^>]*?>", "", match)
        # add Markdown code block
        code_as_markdown_block = f"""```c
{code_without_html_elements}```
"""
        doc_body = doc_body.replace(match, code_as_markdown_block)

    return doc_body


def doc_path_to_page_header_header_label(doc_file_full_path):
    return doc_file_full_path \
        .replace("../docs/", "") \
        .replace(".md", "") \
        .replace("../", "") \
        .replace("/", ":")


def adjust_links_in_doc_body(doc_body):
    # replace blog post paths to the full URL
    doc_body = re.sub(
            r"\(/(20[0-9][0-9]/[0-9][0-9]/[0-9][0-9])/",
            r"(https://duckdb.org/\1/",
            doc_body
        )

    # replace relative installation page links,
    # while keeping the optional '?environment=...' query strings
    doc_body = re.sub(
            r"\[installation page\]\([./]*installation((\?)[a-zA-Z0-9=]+)?\)",
            r"[installation page](https://duckdb.org/docs/installation/\1)",
            doc_body
        )

    # replace link to the Python guides index page
    # with a link to the Python guides section
    doc_body = doc_body.replace(
        "](../../guides/index#python-client)",
        "](../../guides/python)"
    )

    # replace "`, `" (with its typical surroundings) with "`,` " to allow line breaking
    # see https://stackoverflow.com/questions/76951040/pandoc-preserve-whitespace-in-inline-code
    doc_body = doc_body.replace("`*`, `*`", "`*`,` *`")

    # replace "(`" with "(` " to allow line breaking
    doc_body = doc_body.replace("(`", "(` ")

    # replace links to data sets to point to the website
    doc_body = doc_body.replace("](/data/", "](https://duckdb.org/data/")

    # use relative path for images
    doc_body = doc_body.replace("](/images", "](../images")

    # express HUGEINT limits as powers of two (upper and lower limits are ±2^127-1)
    doc_body = doc_body.replace("-170141183460469231731687303715884105727", "$-2^{127}-1$")
    doc_body = doc_body.replace( "170141183460469231731687303715884105727",  "$2^{127}-1$")
    doc_body = doc_body.replace("-170141183460469231731687303715884105728 (-1 << 127)", "$-2^{127}$")

    return doc_body


# change links to filenames to links to headers
def change_link(doc_body, doc_file_path):
    # match links but do not match image definitions (which start with a '!' character) within the link
    matches = re.findall(r"([^!]\[[^]!]*\])\(([^)]*)\)", doc_body)
    for match in matches:
        original_link = match[1]
        if original_link.startswith("http://") or original_link.startswith("https://"):
            continue
        if original_link.startswith("/"):
            full_url_link = f"https://duckdb.org{original_link}"
            doc_body = doc_body.replace(f"]({original_link})", f"]({full_url_link})")
            continue

        link_parts = original_link.split("#")

        # we step up one level to navigate from the Markdown file to the directory,
        # then we concatenate the rest of the path
        link_path = link_parts[0]

        link_to_label = linked_path_to_label(doc_file_path, link_path)
        # if there was an anchor target in the link (#some-item),
        # we append it using double colons as separator (::some-item)
        if len(link_parts) > 1:
            link_to_label = link_to_label + "::" + link_parts[1]

        old_link = f"{match[0]}({original_link})"
        new_link = f"{match[0]}(#{link_to_label})"
        doc_body = doc_body.replace(old_link, new_link)
    return doc_body


# add labels to sections within documents
# e.g., the sql/statements/copy.md file's "Copy To" section gets the label {#sql:statements:copy::copy-to}
def adjust_headers(doc_body, doc_header_label):
    doc_body_with_new_headers = ""
    for line in doc_body.splitlines():
        # We leverage that pages use headers that are at least h2 (##) in depth.
        # This allows us to avoid accidentally picking up and labeling comment lines in Bash, Python, etc.
        matches = re.findall(r"^(##+) (.*)$", line)
        if matches:
            match = matches[0]
            header_title = match[1]
            header_label = header_title \
                .lower() \
                .replace(" ", "-")
            header_label = re.sub("[^-_0-9a-z]", "", header_label)

            new_header = f"{match[0]} {match[1]} {{#{doc_header_label}::{header_label}}}"
            doc_body_with_new_headers += new_header + "\n"
        else:
            doc_body_with_new_headers += line + "\n"
    return doc_body_with_new_headers


def concatenate_page_to_output(of, header_level, docs_root, doc_file_path):
    # skip index files
    if doc_file_path.endswith("index"):
        return
    
    # determine the full path
    doc_file_full_path = f"{docs_root}/{doc_file_path}.md"
    if not os.path.exists(doc_file_full_path):
        doc_file_full_path = f"{docs_root}/{doc_file_path}/index.md"

    with open(doc_file_full_path) as doc_file:
        # parse YAML header and add header to the beginning of the content based on the "title" attribute
        # with a corresponding label to allow cross-references to target this header
        doc = frontmatter.load(doc_file)
        doc_title = doc["title"]
        doc_body = doc.content

        # add header at the beginning of the item with an accompanying label
        # e.g., for the guides/sql_features/ slug, the title is
        doc_header_label = doc_path_to_page_header_header_label(doc_file_full_path)
        of.write(f"""{"#" * header_level} {doc_title} {{#{doc_header_label}}}\n\n""")

        # process document body
        doc_body = reduce_clutter_in_doc(doc_body)
        doc_body = move_headers_down(doc_body)
        doc_body = replace_html_code_blocks(doc_body)
        doc_body = adjust_links_in_doc_body(doc_body)
        doc_body = adjust_headers(doc_body, doc_header_label)
        doc_body = change_link(doc_body, doc_file_path)

        # write to output
        of.write(doc_body)
        of.write("\n")


def add_to_documentation(docs_root, data, of, chapter_title):
    # we use the docs/index.md as the baseline for paths
    docs_index_file_path = "index.md"

    of.write(f"# {chapter_title}\n\n")
    chapter_json = [x for x in data["docsmenu"] if x["page"] == chapter_title][0]
    chapter_slug = chapter_json["slug"]
    main_level_pages = chapter_json["mainfolderitems"]

    for main_level_page in main_level_pages:
        main_title = main_level_page["page"]
        main_url = main_level_page.get("url")
        main_slug = main_level_page.get("slug")

        if main_url:
            logging.info(f"- {main_url}")
            concatenate_page_to_output(of, 2, docs_root, f"{chapter_slug}{main_url}")

        if main_slug:
            # e.g., "## SQL Features {#guides:sql_features}"
            of.write(f"## {main_title} {{#{ linked_path_to_label(docs_index_file_path, f'{chapter_slug}/{main_slug}') }}}\n\n")
        else:
            continue

        logging.info(f"- {main_slug}")
        for subfolder_page in main_level_page["subfolderitems"]:
            subfolder_page_title = subfolder_page["page"]
            subfolder_url = subfolder_page.get("url")
            subfolder_slug = subfolder_page.get("slug")

            if subfolder_url:
                logging.info(f"  - {main_slug}/{subfolder_url}")
                concatenate_page_to_output(of, 3, docs_root, f"{chapter_slug}{main_slug}/{subfolder_url}")

            if subfolder_slug:
                of.write(f"### {subfolder_page_title} {{#{ linked_path_to_label(docs_index_file_path, f'{chapter_slug}/{main_slug}/{subfolder_slug}') }}}\n\n")
            else:
                continue

            logging.info(f"  - {main_slug}/{subfolder_slug}")
            for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                subsubfolder_url = subsubfolder_page.get("url")

                logging.info(f"    - {main_slug}/{subfolder_slug}/{subsubfolder_url}")
                concatenate_page_to_output(of, 4, docs_root, f"{chapter_slug}{main_slug}/{subfolder_slug}/{subsubfolder_url}")


def add_under_the_hood_chapter(docs_root, data, of):
    of.write(f"# Under the Hood\n\n")
    of.write(f"## Internals\n\n")
    concatenate_page_to_output(of, 3, docs_root, "../internals/overview")
    concatenate_page_to_output(of, 3, docs_root, "../internals/storage")
    concatenate_page_to_output(of, 3, docs_root, "../internals/vector")
    of.write(f"## Developer Guides\n\n")
    concatenate_page_to_output(of, 3, docs_root, "../dev/building")
    concatenate_page_to_output(of, 3, docs_root, "../dev/profiling")
    concatenate_page_to_output(of, 3, docs_root, "../dev/testing")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/intro")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/debugging")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/result_verification")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/persistent_testing")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/loops")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/multiple_connections")
    concatenate_page_to_output(of, 4, docs_root, "../dev/sqllogictest/catch")

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()
verbose = args.verbose

if verbose:
    logging.getLogger().setLevel(logging.INFO)

# get version number
with open("../_config.yml") as config_file, open("metadata/metadata.yaml", "w") as metadata_file:
    config = yaml.safe_load(config_file.read())
    metadata_file.write(textwrap.dedent(
        f"""
          ---
          title: DuckDB Documentation
          subtitle: >-
            DuckDB version {config["currentsnapshotversion"]}\\newline
            Generated on {datetime.now(timezone.utc).strftime("%Y-%m-%d at %H:%M UTC")}
          ---
        """))

docs_root = "../docs/"

# compile concatenated document
with open("../_data/menu_docs_dev.json") as menu_docs_file, open(f"duckdb-docs.md", "w") as of:
    data = json.load(menu_docs_file)

    with open("cover-page.md") as cover_page_file:
        of.write(cover_page_file.read())

    add_to_documentation(docs_root, data, of, "Documentation")
    add_to_documentation(docs_root, data, of, "Guides")
    add_under_the_hood_chapter(docs_root, data, of)

    with open("acknowledgments.md") as acknowledgments_file:
        of.write(acknowledgments_file.read())
