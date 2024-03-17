import duckdb
import re
import sys

if len(sys.argv) == 0:
    print("Usage: function-sections.py filename")
    exit(-1)
else:
    input_filename = sys.argv[1]

input_filename_without_extension = input_filename.replace(".md", "")

# do some search-and-replace (e.g., trimming) to trim get rid of the first/last pipe
with open(input_filename) as f:
    content = f.read()
    # take care of concatenation operators manually
    #content = content.replace("||", "XXXXXX")
    content = content.replace("| ", "|")
    content = content.replace(" |", "|")
    content = content.replace("\n|", "\n")
    content = content.replace("|\n", "\n")
    # drop spaces, which were previously inserted to allow for manual line breaks
    # but they are actually quite ugly
    content = content.replace("(` ", "(`")
    content = re.sub(r"^\|", "", content, re.MULTILINE)
    first_line = content.split("\n")[0]
    with open("adjusted.csv", "w") as of:
        of.write(content)

have_aliases_column = "Alias" in first_line
have_result_column = "Result" in first_line

if have_result_column:
    result_column = ", result VARCHAR"
else:
    result_column = ""

if have_aliases_column:
    aliases_column = ", aliases VARCHAR"
else:
    aliases_column = ""


duckdb.sql(f"""
        CREATE OR REPLACE TABLE funs (function VARCHAR, description VARCHAR, example VARCHAR{result_column}{aliases_column});
        """)
duckdb.sql(f"""
        COPY funs FROM 'adjusted.csv' (FORMAT csv, DELIMITER '|', HEADER false, QUOTE '', AUTO_DETECT false, SKIP 2);
        """)

res = duckdb.sql("""
    SELECT printf(
            '| [%s](#%s) | %s |',
            trim(function),
            regexp_replace(lower(replace(function, ',', '-')), '[^-_a-z0-9]', '', 'g'), -- anchor link
            regexp_replace(trim(description) || '.', '\.\.$', '.') -- description; ensure that there is exactly one full stop at the end of the description
        ) AS s
    FROM funs;""")

with open(f"{input_filename_without_extension}-reformatted.md", "w") as md:
    for line in res.fetchall():
        md.write(f"{line[0]}\n")

    res = duckdb.sql("""FROM funs""")
    for line in res.fetchall():
        result_item = ""
        if have_result_column:
            caption = "Result"
            result_item = f"\n* **{caption}:** {line[3]}"

        aliases_item = ""
        if have_aliases_column and line[-1] is not None:
            # use plural form of 'Alias' if there is a comma (indicating a list of aliases)
            if ',' in line[-1]:
                caption = "Aliases"
            else:
                caption = "Alias"
            aliases_item = f"\n* **{caption}:** {line[-1]}"

        md.write(f"""
### {line[0]}

* **Description:** {line[1]}
* **Example:** {line[2]}{result_item}{aliases_item}

""")
