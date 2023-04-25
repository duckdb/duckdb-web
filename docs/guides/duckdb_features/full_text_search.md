---
layout: docu
title: DuckDB Full Text Search
selected: DuckDB Full Text Search
---

Here's a simple "hello world" full text search example using the easily accessible
(and parsable!) kjv.txt. Note that everything past the table creation can
be done in the duckdb cli.

First, some code to read kjv.txt and create a table for it.

```python
% cat duckdb-full-text-search.py

import re
import duckdb

# -------- prepare the data -----------
fd = open('kjv.txt') # https://www.o-bible.com/download/kjv.txt
fd.readline() # skip first line
data = []
for line in fd.readlines():
    line = line.rstrip()
    # book, chap, verse, body = re.match(r'(\d?[A-Za-z]+)(\d+):(\d+)\s+(.*)', line).groups()
    ref, body = re.match(r'(\d?[A-Za-z]+\d+:\d+)\s+(.*)', line).groups()
    data.append((ref,body,))

# -------- create the table -----------
db = duckdb.connect('fts_demo.ddb')
db.cursor().execute("CREATE TABLE corpus(ref TEXT, body TEXT)")
db.cursor().executemany("INSERT INTO corpus(ref, body) VALUES($1, $2)", data)
```

Everything else we need to do can be done in the DuckDB CLI.

```sql
INSTALL 'fts';
LOAD fts;

-- create the index on table corpus, pk ref, indexing ref and body.
PRAGMA create_fts_index('corpus', 'ref', 'ref', 'body');
```

Now we can issue full text queries against that index.  Let's look for "whale".

```
SELECT fts_main_corpus.match_bm25(ref, 'whale') AS score,
  ref, body AS "search for 'whale'"
FROM corpus
WHERE score IS NOT NULL
ORDER BY score;

┌───────────────────┬──────────┬───────────────────────────────────────────────┐
│       score       │   ref    │              search for 'whale'               │
│      double       │ varchar  │                    varchar                    │
├───────────────────┼──────────┼───────────────────────────────────────────────┤
│   2.7248255618541 │ Eze32:2  │ Son of man, take up a lamentation for Phara…  │
│ 3.839526928067141 │ Ge1:21   │ And God created great whales, and every liv…  │
│ 3.839526928067141 │ Mat12:40 │ For as Jonas was three days and three night…  │
│ 6.497660955190547 │ Job7:12  │ Am I a sea, or a whale, that thou settest a…  │
└───────────────────┴──────────┴───────────────────────────────────────────────┘
```

Unlike standard indexes, full text indexes don't auto-updated, so you need to
`PRAGMA drop_fts_index(my_fts_index)` and recreate it.

