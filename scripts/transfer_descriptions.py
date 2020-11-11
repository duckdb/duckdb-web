
import os
import sqlite3

duckdb_web_base = os.getcwd()
benchmarks_db = os.path.join(duckdb_web_base, 'benchmarks.db')
description_db = os.path.join(duckdb_web_base, 'descriptions.db')

con = sqlite3.connect(description_db)
c = con.cursor()
c.execute('select benchmark,description from descriptions')
results = c.fetchall()


con = sqlite3.connect(benchmarks_db)
c = con.cursor()
for result in results:
	benchmark_name = result[0]
	benchmark_description = result[1]
	c.execute('UPDATE benchmarks SET description=? WHERE name=?', (benchmark_description, benchmark_name))

con.commit()
