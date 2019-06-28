
import os
import json

# XXX-stdout.json
# contains [benchmark_name] -> [stdout]
# XXX-stderr.json
# contains [benchmark_name] -> [stderr]

path = "/Users/myth/Programs/duckdb-web/benchmarking/benchmark_results/0361-c1cbc9d0b5f98a425bfb7edb5e6c59b5d10550e4"

name = path.split('/')[-1].split('-')[0]

files = os.listdir(path)

timings = {}

result_csv = open('%06d-results.csv' % (int(name),), 'w+')
stderr = {}
stdout = {}

for f in files:
	with open(os.path.join(path, f), 'r') as p:
		contents = p.read()
	splits = f.split('.')
	benchmark_name = splits[0]
	ext = splits[1]
	# if ext == 'csv':
	# 	# handle CSV
	# 	sum = 0.0
	# 	count = 0
	# 	error = ""
	# 	for line in contents.split('\n'):
	# 		if len(line) == 0:
	# 			continue
	# 		try:
	# 			sum += float(line)
	# 			count += 1
	# 		except:
	# 			error = "T"
	# 			break
	# 	if len(error) == 0:
	# 		error = str(sum / count)
	# 	result_csv.write("%d,%s,%s\n" % (int(name), benchmark_name, error,))
	if ext == 'stderr':
		stderr[benchmark_name] = contents
	elif ext == 'stdout':
		stdout[benchmark_name] = contents


result_csv.close()

with open('%06d-stderr.json' % (int(name),), 'w+') as f:
	json.dump(stderr, f)

with open('%06d-stdout.json' % (int(name),), 'w+') as f:
	json.dump(stdout, f)



