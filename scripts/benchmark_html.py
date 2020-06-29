# benchmark_html.py
# This script generates the benchmark HTML files for display on the website

import numpy, os, sys, sqlite3, json
import duckdb_query_graph

duckdb_web_base = os.getcwd()
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')

name_map = {
	"tpch-sf1": "TPC-H",
	"csv": "CSV",
	"tpcds-sf1": "TPC-DS",
	"bulkupdate": "Bulk Update",
	"imdb": "IMDB"
}

ignored_groups = ['imdb', 'expression_reordering']

def group_is_ignored(groupname):
	return groupname is None or len(groupname) == 0 or groupname in ignored_groups

def get_benchmark_results(results_folder):
	results = [x for x in os.listdir(results_folder) if x != 'info']
	results = sorted(results)
	results.reverse()
	return results

def get_benchmarks(results_folder):
	info_path = os.path.join(results_folder, 'info')
	# get the group and info
	benchmarks = []
	groups = []
	benchmarks_per_group = {}
	files = os.listdir(info_path)
	files.sort()
	for info_file in files:
		with open(os.path.join(info_path, info_file), 'r') as f:
			header = f.readline()
			splits = header.split(' - ')
			name = splits[0].strip()
			group = splits[1].strip()
			description = f.read()
			if group not in benchmarks_per_group:
				benchmarks_per_group[group] = []
				groups.append(group)
			benchmarks_per_group[group].append(len(benchmarks))
			benchmarks.append([name, description, info_file])
	return (benchmarks, groups, benchmarks_per_group)

def begin_row(f, class_name):
	f.write('<tr class="%s">' % (class_name,))

def end_row(f):
	f.write("</tr>")

def begin_header(f):
	f.write('<th>')

def end_header(f):
	f.write("</th>")

def begin_rotated_header(f):
	f.write('<th class="table-active"><div><div>')

def end_rotated_header(f):
	f.write("</div></div></th>")

def begin_value(f, cl = None):
	if cl:
		f.write('<td class="%s">' % cl)
	else:
		f.write("<td>")

def end_value(f):
	f.write("</td>")

def color_output(output, r, g, b):
	return '<span style="color:rgb(%d,%d,%d);">%s</span>' % (r, g, b, output)

def bold_output(output):
	return "<b>%s</b>" % (output,)

def background_color_output(output, r, g, b):
	return '<div style="background-color:rgb(%d,%d,%d);">%s</div>' % (r, g, b, output)

def write_commit(f, commit):
	f.write('<a href="https://github.com/cwida/duckdb/commit/%s">%s</a>'  % (commit, commit[:4]))

def get_group_name(key):
	category_name = key.replace("[", "").replace("]", "").replace("-", " ").title()
	if key in name_map:
		category_name = name_map[key]
	return category_name

def get_log_info(written_commits, commit_hash, benchmark_name):
	base_stderr = '/benchmarks/logs/%s-stderr.html' % (commit_hash,)
	base_stdout = '/benchmarks/logs/%s-stdout.html' % (commit_hash,)
	base_graph = '/benchmarks/logs/%s-graph.html' % (commit_hash,)

	benchmark_has_files = written_commits[commit_hash][benchmark_name]
	has_graph = benchmark_has_files[0]
	has_stdout = benchmark_has_files[1]
	has_stderr = benchmark_has_files[2]

	log_info = []
	if has_graph:
		log_info.append(['Q', base_graph + "?name=" + benchmark_name])
	if has_stdout:
		log_info.append(['L', base_stdout + "?name=" + benchmark_name])
	if has_stderr:
		log_info.append(['E', base_stderr + "?name=" + benchmark_name])

	log_html = ""
	if len(log_info) > 0:
		log_html = "["
		for i in range(len(log_info) - 1):
			log_html += '<a href="%s">%s</a>/' % (log_info[i][1], log_info[i][0])
		log_html += '<a href="%s">%s</a>]' % (log_info[-1][1], log_info[-1][0])
	return log_html

# result of the packing the info directory:
# one CSV file: benchmark,category
# one JSON file: benchmark-info.json
# one CSV file: category
def pack_info(c):
	import os, json

	benchmark_csv_path = os.path.join('_data', 'benchmarks.csv')
	categories_csv_path = os.path.join('_data', 'categories.csv')
	benchmark_info_json = os.path.join('_includes', 'benchmark-info.json')

	# benchmarks.csv:
	# benchmark,category
	with open(benchmark_csv_path, 'w+') as benchmark_csv:
		benchmark_csv.write("benchmark,category\n")
		c.execute("SELECT groupname, name FROM benchmarks")
		for entry in c.fetchall():
			if group_is_ignored(entry[0]):
				continue
			benchmark_csv.write("%s,%s\n" % (entry[1], entry[0]))

	# categories.csv:
	# groupname,name
	with open(categories_csv_path, 'w+') as category_csv:
		category_csv.write("category,name\n")
		c.execute("SELECT DISTINCT groupname FROM benchmarks ORDER BY 1")
		for entry in c.fetchall():
			if group_is_ignored(entry[0]):
				continue
			key = entry[0]
			category_name = get_group_name(key)
			category_csv.write("%s,%s\n" % (key, category_name))

	# benchmark-info.json
	# json file containing benchmark:benchmark-description pairs
	with open(benchmark_info_json, 'w+') as benchmark_json:
		info = dict()
		c.execute("SELECT name, description FROM benchmarks")
		for benchmark_info in c.fetchall():
			info[benchmark_info[0]] = benchmark_info[1]
		json.dump(info, benchmark_json)


def pack_commit(c, commit_hash, written_commits):
	if commit_hash in written_commits:
		return
	# for each commit we generate 6 files:
	# XXX-stdout.json, XXX-stderr.json, XXX-graph.json
	# json mapping of [benchmark_name] -> stdout/stderr/graph data
	# XXX-stdout.html, XXX-stderr.html, XXX-graph.html
	# html file that loads the json for a specific

	graph_path = os.path.join('_includes', 'benchmark_logs', '%s-graph.json' % (commit_hash,))
	stderr_path = os.path.join('_includes', 'benchmark_logs', '%s-stderr.json' % (commit_hash,))
	stdout_path = os.path.join('_includes', 'benchmark_logs', '%s-stdout.json' % (commit_hash,))
	graph_html = os.path.join('benchmarks', 'logs', '%s-graph.html' % (commit_hash,))
	stderr_html = os.path.join('benchmarks', 'logs', '%s-stderr.html' % (commit_hash,))
	stdout_html = os.path.join('benchmarks', 'logs', '%s-stdout.html' % (commit_hash,))
	if os.path.isfile(graph_path):
		# files already exist, no need to rewrite them, instead just look up which benchmarks have graphs/stdout/stderr
		result_dict = {}
		c.execute("SELECT name, profile, stdout, stderr FROM timings JOIN benchmarks ON benchmark_id=id WHERE hash=?", (commit_hash,))
		for entry in c.fetchall():
			name = entry[0]
			has_graph = entry[1] is not None
			has_stdout = entry[2] is not None
			has_stderr = entry[3] is not None
			result_dict[name] = [has_graph, has_stdout, has_stderr]
		written_commits[commit_hash] = result_dict
		return

	result_dict = {}
	graph_data = {
		'meta_info': {},
		'graph_json': {}
	}
	stdout = {}
	stderr = {}
	c.execute("SELECT name, profile, stdout, stderr FROM timings JOIN benchmarks ON benchmark_id=id WHERE hash=?", (commit_hash,))
	for entry in c.fetchall():
		name = entry[0]
		has_graph = False
		if entry[1] is not None:
			# generate the graph
			try:
				text = '{ "result"' + entry[1].split('{ "result"')[1].replace('\\n', ' ').replace('\n', ' ')
				generated_graph = duckdb_query_graph.generate_html(json.loads(text))
				graph_data['meta_info'][name] = generated_graph['meta_info']
				graph_data['graph_json'][name] = json.loads(generated_graph['json'])
				has_graph = True
			except:
				pass
		if entry[2] is not None:
			stdout[name] = entry[2]
		if entry[3] is not None:
			stderr[name] = entry[3]
		result_dict[name] = [has_graph, entry[2] is not None, entry[3] is not None]

	with open(graph_path, 'w+') as f:
		json.dump(graph_data, f)
	with open(stdout_path, 'w+') as f:
		json.dump(stdout, f)
	with open(stderr_path, 'w+') as f:
		json.dump(stderr, f)

	with open(graph_html, 'w+') as f:
		f.write("""---
layout: graph
title: Query Graph for %s
logfile: /benchmark_logs/%s-graph.json
---""" % (commit_hash, commit_hash))
	with open(stderr_html, 'w+') as f:
		f.write("""---
layout: log
title: Revision %s
logfile: /benchmark_logs/%s-stderr.json
---
""" % (commit_hash, commit_hash))

	with open(stdout_html, 'w+') as f:
		f.write("""---
layout: log
title: Revision %s
logfile: /benchmark_logs/%s-stdout.json
---
""" % (commit_hash, commit_hash))

	written_commits[commit_hash] = result_dict

def get_benchmark_html(median, success, error):
	result_html = []
	if success:
		result_html = bold_output("%.2lf" % (median,))
		table_class = None
	else:
		if error.upper() == 'CRASH':
			result_html = bold_output('C')
			table_class = 'table-danger'
		elif error.upper() == 'INCORRECT':
			result_html = bold_output('!')
			table_class = 'table-danger'
		elif error.upper() == 'TIMEOUT':
			result_html = bold_output('T')
			table_class = 'table-warning'
		else:
			table_class = 'table-info'
	return (result_html, table_class)

def create_html(database):
	con = sqlite3.connect(sqlite_db_file)
	c = con.cursor()
	written_commits = {}

	# generate the benchmark, category and benchmark info files
	pack_info(c)

	# generate the individual benchmark pages
	# get a list of all the individual benchmarks
	c.execute("SELECT name, id, groupname, description FROM benchmarks")
	for benchmark_info in c.fetchall():
		benchmark_name = benchmark_info[0]
		benchmark_id = benchmark_info[1]
		groupname = benchmark_info[2]
		description = benchmark_info[3]
		# load the HTML description from disk, if it exists
		description_file = os.path.join('benchmarks', 'info', benchmark_name + '.html')
		if os.path.isfile(description_file):
			with open(description_file, 'r') as descr_file:
				description = descr_file.read()

		with open(os.path.join('_includes', 'individual_results', benchmark_name + '.html'), 'w+') as f:
			# first write the description
			f.write("%s" % (description,))
			# then an image of the graph
			f.write('<img src="%s"/>' % ('/images/graphs/%s.png' % (benchmark_name,),))
			# then a table containing all the results for each of the hashes
			# the table is <hash, time>
			begin_row(f, "table-header")
			begin_header(f)
			f.write("Commit")
			end_header(f)
			begin_header(f)
			f.write("Date")
			end_header(f)
			begin_header(f)
			f.write("Result")
			end_header(f)
			begin_header(f)
			f.write("Logs")
			end_header(f)
			begin_header(f)
			f.write("Message")
			end_header(f)
			end_row(f)

			class_name = "table-even"
			c.execute("SELECT commits.hash, date, median, success, error, commits.message FROM timings JOIN commits ON commits.hash=timings.hash WHERE benchmark_id=? ORDER BY date DESC;", (benchmark_id,))
			results = c.fetchall()
			for entry in results:
				commit_hash = entry[0]
				date = entry[1]
				median = entry[2]
				success = entry[3]
				error = entry[4]
				message = entry[5]

				pack_commit(c, commit_hash, written_commits)
				written_commits[commit_hash]

				(result_html, table_class) = get_benchmark_html(median, success, error)
				begin_row(f, class_name)
				# commit hash
				begin_value(f, None)
				write_commit(f, commit_hash)
				end_value(f)
				# date
				begin_value(f, None)
				f.write(date.split(' ')[0])
				end_value(f)
				# benchmark result
				begin_value(f, table_class)
				f.write(result_html)
				end_value(f)
				# logs
				begin_value(f, None)
				f.write(get_log_info(written_commits, commit_hash, benchmark_name))
				end_value(f)
				# commit message
				begin_value(f, None)
				f.write(message)
				end_value(f)
				end_row(f)
				if class_name == "table-even":
					class_name = "table-odd"
				else:
					class_name = "table-even"

		with open(os.path.join('benchmarks', 'individual_results', benchmark_name + '.md'), 'w+') as f:
			pretty_name = get_group_name(groupname)
			f.write("""---
layout: docu
title: %s
subtitle: Continuous Benchmarking
selected: %s
expanded: Benchmarking
benchmark: /individual_results/%s.html
---""" % (benchmark_name, pretty_name, benchmark_name)
)

	# generate the group benchmark pages
	# get a list of all the groups from the benchmarks
	c.execute("SELECT DISTINCT groupname FROM benchmarks")
	groups = [x[0] for x in c.fetchall()]

	for groupname in groups:
		if group_is_ignored(groupname):
			continue
		# now for each of the groups find the most recent 15 commits that ran a benchmark from that group
		# first select a random benchmark from the group
		c.execute("SELECT id FROM benchmarks WHERE groupname=? LIMIT 1;", (groupname,))
		benchmark_id = c.fetchall()[0][0]

		# now find the 15 most recent commits that ran this benchmark
		c.execute("SELECT commits.hash FROM commits JOIN timings ON commits.hash=timings.hash WHERE benchmark_id=? ORDER BY commits.date DESC LIMIT 15", (benchmark_id,))
		hashes = [x[0] for x in c.fetchall()]

		# for each of the referenced commits, generate the stdout, stderr and graph html files
		for commit_hash in hashes:
			pack_commit(c, commit_hash, written_commits)

		# now finally generate the html for the group
		# get a list of benchmarks for this group
		c.execute("SELECT name, id FROM benchmarks WHERE groupname=? ORDER BY 1;", (groupname,))
		benchmark_results = {}
		benchmark_list = c.fetchall()
		benchmark_map = {}
		found_results = {}
		for benchmark_info in benchmark_list:
			# for each of the benchmarks get the timing or error information for each of the commits
			benchmark_name = benchmark_info[0]
			benchmark_id = benchmark_info[1]
			benchmark_map[benchmark_id] = benchmark_name
			benchmark_results[benchmark_name] = {}
			found_results[benchmark_name] = False
		for commit_hash in hashes:
			benchmark_in_list = ', '.join([str(x) for x in benchmark_map.keys()])

			c.execute("SELECT benchmark_id, success, error, median FROM timings WHERE hash=? AND benchmark_id IN (%s)" % (benchmark_in_list,), (commit_hash,))
			for entry in c.fetchall():
				benchmark_id = entry[0]
				benchmark_name = benchmark_map[benchmark_id]
				success = entry[1]
				error = entry[2]
				median = entry[3]
				(result_html, table_class) = get_benchmark_html(median, success, error)
				log_info = get_log_info(written_commits, commit_hash, benchmark_name)
				if len(log_info) > 0:
					result_html += " " + log_info
				benchmark_results[benchmark_name][commit_hash] = (result_html, table_class)
				found_results[benchmark_name] = True

		pretty_name = get_group_name(groupname)
		normalized_group = pretty_name.replace("[", "").replace("]", "").replace("-", "").replace(" ", "").lower()
		out_html = os.path.join('_includes', 'benchmark_results', normalized_group + '.html')
		with open(os.path.join('benchmarks', normalized_group + '.md'), 'w+') as f:
			f.write("""---
layout: docu
title: %s
subtitle: Continuous Benchmarking
selected: %s
expanded: Benchmarking
benchmark: /benchmark_results/%s.html
---
""" % (pretty_name, pretty_name, normalized_group))
		with open(out_html, 'w+') as f:
			# the header is all the commits
			begin_row(f, "table-header")
			# one extra header for the benchmark name
			begin_header(f)
			end_header(f)
			for commit_hash in hashes:
				begin_rotated_header(f)
				write_commit(f, commit_hash)
				end_rotated_header(f)
			end_row(f)
			# now write the results
			class_name = "table-even"
			for entry in benchmark_list:
				benchmark_name = entry[0]
				if not found_results[benchmark_name]:
					continue
				begin_row(f, class_name)
				# benchmark name
				begin_value(f, 'table-row-header')

				f.write('<a href="/benchmarks/individual_results/%s">%s</a>' % (benchmark_name,benchmark_name))
				end_value(f)
				# benchmark results
				for commit_hash in hashes:
					if commit_hash in benchmark_results[benchmark_name]:
						(html, table_class) = benchmark_results[benchmark_name][commit_hash]
					else:
						html = ""
						table_class = None
					begin_value(f, table_class)
					f.write(html)
					end_value(f)
				end_row(f)
				if class_name == "table-even":
					class_name = "table-odd"
				else:
					class_name = "table-even"


if __name__ == "__main__":
	create_html(sqlite_db_file)