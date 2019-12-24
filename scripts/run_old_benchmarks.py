
import os, sys, time, subprocess, re

default_start_commit = '32c1e53db960f545059b5269b01cf8f28138230b'
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

os.chdir('../duckdb')
commit_list = get_list_of_commits(default_start_commit)
os.chdir('../duckdb-web')

for commit_hash in commit_list:
    proc = subprocess.Popen(['python3', 'scripts/run_benchmarks.py', commit_hash])
    proc.wait()
