import os, sys, re
import duckdb
import subprocess
import sqlite3

duckdb_web_base = os.getcwd()
duckdb_base = os.path.join(os.getcwd(), '..', 'duckdb-bugfix')
sqlite_db_file = os.path.join(duckdb_web_base, 'benchmarks.db')
group_list = os.path.join(duckdb_base, 'benchmark', 'group_descriptions.list')

con = sqlite3.connect(sqlite_db_file)
c = con.cursor()
c.execute('SELECT name FROM benchmarks')

with open(group_list, 'r') as f:
	lines = [x.strip() for x in f.read().split('\n')]

current_group = None
current_subgroup = None
display_name = None
description = []

def flush_group(c, current_group,subgroup, display_name, description):
	c.execute("select count(*) from groups where name = ? and subgroup=?" , (current_group,subgroup))
	count = c.fetchall()[0][0]
	if count == 0:
		# no entry yet
		c.execute('insert into groups (name, display_name, subgroup, description) values (?,?,?)', (current_group, display_name, subgroup, description))
	else:
		# entry exists, update it
		c.execute('update groups set display_name=?, subgroup=?, description=? where name=?', (current_group, display_name, subgroup, description))


for line in lines:
	if len(line) == 0:
		flush_group(c, current_group, current_subgroup, display_name, ' '.join(description))
		current_group = None
		current_subgroup = None
		display_name = None
		description = []
		continue
	if current_group is None:
		if line[0] != '[':
			raise Exception("Expected a [ indicating the name of a group")
		if '][' in line:
			splits = line.split('][')
			current_group = splits[0][1:]
			current_subgroup = splits[1][:-1]
		else:
			current_group = line[1:len(line) - 1]
	elif display_name is None:
		if line[0] != '[':
			raise Exception("Expected a [ indicating the display name of a group")
		display_name = line[1:len(line) - 1]
	else:
		description.append(line)



