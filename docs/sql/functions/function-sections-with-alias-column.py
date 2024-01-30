import duckdb
import re

with open('in.csv') as f:
    content = f.read()
    content = content.replace("| ", "|")
    content = content.replace(" |", "|")
    content = re.sub(r"^\|", "", content, re.MULTILINE)
    content = content.replace("\n|", "\n")
    with open('adjusted.csv', 'w') as of:
        of.write(content)

# duckdb.sql("""CREATE OR REPLACE TABLE funs AS FROM read_csv('adjusted.csv', delim='|', header=false, columns={'function': 'VARCHAR', 'description': 'VARCHAR', 'example': 'VARCHAR', 'result': 'VARCHAR', 'aliases': 'VARCHAR');""")
duckdb.sql("""CREATE OR REPLACE TABLE funs (function VARCHAR, description VARCHAR, example VARCHAR, result VARCHAR, aliases VARCHAR);""")
duckdb.sql("""COPY funs FROM 'adjusted.csv' (format csv, delimiter '|', header false, quote '', auto_detect false);""")
res = duckdb.sql("""SELECT printf('| [%s](#%s) | %s |', function, regexp_replace(lower(replace(function, ',', '-')), '[^-_a-z0-9]', '', 'g'), description) AS s FROM funs;""")

with open('out.md', 'w') as md:
    for line in res.fetchall():
        md.write(f"{line[0]}\n")

    res = duckdb.sql("""FROM funs""")
    for line in res.fetchall():
        aliases = ""
        if line[4] is not None:
            caption = "Aliases" if ',' in line[4] else "Alias"
            aliases = f"\n* **{caption}:** {line[4]}"

        md.write(f"""
### {line[0]}

* **Description:** {line[1]}
* **Example:** {line[2]}
* **Result:** {line[3]}{aliases}
""")

