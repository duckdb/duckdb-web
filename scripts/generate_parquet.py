import os, sys, subprocess, re, time, threading, sqlite3, sys
import duckdb
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb_query_graph

duckdb_web_base = os.getcwd()
benchmark_dir = os.path.join('..', 'benchmark-results')
# image_dir = os.path.join('images', 'graphs')
image_dir = os.path.join('..', 'benchmark-results', 'graphs')
groups_dir = os.path.join(benchmark_dir, 'groups')
individual_benchmarks_dir = os.path.join(benchmark_dir, 'benchmarks')
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
# sqlite_db_file = os.path.join(duckdb_web_base, 'minibenchmarks.db')

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()

# generate the group parquet files
c.execute("select distinct groupname from benchmarks where groupname is not null and groupname <> ''")
groups = [x[0] for x in c.fetchall()]

c.execute("select hash from commits order by date desc limit 15")
commits = ["'" + x[0] + "'" for x in c.fetchall()]

if not os.path.isdir(benchmark_dir):
	os.mkdir(benchmark_dir)

if not os.path.isdir(groups_dir):
	os.mkdir(groups_dir)

if not os.path.isdir(individual_benchmarks_dir):
	os.mkdir(individual_benchmarks_dir)

for groupname in groups:
	query = '''
SELECT timings.hash, commits.date, benchmarks.name, timings.median, timings.success, benchmarks.id
FROM timings, benchmarks, commits
WHERE benchmark_id=benchmarks.id
  AND commits.hash=timings.hash
  AND groupname = '%s'
  AND timings.hash IN (%s)
ORDER BY benchmarks.name ASC, date DESC
''' % (groupname, ', '.join(commits))
	c.execute(query)
	qresults      = c.fetchall()
	hashes        = [x[0] for x in qresults]
	dates         = [x[1] for x in qresults]
	benchmarks    = [x[2] for x in qresults]
	timings       = [x[3] for x in qresults]
	successes     = [x[4] for x in qresults]
	benchmark_ids = [x[5] for x in qresults]
	df = pd.DataFrame({
					'hash': hashes,
					'date': dates,
					'benchmark_name': benchmarks,
					'benchmark_id': benchmark_ids,
					'timing': timings,
					'success': successes
					})

	fname = os.path.join(groups_dir, groupname + ".parquet")
	table = pa.Table.from_pandas(df)
	pq.write_table(table, fname)

# generate the benchmarks file with benchmark metadata
c.execute("select id, name, groupname, description from benchmarks;")
qresults = c.fetchall()
ids = [x[0] for x in qresults]
names = [x[1] for x in qresults]
groups = [x[2] for x in qresults]
descriptions = [x[3] for x in qresults]
images = []
# load the graphs from disk
for i in range(len(ids)):
	graph_name = str(ids[i])
	# graph_name = names[i]
	graph_path = os.path.join(image_dir, graph_name + ".png")
	if os.path.exists(graph_path):
		with open(graph_path, 'rb') as f:
			images.append(f.read())
	else:
		images.append(None)

df = pd.DataFrame({
				'id': ids,
				'name': names,
				'group': groups,
				'description': descriptions,
				'images': images})

fname = os.path.join(benchmark_dir, "benchmarks.parquet")
table = pa.Table.from_pandas(df)
pq.write_table(table, fname)

# now for each benchmark generate the benchmark name
for benchmark_id in ids:
	c.execute('''
SELECT commits.hash, commits.date, commits.message, timings.median, timings.error, timings.profile, timings.stdout, timings.stderr
FROM commits, timings
WHERE commits.hash=timings.hash
AND benchmark_id=%d
ORDER BY date DESC
''' % (benchmark_id,))
	qresults = c.fetchall()
	hashes   = [x[0] for x in qresults]
	dates    = [x[1] for x in qresults]
	messages = [x[2] for x in qresults]
	timings  = [x[3] for x in qresults]
	errors   = [x[4] for x in qresults]

	profiles = [x[5] for x in qresults]
	meta_info = []
	graph_data = []
	for profile_info in profiles:
		try:
			profile_data = '{ "result"' + profile_info.split('{ "result"')[1].replace('\\n', ' ').replace('\n', ' ')
			generated_graph = duckdb_query_graph.generate_html(json.loads(profile_data))
			meta_info.append(generated_graph['meta_info'])
			graph_data.append(generated_graph['json'])
		except:
			meta_info.append(None)
			graph_data.append(None)
	stdouts  = [x[6] for x in qresults]
	stderrs  = [x[7] for x in qresults]

	df = pd.DataFrame({
					'hash': hashes,
					'date': dates,
					'message': messages,
					'timing': timings,
					'error': errors,
					'meta_info': meta_info,
					'graph_data': graph_data,
					'stdout': stdouts,
					'stderr': stderrs})

	fname = os.path.join(individual_benchmarks_dir, str(benchmark_id) + ".parquet")
	table = pa.Table.from_pandas(df)
	pq.write_table(table, fname)
