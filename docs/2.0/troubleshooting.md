---
layout: docu
redirect_from:
- /docs/stable/troubleshooting
- /docs/current/troubleshooting
- /docs/lts/troubleshooting
- /docs/preview/troubleshooting
title: Troubleshooting
---

This page collects the most common issues encountered when working with DuckDB and links to the detailed documentation for each. If you run into a problem that is not covered here, please consult the relevant section of the documentation or the [how-to guides]({% link docs/2.0/guides/overview.md %}).

## File Lock Errors

DuckDB allows only a single process to write to a database file at a time. Errors such as “Could not set lock on file” usually mean another process (for example, an editor, a notebook kernel, or a second CLI session) still holds the database open. The concurrency model and how to work around it are described in the following page.

* [Concurrency]({% link docs/2.0/connect/concurrency.md %})

## Out-of-Memory Errors

When a query needs more memory than is available, DuckDB spills intermediate results to disk, but some workloads can still exhaust memory. The following pages explain how to diagnose and resolve out-of-memory situations.

* [Out-of-Memory Issues]({% link docs/2.0/guides/performance/oom.md %})
* [Out of Memory Errors]({% link docs/2.0/guides/troubleshooting/oom_errors.md %})

## CSV Type Inference

The CSV reader detects column types and the dialect automatically. When a column is read with an unexpected type, or rows fail to parse, the following pages explain how to inspect and override the detection.

* [CSV Auto Detection]({% link docs/2.0/data/csv/auto_detection.md %})
* [Reading Faulty CSV Files]({% link docs/2.0/data/csv/reading_faulty_csv_files.md %})

## Extension Installation

Extensions are downloaded and loaded at runtime. Installation can fail in offline or restricted environments. The following pages cover installation and its troubleshooting.

* [Installing Extensions]({% link docs/2.0/extensions/installing_extensions.md %})
* [Advanced Installation Methods]({% link docs/2.0/extensions/advanced_installation_methods.md %})
* [Troubleshooting of Extensions]({% link docs/2.0/extensions/troubleshooting.md %})

## S3 and Cloud Storage Access

Reading from and writing to S3 and S3-compatible storage requires the `httpfs` extension and correctly configured credentials. The following pages cover the S3 API and authentication.

* [S3 API Support]({% link docs/2.0/core_extensions/httpfs/s3api.md %})
* [S3 and AWS Authentication]({% link docs/2.0/core_extensions/httpfs/authentication.md %})
