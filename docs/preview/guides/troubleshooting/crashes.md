---
layout: docu
title: Crashes
---

DuckDB is [thoroughly tested]({% link why_duckdb.md %}#thoroughly-tested) via an extensive test suite.
However, bugs can still occur and these can sometimes lead to crashes.
This page contains practical information on how to troubleshoot DuckDB crashes.

## Types of Crashes

There are a few major types of crashes:

* **Termination signals:** The process stops with a `SIGSEGV` (segmentation fault), `SIGABRT`, etc.: these should never occur. Please [submit an issue](#submitting-an-issue).

* **Internal errors:** an operation may result in an [`Internal Error`]({% link docs/preview/dev/internal_errors.md %}), e.g.:

  ```console
  INTERNAL Error:
  Attempted to access index 3 within vector of size 3
  ```

  After encountering an internal error, DuckDB enters a restricted mode where any further operations will result in the following error message:

  ```console
  FATAL Error:
  Failed: database has been invalidated because of a previous fatal error.
  The database must be restarted prior to being used again.
  ```

* **Out of memory errors:** A DuckDB crash can also be a symptom of the operating system killing the process.
  For example, many Linux distributions run an [OOM reaper or OOM killer process](https://learn.redhat.com/t5/Platform-Linux/Out-of-Memory-Killer/td-p/48828), which kills processes to free up their memory and thus prevents the operating system from running out of memory.
  If your DuckDB session is killed by the OOM reaper, consult the [“OOM errors” page]({% link docs/preview/guides/troubleshooting/oom_errors.md %})

## Recovering Data

If your DuckDB session was writing to a persistent database file prior to crashing,
there might be a WAL ([write-ahead log](https://en.wikipedia.org/wiki/Write-ahead_logging)) file next to your database named `⟨database_filename⟩.wal`{:.language-sql .highlight}.
To recover data from the WAL file, simply start a new DuckDB session on the persistent database.
DuckDB will then replay the write-ahead log and perform a [checkpoint operation]({% link docs/preview/sql/statements/checkpoint.md %}), restoring the database to the state before the crash.

## Troubleshooting the Crash

### Using the Latest Stable and Preview Builds

DuckDB is constantly improving, so there is a chance that the bug you have encountered has already been fixed in the codebase.
First, try updating to the [**latest stable build**]({% link install/index.html %}?version=stable).
If this doesn't resolve the problem, try using the [**preview build**]({% link install/index.html %}?version=main) (also known as the “nightly build”).

If you would like to use DuckDB with an [open pull request](https://github.com/duckdb/duckdb/pulls) applied to the codebase,
you can try [building it from source]({% link docs/preview/dev/building/overview.md %}).

### Search for Existing Issues

There is a chance that someone else already reported the bug that causes the crash.
Please search in the [GitHub issue tracker](https://github.com/duckdb/duckdb/issues) for the error message to see potentially related issues.
DuckDB has a large community and there may be some suggestions for a workaround.

### Disabling the Query Optimizer

Some crashes are caused by DuckDB's query optimizer component.
To identify whether the optimizer is causing the crash, try to turn it off and re-run the query:

```sql
PRAGMA disable_optimizer;
```

If the query finishes successfully, then the crash was caused by one or more optimizer rules.
To pinpoint the specific rules that caused the crash, you can try to [selectively disable optimizer rules]({% link docs/preview/configuration/pragmas.md %}#selectively-disabling-optimizers). This way, your query can still benefit from the rest of the optimizer rules.

### Try to Isolate the Issue

Some issues are caused by the interplay of different components and extensions, or are specific to certain platforms or client languages.
You can often isolate the issue to a smaller problem.

#### Reproducing in Plain SQL

Issues can also occur due to differences in client libraries.
To understand whether this is the case, try reproducing the issue using plain SQL queries with the [DuckDB CLI client]({% link docs/preview/clients/cli/overview.md %}).
If you cannot reproduce the issue in the command line client, it is likely related to the client library.

#### Different Hardware Setup

According to our experience, several crashes occur due to faulty hardware (overheating hard drives, overclocked CPUs, etc.).
Therefore, it's worth trying another computer to run the same workload.

#### Decomposing the Query

It's a good idea to try to break down the query into multiple smaller queries with each using a separate DuckDB extension and SQL feature.

For example, if you have a query that targets a dataset in an AWS S3 bucket and performs two joins on it, try to rewrite it as a series of smaller steps as follows.
Download the dataset's files manually and load them into DuckDB.
Then perform the first join and the second join separately.
If the multi-step approach still exhibits the crash at some step, then the query that triggers the crash is a good basis for a minimal reproducible example. If the multi-step approach works and the multi-step process no longer crashes, try to reconstruct the original query and observe which step reintroduces the error.
In both cases, you will have a better understanding of what is causing the issue and potentially also a workaround that you can use right away.
In any case, please consider [submitting an issue](#submitting-an-issue) with your findings.

## Submitting an Issue

If you found a crash in DuckDB, please consider submitting an issue in our [GitHub issue tracker](https://github.com/duckdb/duckdb/issues) with a [minimal reproducible example](https://en.wikipedia.org/wiki/Minimal_reproducible_example).
