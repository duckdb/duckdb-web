import os, sys, re
import urllib
from urllib.request import urlopen
import json
import subprocess
import sqlite3

duckdb_web_base = os.getcwd()
duckdb_base = os.path.join(os.getcwd(), '..', 'duckdb')
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
benchmark_runner = os.path.join(duckdb_base, 'build', 'debug', 'benchmark', 'benchmark_runner')

def format_sql(sql):
	with open('format.tmp.sql', 'w+') as f:
		f.write(sql)
	return get_output(['pg_format', '--keyword-case', '2', '--spaces', '4', 'format.tmp.sql'])

def get_output(process):
	proc = subprocess.Popen(process, stdout=subprocess.PIPE)
	return proc.stdout.read().decode('utf8')

sql_codewords = ['COPY', 'HEADER', 'IN', 'SELECT', 'FROM', 'WHERE', 'GROUP', 'BY', 'ORDER', 'AS', 'JOIN', 'ON', 'DELIMITER', 'avg', 'sum', 'count', 'cast', 'SUM', 'INDEX', 'USING', 'ROWS', 'BETWEEN', 'PRECEDING', 'AND', 'OR', 'FOLLOWING', 'DESC', 'LIMIT', 'ASC', 'EXISTS', 'UNION', 'ALL', 'extract', 'FROM', 'LIKE', 'CASE', 'WHEN', 'ELSE', 'END', 'THEN', 'NOT', 'HAVING', 'WITH', 'DISTINCT', 'NULL', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'SUBSTRING', 'INTERSECT', 'PARTITION', 'BY', 'EXCEPT']
string_regex = re.compile("('[^']+')")
comment_regex = re.compile("(--[^\n]+)")

sql_codestyle = 'color:black;font-weight:bold;'
string_codestyle = 'color:firebrick;'
comment_codestyle = 'color:green;'

def char_is_valid(char):
	return char.isspace() or char == '(' or char == ')' or char == ':' or char ==';' or char=='\'' or char == '"' or char =='\n' or char ==',' or char =='.'

def style_code(code, codewords, codestyle):
	for codeword in codewords:
		startpos = 0
		while True:
			pos = code[startpos:].find(codeword)
			if pos >= 0:
				pos = pos + startpos
				if (pos == 0 or char_is_valid(code[pos - 1])) and char_is_valid(code[pos + len(codeword)]):
					styled_string = "<span style=\"%s\">" % codestyle + code[pos:pos + len(codeword)] + "</span>"
					code = code[:pos] + styled_string + code[pos + len(codeword):]
					startpos = pos + len(styled_string) + len(codeword)
				else:
					startpos = pos + len(codeword)
			else:
				break
	return code

def style_code_regex(code, regex, codestyle):
	span_regex = re.compile('(<[^>]+>)')
	startpos = 0
	while True:
		match = regex.search(code[startpos:])
		if match == None:
			break
		ele = match.groups()[0]
		ele = re.sub(span_regex, "", ele)

		styled_string = "<span style=\"%s\">" % codestyle + ele + "</span>"
		code = code[:startpos + match.start()] + styled_string + code[startpos + match.end():]
		startpos = startpos + match.start() + len(styled_string)
	return code

def style(code):
	code = style_code(code, sql_codewords, sql_codestyle)
	code = style_code_regex(code, string_regex, string_codestyle)
	code = style_code_regex(code, comment_regex, comment_codestyle)
	return code

def update_benchmark(benchmark_name, con, c):
	query = get_output([benchmark_runner, '--query', benchmark_name]).strip()
	if len(query) == 0:
		benchmark_info = get_output([benchmark_runner, '--info', benchmark_name]).strip()
		result_html = """<h1>Description</h1><p>%s</p>""" % (benchmark_info,)
	else:
		query = format_sql(query)
		result_html = """
		<h1>SQL Code</h1>
		<pre style="font:courier-new;background-color:rgb(234,234,234);padding:10px;padding-left:20px">%s</pre>
		"""% (style(query),)
	c.execute("UPDATE benchmarks SET description=? WHERE name=?", (result_html, benchmark_name))
	con.commit()

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()
c.execute('SELECT name FROM benchmarks')
for benchmark_name in [x[0] for x in c.fetchall()]:
	update_benchmark(benchmark_name, con, c)
