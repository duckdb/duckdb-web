---
layout: docu
title: Create Synthetic Data
---

DuckDB allows you to quickly generate synthetic data sets. To do so, you may use:

* [range functions](../../sql/functions/nested#range-functions)
* hash functions, e.g.,
  [`hash`](../../sql/functions/utility#hashvalue),
  [`md5`](../../sql/functions/utility#md5string),
  [`sha256`](../../sql/functions/utility#sha256value)
* the [Faker Python package](https://faker.readthedocs.io/) via the [Python function API](../../api/python/function)

For example:

```python
import duckdb

from duckdb.typing import *
from faker import Faker

def random_date():
    fake = Faker()
    return fake.date_between()

duckdb.create_function("random_date", random_date, [], DATE, type="native")
res = duckdb.sql("""
                 SELECT hash(i) AS id, random_date() AS creationDate
                 FROM generate_series(1, 10) s(i)
                 """)
res.show()
```
