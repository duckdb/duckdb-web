---
layout: docu
redirect_from:
- /dev/testing
- /docs/dev/sqllogictest/overview
title: Overview
---

## How is DuckDB Tested?

Testing is vital to make sure that DuckDB works properly and keeps working properly. For that reason, we put a large emphasis on thorough and frequent testing:
* We run a batch of small tests on every commit using [GitHub Actions](https://github.com/duckdb/duckdb/actions), and run a more exhaustive batch of tests on pull requests and commits in the `main` branch.
* We use a [fuzzer](https://github.com/duckdb/duckdb-fuzzer), which automatically reports issues found through fuzzing DuckDB.
* We use [SQLsmith]({% link docs/stable/core_extensions/sqlsmith.md %}) for generating random queries.
