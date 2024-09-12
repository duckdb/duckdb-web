import os
import re


# Replace href="(/docs[^"]*[^/])" with href="$1.html" in HTML files
def process_html_file(file_path):
    # print("procesing html file:\t",file_path)
    with open(file_path, "r", encoding="UTF-8") as file:
        content = file.read()

    # Replace href="(/docs[^"]*[^/])" with href="$1.html"
    content_updated = re.sub(
        r'href="(/docs[^"]*(?<!/)(?<!\.html))"', r'href="\1.html"', content
    )

    # Write the updated content back to the file
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(content_updated)


# Replace in search_data.json file only
# def process_search_data_json(file_path):
#     # print("procesing `search_data.json`")
#     with open(file_path, "r", encoding="UTF-8") as file:
#         content = file.read()

#     # Apply specific replacement for search_data.json
#     content_updated = re.sub(r'"(/docs[^"]*(?<!/)(?<!\.html))"', r'"\1.html"', content)

#     # Write the updated content back to the file
#     with open(file_path, "w", encoding="UTF-8") as file:
#         file.write(content_updated)


# Replace "https://duckdb.org" with an empty string in text file
def replace_duckdb_org(file_path):
    # print('Replace `"https://duckdb.org` with `"`:\t',file_path)
    try:
        # Attempt to open the file in text mode
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Replace `"https://duckdb.org` with `"`
        content_updated = content.replace('"https://duckdb.org', '"')

        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content_updated)

    except (UnicodeDecodeError, IOError):
        # If a UnicodeDecodeError occurs, it's likely a binary file, so we skip it
        # print(f"Skipping binary file: {file_path}")
        pass


# Recursively find and apply changes to files
def process_files(root_dir, file_ext, processing_function):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(file_ext):
                file_path = os.path.join(subdir, file)
                # if file_path == r"./duckdb-docs/data/search_data.json":
                #     process_search_data_json(file_path)
                # else:
                processing_function(file_path)


# Main function to apply all steps
def main():
    root_directory = (
        r"./duckdb-docs"
    )

    process_files(root_directory, "", replace_duckdb_org)

    process_files(root_directory, ".html", process_html_file)


if __name__ == "__main__":
    main()