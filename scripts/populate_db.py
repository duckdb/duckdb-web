# the purpose of this script is to scrape old benchmark results info and use it to populate the sqlite db
import os, sqlite3, subprocess, sys
sqlite_db_file = 'benchmarks.db'
duckdb_base = os.path.join(os.getcwd(), '..', 'duckdb')
benchmark_base = os.path.join(duckdb_base, 'benchmark_results')
info_dir = os.path.join(benchmark_base, 'info')

def initdb():
    con = sqlite3.connect(sqlite_db_file)
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
    error VARCHAR,
    profile VARCHAR,
    stdout VARCHAR,
    stderr VARCHAR);""")
    con.commit()
    con.close()

def benchmark_already_ran(benchmark_id, commit_hash):
    # first check if this benchmark has already been run
    c.execute("SELECT * FROM timings WHERE benchmark_id=? AND hash=?", (benchmark_id, commit_hash))
    results = c.fetchall()
    if len(results) > 0:
        return True
    return False

def write_benchmark_info(benchmark, description):
    # first figure out if the benchmark is already in the database
    c.execute("SELECT id, groupname FROM benchmarks WHERE name=?", (benchmark,))
    results = c.fetchall()
    if len(results) > 0:
        # benchmark already exists, return the id
        return (results[0][0], results[0][1])
    # benchmark does not exist, write it to the database
    # get info and group
    groupname = description.split('\n')[0].split(' - ')[1].strip().lstrip('[').rstrip(']')
    # proc = subprocess.Popen([benchmark_runner, '--group', benchmark], stdout=subprocess.PIPE)
    # groupname = proc.stdout.read().decode('utf8').strip().lstrip('[').rstrip(']')
    # write to db
    c.execute("INSERT INTO benchmarks (name, groupname, description) VALUES (?, ?, ?)", (benchmark, groupname, description))
    # now fetch the id
    return write_benchmark_info(benchmark, description)

# initialize the sqlite database, if it does not exist yet
if not os.path.isfile(sqlite_db_file):
    initdb()

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()

os.chdir(duckdb_base)

# first get a list of all the benchmarks and insert them into the database
benchmarks = {}
for fname in os.listdir(info_dir):
    benchmark = fname.split('.')[0]
    with open(os.path.join(info_dir, fname), 'r') as f:
        description = f.read()
        (id, groupname) = write_benchmark_info(benchmark, description)
        benchmarks[benchmark] = [id, benchmark, groupname, description]

commit_list = os.listdir(benchmark_base)
commit_list.sort()

for benchmark_dir in commit_list:
    current_path = os.path.join(duckdb_base, benchmark_base, benchmark_dir)
    splits = benchmark_dir.split('-')
    if len(splits) != 2:
        continue
    commit_hash = benchmark_dir.split('-')[1]
    # check if we already ran the benchmark
    c.execute("SELECT hash FROM commits WHERE hash=?", (commit_hash,))
    results = c.fetchall()
    if len(results) > 0:
        continue

    print(commit_hash)
    # get the date from the commit
    proc = subprocess.Popen(['git', 'show', '-s', '--format=%ci', commit_hash], stdout=subprocess.PIPE)
    date = proc.stdout.read().decode('utf8').strip()
    proc = subprocess.Popen(['git', 'show', '-s', '--format=%B', commit_hash], stdout=subprocess.PIPE)
    commit_msg = proc.stdout.read().decode('utf8').strip()
    for bname in benchmarks.keys():
        benchmark_id = benchmarks[bname][0]
        if benchmark_already_ran(benchmark_id, commit_hash):
            continue
        # check if we have the files for this benchmark
        base = os.path.join(current_path, bname)
        tfile = base + '.csv'
        logfile = base + '.log'
        stderr_file = base + '.stderr.log'
        stdout_file = base + '.stdout.log'
        if not os.path.isfile(tfile):
            continue
        success = True
        error_msg = ""
        try:
            with open(tfile, 'r') as f:
                text = f.read().split('\n')
                timings = []
                for line in text:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    try:
                        timings.append(float(line))
                    except:
                        error_msg = line
                        raise
                timing_info = ','.join([str(x) for x in timings])
                timings.sort()
                median = timings[int(len(timings) / 2)]
                with open(logfile, 'r') as f:
                    profile_info = f.read()
                with open(stdout_file, 'r') as f:
                    stdout = f.read()
                with open(stderr_file, 'r') as f:
                    stderr = f.read()
        except:
            if len(error_msg) == 0:
                raise
            success = False
        if len(error_msg) > 0:
            # insert error into database
            # print("Error: " + error_msg)
            c.execute("INSERT INTO timings (benchmark_id, hash, success, error) VALUES (?, ?, ?, ?)", (benchmark_id, commit_hash, False, error_msg))
        else:
            # insert data about benchmark into database
            # print("Median timing: " + str(median))
            c.execute("INSERT INTO timings (benchmark_id, hash, success, median, timings, profile, stdout, stderr) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (benchmark_id, commit_hash, True, median, timing_info, profile_info, stdout, stderr))
        con.commit()

    # finished running this commit: insert it into the list of completed commits
    c.execute('INSERT INTO commits (hash, date, message) VALUES (?, ?, ?)', (commit_hash, date, commit_msg))
    con.commit()


