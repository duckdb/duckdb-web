# generate_descriptions.py
# This file generates descriptions for display on the individual benchmark pages

import os, sys, re
import urllib
from urllib.request import urlopen
import duckdb
import json
import subprocess
import sqlite3

duckdb_web_base = os.getcwd()
duckdb_base = os.path.join(os.getcwd(), '..', 'duckdb-bugfix')
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
benchmark_runner = os.path.join(duckdb_base, 'build', 'release', 'benchmark', 'benchmark_runner')

def format_sql(sql):
	with open('format.tmp.sql', 'w+') as f:
		f.write(sql)
	return get_output(['pg_format', '--keyword-case', '2', '--spaces', '4', 'format.tmp.sql'])

def get_output(process):
	proc = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return proc.stdout.read().decode('utf8')

keyword_codestyle = 'color:black;font-weight:bold;'
string_codestyle = 'color:firebrick;'
numeric_codestyle = 'color:gold;'
comment_codestyle = 'color:green;'

def wrap_in_span(codestyle):
	return ['<span style="' + codestyle + '">', "</span>"]

def style(query):
	tokens = duckdb.tokenize(query)
	result = ""
	for i in range(len(tokens)):
		token = tokens[i]
		token_type = token[1]
		start = token[0]
		end = len(query) - 1
		if i + 1 < len(tokens):
			end = tokens[i + 1][0]
		style = ["", ""]
		if token_type == duckdb.string_const:
			style = wrap_in_span(string_codestyle)
		elif token_type == duckdb.numeric_const:
			style = wrap_in_span(numeric_codestyle)
		elif token_type == duckdb.comment:
			style = wrap_in_span(comment_codestyle)
		elif token_type == duckdb.keyword:
			style = wrap_in_span(keyword_codestyle)
		result += style[0] + query[start:end] + style[1]
	return result

def generate_benchmark_info(benchmark_name, con, c):
	query = get_output([benchmark_runner, '--query', benchmark_name]).strip()
	if len(query) == 0:
		result_html = ""
	else:
		query = format_sql(query)
		result_html = """
		<h1>SQL Code</h1>
		<pre style="font:courier-new;background-color:rgb(234,234,234);padding:10px;padding-left:20px">%s</pre>
		"""% (style(query),)
		result_html = result_html.strip()
	print(result_html)

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()
c.execute('SELECT name FROM benchmarks')
for benchmark_name in [x[0] for x in c.fetchall()]:
	generate_benchmark_info(benchmark_name, con, c)
