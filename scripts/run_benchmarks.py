import os, sys, subprocess, re, time, threading, sqlite3, sys

FNULL = open(os.devnull, 'w')
benchmark_runner = os.path.join('build', 'release', 'benchmark', 'benchmark_runner')
out_file = 'out.csv'
log_file = 'out.log'
default_start_commit = '32c1e53db960f545059b5269b01cf8f28138230b'
duckdb_base = os.path.join(os.getcwd(), '..', 'duckdb')
duckdb_web_base = os.getcwd()
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
# 5 minute timeout per benchmark
total_timeout = 300
# run at most 30 commits per pull
maximum_commit_count = 30
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

def run_with_timeout(command, timeout):
    def run_with_timeout_internal(proc):
        proc.wait()

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    thread = threading.Thread(target=run_with_timeout_internal, args=(proc,))
    thread.start()

    thread.join(timeout)

    stdout = proc.stdout.read().decode('utf8')
    stderr = proc.stderr.read().decode('utf8')

    if thread.is_alive():
        log("Force terminating process...")
        error_msg = "TIMEOUT"
        proc.kill()
        thread.join()
        return (1, stdout, stderr, error_msg)
    return (proc.returncode, stdout, stderr, "")


def pull_new_changes():
    # pull from duckdb-web
    os.chdir(duckdb_web_base)
    proc = subprocess.Popen(['git', 'pull'], stdout=FNULL)
    proc.wait()
    # pull from duckdb
    os.chdir(duckdb_base)
    proc = subprocess.Popen(['git', 'pull'], stdout=FNULL)
    proc.wait()

def build_optimized():
    log("Starting optimized build")
    # always rebuild
    os.system('rm -rf build')
    os.environ['BUILD_BENCHMARK'] = '1'
    os.environ['BUILD_TPCH'] = '1'

    (return_code, stdout, stderr, error_msg) = run_with_timeout(['make', 'opt', '-j'], 1200)

    if returncode != 0:
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
        c.execute("INSERT INTO timings (benchmark_id, hash, success, median, timings, profile, stdout, stderr) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (benchmark_id, commit_hash, True, median, timing_info, profile_info, stdout, stderr))
    con.commit()

def write_benchmark_info(benchmark):
    # first figure out if the benchmark is already in the database
    c.execute("SELECT id, groupname FROM benchmarks WHERE name=?", (benchmark,))
    results = c.fetchall()
    if len(results) > 0:
        # benchmark already exists, return the id
        return (results[0][0], results[0][1])
    # benchmark does not exist, write it to the database
    # get info and group
    try:
        proc = subprocess.Popen([benchmark_runner, '--info', benchmark], stdout=subprocess.PIPE)
        description = proc.stdout.read().decode('utf8').strip()
        # groupname = description.split('\n')[0].split(' - ')[1].strip().lstrip('[').rstrip(']')
        proc = subprocess.Popen([benchmark_runner, '--group', benchmark], stdout=subprocess.PIPE)
        groupname = proc.stdout.read().decode('utf8').strip().lstrip('[').rstrip(']')
    except:
        print("Could not figure out description or group name for benchmark " + benchmark)
        raise
    # write to db
    c.execute("INSERT INTO benchmarks (name, groupname, description) VALUES (?, ?, ?)", (benchmark, groupname, description))
    # now fetch the id
    return write_benchmark_info(benchmark)

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
        if groupname in ignored_benchmarks or (groupname in slow_benchmarks and not run_slow_benchmarks):
            continue
        run_benchmark(benchmark, benchmark_id, commit)
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

# get a list of all commits we need to run
commit_list = get_list_of_commits(prev_hash)
if len(commit_list) == 0:
    exit(1)

# we limit the amount of commits we run at once
if len(commit_list) > maximum_commit_count:
    new_commit_list = []
    interval = int(len(commit_list) / maximum_commit_count)
    index = 0
    while index < len(commit_list):
        new_commit_list.append(commit_list[index])
        index += interval
    if commit_list[-1] not in new_commit_list:
        new_commit_list.append(commit_list[-1])
    commit_list = new_commit_list

for commit in commit_list:
    is_final_commit = commit == commit_list[-1]
    run_benchmark_for_commit(commit, is_final_commit)



