import os
import re


# Modify the content of a file: replace "https://duckdb.org" in all files,
# and if it's an HTML file, also perform HTML-specific replacements
def modify_file(file_path):
    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Replace "https://duckdb.org" with `"` in all files
        content_updated = content.replace('"https://duckdb.org', '"')

        # If the file is an HTML file, perform additional replacements
        if file_path.endswith(".html"):
            content_updated = re.sub(
                r'href="(/docs[^"]*(?<!/)(?<!\.html))"', r'href="\1.html"', content_updated
            )

        # Write back only if changes were made
        if content != content_updated:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content_updated)

    except (UnicodeDecodeError, IOError):
        # Skip binary files or files that cannot be read properly
        pass


if __name__ == "__main__":
    root_directory = r"./duckdb-docs"  # Define duckdb-docs directory
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            modify_file(file_path)