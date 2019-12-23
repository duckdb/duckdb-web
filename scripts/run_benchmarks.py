import os, sys, subprocess, re, time, threading, sqlite3

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
slow_benchmarks = ['append', 'imdb', 'tpcds-sf1']

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
    proc = subprocess.Popen(['make', 'opt', '-j'], stdout=FNULL, stderr=subprocess.PIPE)
    proc.wait()
    if proc.returncode != 0:
        print("Failed to compile, moving on to next commit")
        while True:
            line = proc.stderr.readline()
            if line == '':
                break
            print(line)
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
        benchmark_list.append(line.rstrip())
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
        def run_benchmark_target(self):
            self.proc.wait()

        self.proc = subprocess.Popen([benchmark_runner, '--out=' + self.out_file, '--log=' + self.log_file, self.benchmark], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        thread = threading.Thread(target=run_benchmark_target, args=(self,))
        thread.start()

        thread.join(timeout)

        self.stdout = self.proc.stdout.read().decode('utf8')
        self.stderr = self.proc.stderr.read().decode('utf8')

        if thread.is_alive():
            log("Force terminating process...")
            self.error_msg = "TIMEOUT"
            self.proc.kill()
            thread.join()
            return 1
        return self.proc.returncode

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
        # succeeded, gather data
        stdout = runner.stdout
        stderr = runner.stderr
        timings = []
        with open(runner.out_file, 'r') as f:
            for line in f.read().split('\n'):
                line = line.strip()
                if len(line) == 0:
                    continue
                timings.append(float(line))
        timing_info = ','.join([str(x) for x in timings])
        timings.sort()
        median = timings[int(len(timings) / 2)]
        with open(runner.log_file, 'r') as f:
            profile_info = f.read()
    if len(error_msg) > 0:
        # insert error into database
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
    proc = subprocess.Popen([benchmark_runner, '--info', benchmark], stdout=subprocess.PIPE)
    description = proc.stdout.read().decode('utf8').strip()
    groupname = description.split('\n')[0].split(' - ')[1].strip().lstrip('[').rstrip(']')
    # proc = subprocess.Popen([benchmark_runner, '--group', benchmark], stdout=subprocess.PIPE)
    # groupname = proc.stdout.read().decode('utf8').strip().lstrip('[').rstrip(']')
    # write to db
    c.execute("INSERT INTO benchmarks (name, groupname, description) VALUES (?, ?, ?)", (benchmark, groupname, description))
    # now fetch the id
    return write_benchmark_info(benchmark)

# initialize the sqlite database, if it does not exist yet
if not os.path.isfile(sqlite_db_file):
    initdb()

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()

# figure out the highest commit hash we already ran by looking into the db
c.execute("""
SELECT hash
FROM commits
ORDER BY date DESC
LIMIT 1
""")

pull_new_changes()

prev_hash = default_start_commit
results = c.fetchall()
if len(results) > 0:
    prev_hash = results[0][0]

# get a list of all commits we need to run
commit_list = get_list_of_commits(prev_hash)
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
    log("Benchmarking commit " + commit)
    # switch to this commit in the source tree
    if not switch_to_commit(commit):
        log("Failed to switch to commit! Moving to next commit")
        continue
    # now try to compile it
    if not build_optimized():
        continue

    # get the date from the commit
    proc = subprocess.Popen(['git', 'show', '-s', '--format=%ci', commit], stdout=subprocess.PIPE)
    date = proc.stdout.read().decode('utf8').strip()
    proc = subprocess.Popen(['git', 'show', '-s', '--format=%B', commit], stdout=subprocess.PIPE)
    commit_msg = proc.stdout.read().decode('utf8').strip()

    # now run the benchmarks
    benchmarks_to_run = get_benchmark_list()
    for benchmark in benchmarks_to_run:
        (benchmark_id, groupname) = write_benchmark_info(benchmark)
        if groupname in slow_benchmarks and not is_final_commit:
            continue
        run_benchmark(benchmark, benchmark_id, commit)
    # finished running this commit: insert it into the list of completed commits
    c.execute('INSERT INTO commits (hash, date, message) VALUES (?, ?, ?)', (commit, date, commit_msg))
    con.commit()



