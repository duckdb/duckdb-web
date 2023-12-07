import os
import argparse


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
parser.add_argument(
    '--execute',
    dest='execute',
    action='store_true',
    help='The unittest filter to apply',
    default=False,
)
args = parser.parse_args()

source_page = args.source_file
target_page = args.target_file
archive_dir = 'docs/archive'

if not source_page.startswith('docs/') or not target_page.startswith('docs/'):
    raise Exception(
        f"Both source ({source_page}) and target ({target_page}) need to be in docs/ subdirectory"
    )

jekyll_marker = '\n---\n\n'

if not args.execute:
    print('-----------------------------------------')
    print('DRY RUN - NOT ACTUALLY PERFORMING RENAME')
    print('Run with --execute to perform rename')
    print('-----------------------------------------')

def rename_page(source, target):
    print(f'{source} -> {target}')
    if not args.execute:
        return
    with open(source, 'r') as f:
        text = f.read()
    index = text.find(jekyll_marker)
    if index < 0:
        raise Exception(f"Could not find --- marker in jekyll file {source} - failed to add redirect")
    redirect_target = source.replace('.md', '')
    new_text = text[:index]
    new_text += f'\nredirect_from:\n  - {redirect_target}' + jekyll_marker
    new_text += text[index + len(jekyll_marker):]
    with open(target, 'w+') as f:
        f.write(new_text)
    os.remove(source)

# rename the main page
rename_page(source_page, target_page)

# rename the archived versions
for archive_version in os.listdir(archive_dir):
    current_archive_dir = os.path.join(archive_dir, archive_version)
    archive_source = source_page.replace('docs', current_archive_dir)
    archive_target = target_page.replace('docs', current_archive_dir)
    if not os.path.isfile(archive_source):
        continue
    rename_page(archive_source, archive_target)
