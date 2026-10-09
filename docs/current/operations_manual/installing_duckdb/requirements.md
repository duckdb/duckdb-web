---
layout: docu
title: Requirements
---

DuckDB is designed to be [portable]({% link why_duckdb.md %}#portable) and has very few runtime dependencies. Still, there are a few requirements to be aware of before installing or running DuckDB.

## Linux

DuckDB's official Linux binaries require [glibc](https://www.gnu.org/software/libc/) 2.28 or newer. Since DuckDB 1.3.0, the official Linux binaries are [built using the `manylinux_2_28` image](https://github.com/duckdb/duckdb/pull/16956), which combines an older glibc with a newer compiler. As a result, extensions are no longer distributed for the `linux_amd64_gcc4` platform.

Most mainstream Linux distributions ship with [glibc 2.28](https://lists.gnu.org/archive/html/info-gnu/2018-08/msg00000.html) or newer, so no action is needed on these systems. If you need to run DuckDB on a system with an older glibc, you can [build DuckDB from source]({% link docs/current/dev/building/overview.md %}) against that version.
