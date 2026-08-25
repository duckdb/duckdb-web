---
layout: default
title: DuckDB Community Support Policy
body_class: tmguidelines
max_page_width: small
redirect_from:
- /support
---

# DuckDB Community Support Policy

(Last updated: August 26, 2026)

## Overview

We continue to be amazed by the growth of the DuckDB community. DuckDB now sees more than three million downloads each day, alongside an active and rapidly growing community across GitHub, social media, meetups, and other channels. When we started DuckDB in 2018, we could not have imagined this level of adoption. We remain deeply grateful to everyone who uses, contributes to, and supports the project.

Until now, the size of our team has limited the level of support we could provide as the community grew. We have had to make difficult choices about where to focus our time, balancing the development and maintenance of DuckDB with the needs of an increasingly large and diverse user base.

By [joining AWS](https://ducklabs.com/ducklabs-to-join-aws), DuckLabs now has access to additional resources that will allow us to expand our support for the DuckDB community. We are pleased to be able to invest more deeply in documentation, education, community programs, contributor support, and the channels through which users can ask questions and share feedback. We will provide further details about these initiatives as they become available.

Starting this fall, the [DuckDB Foundation](https://duckdb.foundation/) will also establish a Technical Advisory Board. The board will bring together members of the wider DuckDB community to provide input on the project’s technical direction and help ensure that its development continues to reflect the needs of its users and contributors.

## Support Model

- **Where to file tickets:** Users can file bug reports as issues on GitHub ([DuckDB](https://github.com/duckdb/duckdb/issues), [DuckLake](https://github.com/duckdb/ducklake/issues), [Quack](https://github.com/duckdb/duckdb-quack/issues), and [other repositories](https://duckdb.org/docs/current/dev/repositories)). Users can also suggest features on GitHub Discussions of the respective repositories.  
- **Response time:** We attempt to reproduce incoming issues within a few business days. Internally, we assign issues in weekly batches. However, we are unable to guarantee that issues will be resolved (e.g., fixed) within any time frame.

## Scope

- **Client APIs:**  
  - We provide first-tier support for the command line shell as well as the C, Go, Java (JDBC), ODBC, Node.js, Python, Rust and WebAssembly client APIs.  
  - The C++ API is intended for internal use and is not designed as a stable user-facing API. See the [Client overview page](https://duckdb.org/docs/current/clients/overview) for more details. (Note that starting from version v2.0, we will ship a stable C++ API.)  
- **Extensions:** The community support policy only covers the primary extensions from the [core extensions](https://duckdb.org/docs/current/core_extensions/overview).  
- **Crashes and internal errors:** Issues that cause crashes (segfault, bus error, abort) and issues that result in [internal errors](https://duckdb.org/docs/current/dev/internal_errors) get higher priority.  
- **Platforms:** We only support the following platforms:  
  - Linux x86_64 & aarch64 (mainstream distributions under support by distributor running with glibc). The last three Ubuntu LTS releases are safe bets (currently: Ubuntu 22.04, 24.04 and 26.04)  
  - macOS latest  
  - Windows 11+ on x86_64  
- **Versions:** We support the following versions:  
  - The latest stable version (currently v{{ site.current_duckdb_version }})  
  - The latest LTS version (currently v{{ site.lts_duckdb_version }})  
  - The bleeding edge version ([`main` branch](https://github.com/duckdb/duckdb/tree/main)) of DuckDB

Out of scope:

- **Architectures:** We [do not support](https://duckdb.org/docs/current/dev/building/unofficial_and_unsupported_platforms) 32-bit and big-endian architectures.  
- **Debug builds:** Debug builds of DuckDB's clients and tooling are out of scope.  
- **Internals:** We are unable to answer questions about DuckDB internals, e.g., physical operators or storage internals. In general, if an issue cannot be triggered from SQL or one of the [supported client APIs](#apis), it's probably out of scope.

## Issue Submission Guide

There are several ways that you can help us resolve issues more quickly. The more time you can spend to reduce our team's workload regarding the issue, the more likely we can help. We receive a high volume of issues and we sometimes spend an enormous amount of time divining missing information in bug reports like schema, datasets, previous state, environment, etc. If you make sure that this information is available upon submission, we can proceed much more quickly with resolving the issue.

- **Issue template:** Please follow the [issue template](https://github.com/duckdb/duckdb/blob/main/.github/ISSUE_TEMPLATE/bug_report.yml).  
- **Data sharing:** Please make every effort to provide the data that is triggering the issue. The template advises to include all of the required data in your issue itself. Sometimes this means actually creating a dataset that you can share, which is preferably minimal in size.  
- **Succeeding examples:** If possible, include test cases that succeed that are similar to the failure to help pinpoint the problem.  
- **Multiple clients:** Try to replicate the issue in multiple clients (CLI preferred).  
- **Debugging issues:** Debugging issues is a fantastic way to contribute to DuckDB\!  
- **Background information:** Providing background information about why you are approaching your task the way you are can help DuckLabs suggest workarounds prior to a fix.  
- **Conciseness:** Agentic coding tools tend to generate large amounts of text with a low information content. Please clean these up before submitting.

## LTS Releases

We are delighted to see that DuckDB is used regularly in production environments and realize that such deployments often come with a requirement for long-term maintenance. Hence, starting with release v1.4.0, every other DuckDB version is a Long Term Support (LTS) edition. For LTS DuckDB versions, community support lasts at least one year after the release.