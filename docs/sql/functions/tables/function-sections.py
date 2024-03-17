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
            function,
            regexp_replace(lower(replace(function, ',', '-')), '[^-_a-z0-9]', '', 'g'),
            regexp_replace(trim(description) || '.', '\.\.$', '.'), -- ensure there is exactly one full stop at the end of the description
        ) AS s
    FROM funs;
    """)

with open(f"{input_filename_without_extension}-reformatted.md", "w") as md:
    for line in res.fetchall():
        md.write(f"{line[0]}\n")

    res = duckdb.sql("""FROM funs""")
    for line in res.fetchall():
        result_item = ""
        if have_result_column:
            caption = "Result"
            result = f"\n* **{caption}:** {line[4]}"

        aliases_item = ""
        if have_aliases_column:
            # use plural form of 'Alias' if there is a comma (indicating a list of aliases)
            caption = "Aliases" if ',' in line[-1] else "Alias"
            aliases = f"\n* **{caption}:** {line[-1]}"

        md.write(f"""
### {line[0]}

* **Description:** {line[1]}
* **Example:** {line[2]}{result}{aliases}

""")
