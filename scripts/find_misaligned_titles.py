import json
import os
import frontmatter

# This script finds misaligned titles, i.e., instances where the page title displayed in the menu bar
# (on the left side) and the title in the page header do not align.
# 
# Usage: in the scripts/ directory, run
#
# $ python find_misaligned_titles.py

def check_page_for_misaligned_title(menu_bar_title, docs_root, doc_file_path):
    # skip index files
    if doc_file_path.endswith("index"):
        return
    doc_file_full_path = f"{docs_root}/{doc_file_path}.md"

    if not os.path.exists(doc_file_full_path):
        doc_file_full_path = f"{docs_root}/{doc_file_path}/index.md"

    with open(doc_file_full_path) as doc_file:
        doc = frontmatter.load(doc_file)
        doc_title = doc["title"]
    
    if menu_bar_title == "Overview":
        return

    if menu_bar_title != doc_title and not menu_bar_title in doc_title:
        print(doc_file_path)
        print(f"- menu title: {menu_bar_title}")
        print(f"- doc title:  {doc_title}")
        print()


def check_section(docs_root, data, section_title):
    section_json = [x for x in data["docsmenu"] if x["page"] == section_title][0]
    section_slug = section_json["slug"]
    main_level_pages = section_json["mainfolderitems"]

    for main_level_page in main_level_pages:
        main_title = main_level_page["page"]
        main_url = main_level_page.get("url")
        main_slug = main_level_page.get("slug")

        if main_url:
            check_page_for_misaligned_title(main_title, docs_root, f"{section_slug}{main_url}")

        if not main_slug:
            continue

        for subfolder_page in main_level_page["subfolderitems"]:
            subfolder_page_title = subfolder_page["page"]
            subfolder_url = subfolder_page.get("url")
            subfolder_slug = subfolder_page.get("slug")

            if subfolder_url:
                check_page_for_misaligned_title(subfolder_page_title, docs_root, f"{section_slug}{main_slug}/{subfolder_url}")

            if not subfolder_slug:
                continue

            for subsubfolder_page in subfolder_page["subsubfolderitems"]:
                subsubfolder_page_title = subsubfolder_page["page"]
                subsubfolder_url = subsubfolder_page.get("url")

                check_page_for_misaligned_title(subsubfolder_page_title, docs_root, f"{section_slug}{main_slug}/{subfolder_slug}/{subsubfolder_url}")


docs_root = "../docs"

# compile concatenated document
with open("../_data/menu_docs_dev.json") as menu_docs_file:
    data = json.load(menu_docs_file)
    check_section(docs_root, data, "Documentation")
    check_section(docs_root, data, "Guides")
