import os, sys, subprocess, re, time, threading, sqlite3, sys

FNULL = open(os.devnull, 'w')
benchmark_runner = os.path.join('build', 'release', 'benchmark', 'benchmark_runner')
out_file = 'out.csv'
log_file = 'out.log'
default_start_commit = '0109d4301b8ed005ca5396c177cf5ef36bef5274'
duckdb_base = os.path.join(os.getcwd(), '..', 'duckdb')
duckdb_web_base = os.getcwd()
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
# 5 minute timeout per benchmark
total_timeout = 300
# slow benchmarks are skipped for all commits except the most recent commit to speed up benchmarking
# e.g. if a merge of 20+ commits is done, we don't want to run the slow benchmarks for all commits
slow_benchmarks = ['imdb']
ignored_benchmarks = ['expression_reordering']
# the specific commit to run (if any)
specific_commit = None

if len(sys.argv) > 1:
    specific_commit = sys.argv[1]
    print("Running specific commit " + specific_commit)

def log(msg):
    print(msg)

def initdb():
    con = sqlite3.connect(sqlite_db_file)
    c = con.cursor()
    c.execute("""
CREATE TABLE benchmarks(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    groupname VARCHAR,
    subgroup VARCHAR,
    description VARCHAR);""")
    c.execute("""
CREATE TABLE groups(
    name VARCHAR,
    subgroup VARCHAR,
    display_name VARCHAR,
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
    meta_info VARCHAR,
    graph_json VARCHAR,
    stdout VARCHAR,
    stderr VARCHAR);""")
    con.commit()
    con.close()

run_with_timeout_returncode = 0
def run_with_timeout(command, timeout):
    global run_with_timeout_returncode
    def run_with_timeout_internal(command):
        global run_with_timeout_returncode
        run_with_timeout_returncode = os.system(' '.join(command) + " > out.log 2>err.log")

    try:
        os.remove('out.log')
    except:
        pass
    try:
        os.remove('err.log')
    except:
        pass
    thread = threading.Thread(target=run_with_timeout_internal, args=(command,))
    thread.start()

    thread.join(timeout)

    stdout = ""
    stderr = ""
    try:
        with open('out.log', 'r') as f:
            stdout = f.read()
        with open('err.log', 'r') as f:
            stderr = f.read()
    except:
        pass

    if thread.is_alive():
        log("Force terminating process...")
        os.system('killall -9 benchmark_runner')
        error_msg = "TIMEOUT"
        thread.join()
        return (1, stdout, stderr, error_msg)
    return (run_with_timeout_returncode, stdout, stderr, "")


def pull_new_changes():
    # pull from duckdb-web
    os.chdir(duckdb_web_base)
    proc = subprocess.Popen(['git', 'pull'], stdout=FNULL)
    proc.wait()
    # pull from duckdb
    os.chdir(duckdb_base)
    proc = subprocess.Popen(['git', 'pull', 'origin', 'master'], stdout=FNULL)
    proc.wait()

def build_optimized():
    log("Starting optimized build")
    # always rebuild
    os.system('rm -rf build')
    os.environ['BUILD_BENCHMARK'] = '1'
    os.environ['BUILD_TPCH'] = '1'
    os.environ['BUILD_PYTHON'] = '1'
    os.environ['USER_SPACE'] = '1'
    (return_code, stdout, stderr, error_msg) = run_with_timeout(['make', 'opt', '-j'], 1200)

    if return_code != 0:
        print("Failed to compile, moving on to next commit")
        print(stdout)
        print(stderr)
        print(error_msg)
        return False
    else:
        log("Finished optimized build")
        return True

def get_list_of_commits(until_commit=None):
    proc = subprocess.Popen(['git', 'checkout', 'master'], stdout=subprocess.PIPE)
    proc.wait()
    commit_list = []
    commit_regex = re.compile('commit ([a-z0-9]{40})')
    proc = subprocess.Popen(['git', 'log'], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode('utf8')
        if line == '':
            break
        match = commit_regex.search(line)
        if match != None:
            commit_number = match.groups()[0]
            if commit_number == until_commit:
                break
            commit_list.append(commit_number)
    commit_list.reverse()
    return commit_list

def switch_to_commit(commit_number):
    proc = subprocess.Popen(['git', 'checkout', commit_number])
    proc.wait()
    return proc.returncode == 0

def get_benchmark_list():
    benchmark_list = []
    proc = subprocess.Popen([benchmark_runner, '--list'], stdout=subprocess.PIPE)
    for line in proc.stdout.read().decode('utf8').split('\n'):
        bname = line.rstrip()
        if len(bname) > 0:
            benchmark_list.append(bname)
    return benchmark_list


class RunBenchmark(object):
    def __init__(self, benchmark, log_file, stdout_name, stderr_name, out_file):
        self.benchmark = benchmark
        self.log_file = log_file
        self.stdout_name = stdout_name
        self.stderr_name = stderr_name
        self.out_file = out_file
        self.proc = None
        self.error_msg = ""

    def run(self, timeout):
        command = [benchmark_runner, '--out=' + self.out_file, '--log=' + self.log_file, self.benchmark]

        (returncode, self.stdout, self.stderr, self.error_msg) = run_with_timeout(command, timeout)
        return returncode

def benchmark_already_ran(benchmark_id, commit_hash):
    # first check if this benchmark has already been run
    c.execute("SELECT * FROM timings WHERE benchmark_id=? AND hash=?", (benchmark_id, commit_hash))
    results = c.fetchall()
    if len(results) > 0:
        return True
    return False

def run_benchmark(benchmark, benchmark_id, commit_hash):
    if benchmark_already_ran(benchmark_id, commit_hash):
        return

    log("Starting benchmark " + benchmark)
    base_path = '/tmp/benchmark'

    log_file = base_path + ".log"
    stdout_name = base_path + ".stdout.log"
    stderr_name = base_path + ".stderr.log"
    runner = RunBenchmark(benchmark, log_file, stdout_name, stderr_name, out_file)

    return_code = runner.run(total_timeout)

    error_msg = ""
    if len(runner.error_msg) > 0:
        error_msg = runner.error_msg
    elif return_code != 0:
        log("Failed to run benchmark " + benchmark)
        error_msg = "CRASH"
    else:
        log("Succeeded in running benchmark " + benchmark)
        try:
            # succeeded, gather data
            stdout = runner.stdout
            stderr = runner.stderr
            timings = []
            with open(runner.out_file, 'r') as f:
                for line in f.read().split('\n'):
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
            with open(runner.log_file, 'r') as f:
                profile_info = f.read()
        except:
            if len(error_msg) == 0:
                # no error message specified
                raise

    if len(error_msg) > 0:
        # insert error into database
        print("Error: " + error_msg)
        c.execute("INSERT INTO timings (benchmark_id, hash, success, error) VALUES (?, ?, ?, ?)", (benchmark_id, commit_hash, False, error_msg))
    else:
        # insert data about benchmark into database
        print("Median timing: " + str(median))
        c.execute("INSERT INTO timings (benchmark_id, hash, success, median, timings, profile, stdout, stderr, meta_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'none')", (benchmark_id, commit_hash, True, median, timing_info, profile_info, stdout, stderr))
    con.commit()

def get_benchmark_info(benchmark):
    display_name = None
    groupname = None
    subgroup = None
    proc = subprocess.Popen([benchmark_runner, '--info', benchmark], stdout=subprocess.PIPE)
    lines = proc.stdout.read().decode('utf8').strip().split('\n')
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        splits = line.split(':')
        if splits[0] == 'display_name':
            display_name = splits[1].strip()
        elif splits[0] == 'group':
            groupname = splits[1].strip()
        elif splits[0] == 'subgroup':
            subgroup = splits[1].strip()
            if len(subgroup) == 0:
                subgroup = None
    return (display_name, groupname, subgroup)

def insert_benchmark_info(display_name,groupname,subgroup):
    # first figure out if the benchmark is already in the database
    c.execute("SELECT id, groupname FROM benchmarks WHERE name=?", (display_name,))
    results = c.fetchall()
    if len(results) > 0:
        # benchmark already exists, return the id
        return (results[0][0], results[0][1])
    # benchmark does not exist, write it to the database
    # get info and group
    # write to db
    c.execute("INSERT INTO benchmarks (name, groupname, subgroup) VALUES (?, ?, ?)", (display_name, groupname, subgroup))
    c.execute("SELECT id, groupname FROM benchmarks WHERE name=?", (display_name,))
    results = c.fetchall()
    if len(results) > 0:
        # benchmark already exists, return the id
        return (results[0][0], results[0][1])


def write_benchmark_info(benchmark):
    (display_name, groupname, subgroup) = get_benchmark_info(benchmark)
    if display_name is None:
        log("Failed to fetch display name for benchmark " + benchmark)
        return (None, None)
    return insert_benchmark_info(display_name,groupname,subgroup)

def run_arrow(commit_hash,column_name,experiment_name,duck_con):
    import statistics,duckdb,pyarrow
    duck_to_arrow = []
    arrow_to_duck = []
    for i in range(6):
        duck_con.execute("select " + column_name +  " from t;")

        start_time = time.time()
        result = duck_con.fetch_arrow_table()
        time_duck_to_arrow = time.time() - start_time

        start_time = time.time()
        result = duckdb.from_arrow_table(result)
        time_arrow_to_duck = time.time() - start_time

        if i!= 0:
            duck_to_arrow.append(time_duck_to_arrow)
            arrow_to_duck.append(time_arrow_to_duck)

    (benchmark_id, groupname) = insert_benchmark_info('duckdb -> arrow ' + experiment_name,'arrow_integration','')
    c.execute("INSERT INTO timings (benchmark_id, hash, success, median) VALUES (?, ?, ?, ?)", (benchmark_id, commit_hash, True, statistics.median(duck_to_arrow)))
    (benchmark_id, groupname) = insert_benchmark_info('arrow -> duckdb ' + experiment_name,'arrow_integration','')
    c.execute("INSERT INTO timings (benchmark_id, hash, success, median) VALUES (?, ?, ?, ?)", (benchmark_id, commit_hash, True, statistics.median(arrow_to_duck)))
    con.commit()

def run_arrow_tpch(commit_hash,duck_con):
    #Only run Queries 1 and 6
    import statistics,duckdb,pyarrow
    query_times = []
    tpch_queries = [1,6]
    duck_con.execute("CALL dbgen(sf=1);")
    tpch_tables = ['lineitem']
    arrow_tables = []
    for tpch_table in tpch_tables:
        duck_tbl = duck_con.table(tpch_table)
        arrow_tables.append(duck_tbl.arrow())
        duck_arrow_table = duck_con.from_arrow_table(arrow_tables[-1])
        duck_con.execute("DROP TABLE "+tpch_table)
        duck_arrow_table.create(tpch_table)

    for tpch_query in tpch_queries:
        query = duck_con.execute("select query from tpch_queries() where query_nr="+str(tpch_query)).fetchone()[0]
        for i in range(6):
            start_time = time.time()
            result = duck_con.execute(query)
            q_time = time.time() - start_time
            if i!= 0:
                query_times.append(q_time)

        (benchmark_id, groupname) = insert_benchmark_info('arrow tpch Q'+str(tpch_query),'arrow_integration','')
        c.execute("INSERT INTO timings (benchmark_id, hash, success, median) VALUES (?, ?, ?, ?)", (benchmark_id, commit_hash, True, statistics.median(query_times)))
    con.commit()

def run_arrow_parallel(commit_hash,duck_con):
    import statistics,duckdb,pyarrow, numpy
    batch_sizes = [1024, 100000, 1000000]
    num_threads = [1,2,4,8]
    data = (pyarrow.array(numpy.random.randint(800, size=100000000), type=pyarrow.int32()))
    duckdb_conn = duckdb.connect()
    for batch in batch_sizes:
        for thread in num_threads:
            tbl = pyarrow.Table.from_batches(pyarrow.Table.from_arrays([data],['a']).to_batches(batch))
            rel = duckdb_conn.from_arrow_table(tbl)
            duckdb_conn.execute("PRAGMA threads="+str(thread))
            duckdb_conn.execute("PRAGMA force_parallelism")
            total_times=[]
            for i in range(6):
                start_time = time.time()
                result = rel.aggregate("(count(a))::INT").execute()
                total_time = time.time() - start_time
                if i!= 0:
                    total_times.append(total_time)

            (benchmark_id, groupname) = insert_benchmark_info('threads:' +str(thread) + ' batch_size:' +str(batch) ,'arrow_integration','')
            c.execute("INSERT INTO timings (benchmark_id, hash, success, median) VALUES (?, ?, ?, ?)", (benchmark_id, commit_hash, True, statistics.median(total_times)))
    con.commit()

def run_arrow_benchmarks(commit_hash):
    import duckdb
    duck_con = duckdb.connect()
    duck_con.execute ("""create temporary table t as 
                select (RANDOM()*(100000)+10000000)::INTEGER int_val,
                    CASE
                        WHEN range%10=0 THEN NULL
                        ELSE (RANDOM()*(100000)+10000000)::INTEGER
                    END int_n_val,

                    (RANDOM()*(100000)+10000000)::INTEGER::VARCHAR str_val,
                     CASE
                        WHEN range%10=0 THEN NULL
                        ELSE (RANDOM()*(100000)+10000000)::INTEGER::VARCHAR
                    END str_n_val

                    from range(100000000);""")

    run_arrow(commit_hash,'int_val','int',duck_con)
    run_arrow(commit_hash,'int_n_val','int (null)',duck_con)
    run_arrow(commit_hash,'str_val','str',duck_con)
    run_arrow(commit_hash,'str_n_val','str (null)',duck_con)
    run_arrow_parallel(commit_hash,duck_con)
    run_arrow_tpch(commit_hash,duck_con)


def run_benchmark_for_commit(commit, run_slow_benchmarks):
    log("Benchmarking commit " + commit)
    # switch to this commit in the source tree
    if not switch_to_commit(commit):
        log("Failed to switch to commit!")
        return

    # get the commit hash, date and commit msg from the commit
    proc = subprocess.Popen(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
    commit = proc.stdout.read().decode('utf8').strip()
    proc = subprocess.Popen(['git', 'show', '-s', '--format=%ci', commit], stdout=subprocess.PIPE)
    date = proc.stdout.read().decode('utf8').strip()
    proc = subprocess.Popen(['git', 'show', '-s', '--format=%B', commit], stdout=subprocess.PIPE)
    commit_msg = proc.stdout.read().decode('utf8').strip()
    if 'Merge pull request' not in commit_msg:
        log("Skipping commit " + commit + ", not a pull request merge (" + commit_msg + ")")
        return

    # now try to compile it
    if not build_optimized():
        log("Failed to build!")
        return

    # now run the benchmarks
    benchmarks_to_run = get_benchmark_list()
    for benchmark in benchmarks_to_run:
        (benchmark_id, groupname) = write_benchmark_info(benchmark)
        if benchmark_id is None:
            log("Failed to fetch benchmark id for benchmark " + benchmark)
            return
        if groupname in ignored_benchmarks or (groupname in slow_benchmarks and not run_slow_benchmarks):
            continue
        run_benchmark(benchmark, benchmark_id, commit)
    run_arrow_benchmarks(commit)
    # finished running this commit: insert it into the list of completed commits
    c.execute("SELECT * FROM commits WHERE hash=?", (commit,))
    if len(c.fetchall()) == 0:
        c.execute('INSERT INTO commits (hash, date, message) VALUES (?, ?, ?)', (commit, date, commit_msg))
    con.commit()

# initialize the sqlite database, if it does not exist yet
if not os.path.isfile(sqlite_db_file):
    initdb()

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()

pull_new_changes()

if specific_commit != None:
    run_benchmark_for_commit(specific_commit, False)
    exit(0)

# figure out the highest commit hash we already ran by looking into the db
c.execute("""
SELECT hash
FROM commits
ORDER BY date DESC
LIMIT 1
""")

prev_hash = default_start_commit
results = c.fetchall()
if len(results) > 0:
    prev_hash = results[0][0]

print("Running benchmarks since commit " + prev_hash)

# get a list of all commits we need to run
commit_list = get_list_of_commits(prev_hash)
if len(commit_list) == 0:
    exit(1)

print("List of commits: " + str(commit_list))

for commit in commit_list:
    is_final_commit = commit == commit_list[-1]
    run_benchmark_for_commit(commit, is_final_commit)



