---
layout: docu
title: Create Synthetic Data
---

DuckDB lets you quickly generate synthetic datasets by combining a few building blocks: functions and clauses that generate *rows*, functions that generate *values* to fill those rows, and extensions that generate whole benchmark datasets. This page shows each building block with a runnable example.

## Generating Rows

### `range` and `generate_series`

The [range functions]({% link docs/preview/sql/functions/list.md %}#range-functions) turn a start, stop, and step into a table of rows, which is the usual starting point for a synthetic dataset:

```sql
SELECT i FROM range(1, 4) t(i);
```

```text
┌───────┐
│   i   │
│ int64 │
├───────┤
│     1 │
│     2 │
│     3 │
└───────┘
```

`range` excludes the stop value, while [`generate_series`]({% link docs/preview/sql/functions/list.md %}#range-functions) includes it.

### `VALUES`

The [`VALUES` clause]({% link docs/preview/sql/query_syntax/values.md %}) generates rows from literal tuples, which is convenient for a small fixed set of values to draw from:

```sql
SELECT * FROM (VALUES ('Alice', 'Engineering'), ('Bob', 'Sales')) t(name, department);
```

```text
┌─────────┬─────────────┐
│  name   │ department  │
│ varchar │   varchar   │
├─────────┼─────────────┤
│ Alice   │ Engineering │
│ Bob     │ Sales       │
└─────────┴─────────────┘
```

### `repeat_row`

[`repeat_row(varargs, num_rows)`]({% link docs/preview/sql/functions/utility.md %}#repeat_rowvarargs-num_rows) returns a fixed number of identical rows, which is useful as a scaffold to fill with generated values:

```sql
FROM repeat_row('placeholder', 0, num_rows = 3);
```

```text
┌─────────────┬─────────┐
│   column0   │ column1 │
│   varchar   │  int32  │
├─────────────┼─────────┤
│ placeholder │       0 │
│ placeholder │       0 │
│ placeholder │       0 │
└─────────────┴─────────┘
```

### Cross Products

A [cross product (Cartesian product)]({% link docs/preview/sql/query_syntax/from.md %}#cross-product-joins-cartesian-product) multiplies rows from two sources, so combining two `range` calls is a compact way to produce a large number of rows:

```sql
SELECT i, j FROM range(1, 3) s(i) CROSS JOIN range(1, 3) t(j);
```

## Generating Values

### Random Numbers

[`random()`]({% link docs/preview/sql/functions/numeric.md %}#random) returns a random `DOUBLE` in the range `[0, 1)`, which you can scale and cast into any numeric range:

```sql
SELECT (random() * 100)::INTEGER AS score FROM range(3);
```

### UUIDs

Several [utility functions]({% link docs/preview/sql/functions/utility.md %}) generate universally unique identifiers, which make good synthetic primary keys:
[`uuid()`]({% link docs/preview/sql/functions/utility.md %}#uuid) and its alias [`uuidv4()`]({% link docs/preview/sql/functions/utility.md %}#uuidv4) generate random (version 4) UUIDs, [`uuidv7()`]({% link docs/preview/sql/functions/utility.md %}#uuidv7) generates time-ordered (version 7) UUIDs, and [`gen_random_uuid()`]({% link docs/preview/sql/functions/utility.md %}#gen_random_uuid) is an alias for `uuid()`:

```sql
SELECT uuidv7() AS id FROM range(3);
```

### Current Date and Time

Functions that return the current date or time are handy for populating timestamp columns:
[`today()`]({% link docs/preview/sql/functions/date.md %}#today) returns the current date,
[`get_current_time()`]({% link docs/preview/sql/functions/time.md %}#get_current_time) returns the current time, and
[`current_localtimestamp()`]({% link docs/preview/sql/functions/timestamp.md %}#current_localtimestamp) returns the current local timestamp:

```sql
SELECT today() AS date, get_current_time() AS time, current_localtimestamp() AS timestamp;
```

### Hashing

Hash functions such as [`hash`]({% link docs/preview/sql/functions/utility.md %}#hashvalue), [`md5`]({% link docs/preview/sql/functions/utility.md %}#md5string), and [`sha256`]({% link docs/preview/sql/functions/utility.md %}#sha256value) turn a row number into a deterministic pseudo-random value, which is useful when you want reproducible identifiers:

```sql
SELECT hash(i) AS id, md5(i::VARCHAR) AS token FROM range(3) t(i);
```

### Repeating Strings

[`repeat(string, count)`]({% link docs/preview/sql/functions/text.md %}#repeatstring-count) builds a string by repeating another, which is useful for padding values to a target length:

```sql
SELECT repeat('ab', 3) AS padded;
```

### Sequences

A [sequence]({% link docs/preview/sql/statements/create_sequence.md %}) produces a monotonically increasing series of numbers. [`nextval('sequence_name')`]({% link docs/preview/sql/functions/utility.md %}#nextvalsequence_name) advances the sequence and returns the next value, while [`currval('sequence_name')`]({% link docs/preview/sql/functions/utility.md %}#currvalsequence_name) returns the value most recently produced:

```sql
CREATE SEQUENCE id_seq START 100;
SELECT nextval('id_seq') AS id FROM range(3);
```

## Generating Text with Faker

For realistic-looking names, addresses, and other text, you can call the [Faker Python package](https://faker.readthedocs.io/) through the [Python function API]({% link docs/preview/clients/python/function.md %}):

```python
import duckdb

from duckdb.sqltypes import *
from faker import Faker

fake = Faker()

def random_date():
    return fake.date_between()

def random_short_text():
    return fake.text(max_nb_chars=20)

def random_long_text():
    return fake.text(max_nb_chars=200)

con = duckdb.connect()
con.create_function("random_date",       random_date,       [], DATE,    type="native", side_effects=True)
con.create_function("random_short_text", random_short_text, [], VARCHAR, type="native", side_effects=True)
con.create_function("random_long_text",  random_long_text,  [], VARCHAR, type="native", side_effects=True)

res = con.sql("""
                 SELECT
                    hash(i * 10 + j) AS id,
                    random_date() AS creationDate,
                    random_short_text() AS short,
                    random_long_text() AS long,
                    IF (j % 2, true, false) AS bool
                 FROM generate_series(1, 5) s(i)
                 CROSS JOIN generate_series(1, 2) t(j)
                 """)
res.show()
```

This generates the following:

```text
┌──────────────────────┬──────────────┬─────────┐
│          id          │ creationDate │  flag   │
│        uint64        │     date     │ boolean │
├──────────────────────┼──────────────┼─────────┤
│  6770051751173734325 │ 2019-11-05   │ true    │
│ 16510940941872865459 │ 2002-08-03   │ true    │
│ 13285076694688170502 │ 1998-11-27   │ true    │
│ 11757770452869451863 │ 1998-07-03   │ true    │
│  2064835973596856015 │ 2010-09-06   │ true    │
│ 17776805813723356275 │ 2020-12-26   │ false   │
│ 13540103502347468651 │ 1998-03-21   │ false   │
│  4800297459639118879 │ 2015-06-12   │ false   │
│  7199933130570745587 │ 2005-04-13   │ false   │
│ 18103378254596719331 │ 2014-09-15   │ false   │
├──────────────────────┴──────────────┴─────────┤
│ 10 rows                             3 columns │
└───────────────────────────────────────────────┘
```

## Generating Benchmark Datasets with Extensions

To generate large, well-defined datasets, DuckDB ships with the [TPC-H]({% link docs/preview/core_extensions/tpch.md %}) and [TPC-DS]({% link docs/preview/core_extensions/tpcds.md %}) extensions. Each provides a data generator function that creates and populates the benchmark's tables at a given scale factor:

```sql
INSTALL tpch;
LOAD tpch;
CALL dbgen(sf = 0.1);
SELECT count(*) AS lineitem_rows FROM lineitem;
```

## Community Extensions

The [`fakeit` community extension](https://duckdb.org/community_extensions/extensions/fakeit) provides table functions that generate fake data (such as names, emails, and addresses) directly in SQL, similar to the Faker Python package.
