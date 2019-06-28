

# result of the packing the info directory:
# one CSV file: benchmark,category

# one JSON file: benchmark-info.json

# one CSV file: category

import os, json

path = '/Users/myth/Programs/duckdb-web/benchmarking/benchmark_results/info'

name_map = {
	"[tpch-sf1]": "TPC-H",
	"[csv]": "CSV",
	"[tpcds-sf1]": "TPC-DS"
}

categories = dict()

result_csv = open('benchmarks.csv', 'w+')
result_csv.write("benchmark,category,info\n")

info = dict()

for fname in os.listdir(path):
	with open(os.path.join(path, fname), 'r') as f:
		contents = f.read()
	first_line = contents.split('\n')[0]
	category = first_line.split(' - ')[1]
	categories[category] = 1
	benchmark_name = fname.split('.')[0]
	info[benchmark_name] = contents
	result_csv.write("%s,%s\n" % (benchmark_name,category))

result_csv.close()

with open('benchmark-info.json', 'w+') as f:
	json.dump(info, f)


with open('categories.csv', 'w+') as f:
	f.write("category,name\n")
	for key in categories.keys():
		category_name = key.replace("[", "").replace("]", "").replace("-", " ").title()
		if key in name_map:
			category_name = name_map[key]
		f.write("%s,%s\n" % (key, category_name))

