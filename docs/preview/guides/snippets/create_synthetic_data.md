---
layout: docu
title: Create Synthetic Data
---

DuckDB allows you to quickly generate synthetic data sets. To do so, you may use:

* [range functions]({% link docs/preview/sql/functions/list.md %}#range-functions)
* hash functions, e.g.,
  [`hash`]({% link docs/preview/sql/functions/utility.md %}#hashvalue),
  [`md5`]({% link docs/preview/sql/functions/utility.md %}#md5string),
  [`sha256`]({% link docs/preview/sql/functions/utility.md %}#sha256value)
* the [Faker Python package](https://faker.readthedocs.io/) via the [Python function API]({% link docs/preview/clients/python/function.md %})
* using [cross products (Cartesian products)]({% link docs/preview/sql/query_syntax/from.md %}#cross-product-joins-cartesian-product)

For example:

```python
import duckdb

from duckdb.typing import *
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
