import duckdb
import re

with open('in.csv') as f:
    content = f.read()
    content = content.replace("| ", "|")
    content = content.replace(" |", "|")
    content = re.sub(r"^\|", "", content, re.MULTILINE)
    content = content.replace("\n|", "\n")
    content = content.replace("|\n", "\n")
    with open('adjusted.csv', 'w') as of:
        of.write(content)

duckdb.sql("""CREATE OR REPLACE TABLE funs (function VARCHAR, description VARCHAR, example VARCHAR, result VARCHAR);""")
duckdb.sql("""INSERT INTO funs FROM read_csv('adjusted.csv', delim='|');""")
res = duckdb.sql("""SELECT printf('| [%s](#%s) | %s |', function, regexp_replace(lower(replace(function, ',', '-')), '[^-_a-z0-9]', '', 'g'), description) AS s FROM funs;""")

with open('out.md', 'w') as md:
    for line in res.fetchall():
        md.write(f"{line[0]}\n")

    res = duckdb.sql("""FROM funs""")
    for line in res.fetchall():
        md.write(f"""
### {line[0]}

* **Description:** {line[1]}
* **Example:** {line[2]}
* **Result:** {line[3]}
""")

