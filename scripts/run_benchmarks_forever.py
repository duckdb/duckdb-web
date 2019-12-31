
import os, sys, time, subprocess

# move to the base directory
path = os.path.dirname(sys.argv[0])
if len(path) > 0:
    os.chdir(path)
os.chdir("..")

while True:
    proc = subprocess.Popen(['python3', 'scripts/run_benchmarks.py'])
    proc.wait()
    if proc.returncode == 0:
        os.system('scripts/transfer.sh')
    time.sleep(60)
