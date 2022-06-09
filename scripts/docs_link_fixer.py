import os
import sys

check_only = False
if '--check' in sys.argv:
	check_only = True

base_path = 'docs'
archive_path = os.path.join('docs', 'archive')

def cleanup_links_in_directory(current_path, depth = 0):
	files = os.listdir(current_path)
	for file in files:
		if file == 'archive' and current_path == 'docs':
			continue

		abs_path = os.path.join(current_path, file)
		if os.path.isdir(abs_path):
			cleanup_links_in_directory(abs_path, depth + 1)
		else:
			if not file.endswith('.md'):
				continue
			with open(abs_path, 'r') as f:
				text = f.read()
			new_text = text.replace('](/docs/', '](' + depth * '../')
			if new_text == text:
				continue
			if check_only:
				print(f"Found absolute link to documentation in file {abs_path}")
				exit(1)
			with open(abs_path, 'w+') as f:
				f.write(new_text)

cleanup_links_in_directory(base_path)

archived_versions = os.listdir(archive_path)
for archived_version in archived_versions:
	archived_path = os.path.join(archive_path, archived_version)
	cleanup_links_in_directory(archived_path)
