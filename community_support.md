---
layout: default
title: Community Support
body_class: tmguidelines
max_page_width: small
redirect_from:
- /support
---

# DuckDB Community Support Policy

(Last updated: August 2026)

## Changelog

* We removed the limitation on volume. We are now accepting any volume of issues from both individuals and companies.  
* Removed Discord mention.

## Overview

We are continuously amazed by the growth of the DuckDB community. There are now 50M+ downloads each month and a large amount of social media followers, GitHub stars and so forth. When we started DuckDB back in 2018, we could not have imagined this level of adoption and we are absolutely humbled to see it.

Having many users and many AI agents working on DuckDB means there are a large number of new issues each day. Hence, we need to prioritize them. We would like to be upfront and clarify DuckDB's support model, and the following policies apply to our community support.

## Support Model

- **Where to file tickets:** Users can file bug reports as issues on GitHub ([DuckDB](https://github.com/duckdb/duckdb/issues), [DuckLake](https://github.com/duckdb/ducklake/issues), [Quack](https://github.com/duckdb/duckdb-quack/issues)) and suggest features on GitHub Discussions.  
- **Response time:** We attempt to reproduce incoming issues within a few business days. Internally, we assign issues in weekly batches. However, we are unable to guarantee that issues will be resolved (e.g., fixed) within any time frame.

## Scope

- **APIs:** We only support the C, Go, Java (JDBC), ODBC, Node.js, Python, R, Rust and WebAssembly client APIs as well as the command line shell. The C++ API is intended for internal use and is not designed as a stable user-facing API. See the [Client overview page](https://duckdb.org/docs/current/clients/overview) for more details.  
- **Extensions:** Within the main project, the community support policy only covers the httpfs, icu, json and parquet extensions.  
- **Internals:** We are unable to answer questions about DuckDB internals, e.g., physical operators or storage internals. In general, if an issue cannot be triggered from SQL or one of the [supported client APIs](#apis), it's probably out of scope.  
- **Crashes and internal errors:** Issues that cause crashes (segfault, bus error, abort) and issues that result in internal errors get higher priority.  
- **Platforms:** We only support the following platforms: Windows 11+ on x86_64, macOS latest, Linux x86_64 & aarch64 (mainstream distributions under support by distributor running with glibc). The last three Ubuntu LTS releases are safe bets (currently: Ubuntu 22.04, 24.04 and 26.04).  
- **Versions:** We support the latest stable version (currently v{{ site.current_duckdb_version }}), the latest LTS version (currently v{{ site.lts_duckdb_version }}) and the bleeding edge version ([`main` branch](https://github.com/duckdb/duckdb/tree/main)) of DuckDB.  
- **Architectures:** We [do not support](https://duckdb.org/docs/current/dev/building/unofficial_and_unsupported_platforms) 32-bit and big-endian architectures.  
- **Debug builds:** Debug builds of DuckDB's clients and tooling are out of scope.

## Issue Submission Guide

There are several ways that you can help us resolve issues more quickly. The more time you can spend to reduce our team's workload regarding the issue, the more likely we can help. We receive a high volume of issues and we sometimes spend an enormous amount of time divining missing information in bug reports like schema, datasets, previous state, environment, etc. If you make sure that this information is available upon submission, we can proceed much more quickly with resolving the issue.

- **Issue template:** Please follow the [issue template](https://github.com/duckdb/duckdb/blob/main/.github/ISSUE_TEMPLATE/bug_report.yml).  
- **Data sharing:** Please make every effort to provide the data that is triggering the issue. The template advises to include all of the required data in your issue itself. Sometimes this means actually creating a dataset that you can share, which is preferably minimal in size.  
- **Succeeding examples:** If possible, include test cases that succeed that are similar to the failure to help pinpoint the problem.  
- **Multiple clients:** Try to replicate the issue in multiple clients (CLI preferred).  
- **Debugging issues:** Debugging issues is a fantastic way to contribute to DuckDB\!  
- **Background information:** Providing background information about why you are approaching your task the way you are can help DuckLabs suggest workarounds prior to a fix.

## LTS Releases

We are delighted to see that DuckDB is used regularly in production environments and realize that such deployments often come with a requirement for long-term maintenance. Hence, starting with release v1.4.0, every other DuckDB version is a Long Term Support (LTS) edition. For LTS DuckDB versions, community support lasts a year after the release.
