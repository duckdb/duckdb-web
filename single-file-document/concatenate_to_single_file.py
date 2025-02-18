import json
import os
import re
import yaml
import textwrap
from datetime import datetime, timezone
import argparse
import frontmatter
import logging
import glob


# Function to convert a path (a link from in a Markdown document) to a label.
def linked_path_to_label(link_path):
    # ensure that the path is relative
    if link_path.startswith("/"):
        link_path = link_path[1:]

    # for links pointing within the same document - [example](#section_header) -
    # we set the document's filename to the link path
    if link_path == "":
        link_path = link_path.split("/")[-1]

    # cleanup extension, use colons (as labels cannot use slashes)
    label = link_path.replace("/", ":")
    return label


def reduce_clutter_in_doc(doc_body):
    # drop "Pages in This Section" sections which are only used in HTML
    doc_body = doc_body.replace("## Pages in This Section", "")

    # drop lines containing "---", pandoc interprets these as h2 headers
    doc_body = re.sub(r"^---$", "", doc_body, flags=re.MULTILINE)
    return doc_body


def replace_jekyll_tags_for_variables(doc_body, config):
    doc_body = doc_body.replace("{{ site.currentduckdbhash }}",         config["currentduckdbhash"])
    doc_body = doc_body.replace("{{ site.currentduckdbodbcversion }}",  config["currentduckdbodbcversion"])
    doc_body = doc_body.replace("{{ site.currentduckdbversion }}",      config["currentduckdbversion"])
    doc_body = doc_body.replace("{{ site.currentjavaversion }}",        config["currentjavaversion"])
    doc_body = doc_body.replace("{{ site.currentshortduckdbversion }}", config["currentshortduckdbversion"])
    return doc_body


def replace_box_names(doc_body):
    doc_body = doc_body.replace("> Bestpractice", "> **Best practice.**")
    doc_body = doc_body.replace("> Note",         "> **Note.**")
    doc_body = doc_body.replace("> Warning",      "> **Warning.**")
    doc_body = doc_body.replace("> Tip",          "> **Tip.**")
    doc_body = doc_body.replace("> Deprecated",   "> **Deprecated.**")
    return doc_body


def fix_language_tags_for_syntax_highlighting(doc_body):
    # The Markdown pages use the additional language tags:
    # - 'plsql' (to add the 'D' prompt to sql)
    # - 'batch' (to remove the $ prompt from bash)
    # We do not want explicit prompts in the single-file version of the documentation,
    # so we unify these.
    doc_body = doc_body.replace("```plsql", "```sql")
    doc_body = doc_body.replace("```batch", "```bash")
    return doc_body


def move_headers_down(doc_body):
    # move headers h2-h4 down by 1 level
    extra_header_levels = "#"
    return re.sub(r"^##", f"##{extra_header_levels}", doc_body, flags=re.MULTILINE)


def replace_html_code_blocks(doc_body):
    matches = re.findall('(<div class="language-c highlighter-rouge">[^§]*?</code></pre></div></div>)', doc_body, flags=re.MULTILINE)
    for match in matches:
        # strip html elements
        code_without_html_elements = re.sub("<[^>]*?>", "", match)
        # add Markdown code block
        code_as_markdown_block = textwrap.dedent(f"""```c
            {code_without_html_elements}```
            """)
        doc_body = doc_body.replace(match, code_as_markdown_block)

    return doc_body


def doc_path_to_page_header_header_label(doc_file_full_path):
    return doc_file_full_path \
        .replace("../docs/", "docs/") \
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

    # replace relative installation page links
    doc_body = re.sub(
            r"\[installation page\]\((.*)?\)",
            r"[installation page](https://duckdb.org/docs/installation/)",
            doc_body
        )

    # replace link to the Python guides index page
    # with a link to the Python guides section
    doc_body = doc_body.replace(
        "]({% link docs/guides/overview.md %}#python-client)",
        "]({% link docs/python/overview.md %})"
    )

    # replace "`, `" (with the surrounding characters used for emphasis) with "`,` " to allow line breaking
    # see https://stackoverflow.com/questions/76951040/pandoc-preserve-whitespace-in-inline-code
    doc_body = doc_body.replace("`*`, `*`", "`*`,` *`")

    # replace "(`" with "(` " to allow line breaking
    doc_body = doc_body.replace("(`", "(` ")

    # replace links to data sets to point to the website
    doc_body = doc_body.replace("](/data/", "](https://duckdb.org/data/")

    # remove '<div>' HTML tags
    doc_body = re.sub(r'<div[^>]*?>[\n ]*([^§]*?)[\n ]*</div>', r'\1', doc_body, flags=re.MULTILINE)

    # replace '<img>' HTML tags with Markdown's '![]()' construct
    doc_body = re.sub(r'<img src="([^"]*)"[^§]*?/>', r'![](\1)\n', doc_body, flags=re.MULTILINE)

    # use relative path for images in Markdown
    doc_body = doc_body.replace("](/images", "](../images")

    # express HUGEINT limits as powers of two (upper and lower limits are ±2^127-1)
    doc_body = doc_body.replace("-170141183460469231731687303715884105727", "$-2^{127}-1$")
    doc_body = doc_body.replace( "170141183460469231731687303715884105727",  "$2^{127}-1$")
    doc_body = doc_body.replace("-170141183460469231731687303715884105728 (-1 << 127)", "$-2^{127}$")

    return doc_body


# change links to filenames to links to headers
def change_links(doc_body):
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

        # default: the link is unchanged
        new_link = original_link

        # {% link ... %} tags
        if original_link.startswith("{% link"):
            new_link = original_link

            # links to other pages (drop the .md extension)
            new_link = re.sub(
                r"{% link (.*?)\.md %}(#.*?)?",
                r"\1\2",
                new_link
            )

            # other links, e.g., PDFs
            new_link = re.sub(
                r"{% link (.*?) %}",
                r"https://duckdb.org/\1",
                new_link
            )

        # {% post_url ... %} tags
        if original_link.startswith("{% post_url "):
            new_link = re.sub(
                r"{% post_url (20[0-9][0-9])-([0-9][0-9])-([0-9][0-9])-(.*?) %}",
                r"https://duckdb.org/\1/\2/\3/\4",
                original_link
            )

        if new_link.startswith("https://"):
           new_link_replacement = new_link
        else:
            # we split links of the form a#b to along the #, leave links without # as they are
            link_parts = new_link.split("#")
            link_path = link_parts[0]
            new_link_replacement = f"#{linked_path_to_label(link_path)}"
            # if there was an anchor target in the link (#some-item),
            # we append it using double colons as separator (::some-item)
            if len(link_parts) > 1:
                new_link_replacement = new_link_replacement + "::" + link_parts[1]

        old_link = f"{match[0]}({original_link})"
        new_link_anchor = f"{match[0]}({new_link_replacement})"

        doc_body = doc_body.replace(old_link, new_link_anchor)
    return doc_body


def cleanup_doc(doc_body):
    doc_body = re.sub(r"<iframe.*</iframe>", "", doc_body)
    doc_body = re.sub(r"{% include .*}", "", doc_body)
    doc_body = doc_body.replace("{::nomarkdown}", "")
    doc_body = doc_body.replace("{::/nomarkdown}", "")
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


def change_function_table_headers(doc_body):
    doc_body = doc_body.replace("""| **Description** | """, """|   |   |
|:--|:--------|
| **Description** |""")
    doc_body = doc_body.replace("""| **Handle name** | """, """|   |   |
|:--|:--------|
| **Handle name** |""")
    return doc_body


def concatenate_page_to_output(config, of, header_level, docs_root, doc_file_path):
    # skip index files
    if doc_file_path.endswith("index"):
        return

    if doc_file_path.endswith("release_calendar"):
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
        doc_body = replace_jekyll_tags_for_variables(doc_body, config)
        doc_body = replace_box_names(doc_body)
        doc_body = move_headers_down(doc_body)
        doc_body = replace_html_code_blocks(doc_body)
        doc_body = adjust_links_in_doc_body(doc_body)
        doc_body = adjust_headers(doc_body, doc_header_label)
        doc_body = change_function_table_headers(doc_body)
        doc_body = change_links(doc_body)
        doc_body = cleanup_doc(doc_body)

        # write to output
        of.write(doc_body)
        of.write("\n")


def add_main_documentation(docs_root, menu, config, of):
    chapter_json = [x for x in menu["docsmenu"] if x["page"] == "Documentation"][0]
    chapter_slug = chapter_json["slug"]
    main_level_pages = chapter_json["mainfolderitems"]

    for main_level_page in main_level_pages:
        main_title = main_level_page["page"]
        main_url = main_level_page.get("url")
        main_slug = main_level_page.get("slug")

        if main_url:
            logging.info(f"- {main_url}")
            concatenate_page_to_output(config, of, 1, docs_root, f"{chapter_slug}{main_url}")

        if main_slug:
            # e.g., "# SQL Features {#guides:sql_features}"
            of.write(f"# {main_title} {{#{ linked_path_to_label(f'{chapter_slug}/{main_slug}') }}}\n\n")
        else:
            continue

        logging.info(f"- {main_slug}")
        for subfolder_page in main_level_page["subfolderitems"]:
            subfolder_page_title = subfolder_page["page"]
            subfolder_url = subfolder_page.get("url")
            subfolder_slug = subfolder_page.get("slug")

            if subfolder_url:
                logging.info(f"  - {main_slug}/{subfolder_url}")
                concatenate_page_to_output(config, of, 2, docs_root, f"{chapter_slug}{main_slug}/{subfolder_url}")

            if subfolder_slug:
                of.write(f"## {subfolder_page_title} {{#{ linked_path_to_label(f'{chapter_slug}/{main_slug}/{subfolder_slug}') }}}\n\n")
            else:
                continue

            logging.info(f"  - {main_slug}/{subfolder_slug}")
            for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                subsubfolder_url = subsubfolder_page.get("url")

                logging.info(f"    - {main_slug}/{subfolder_slug}/{subsubfolder_url}")
                concatenate_page_to_output(config, of, 3, docs_root, f"{chapter_slug}{main_slug}/{subfolder_slug}/{subsubfolder_url}")


def add_blog_posts(blog_root, of):
    of.write("# DuckDB Blog\n\n")

    blog_post_files = sorted(glob.glob(f"{blog_root}/*.md"))
    for blog_post_file in blog_post_files:
        print(blog_post_file)
        doc = frontmatter.load(blog_post_file)

        doc_title = doc["title"]
        doc_excerpt = doc["excerpt"]
        doc_author = doc["author"]
        doc_date = blog_post_file.split("/")[-1][0:10]
        doc_body = doc.content

        doc_body = fix_language_tags_for_syntax_highlighting(doc_body)
        doc_body = replace_box_names(doc_body)
        doc_body = move_headers_down(doc_body)
        doc_body = adjust_links_in_doc_body(doc_body)
        doc_body = change_links(doc_body)
        doc_body = cleanup_doc(doc_body)

        if ',' in doc_author or ' and ' in doc_author:
            author_field = "Authors"
        else:
            author_field = "Author"

        of.write(f"""## {doc_title}\n\n""")
        of.write(f"""**Publication date:** {doc_date}\n\n""")
        of.write(f"""**{author_field}:** {doc_author}\n\n""")
        if doc_excerpt is not None and doc_excerpt != "":
            of.write(f"""**TL;DR:** {doc_excerpt}\n\n""")
        of.write(f"""{doc_body}\n\n""")


parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
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

# compile concatenated document
with open(f"duckdb-docs.md", "w") as of:
    with open("cover-page.md") as cover_page_file:
        of.write(cover_page_file.read())

    with open("../_data/menu_docs_dev.json") as menu_docs_file:
        menu = json.load(menu_docs_file)
        add_main_documentation("../docs", menu, config, of)

    add_blog_posts("../_posts", of)

    with open("acknowledgments.md") as acknowledgments_file:
        of.write(acknowledgments_file.read())
