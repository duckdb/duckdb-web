---

layout: post
title:  "Testing out DuckDB's Full Text Search Extension"
author: Laurens Kuiper
excerpt_separator: <!--more-->

---

_TLDR: DuckDB now has full-text search functionality, similar to the FTS5 extension in SQLite. The main difference is that our FTS extension is fully formulated in SQL. We tested it out on TREC disks 4 and 5._

Searching through textual data stored in a database can be cumbersome, as SQL does not provide a good way of formulating questions such as "Give me all the documents about __Mallard Ducks__": string patterns with `LIKE` will only get you so far. Despite SQL's shortcomings here, storing textual data in a database is commonplace. Consider the table `products (id INT, name VARCHAR, description VARCHAR`) - it would be useful to search through the `name` and `description` columns for a website that sells these products.

<!--more-->

We expect a search engine to return us results within milliseconds. For a long time databases were unsuitable for this task, because they could not search large inverted indices at this speed: transactional database systems are not made for this use case. However, analytical database systems, can keep up with state-of-the art information retrieval systems. The company [Spinque](https://www.spinque.com/) is a good example of this. At Spinque, MonetDB is used as a computation engine for customized search engines.

DuckDB's FTS implementation follows the paper "[Old Dogs Are Great at New Tricks](https://www.duckdb.org/pdf/SIGIR2014-column-stores-ir-prototyping.pdf)". A keen observation there is that advances made to the database system, such as parallelization, will speed up your search engine "for free"!

Alright, enough about the "why", let's get to the "how".

### Preparing the Data
The TREC 2004 Robust Retrieval Track has 250 "topics" (search queries) over TREC disks 4 and 5. The data consist of many text files stored in SGML format, along with a corresponding DTD (document type definition) file. This format is rarely used anymore, but it is similar to XML. We will use OpenSP's command line tool `osx` to convert it to XML. Because there are many files, I wrote a bash script:
```bash
#!/bin/bash
mkdir -p latimes/xml
for i in $(seq -w 1 9)
do
        cat dtds/la.dtd latimes-$i | osx > latimes/xml/latimes-$i.xml
done
```
This sorts the `latimes` files. Repeat for the `fbis`, `cr`, `fr94`, and `ft` files.

To parse the XML I used BeautifulSoup. Each document has a `docno` identifier, and a `text` field. Because the documents do not come from the same source, they differ in what other fields they have. I chose to take all of the fields.
```python
import duckdb
import multiprocessing
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

# fill variable 'files' with the path to each .xml file that we created here

def process_file(fpath):
    dict_list = []
    with open(fpath, 'r') as f:
        content = f.read()
        bs_content = bs(content, "html.parser")
        # find all 'doc' nodes
        for doc in bs_content.findChildren('doc', recursive=True):
            row_dict = {}
            for c in doc.findChildren(recursive=True):
                row_dict[c.name] = ''.join(c.findAll(text=True, recursive=False)).trim()
            dict_list.append(row_dict)
    return dict_list

# process documents (in parallel to speed things up)
pool = multiprocessing.Pool(multiprocessing.cpu_count())
list_of_dict_lists = []
for x in tqdm(pool.imap_unordered(process_file, files), total=len(files)):
    list_of_dict_lists.append(x)
pool.close()
pool.join()

# create pandas dataframe from the parsed data
documents_df = pd.DataFrame([x for sublist in list_of_dict_lists for x in sublist])
```

Now that we have a dataframe, we can register it in DuckDB.
```python
# create database connection and register the dataframe
con = duckdb.connect(database='db/trec04_05.db', read_only=False)
con.register('documents_df', documents_df)

# create a table from the dataframe so that it persists
con.execute("CREATE TABLE documents AS (SELECT * FROM documents_df)")
con.close()
```
This is the end of my preparation script, so I closed the database connection.

### Building the Search Engine
We can now build the inverted index and the retrieval model using a `PRAGMA` statement. The extension is [documented here](/docs/extensions/full_text_search). We create an index table on table `documents` or `main.documents` that we created with our script. The column that identifies our documents is called `docno`, and we wish to create an inverted index on the fields supplied. I supplied all fields by using the '\*' shortcut.
```python
con = duckdb.connect(database='db/trec04_05.db', read_only=False)
con.execute("PRAGMA create_fts_index('documents', 'docno', '*', stopwords='english')")
```

Under the hood, a parameterized SQL script is called. The schema `fts_main_documents` is created, along with tables `docs`, `terms`, `dict`, and `stats`, that make up the inverted index. If you're curious what this look like, take a look at our source code under the `extension` folder in DuckDB's source code!

### Running the Benchmark
The data is now fully prepared. Now we want to run the queries in the benchmark, one by one. We load the topics file as follows:
```python
# the 'topics' file is not structured nicely, therefore we need parse some of it using regex
def after_tag(s, tag):
    m = re.findall(r'<' + tag + r'>([\s\S]*?)<.*>', s)
    return m[0].replace('\n', '').strip()

topic_dict = {}
with open('../../trec/topics', 'r') as f:
    bs_content = bs(f.read(), "lxml")
    for top in bs_content.findChildren('top'):
        top_content = top.getText()
        # we need the number and title of each topic
        num = after_tag(str(top), 'num').split(' ')[1]
        title = after_tag(str(top), 'title')
        topic_dict[num] = title
```
This gives us a dictionary that has query number as keys, and query strings as values, e.g. `301 -> 'International Organized Crime'`.

We want to store the results in a specific format, so that they can be evaluated by [trec eval](https://github.com/usnistgov/trec_eval.git):
```python
# create a prepared statement to make querying our document collection easier
con.execute("""
    PREPARE fts_query AS (
        WITH scored_docs AS (
            SELECT *, fts_main_documents.match_bm25(docno, ?) AS score FROM documents)
        SELECT docno, score
        FROM scored_docs
        WHERE score IS NOT NULL
        ORDER BY score DESC
        LIMIT 1000)
    """)

# enable parallelism
con.execute('PRAGMA threads=32')
results = []
for query in topic_dict:
    q_str = topic_dict[query].replace('\'', ' ')
    con.execute("EXECUTE fts_query('" + q_str + "')")
    for i, row in enumerate(con.fetchall()):
        results.append(query + " Q0 " + row[0].trim() + " " + str(i) + " " + str(row[1]) + " STANDARD")
con.close()

with open('results', 'w+') as f:
    for r in results:
        f.write(r + '\n')
```

### Results
Now that we have created our 'results' file, we can compare them to the relevance assessments `qrels` using `trec_eval`.
```bash
$ ./trec_eval -m P.30 -m map qrels results
map                     all 0.2324
P_30                    all 0.2948
```

Not bad! While these results are not as high as the reproducible by [Anserini](https://github.com/castorini/anserini), they are definitely acceptable. The difference in performance can be explained by differences in
1. Which stemmer was used (we used 'porter')
2. Which stopwords were used (we used the list of 571 English stopwords used in the SMART system)
3. Pre-processing (removal of accents, punctuation, numbers)
4. BM25 parameters (we used the default k=1.2 and b=0.75, non-conjunctive)
5. Which fields were indexed (we used all columns by supplying '\*')

Retrieval time for each query was between 0.5 and 1.3 seconds on our machine, which will be improved with further improvements to DuckDB. I hope you enjoyed reading this blog, and become inspired to test out the extension as well!
