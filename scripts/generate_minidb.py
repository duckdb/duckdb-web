import numpy, os, sys, sqlite3, json

duckdb_web_base = os.getcwd()
big_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
minidb_file = os.path.join(duckdb_web_base, 'minibenchmarks.db')

def initminidb():
    con = sqlite3.connect(minidb_file)
    c = con.cursor()
    c.execute("""
CREATE TABLE benchmarks(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    groupname VARCHAR,
    description VARCHAR);""")
    c.execute("""
CREATE TABLE commits(
    hash VARCHAR PRIMARY KEY,
    date VARCHAR,
    message VARCHAR);""")
    c.execute("""
CREATE TABLE timings(
    hash VARCHAR,
    benchmark_id INTEGER,
    success BOOLEAN,
    median DOUBLE,
    timings VARCHAR,
    error VARCHAR);""")
    c.execute("""CREATE INDEX i_index ON timings(hash);""")
    con.commit()
    con.close()

# initialize the sqlite database, if it does not exist yet
if not os.path.isfile(minidb_file):
    initminidb()

con = sqlite3.connect(big_db_file)
c = con.cursor()

# read partial data from big database file
c.execute("SELECT id, name, groupname, description FROM benchmarks")
benchmarks = c.fetchall()
c.execute("SELECT hash, date, message FROM commits")
commits = c.fetchall()
c.execute("SELECT hash, benchmark_id, success, median, timings, error FROM timings")
timings = c.fetchall()
con.close()

# now push the data into the minidb file
con = sqlite3.connect(minidb_file)
c = con.cursor()

for benchmark_info in benchmarks:
	c.execute('SELECT * FROM benchmarks WHERE id=?', (benchmark_info[0],))
	if len(c.fetchall()) > 0:
		continue
	c.execute('INSERT INTO benchmarks (id, name, groupname, description) VALUES (?, ?, ?, ?)', benchmark_info)

for commit_info in commits:
	c.execute('SELECT * FROM commits WHERE hash=?', (commit_info[0],))
	if len(c.fetchall()) > 0:
		continue
	c.execute('INSERT INTO commits (hash, date, message) VALUES (?, ?, ?)', commit_info)

for timing_info in timings:
	c.execute('SELECT * FROM timings WHERE hash=? AND benchmark_id=?', (timing_info[0], timing_info[1]))
	if len(c.fetchall()) > 0:
		continue
	c.execute('INSERT INTO timings (hash, benchmark_id, success, median, timings, error) VALUES (?, ?, ?, ?, ?, ?)', timing_info)

con.commit()




