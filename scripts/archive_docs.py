import sys
import os
import shutil
import datetime
import subprocess

# Usage instructions: 
# Update _config.yml to specify the new version number
# Add a new row to /_data/versions.csv with the new version number
# Run this script. More options below, but as an example:
# 	run this script in the top level docs directory like: python scripts/archive_docs.py 0.3.4

if len(sys.argv) < 2:
	print("Usage: python scripts/archive_docs.py [version] [--noconfirm] [--date=YYYY-MM-DD]")
	print("If date is specified, this script will copy docs that existed at that specific date")
	print("Otherwise files are copied over as-is")
	exit(1)

git_log_cmd = ['git', 'log', "--pretty=format:%H %cI"]
git_ls_cmd = ['git', 'ls-tree', '--name-only']
git_show_cmd = ['git', 'show']

date = None
confirm = True
arguments = sys.argv
for i in range(len(arguments)):
	if arguments[i] == '--noconfirm':
		confirm = False
		del arguments[i]
		i -= 1
	elif arguments[i].startswith("--date="):
		date = datetime.datetime.strptime(arguments[i].split('=')[1], '%Y-%m-%d')
		date = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)

def execute_and_get_output(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout = proc.stdout.read()
	stderr = proc.stderr.read()
	proc.wait()
	if proc.returncode != 0:
		print(f"Command '{cmd}' failed!")
		print(stdout)
		print(stderr)
		exit(1)
	return stdout

revision = None
if date != None:
	log_files = execute_and_get_output(git_log_cmd).decode('utf8').split('\n')
	for line in log_files:
		splits = line.split(' ')
		parsed_date = datetime.datetime.strptime(splits[1], '%Y-%m-%dT%H:%M:%S%z')
		rev_date = datetime.datetime(parsed_date.year, parsed_date.month, parsed_date.day, parsed_date.hour, parsed_date.minute, parsed_date.second)
		if rev_date < date:
			break
		else:
			revision = splits[0]
	print(f"Formatting for {revision} (committed on {rev_date})")

ignored_files = ['.DS_Store', 'archive', 'faq.md', 'twitter_wall.md', 'why_duckdb.md']

version = arguments[1]
folder = os.path.join('docs', 'archive', version)

print(f"Archiving current docs for version \"{version}\" to path \"{folder}\". Remember to update _config.yml and /_data/versions.csv also.")
if confirm:
    result = input("Continue with archival (y/n)?\n")
    if result != 'y':
        print("Aborting.")
        exit(0)

def list_tree(source):
	if revision == None:
		return os.listdir(source)
	else:
		output = execute_and_get_output(git_ls_cmd + [revision, source + '/'])
		output = output.decode('utf8').split('\n')
		output = [os.path.basename(x) for x in output if len(x) > 0]
		return output

def copy_file(source_path, target_path):
	print(f"{source_path} -> {target_path}")
	if revision == None:
		shutil.copy(source_path, target_path)
	else:
		output = execute_and_get_output(git_show_cmd + [revision + ':' + source_path])
		file_content = output
		with open(target_path, 'wb+') as f:
			f.write(file_content)



def recursive_copy(source, target):
	if not os.path.exists(target):
		os.mkdir(target)
	for fname in list_tree(source):
		if fname in ignored_files:
			continue
		source_path = os.path.join(source, fname)
		target_path = os.path.join(target, fname)
		if os.path.isfile(source_path):
			copy_file(source_path, target_path)
		elif os.path.isdir(source_path):
			recursive_copy(source_path, target_path)


recursive_copy('docs', folder)
copy_file('_data/menu_docs_dev.json', '_data/menu_docs_%s.json' % (version.replace('.', ''),), )
