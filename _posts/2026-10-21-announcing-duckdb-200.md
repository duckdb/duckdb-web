---
layout: post
title: "Announcing DuckDB 2.0.0 LTS “Cinnamon Teal”"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/duckdb-release-2-0-0.svg"
image: "/images/blog/thumbs/duckdb-release-2-0-0.png"
excerpt: "The DuckDB team is happy to announce that today we're releasing DuckDB version 2.0.0 LTS, codenamed “Cinnamon Teal” (Spatula cyanoptera). This is our biggest feature release so far, shipping asynchronous I/O, triggers and an extensible SQL parser, along with a first-class `VARIANT` type, a more efficient storage format and much more, built from close to 20,000 commits since v1.5."
tag: release
---

We are proud to release DuckDB v2.0.0, codenamed “Cinnamon Teal” after the [_Spatula cyanoptera_](https://en.wikipedia.org/wiki/Cinnamon_teal), a strikingly reddish-brown duck found in the western Americas.

While [DuckDB v1.0]({% post_url 2024-06-03-announcing-duckdb-100 %}) was all about stability and backward compatibility, DuckDB v2.0 is above all a feature release.
In this blog post, we summarize the highlights and then walk through the breaking changes and how to migrate.
We showcased many of the new features in [“A Preview of DuckDB v2.0”]({% post_url 2026-08-17-duckdb-20-highlights %}), which covers each one in more depth.
For the complete release notes, see the [release page on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.0).

> Tip To install the new version, please visit the [installation page]({% link install/index.html %}).
> Note that it can take a few days to release some extensions and client libraries (e.g., Go, R, Java) due to the extra changes and review rounds required.

With this release, there are currently three DuckDB lines available.
DuckDB v2.0 is a long-term support (LTS) release with support until at least October 2027.
The previous LTS release, version 1.4, is still supported until late November 2026.
To ensure a smooth transition and allow sufficient time for testing,
we extended the support period of DuckDB v1.5 until March 2027, effectively also turning it into an LTS release.
For details, see the [release calendar]({% link release_calendar.md %}).

To find your way around the documentation for all of the new features, we also published a [“What's New in the Docs for 2.0”]({% link docs/preview/whats_new_in_the_docs.md %}) page that links each feature below to its documentation.

## DuckDB as a Server

DuckDB has been an in-process database since day one.
In [DuckDB 1.5.3]({% post_url 2026-05-20-announcing-duckdb-153 %}), released in May, we introduced the Quack protocol that lets you run DuckDB in a traditional client-server setup, along with the [`quack` extension]({% link docs/preview/core_extensions/quack.md %}), which implements DuckDB's native protocol, so any DuckDB process can [serve its databases]({% link docs/preview/quack/overview.md %}#server-side-usage).

### Quack and `CONNECT`

DuckDB 2.0.0 ships a polished version of the Quack protocol with substantial performance and stability improvements. It also introduces the new [`CONNECT` statement]({% link docs/preview/sql/statements/connect.md %}) that allows attaching and switching to a remote database in a single command for better ergonomics:

<!-- markdownlint-disable MD001 -->

<div class="duck-diagram" markdown="1">

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB server

```sql
CALL quack_serve(
    token = 'my_token'
);

CREATE TABLE events
    (date DATE, name VARCHAR);

INSERT INTO events VALUES
    ('2027-04-07',
     'DuckCon #8');
```

</div>

<div class="duck-diagram-arrow">quack:</div>

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB client

```sql
ATTACH 'quack:myserver.com'
    AS qk (TOKEN 'my_token');

CONNECT qk;
SELECT * FROM events;

┌────────────┬────────────┐
│    date    │    name    │
│    date    │  varchar   │
├────────────┼────────────┤
│ 2027-04-07 │ DuckCon #8 │
└────────────┴────────────┘
```

</div>

</div>

<!-- markdownlint-enable MD001 -->

The `CONNECT` statement is not limited to Quack: it points your session at any remote database that supports it, and the new remote pushdown optimizer ships SQL directly to PostgreSQL and MySQL instead of pulling tables over the wire.

### Quack in the CLI

The CLI also has shortcuts for setting up a Quack client-server pair: the new [`-serve` and `-connect` arguments]({% link docs/preview/clients/cli/arguments.md %}#serving-and-connecting-to-remote-databases) start a Quack server or connect to one directly from the command line:

<!-- markdownlint-disable MD001 -->

<div class="duck-diagram" markdown="1">

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> CLI server

```batch
duckdb -serve
```

<!-- «memory» D -->
```plsql
CREATE TABLE t AS
      SELECT 42 AS x;
```

</div>

<div class="duck-diagram-arrow">quack:</div>

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> CLI client

```batch
duckdb -connect
```

<!-- «quack:localhost memory» -->
```plsql
FROM t;

┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

</div>

</div>

<!-- markdownlint-enable MD001 -->

## Performance

### Asynchronous I/O

DuckDB v2.0 introduces [asynchronous I/O]({% link docs/preview/data/io.md %}) throughout the engine. The I/O layer now scales independently from the query processing layer, issuing reads in the background and keeping multiple requests in flight. This means far more parallelism for remote reads and dramatically faster queries on object storage such as [`s3://`]({% link docs/preview/core_extensions/httpfs/s3api.md %}).

We described the design in detail in a [dedicated blog post]({% post_url 2026-07-31-asynchronous-io %}).
In that post, we showed the network throughput over the course of a query with and without asynchronous I/O:

![Network throughput]({% link images/blog/v20-release/sync-vs-async-network-throughput-light.svg %}){: .lightmode-img }
![Network throughput]({% link images/blog/v20-release/sync-vs-async-network-throughput-dark.svg %}){: .darkmode-img }
*Network throughput. Higher utilization and shorter runtime are better.*{: .caption }

### The `VARIANT` Type Becomes a First-Class Citizen

The [`VARIANT` type]({% link docs/preview/sql/data_types/variant.md %}) stores semi-structured, schema-less data such as JSON while keeping the performance of columnar execution. First introduced [in v1.5]({% post_url 2026-03-09-announcing-duckdb-150 %}#variant-type), it is now fully integrated. Think of it as JSON on steroids: a `VARIANT` column can store differently shaped data in every row, but unlike JSON it is not a text format. DuckDB detects the common structure in your data and “shreds” it, so it compresses well and executes fast. In v2.0 the pipeline works end to end, from shredded execution straight out of storage to shredded `VARIANT` reading and writing for Parquet, backed by a family of [`variant_*` functions]({% link docs/preview/sql/functions/variant.md %}).

```sql
CREATE TABLE events (payload VARIANT);
INSERT INTO events
VALUES
    ('{"user": {"id": 42, "tags": ["a", "b"]}}'::JSON::VARIANT),
    ('{"event": "click", "x": 10, "y": 20}'::JSON::VARIANT);

SELECT variant_type(payload), variant_keys(payload)
FROM events;
```

### Agent Mode in the CLI

Coding agents such as Claude Code, Codex and Cursor increasingly drive the DuckDB CLI on their users' behalf. The v2.0 CLI detects when it is being run by an agent and switches to [agent mode]({% post_url 2026-10-09-agent-mode %}): it prints compact Markdown tables instead of padded boxes, says clearly when a result was truncated, stops runaway queries early and reports errors as JSON.

Long-running SQL queries report their expected cost prior to running, so the agent can decide whether to wait. In our experiments on TPC-H, agent mode cut the number of output tokens the model had to read by 59%. You can turn it _on_ for manual testing using the [`-agent` flag]({% link docs/preview/clients/cli/agent_mode.md %}#activating-agent-mode) or instruct your agent to turn it _off_ using the `-no-agent` flag.

## Extensibility

### A Brand New SQL Parser

DuckDB has always used a parser derived from PostgreSQL's. In v2.0 we ship our own modern, extensible [PEG-based parser]({% post_url 2026-08-20-duckdb-20-peg-parser %}). Extensions can now hook into the grammar itself (an idea we first explored in our [research on runtime-extensible parsers]({% post_url 2024-11-22-runtime-extensible-parsers %})), so expect extensions that expose entirely new SQL syntax. Error messages now come with precise source locations. For details, see the [PEG parser documentation]({% link docs/preview/sql/peg_parser.md %}). The new parser is designed to be compatible with the old one, so you should not notice the swap. If you do, please file an issue. In the meantime, you can switch back to the old parser using the [`legacy_parser` extension]({% link docs/preview/core_extensions/legacy_parser.md %}) by running `SET enable_legacy_parser = true;`{:.language-sql .highlight}.

The old parser had served DuckDB since its first commit in 2018. Its grammar was generated with YACC/Bison, which produces an LALR(1) parser, so as DuckSQL grew, even small additions could collide with existing rules and raise `shift/reduce` or `reduce/reduce` conflicts. A PEG grammar avoids this by trying alternatives in the order they are written, so adding syntax no longer risks breaking unrelated rules. Python itself moved to a PEG-based parser in [version 3.9](https://peps.python.org/pep-0617/) for the same flexibility.

### Write Extensions Once and Host Them Yourself

DuckDB v2.0 ships a revamped [C API v2]({% link docs/preview/clients/c/overview.md %}#stable-c-api-and-c-api), which is considerably more powerful than its predecessor and exposes components such as file systems and table functions to extensions. Before marking it as stable, we would like to test it in the field, so please give it a try and send us your feedback!

You can also register and host your own trusted extension repositories, so an organization can host and sign its own extensions and have them install and load just like the built-in ones:

```sql
SET allow_extension_repositories = 'allowed';

CREATE EXTENSION REPOSITORY my_repo
    WITH PREFIX 'https://extensions.example.org';

INSTALL my_ext FROM my_repo;
LOAD my_repo/my_ext;
```

A repository is a name, a URL prefix and one or more RSA public keys that are trusted to sign the extensions served from it. The prefix can point at anything DuckDB can read: a local path, `https`, `s3`, you name it. At `CREATE` time, DuckDB fetches the repository's public keys and pins them into the repository definition, printing each key's SHA-256 fingerprint so you can compare it against one published out of band.

For more details, see the [Extension Repositories page]({% link docs/preview/extensions/extension_repositories.md %}).

### Core Extension Updates

(TODO: turn this into text)

* We released [DuckLake 1.1](https://ducklake.select/2026/10/21/ducklake-11/), incl. spec and reference implementation
* The Iceberg extension ...
* The Delta extension ...

In the coming weeks, we'll release more blog posts about these features.

## SQL Features

### Triggers

DuckDB v2.0 delivers triggers in full: `BEFORE` and `AFTER` triggers, `FOR EACH ROW` and `FOR EACH STATEMENT`, transition tables via `REFERENCING OLD/NEW TABLE`, multiple triggers per event, `RETURNING` on triggered tables and `DROP TRIGGER`. The classic use case is audit tables, where a trigger records what changed in response to a table modification.

```sql
CREATE TRIGGER trg_audit
    AFTER UPDATE ON target
    REFERENCING
        OLD TABLE AS o
        NEW TABLE AS n
    FOR EACH STATEMENT
        INSERT INTO audit
        SELECT n.id, o.val, n.val
        FROM o JOIN n ON o.id = n.id;
```

For more details, see the [`CREATE TRIGGER` statement page]({% link docs/preview/sql/statements/create_trigger.md %}).

### SQL Dialect Additions

As always, DuckDB's SQL dialect keeps growing. A few favorites from this release cycle:

* [`NEAREST` joins]({% link docs/preview/sql/query_syntax/from.md %}#nearest-joins) turn top-k similarity search into a join clause, handy for vector and embedding workloads.
* [Data-modifying CTEs]({% link docs/preview/sql/query_syntax/with.md %}#data-modifying-ctes) let you use `INSERT`, `UPDATE`, `DELETE` and `COPY` as pipeline steps.
* [Nested schemas]({% link docs/preview/sql/statements/create_schema.md %}#nested-schemas) allow schemas within schemas, e.g., `CREATE SCHEMA finance.reports`.
* The [`$⟨variable⟩`{:.language-sql .highlight} shorthand]({% link docs/preview/sql/statements/set_variable.md %}#the-name-shorthand) lets you write `$x` anywhere an expression is allowed, instead of `getvariable('⟨variable⟩')`{:.language-sql .highlight}.
* [JSON mutation functions]({% link docs/preview/data/json/json_functions.md %}#json-mutation-functions) `json_set`, `json_insert`, `json_replace` and `json_remove` modify JSON documents in place (see also our [blog post on JSON patches]({% post_url 2026-08-18-reconciling-json %})).

There is more: SQL-standard [`FETCH FIRST`]({% link docs/preview/sql/query_syntax/limit.md %}#fetch-first), [`UNNEST` in `GROUP BY`]({% link docs/preview/sql/query_syntax/groupby.md %}#grouping-by-unnest) and well-defined [`MERGE`]({% link docs/preview/sql/statements/merge_into.md %}) / [`UPDATE ... FROM`]({% link docs/preview/sql/statements/update.md %}) semantics for multi-matched rows.

## Migrating to v2.0

DuckDB v2.0 comes with a small set of breaking changes. For most users, upgrading is straightforward, but complex deployments running many DuckDB processes need more care. The storage format is the most likely source of problems. We recommend testing v2.0.0 on a shadow system before switching production over, and if your workload is mission-critical, you may want to wait for the first patch releases.

For the full details, see the [migration guide]({% link docs/preview/operations_manual/migration.md %}).

## Internals and Deprecations

### Compiler Requirements

Following DuckDB's long stint on C++11, DuckDB v2.0 now [requires a C++17 compiler]({% link docs/preview/dev/building/overview.md %}#prerequisites).

We also switched to Clang as the default compiler for our release builds. On Linux and macOS, both DuckDB and its core extensions are built with Clang. On Windows, the CLI is built with Clang, while most core extensions are still built with MSVC. We may move more Windows builds to Clang in the future, but this requires further changes.

### Timezones, Calendars and Collations Without ICU

Timezone-aware timestamps, calendars and collations have always been powered by the ICU library. In v2.0, the ICU library is gone entirely: the [`icu` extension]({% link docs/preview/core_extensions/icu.md %}) now implements timezones, calendars and collations itself, with the timezone data built directly from the IANA database and compressed down to around 45 kB.

Everything keeps working exactly as before, and the native implementation is also faster. If you find any issues, please [let us know](https://github.com/duckdb/duckdb/issues)!

### Deprecations

#### Lambda Syntax

The old single-arrow lambda syntax (`x -> x + 1`) is now disabled by default. Use the Python-style syntax instead:

```sql
SELECT list_transform([1, 2, 3], lambda x: x + 1);
```

You can temporarily re-enable the old syntax with `SET lambda_syntax = 'ENABLE_SINGLE_ARROW';`{:.language-sql .highlight}. Both the flag and the single-arrow syntax will be removed entirely in v2.1.

#### Amalgamation Builds

The [amalgamation build]({% link docs/lts/dev/building/overview.md %}), which bundles DuckDB's entire source code into a single header and a single source file, is now deprecated. The amalgamation has grown too large to be realistically useful in most cases.

#### Gradual Phase-Out of macOS x86_64

We are gradually phasing out `osx_amd64` from the list of fully supported [platforms]({% link docs/preview/dev/building/overview.md %}#platforms).
For the time being, DuckDB and [core extensions]({% link docs/preview/core_extensions/overview.md %}) are still built and supported, but [community extensions]({% link docs/preview/extensions/community_extensions.md %}) are no longer built for this platform.

DuckDB version 2.1 will stop supporting `osx_amd64`.

## Summary

These were a few highlights, but there are many more features and improvements in this release. There have been almost 20,000 commits by many contributors since v1.5, shipping smaller features as well as performance and usability improvements. The full [release notes can be found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.0).

We would like to thank our community for the detailed issue reports and feedback that have driven this release, and our special thanks go to our contributors!

<!-- TODO: maybe drop these? -->

## Tmp

### Faster Queries Across the Board

As with every release, a lot of work went into making your existing queries faster without you doing anything. Partial aggregates are now pushed below joins, redundant aggregations are reused, the recursive CTE engine has been rewritten, aggregations spill to disk when they outgrow memory, and row-group pruning has been massively expanded across structs, lists, decimals, UUIDs, `IN` filters and even function predicates.

In a [microbenchmark]({% post_url 2026-08-17-duckdb-20-highlights %}#6-faster-queries-across-the-board) of single-source reachability over a graph with one million edges, DuckDB v2.0 runs a plain recursive CTE about 40× faster than v1.5. We explain how in a [dedicated blog post]({% post_url 2026-08-25-how-duckdb-runs-recursive-ctes-faster %}).

### Storage Format v2.0

DuckDB v2.0 bumps the default [storage format version]({% link docs/preview/internals/storage.md %}) to v2.0.0. Column metadata is now loaded lazily, so databases with big indexes and wide tables open faster and use far less memory; the `DICT_FSST` string compression method is enabled by default; deletes are stored compactly; and the storage layer performs much stronger corruption validation on read.

Because the new format is not backward compatible, see the [migration section](#migrating-to-v20).
