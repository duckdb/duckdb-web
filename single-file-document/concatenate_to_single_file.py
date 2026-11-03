import json
import os
import posixpath
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

    # remove comments
    doc_body = re.sub(r"<!--[^§]*?-->", "", doc_body, flags=re.MULTILINE)

    # drop lines containing "---", pandoc interprets these as h2 headers
    doc_body = re.sub(r"^---$", "", doc_body, flags=re.MULTILINE)
    return doc_body


# emulate the install/latest_client.html include: find the newest release in _data/releases.yml that offers the client
def latest_client_variables(config, client):
    config_keys = {
        "java": ("java_short_version", "java_version"),
        "odbc": ("odbc_short_version", "odbc_version"),
        "nodejs": ("node_neo_version", "node_neo_version"),
        "go": ("go_version", "go_tag"),
        "r": ("r_version", "r_version"),
        "rust": ("rust_version", "rust_crate_version"),
        "wasm": ("wasm_version", "wasm_tag"),
        "csharp": ("csharp_version", "csharp_version"),
    }
    version_key, package_key = config_keys.get(client, ("version", "version"))
    for release in config["data"]["releases"]:
        config_prefix = f"{release['config_prefix']}_duckdb_"
        variables = {
            "latest_version": config.get(config_prefix + version_key, ""),
            "latest_package": config.get(config_prefix + package_key, ""),
            "latest_release": release["version"],
        }
        if variables["latest_version"]:
            break
    return variables


def replace_jekyll_tags_for_variables(doc_body, config):
    # stash the content of {% raw %} blocks so that it is not processed
    raw_blocks = []
    def stash_raw_block(match):
        raw_blocks.append(match.group(1))
        return f"@@RAW_BLOCK_{len(raw_blocks) - 1}@@"
    doc_body = re.sub(r"{% raw %}(.*?){% endraw %}", stash_raw_block, doc_body, flags=re.DOTALL)

    # evaluate conditionals of the form {% if site.x != "" %}...{% else %}...{% endif %}
    doc_body = re.sub(
        r'{% if site\.(\w+) != "" %}(.*?)(?:{% else %}(.*?))?{% endif %}',
        lambda m: m.group(2) if config.get(m.group(1), "") != "" else (m.group(3) or ""),
        doc_body,
        flags=re.DOTALL
    )

    # evaluate version numbers split into components, e.g., for the Rust crate version:
    # {% assign rust_v = site.maintained_duckdb_rust_version | split: "." %}...{{ rust_v[1] | prepend: "0" | slice: -2, 2 }}
    for variable, config_key in re.findall(r'{% assign (\w+) = site\.(\w+) \| split: "\." %}', doc_body):
        parts = str(config[config_key]).split(".")
        doc_body = re.sub(
            rf'{{{{ {variable}\[(\d)\] }}}}',
            lambda m: parts[int(m.group(1))],
            doc_body
        )
        doc_body = re.sub(
            rf'{{{{ {variable}\[(\d)\] \| prepend: "0" \| slice: -2, 2 }}}}',
            lambda m: ("0" + parts[int(m.group(1))])[-2:],
            doc_body
        )

    # evaluate the variables assigned by the install/latest_client.html include, which are available until the next include, e.g.,
    # {% include install/latest_client.html client="java" %}{% assign jdbc_version = latest_package %}...{{ jdbc_version }}
    segments = re.split(r'{% include install/latest_client\.html client="(\w+)" %}', doc_body)
    doc_body = segments[0]
    for client, segment in zip(segments[1::2], segments[2::2]):
        variables = latest_client_variables(config, client)
        for variable, latest_variable in re.findall(r"{% assign (\w+) = (latest_\w+) %}", segment):
            variables[variable] = variables[latest_variable]
        doc_body += re.sub(r"{{ (\w+) }}", lambda m: variables.get(m.group(1), m.group(0)), segment)

    doc_body = re.sub(r'{% assign .*? %}', "", doc_body)

    # replace variables, e.g., {{ site.maintained_duckdb_version }}, undefined variables are rendered as empty strings (as in Jekyll)
    doc_body = re.sub(r"{{ site\.(\w+) }}", lambda m: str(config.get(m.group(1), "")), doc_body)

    # restore the content of {% raw %} blocks
    doc_body = re.sub(r"@@RAW_BLOCK_(\d+)@@", lambda m: raw_blocks[int(m.group(1))], doc_body)
    return doc_body


def replace_box_names(doc_body):
    doc_body = doc_body.replace("> Update",       "> **Update.**")
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


def move_headers_down(doc_body, header_level):
    # move headers h2-h5 below the page's header (by at least 2 levels),
    # capped at h6, the deepest header level supported by Markdown
    extra_header_levels = max(2, header_level - 1)
    return re.sub(
        r"^(##+) ",
        lambda m: "#" * min(len(m.group(1)) + extra_header_levels, 6) + " ",
        doc_body,
        flags=re.MULTILINE
    )


def section_title_to_label(title):
    # e.g., "CSV Files" -> "csv-files"
    return re.sub("[^0-9a-z]+", "-", title.lower()).strip("-")


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
        .replace(".md", "") \
        .replace("../", "") \
        .replace("/", ":")


def blog_post_file_to_label(blog_post_file):
    # e.g., ../_posts/2024-10-02-pyodide.md -> blog:2024-10-02-pyodide
    return "blog:" + os.path.basename(blog_post_file).replace(".md", "")


# convert the path of a Jekyll source file to its URL on the website
def jekyll_path_to_url(path):
    # collections, e.g., _events/2024-08-15-duckcon5.md -> events/2024/08/15/duckcon5/
    match = re.match(r"_events/([0-9]{4})-([0-9]{2})-([0-9]{2})-(.*)\.(md|html)$", path)
    if match:
        return f"https://duckdb.org/events/{match.group(1)}/{match.group(2)}/{match.group(3)}/{match.group(4)}/"
    match = re.match(r"_(library|everywhere)/(?:[0-9]{4}-[0-9]{2}-[0-9]{2}-)?(.*)\.(md|html)$", path)
    if match:
        return f"https://duckdb.org/{match.group(1)}/{match.group(2)}/"

    # index pages, e.g., install/index.html -> install/
    path = re.sub(r"(^|/)index\.(md|html)$", r"\1", path)
    path = re.sub(r"\.md$", "", path)
    return f"https://duckdb.org/{path}"


def adjust_links_in_doc_body(doc_body):
    # replace blog post paths to the full URL
    doc_body = re.sub(
            r"\(/(20[0-9][0-9]/[0-9][0-9]/[0-9][0-9])/",
            r"(https://duckdb.org/\1/",
            doc_body
        )

    # replace "`, `" (with the surrounding characters used for emphasis) with "`,` " to allow line breaking
    # see https://stackoverflow.com/questions/76951040/pandoc-preserve-whitespace-in-inline-code
    doc_body = doc_body.replace("`*`, `*`", "`*`,` *`")

    # replace "(`" with "(` " to allow line breaking
    doc_body = doc_body.replace("(`", "(` ")

    # replace links to data sets to point to the website
    doc_body = doc_body.replace("](/data/", "](https://duckdb.org/data/")

    # remove '<div>' HTML tags
    doc_body = re.sub(
        r'<div[^>]*?>[\n ]*([^§]*?)[\n ]*</div>',
        r'\1',
        doc_body,
        flags=re.MULTILINE
    )

    # remove videos
    doc_body = re.sub(
        r'<video[^§]*?</video>',
        '',
        doc_body,
        flags=re.MULTILINE
    )

    # remove dark mode images
    doc_body = re.sub(
        r'.*{: .darkmode-img }',
        '',
        doc_body
    )
    doc_body = re.sub(
        r'<img [^>]*class="darkmode-img"[^>]*>',
        '',
        doc_body,
        flags=re.MULTILINE
    )

    # replace '<img>' HTML tags with Markdown's '![]()' construct
    doc_body = re.sub(
        r'<img src="([^"]*)"[^§]*?/>',
        r'![](\1)\n',
        doc_body,
        flags=re.MULTILINE
    )

    # replace links to images
    doc_body = re.sub(
        r'{% link images/(.*?)\.(gif|jpg|png|svg) %}',
        r'/images/\1.\2',
        doc_body
    )

    # use relative path for images in Markdown
    doc_body = doc_body.replace("](/images", "](../images")

    # express HUGEINT limits as powers of two (upper and lower limits are ±2^127-1)
    doc_body = doc_body.replace("-170141183460469231731687303715884105727", "$-2^{127}-1$")
    doc_body = doc_body.replace( "170141183460469231731687303715884105727",  "$2^{127}-1$")
    doc_body = doc_body.replace("-170141183460469231731687303715884105728 (-1 << 127)", "$-2^{127}$")

    return doc_body


# change links to filenames to links to headers
# links to pages included in the document (internal_labels) become cross-references,
# links to other pages (e.g., other versions of the documentation) become links to the website
def change_links(doc_body, page_label, internal_labels):
    # match links (allowing brackets in the link text, e.g., [`UNION [ALL]`](#union))
    # but do not match image definitions (which start with '![') within the link
    matches = re.findall(r"(?<!!)(\[(?:[^]\[!]|!(?!\[)|\[[^]\[]*\])*\])\(([^)]*)\)", doc_body)
    for link_text, original_link in matches:
        if original_link.startswith(("http://", "https://", "mailto:", "<")):
            continue
        if original_link.startswith("/"):
            full_url_link = f"https://duckdb.org{original_link}"
            doc_body = doc_body.replace(f"]({original_link})", f"]({full_url_link})")
            continue

        # links pointing within the same page, e.g., [example](#section-header)
        if original_link.startswith("#"):
            target_label = page_label
            link_suffix = original_link
            external_url = None

        # {% link ... %} tags
        elif original_link.startswith("{% link "):
            link_target, link_suffix = re.match(r"{% link (.*?) %}(.*)", original_link).groups()
            target_label = linked_path_to_label(link_target.replace(".md", ""))
            external_url = jekyll_path_to_url(link_target)

        # {% post_url ... %} tags
        elif original_link.startswith("{% post_url "):
            post_name, link_suffix = re.match(r"{% post_url (.*?) %}(.*)", original_link).groups()
            target_label = f"blog:{post_name}"
            external_url = re.sub(
                r"(20[0-9][0-9])-([0-9][0-9])-([0-9][0-9])-(.*)",
                r"https://duckdb.org/\1/\2/\3/\4",
                post_name
            )

        # relative links in the documentation, e.g., [types](types) on the docs/2.0/clients/c/query.md page
        elif not page_label.startswith("blog:"):
            link_target, _, anchor = original_link.partition("#")
            page_directory = posixpath.dirname(page_label.replace(":", "/"))
            link_target = posixpath.normpath(posixpath.join(page_directory, link_target))
            link_suffix = f"#{anchor}" if anchor else ""
            target_label = linked_path_to_label(link_target)
            external_url = f"https://duckdb.org/{link_target}"

        else:
            continue

        if target_label in internal_labels:
            new_link = f"#{target_label}"
            # if there was an anchor target in the link (#some-item),
            # we append it using double colons as separator (::some-item)
            if link_suffix.startswith("#") and len(link_suffix) > 1:
                new_link += "::" + link_suffix[1:]
        elif external_url:
            new_link = f"{external_url}{link_suffix}"
        else:
            continue

        doc_body = re.sub(
            "(?<!!)" + re.escape(f"{link_text}({original_link})"),
            lambda _: f"{link_text}({new_link})",
            doc_body
        )
    return doc_body


def cleanup_doc(doc_body):
    doc_body = re.sub(r"<iframe.*</iframe>", "", doc_body)
    # replace tooltips with their labels
    doc_body = re.sub(r'{% include tooltip\.html label="(.*?)".*? %}', r"\1", doc_body)
    doc_body = re.sub(r"{% include .*? %}", "", doc_body)
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


def resolve_doc_file_path(docs_root, doc_file_path):
    # skip index files
    if doc_file_path.endswith("index"):
        return None

    if doc_file_path.endswith("release_calendar"):
        return None

    # skip HTML pages (e.g., the installation page), links to these point to the website
    if os.path.exists(f"{docs_root}/{doc_file_path}.html"):
        return None

    # determine the full path
    doc_file_full_path = f"{docs_root}/{doc_file_path}.md"
    if not os.path.exists(doc_file_full_path):
        doc_file_full_path = f"{docs_root}/{doc_file_path}/index.md"
    return doc_file_full_path


def concatenate_page_to_output(config, internal_labels, of, header_level, doc_file_full_path):
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
        doc_body = move_headers_down(doc_body, header_level)
        doc_body = replace_html_code_blocks(doc_body)
        doc_body = adjust_links_in_doc_body(doc_body)
        doc_body = adjust_headers(doc_body, doc_header_label)
        doc_body = change_function_table_headers(doc_body)
        doc_body = change_links(doc_body, doc_header_label, internal_labels)
        doc_body = cleanup_doc(doc_body)

        # write to output
        of.write(doc_body)
        of.write("\n")


# collect the sections and pages of the documentation in the order of the menu
# sections are represented as ("section", header_level, title, label), pages as ("page", header_level, doc_file_full_path)
def collect_main_documentation(docs_root, docs_url_prefix, menu):
    items = []

    def add_page(header_level, doc_file_path):
        doc_file_full_path = resolve_doc_file_path(docs_root, doc_file_path)
        if doc_file_full_path:
            items.append(("page", header_level, doc_file_full_path))

    # add the pages and subsections of a menu section, e.g., "Import & Export" > "CSV Files" > "Overview"
    def add_menu_items(menu_items, header_level, parent_label):
        for menu_item in menu_items:
            path = menu_item.get("path")
            if path and path.startswith(docs_url_prefix):
                logging.info(f"{'  ' * (header_level - 2)}- {path}")
                add_page(header_level, path[len(docs_url_prefix):])

            subitems = menu_item.get("subfolderitems") or menu_item.get("subsubfolderitems")
            if subitems:
                # e.g., "## CSV Files {#data:csv-files}"
                label = f"{parent_label}:{section_title_to_label(menu_item['page'])}"
                items.append(("section", header_level, menu_item["page"], label))
                add_menu_items(subitems, header_level + 1, label)

    how_to_guides_position = None
    for chapter_json in menu["docsmenu"]:
        chapter_url = chapter_json.get("url")

        # the How-to Guides page lists the guides based on their front matter, so they are collected separately
        if chapter_url == f"{docs_url_prefix}guides/":
            how_to_guides_position = len(items)

        # standalone pages in the documentation, e.g., "Quickstart"
        elif chapter_url and chapter_url.startswith(docs_url_prefix):
            logging.info(f"- {chapter_url}")
            add_page(1, chapter_url[len(docs_url_prefix):])

        # sections of the documentation, e.g., "Import & Export"
        if chapter_json["page"] != "Documentation":
            if "mainfolderitems" in chapter_json:
                logging.info(f"- {chapter_json['slug']}")
                items.append(("section", 1, chapter_json["page"], chapter_json["slug"]))
                add_menu_items(chapter_json["mainfolderitems"], 2, chapter_json["slug"])
            continue

        # the "Documentation" section of the menu used in v1.5 and earlier versions
        chapter_slug = chapter_json["slug"]
        for main_level_page in chapter_json["mainfolderitems"]:
            main_title = main_level_page["page"]
            main_url = main_level_page.get("url")
            main_slug = main_level_page.get("slug")

            if main_url:
                logging.info(f"- {main_url}")
                add_page(1, f"{chapter_slug}{main_url}")

            if main_slug:
                # e.g., "# SQL Features {#guides:sql_features}"
                items.append(("section", 1, main_title, linked_path_to_label(f"{chapter_slug}/{main_slug}")))
            else:
                continue

            logging.info(f"- {main_slug}")
            for subfolder_page in main_level_page["subfolderitems"]:
                subfolder_page_title = subfolder_page["page"]
                subfolder_url = subfolder_page.get("url")
                subfolder_slug = subfolder_page.get("slug")

                if subfolder_url:
                    logging.info(f"  - {main_slug}/{subfolder_url}")
                    add_page(2, f"{chapter_slug}{main_slug}/{subfolder_url}")

                if subfolder_slug:
                    items.append(("section", 2, subfolder_page_title, linked_path_to_label(f"{chapter_slug}/{main_slug}/{subfolder_slug}")))
                else:
                    continue

                logging.info(f"  - {main_slug}/{subfolder_slug}")
                for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                    subsubfolder_url = subsubfolder_page.get("url")

                    logging.info(f"    - {main_slug}/{subfolder_slug}/{subsubfolder_url}")
                    add_page(3, f"{chapter_slug}{main_slug}/{subfolder_slug}/{subsubfolder_url}")

    if how_to_guides_position is not None:
        menu_pages = set(item[2] for item in items if item[0] == "page")
        items[how_to_guides_position:how_to_guides_position] = collect_how_to_guides(docs_root, menu_pages)

    return items


# collect the how-to guides (pages with a "how_to_topic" front matter field) grouped by topic,
# skipping the guides that are already included via the menu
def collect_how_to_guides(docs_root, menu_pages):
    with open("../_data/post_types.yml") as post_types_file:
        topic_labels = yaml.safe_load(post_types_file)["tag_labels"]

    guides_by_topic = {}
    for doc_file_full_path in glob.glob(f"{docs_root}/**/*.md", recursive=True):
        doc = frontmatter.load(doc_file_full_path)
        topic = doc.get("how_to_topic")
        if topic and doc_file_full_path not in menu_pages:
            guides_by_topic.setdefault(topic, []).append((doc["title"], doc_file_full_path))

    items = [("section", 1, "How-to Guides", "guides")]
    for topic in sorted(guides_by_topic, key=lambda topic: topic_labels.get(topic, topic)):
        logging.info(f"- guides: {topic}")
        items.append(("section", 2, topic_labels.get(topic, topic), f"guides:{topic}"))
        items.extend(("page", 3, guide) for _, guide in sorted(guides_by_topic[topic]))
    return items


def add_main_documentation(items, config, internal_labels, of):
    for item in items:
        if item[0] == "section":
            _, header_level, title, label = item
            of.write(f"{'#' * header_level} {title} {{#{label}}}\n\n")
        else:
            _, header_level, doc_file_full_path = item
            concatenate_page_to_output(config, internal_labels, of, header_level, doc_file_full_path)


def add_blog_posts(blog_post_files, config, internal_labels, of):
    of.write("# DuckDB Blog {#blog}\n\n")

    for blog_post_file in blog_post_files:
        print(blog_post_file)
        doc = frontmatter.load(blog_post_file)

        doc_title = doc["title"]
        doc_excerpt = doc["excerpt"]
        doc_authors = doc.get("authors") or [doc.get("author", "")]
        doc_author = ", ".join(doc_authors)
        doc_date = blog_post_file.split("/")[-1][0:10]
        doc_body = doc.content
        doc_header_label = blog_post_file_to_label(blog_post_file)

        doc_body = reduce_clutter_in_doc(doc_body)
        doc_body = replace_jekyll_tags_for_variables(doc_body, config)
        doc_body = fix_language_tags_for_syntax_highlighting(doc_body)
        doc_body = replace_box_names(doc_body)
        doc_body = move_headers_down(doc_body, 2)
        doc_body = adjust_links_in_doc_body(doc_body)
        doc_body = adjust_headers(doc_body, doc_header_label)
        doc_body = change_links(doc_body, doc_header_label, internal_labels)
        doc_body = cleanup_doc(doc_body)

        if len(doc_authors) > 1:
            author_field = "Authors"
        else:
            author_field = "Author"

        of.write(f"""## {doc_title} {{#{doc_header_label}}}\n\n""")
        of.write(f"""**Publication date:** {doc_date}\n\n""")
        of.write(f"""**{author_field}:** {doc_author}\n\n""")
        if doc_excerpt is not None and doc_excerpt != "":
            of.write(f"""**TL;DR:** {doc_excerpt}\n\n""")
        of.write(f"""{doc_body}\n\n""")


# get the full DuckDB version number for the documentation version, e.g., 2.0 -> 2.0.0
def get_duckdb_version(config, docs_version):
    for prefix in ["maintained", "latest", "old_lts"]:
        if config.get(f"{prefix}_short_duckdb_version") == docs_version:
            return config[f"{prefix}_duckdb_version"]
    return docs_version


# compile a document from its cover page, its content and the acknowledgments
def write_document(output_file_path, cover_page_file_path, add_content):
    with open(output_file_path, "w") as of:
        with open(cover_page_file_path) as cover_page_file:
            of.write(cover_page_file.read())

        add_content(of)

        with open("acknowledgments.md") as acknowledgments_file:
            of.write(acknowledgments_file.read())


parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--docs-version", default="2.0", help="version of the documentation, i.e., a directory in docs/")
args = parser.parse_args()
verbose = args.verbose
docs_version = args.docs_version

if verbose:
    logging.getLogger().setLevel(logging.INFO)

with open("../_config.yml") as config_file:
    config = yaml.safe_load(config_file.read())

# data files used in the pages, available as site.data.* in Jekyll
with open("../_data/releases.yml") as releases_file:
    config["data"] = {"releases": yaml.safe_load(releases_file.read())}

# write the metadata (title page) of the documents
generated_on = f"Generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d at %H:%M UTC')}"
with open("metadata/duckdb-docs.yaml", "w") as metadata_file:
    metadata_file.write(textwrap.dedent(
        f"""
          ---
          title: DuckDB Documentation
          subtitle: >-
            DuckDB version {get_duckdb_version(config, docs_version)}\\newline
            {generated_on}
          ---
        """))
with open("metadata/duckdb-blog.yaml", "w") as metadata_file:
    metadata_file.write(textwrap.dedent(
        f"""
          ---
          title: DuckDB Blog
          subtitle: >-
            {generated_on}
          ---
        """))

with open(f"../_data/menu_docs_{docs_version.replace('.', '')}.json") as menu_docs_file:
    menu = json.load(menu_docs_file)
doc_items = collect_main_documentation(f"../docs/{docs_version}", f"/docs/{docs_version}/", menu)
blog_post_files = sorted(glob.glob("../_posts/*.md"))

# labels of the pages included in each document, links to other pages (including pages in the other document) point to the website
docs_internal_labels = set(doc_path_to_page_header_header_label(item[2]) for item in doc_items if item[0] == "page")
blog_internal_labels = set(blog_post_file_to_label(blog_post_file) for blog_post_file in blog_post_files)

# compile concatenated documents
write_document(
    "duckdb-docs.md",
    "cover-page-docs.md",
    lambda of: add_main_documentation(doc_items, config, docs_internal_labels, of)
)
write_document(
    "duckdb-blog.md",
    "cover-page-blog.md",
    lambda of: add_blog_posts(blog_post_files, config, blog_internal_labels, of)
)
