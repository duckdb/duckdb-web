---
layout: post
title: "Announcing DuckDB 1.4.3 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-3-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-3-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.3."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.4.3, the third patch release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.3).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Fixes

This version ships a number of fixes:

* [`#18782` Incorrect “rows affected” was reported by ART index](https://github.com/duckdb/duckdb/issues/18782)
* [`#18997` Macro binding had slow performance for unbalanced trees](https://github.com/duckdb/duckdb/issues/18997)
* [`#19313` Wrong result in cornercase: a `HAVING` clause without a `GROUP BY` returned an incorrect result](https://github.com/duckdb/duckdb/issues/19313)
* [`#19469` Potential error occurred in constraint violation message when checking foreign key constraints](https://github.com/duckdb/duckdb/issues/19469)
* [`#19517` `JOIN` with a `LIKE` pattern resulted in columns being incorrectly included](https://github.com/duckdb/duckdb/issues/19517)
* [`#19575` Invalid Unicode error with `LIKE` expressions](https://github.com/duckdb/duckdb/issues/19575)
* [`#19754` Race condition could trigger a segfault in the encryption key cache](https://github.com/duckdb/duckdb/issues/19754)
* [`#19884` Copying to Parquet with a prepared statement did not work](https://github.com/duckdb/duckdb/issues/19884)
* [`#19901` Memory management has been improved during WAL replay in the presence of indexes](https://github.com/duckdb/duckdb/pull/19901)
* [`#19916` The default timezone of DuckDB Wasm in a browser had an offset inverted from what it should be](https://github.com/duckdb/duckdb/issues/19916)
* [`#19924` The optimizer incorrectly removed the `ORDER BY` from aggregates](https://github.com/duckdb/duckdb/issues/19924)
* [`#19970` Fixed updates on indexed tables with DICT_FSST compression](https://github.com/duckdb/duckdb/pull/19970)
* [`#20009` Fixed updates with DICT_FSST compression](https://github.com/duckdb/duckdb/pull/20009)
* [`#20044` Fixed edge case in index deletion code path](https://github.com/duckdb/duckdb/pull/20044)

## Windows ARM64

We are introducing beta support for Windows ARM64 by supporting extensions and shipping Python wheels.

### Extension Distribution for Windows ARM64

On Windows ARM64, you can now natively install core extensions, including complex ones like [`spatial`]({% link docs/stable/core_extensions/spatial/overview.md %}):

```batch
duckdb
```

```sql
PRAGMA platform;
```

```text
┌───────────────┐
│   platform    │
│    varchar    │
├───────────────┤
│ windows_arm64 │
└───────────────┘
```

```sql
INSTALL spatial;
LOAD spatial;
SELECT ST_Area(ST_GeomFromText(
        'POLYGON((0 0, 4 0, 4 3, 0 3, 0 0))')
    ) AS area;
```

```text
┌────────┐
│  area  │
│ double │
├────────┤
│  12.0  │
└────────┘
```

### Python Wheel Distribution for Windows ARM64

We now distribute Python wheels for Windows ARM64. This means that you take e.g. a Copilot+ laptop and run:

```batch
pip install duckdb
```

This installs the `duckdb` package using the binary distributed through [PyPI](https://pypi.org/project/duckdb/).

```batch
python
```

```console
Python 3.13.9 (tags/v3.13.9:8183fa5, Oct 14 2025, 14:51:39) [MSC v.1944 64 bit (ARM64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import duckdb
>>> duckdb.__version__
'1.4.3'
```

Currently, many Python installations that you'll find on Windows ARM64 computers use the x86_64 (AMD64) Python distribution and run through Microsoft's [Prism emulator](https://learn.microsoft.com/en-us/windows/arm/apps-on-arm-x86-emulation). For example, if you install Python through the Windows Store, you will get the Python AMD64 installation.

> To understand which platform your Python installation is using, observe the Python CLI's first line (e.g., `Python 3.13.9 ... (ARM64)`).

Using the [`tpch` extension]({% link docs/stable/core_extensions/tpch.md %}), we can perform a quick benchmark by running the queries on the TPC-H SF100 dataset:

<details markdown='1'>
<summary markdown='span'>
Click here to see the benchmark snippet.
</summary>
```python
import duckdb
import os
import time

con = duckdb.connect("tpch-sf100.db")

con.execute("INSTALL tpch")
con.execute("LOAD tpch")
con.execute("CREATE OR REPLACE TABLE timings(query INTEGER, runtime DOUBLE)")

print(f"Architecture: {os.environ.get('PROCESSOR_ARCHITECTURE')}")

for i in range(1, 23):    
    start = time.time()
    con.execute(f"PRAGMA tpch({i})")
    duration = time.time() - start
    print(f"Q{i}: {duration:.02f}")
    con.execute(f"INSERT INTO timings VALUES ({i}, {duration})")

res = con.execute(f"""
    SELECT median(runtime)::DECIMAL(8, 2), geomean(runtime)::DECIMAL(8, 2)
    FROM timings""").fetchall()
print(f"Median runtime: {res[0][0]}")
print(f"Geomean runtime: {res[0][1]}")
```
</details>

Running the queries using the ARM64 package yielded a geomean runtime of 1.59 seconds, a 24% performance improvement.

## Conclusion

This post was a short summary but, as usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.3).
We would like to thank our contributors for providing detailed issue reports and patches.
Stay tuned for the release of v1.4.4 and v1.5.0 early next year!
