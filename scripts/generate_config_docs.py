import os
import sys
import re
import subprocess
import csv
import io

if len(sys.argv) < 2:
	print("Expected usage: python3 scripts/generate_docs.py /path/to/duckdb")
	exit(1)

db_path = sys.argv[1]

cmd = '''
.mode markdown
SELECT name, description, input_type, value AS default_value FROM duckdb_settings() WHERE name NOT LIKE '%debug%' AND description NOT ILIKE '%debug%';
'''

res = subprocess.run(db_path, input=bytearray(cmd, 'utf8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout = res.stdout.decode('utf8').strip()
stderr = res.stderr.decode('utf8').strip()

if len(stderr) != 0:
	print("Failed to run command " + cmd)
	print(stdout)
	print(stderr)
	exit(1)

option_split = '## **Option Reference**'
doc_file = 'docs/sql/configuration.md'

with open(doc_file, 'r') as f:
	text = f.read()

if option_split not in text:
	print("Could not find " + option_split)
	exit(1)

text = text.split(option_split)[0]

text += option_split + '\n\n' + 'Below is a list of all available settings.'

text += '\n\n' + stdout + '\n'

with open(doc_file, 'w+') as f:
	f.write(text)