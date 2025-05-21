---
layout: docu
redirect_from: null
title: Working with Huge Databases
---

This page contains information for working with huge DuckDB database files.
While most DuckDB databases are well below 1 TB,
in our [2024 user survey]({% post_url 2024-10-04-duckdb-user-survey-analysis %}#dataset-sizes), 1% of respondents used DuckDB files of 2 TB or more (corresponding to roughly 10 TB of CSV files).

DuckDB supports huge database files without any practical restrictions, however, there are a few things to keep in mind when working with huge database files.

1. Object storage systems have lower limits on file sizes than block-based storage systems. For example, [AWS S3 limits the file size to 5 TB](https://aws.amazon.com/s3/faqs/).

2. Checkpointing a DuckDB database can be slow. For example, checkpointing after adding a few rows to a table in the [TPC-H]({% link docs/stable/core_extensions/tpch.md %}) SF1000 database takes approximately 5 seconds.

3. On block-based storage, the file has a big effect on performance when working with large files. On Linux, DuckDB performs best with XFS on large files.
