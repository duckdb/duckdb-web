import os
import argparse
import glob

parser = argparse.ArgumentParser(
    description='Rename a page in the docs, propagate rename to archived versions and add correct redirects.'
)
parser.add_argument(
    '--source',
    dest='source_file',
    action='store',
    help='Source path (e.g. docs/extensions/sqlite_scanner.md)',
    required=True,
)
parser.add_argument(
    '--target',
    dest='target_file',
    action='store',
    help='Target path (e.g. docs/extensions/sqlite.md)',
    required=True,
)
args = parser.parse_args()

source_page = args.source_file
target_page = args.target_file

if not source_page.startswith('docs/') or not target_page.startswith('docs/'):
    raise Exception(
        f"Both source ({source_page}) and target ({target_page}) need to be in docs/ subdirectory"
    )

jekyll_marker = '\n---\n\n'


def rename_page(source, target):
    print(f'{source} -> {target}')
    with open(source, 'r') as f:
        text = f.read()
    index = text.find(jekyll_marker)
    if index < 0:
        raise Exception(
            f"Could not find front matter marker ('---') in Jekyll file {source} - failed to add redirect"
        )
    redirect_target = source.replace('.md', '')
    new_text = text[:index]
    new_text += f'\nredirect_from:\n  - {redirect_target}' + jekyll_marker
    new_text += text[index + len(jekyll_marker) :]
    with open(target, 'w+') as f:
        f.write(new_text)
    os.remove(source)

    doc_files = glob.glob('**/*.md', recursive=True)
    for doc_file in doc_files:
        with open(doc_file, 'r+') as f:
            doc_content = f.read()

        doc_content = doc_content.replace(
            f"{{% link {source} %}}", f"{{% link {target} %}}"
        )
        with open(doc_file, 'w') as f:
            f.write(doc_content)


rename_page(source_page, target_page)
