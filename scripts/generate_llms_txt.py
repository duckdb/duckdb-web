#!/usr/bin/env python3

import os
import frontmatter
from pathlib import Path


def generate_docs_llms_files():
    """Generate llms.txt and llms-full.txt for the docs/stable directory"""
    # Path to the docs/stable directory
    docs_dir = Path('docs/stable')

    # Initialize content for both files
    llms_content = []
    llms_full_content = []

    # Group files by directory
    file_groups = {}

    # Walk through all markdown files in docs/stable
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if not file.endswith('.md'):
                continue

            file_path = Path(root) / file
            relative_path = file_path.relative_to(docs_dir)

            # Get the directory name for grouping
            dir_name = str(relative_path.parent)
            if dir_name == '.':
                dir_name = 'root'

            # Read and parse the markdown file
            with open(file_path, 'r') as f:
                doc = frontmatter.load(f)

            # Get the title and content
            title = doc.get('title', '')
            content = doc.content.strip()

            # For website URL, remove the .md extension
            website_path = str(relative_path)
            if website_path.endswith('.md'):
                website_path = website_path[:-3]
            website_url = f"https://duckdb.org/docs/stable/{website_path}"

            # Add to file groups
            if dir_name not in file_groups:
                file_groups[dir_name] = []

            file_groups[dir_name].append(
                {
                    'title': title,
                    'website_url': website_url,
                    'content': content,
                }
            )

            # Add to llms-full.txt (titles, links, and content)
            llms_full_content.append(f"# {title}\n")
            llms_full_content.append(f"Website: {website_url}\n")
            llms_full_content.append("---\n")
            llms_full_content.append(content)
            llms_full_content.append("\n\n")

    # Generate llms.txt content with grouped structure
    for dir_name, files in sorted(file_groups.items()):
        # Format directory name for display
        if dir_name == 'root':
            section_title = "Documentation"
        else:
            section_title = dir_name.replace('/', ' ').title()

        llms_content.append(f"## {section_title}\n")

        for file_info in sorted(files, key=lambda x: x['title']):
            llms_content.append(f"- [{file_info['title']}]({file_info['website_url']})")

        llms_content.append("")

    # Write llms.txt
    with open(docs_dir / 'llms.txt', 'w') as f:
        f.write("# DuckDB Documentation\n\n")
        f.write(
            "> Comprehensive documentation for DuckDB, an in-process analytical database management system.\n\n"
        )
        f.write('\n'.join(llms_content))

    # Write llms-full.txt
    with open(docs_dir / 'llms-full.txt', 'w') as f:
        f.write("# DuckDB Full Documentation\n\n")
        f.write('\n'.join(llms_full_content))


def main():
    # Generate the docs-specific llms.txt and llms-full.txt files
    generate_docs_llms_files()

    print("Generated docs/stable/llms.txt and docs/stable/llms-full.txt successfully!")


if __name__ == '__main__':
    main()
