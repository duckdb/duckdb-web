---
layout: post
title: "Delta Grows Up: Writes, Unity Catalog and Time Travel"
author: "Ben Fleis"
excerpt: "DuckDB's Delta and Unity Catalog extensions shed their experimental tags — now with writes, Unity Catalog and time travel support."
tags: ["extensions"]
thumb: "/images/blog/thumbs/delta-uc-updates.svg"
image: "/images/blog/thumbs/delta-uc-updates.jpg"
---

Welcome back! While we here at DuckDB Labs are typically of the quacking
persuasion, we’ve been busy as beavers, shoring up our Delta to prepare for
what’s next… Unity Catalog! Let’s look at how DuckDB’s
[Delta]({% link docs/current/core_extensions/delta.md %}) and
[Unity Catalog]({% link docs/current/core_extensions/unity_catalog.md %})
extensions have grown up enough to shed the experimental tag, and see what
has changed since our [last
update]({% post_url 2025-03-21-maximizing-your-delta-scan-performance %}).

## Time to Open the Delta

Before we jump in, let's review briefly. Delta is a foundational [open
table format and toolset](https://docs.delta.io/) for building and managing
data lakes, related to Iceberg and other lakehouse formats. DuckDB supports
Delta tables via its [Delta
Extension]({% link docs/current/core_extensions/delta.md %}).

In that last update we highlighted performance wins, particularly file skipping
via filter pushdowns, and metadata caching with snapshot pinning. Now we build
on these, and add writes, time travel and Unity Catalog support, plus
more performance gains!

### Building Up the Delta (Lake): Writes

What fun are reads without writes? The big addition since we last chatted is
`INSERT` support! It works as simply as you expect. Let's assume you have a Delta
table ready to go. `INSERT` away, it's that simple:

```sql
-- Schema: (text VARCHAR, code BIGINT)
ATTACH './path/to/my_table' AS my_table (TYPE delta);

INSERT INTO my_table
VALUES ('Question 2', 2), ('The Answer', 42);

-- Bulk insert from a query
INSERT INTO my_table
FROM (SELECT text || ' (copy)', code + 100 FROM my_table);
```

Also worth calling out – multiple `INSERT`s within a `BEGIN` / `COMMIT` block are
stored as a single Delta version: one atomic commit, one new log entry. And,
as you'll see later, this works with catalogs too! `UPDATE`, `MERGE`, and `DELETE`
are not yet supported, but on our future work list.

### Time Travel

DuckDB's Delta extension now supports [time
travel](https://delta.io/blog/2023-02-01-delta-lake-time-travel/). Any Delta
table can be queried as of a particular version. DuckDB supports binding to a
specific `VERSION` either at `ATTACH` time, or as part of an individual query.

Let's assume that we have built up the above `my_table` incrementally, with
versions 0, 1, and 2 containing:

| Version | Contents                                                                                   |
| ------- | ------------------------------------------------------------------------------------------ |
| 0       | `('Question 1', 1)`                                                                        |
| 1       | + `('Question 2', 2)`, `('The Answer', 42)`                                                |
| 2       | + `('Question 1 (copy)', 101)`, `('Question 2 (copy)', 102)`, `('The Answer (copy)', 142)` |

You can attach normally and query arbitrary versions inline as needed. The
most flexible approach:

```sql
ATTACH './path/to/my_table' AS my_table (TYPE delta);

SELECT count() FROM my_table AT (VERSION => 0); -- 1  (Question 1 only)
SELECT count() FROM my_table AT (VERSION => 1); -- 3  (after 1st insert)
SELECT count() FROM my_table;                   -- 6  (latest)
```

Or attach, pinned to a specific version, which is useful when you want a stable
reference that never changes, regardless of future writes:

```sql
-- Always v1, no matter what gets written later
ATTACH './path/to/my_table' AS my_table_v1
    (TYPE delta, VERSION 1);

SELECT count() FROM my_table_v1;      -- → 3

-- Locked to whatever was latest at attach time
ATTACH './path/to/my_table' AS my_table_pinned
    (TYPE delta, PIN_SNAPSHOT);

SELECT count() FROM my_table_pinned;  -- → 6
```

### Growing Up: No Longer a Kit 🦫

The DuckDB Delta extension is no longer a
[kit](https://duckduckgo.com/?q=what+is+a+baby+beaver+called) and has grown
up quite a bit since a year ago.
As you just saw, we added writes and time travel. These features open the
door to something bigger: Unity Catalog coordination.

## Unity Catalog Support atop the Delta

Data lake systems excel at scale. As your data assets multiply,
you need a way to discover what exists, control who can access it, audit how
it's being used, and coordinate writes across multiple engines. Data catalogs
have evolved to address exactly these needs, sitting above the storage layer
to manage the metadata, governance, and transactional bookkeeping that make
large-scale data lakes effective. The OSS Unity Catalog team has a [good
overview](https://unitycatalog.io/blogs/what-is-a-data-catalog-and-why-do-i-need-one/)
if you'd like to go deeper; the concepts apply broadly regardless of which
catalog you use.

### What is Unity Catalog?

Unity Catalog (UC for short) is an open standard for governing data and AI
assets, including tables, volumes, models, and functions, across engines and
clouds. It turns your data lake into a lakehouse, and gives you a single place
to discover, audit, and control access to your data, regardless of what's
reading or writing it. DuckDB's Unity Catalog extension is built upon the
[Unity Catalog Open API](https://go.unitycatalog.io/apidocs). There are two main
implementations: [OSS Unity Catalog](https://unitycatalog.io/), which you can
self-host (and Docker-ify in minutes), and [Databricks Unity
Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/),
the managed version. Like Delta, the DuckDB Unity Catalog extension has shed
its experimental tag. Let's put both to work.

### Getting Started: OSS Unity Catalog

We've set up a [Docker image playground bundling OSS Unity Catalog and DuckDB
together](https://github.com/benfleis/duckdb-unitycatalog-playground/),
so you can follow along with easy docker build-and-run setup. Grab it
if you would like to walk through the samples or experiment on your own. (If
you'd prefer to run OSS UC directly, the official image is the upstream of our
playground.)

Let's start with Docker. Assuming you now have the image running, it
already executed (roughly) the following steps in the build phase to prepare
our playground:

```bash
# Create a schema
/home/unitycatalog/bin/uc schema create --catalog unity --name my_schema

# Create the "pets" table
/home/unitycatalog/bin/uc table create \
    --full_name        unity.my_schema.pets \
    --columns          "uuid STRING, name STRING, age INT, adopted BOOLEAN" \
    --format           DELTA \
    --storage_location file:///home/unitycatalog/etc/data/external/unity/my_schema/tables/pets
```

After that, we can test things out from DuckDB. To see for
yourself, `docker exec -it duckdb-playground duckdb` will give you a DuckDB shell
inside the container.

Before doing anything meaningful we'll need to set up a DuckDB secret. In this
example the `TOKEN` value is ignored by local OSS UC server, but the field is
required. Create the secret, then you can immediately attach and read:

```sql
LOAD unity_catalog;

CREATE SECRET (
    TYPE     unity_catalog,
    TOKEN    'demo-ignored-token',
    ENDPOINT 'http://unitycatalog:8080'
);

ATTACH 'unity' AS my_catalog
    (TYPE unity_catalog, DEFAULT_SCHEMA 'my_schema');

SELECT name, age, adopted FROM my_catalog.pets ORDER BY name;
-- returns a single 'Seed' row
```

That's it! You just queried Unity-Catalog-managed, Delta-stored pets data.

> Tip Want to experiment with this on Databricks Unity Catalog? Setting up a
> Databricks Unity Catalog is out of scope for this blog, but if you have one
> ready to go, you will need these to get bootstrapped with DuckDB:
>
> - set `ENDPOINT` to [your Workspace
>   URL](https://docs.databricks.com/aws/en/workspace/workspace-details#workspace-instance-names-urls-and-ids)
>   (typically: https://{instance}.cloud.databricks.com/)
> - set `TOKEN` appropriately (e.g. [create a
>   PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat) with
>   `unity-catalog` scope); getting the correct token depends
>   entirely on your setup. To dive in, see [Access Control in Unity
>   Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/).
>
> With these in hand you can use DuckDB directly, or access
> the extensive [UC Open
> API](https://docs.databricks.com/api/workspace/introduction) directly.

Next, let's complete the circle and write some data into our pets table:

```sql
INSERT INTO my_catalog.pets
    (uuid, name, age, adopted)
SELECT
    gen_random_uuid()::VARCHAR,
    ['Luna', 'Milo', 'Bella', 'Charlie', 'Max', 'Lucy', 'Cooper',
     'Daisy', 'Buddy', 'Lily', 'Rocky', 'Molly', 'Bear', 'Lola',
     'Duke', 'Sadie', 'Tucker', 'Zoe', 'Oliver', 'Stella'
    ][1 + (random() * 19)::INT],
    (1 + (random() * 14)::INT)::INT,
    random() > 0.5
FROM range(10);

SELECT count() FROM my_catalog.pets;
```

You can also easily find and see the created files; check the local `data`
directory (also bind-mounted in Docker), and you should find both pre-existing
files, and a new Parquet file containing the inserted rows. In my case it looks
like this:

```batch
tree data
```

```text
data
└── external
    └── unity
        └── my_schema
            └── tables
                └── pets
                    ├── _delta_log
                    │   ├── 00000000000000000000.json
                    │   ├── 00000000000000000001.json
                    │   └── 00000000000000000002.json
                    ├── duckdb-19cb47ae-9f35-4126-b67d-c94fcade68cc.parquet
                    └── duckdb-e3bb0336-f16a-4d21-9495-0fbf55c6cba8.parquet

7 directories, 5 files
```

### Catalog Managed Tables

With the basics out of the way, we can talk about [Catalog Managed Tables
(CMT)](https://docs.databricks.com/aws/en/tables/managed). This is available
today in both [OSS](https://www.unitycatalog.io/) and
[Databricks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
Unity Catalog.

The big feature in CMT is Catalog Commits, which enables coordinated concurrent writes. Without Catalog Commits,
DuckDB writes go directly to the Delta log. While modern storage backends
prevent outright lost writes, UC is left out of the loop entirely. Its
metadata, audit trail, and statistics fall out of sync with the actual table
state, and other engines querying through UC may see a stale view.

Catalog Commits (CC) fixes this: every write is staged and registered through UC before it
becomes visible. UC acts as the commit arbiter, preserving first writer
commits, and sending a conflict error to later writers. This matters
wherever multiple writers are appending simultaneously, e.g., parallel ETL
pipelines, partitioned bulk loads, and concurrent analytical inserts. Each
writer works independently; UC ensures exactly one commit lands per version and
keeps its own catalog in sync with every one of them.

Consistent reads and audit history are already inherent to Delta and UC
respectively. CC doesn't add functionality, it just ensures UC stays in sync with
every commit. And Catalog Commits coordinate per table; there is no cross-table
atomicity. If you write to two tables in the same `BEGIN` / `COMMIT` block,
each table commits independently.

To opt a table into CMT (and therefore CC), set the `delta.feature.catalogManaged` table property
at creation time. This is done via Spark or the UC CLI, as DuckDB's Unity Catalog
extension does not yet support `CREATE TABLE` DDL:

```sql
-- Via Spark
CREATE TABLE my_catalog.my_schema.concurrent_tbl (
    uuid    STRING  NOT NULL,
    name    STRING  NOT NULL,
    age     INT     NOT NULL,
    adopted BOOLEAN NOT NULL
)
TBLPROPERTIES ('delta.feature.catalogManaged' = 'supported');
```

Once enabled, DuckDB writes go through UC's commit staging automatically —
the `INSERT` syntax is unchanged:

```sql
INSERT INTO my_catalog.my_schema.concurrent_tbl
    (uuid, name, age, adopted)
VALUES (gen_random_uuid()::VARCHAR, 'Luna', 3, true);
```

Now each DuckDB writer stages its commit to a `_staged_commits/` directory and
registers it with UC before that data becomes visible. UC arbitrates: exactly
one writer wins each version in a race, the others get a conflict error and can
retry. Next, let's look at how UC handles the race.

## Deeper Dive

### Racing Commits

To see how Catalog Commits arbitrates, we launched 20 concurrent DuckDB
writers, 8 at a time, all inserting into the same managed table:

```batch
seq 1 20 | xargs -P 8 -I{} scripts/unity/05-cmc/write-single {}
```

```text
[worker 6] OK - inserted 5 rows
[worker 5] CONFLICT - another writer won this version, retry needed
[worker 2] CONFLICT - another writer won this version, retry needed
[worker 8] CONFLICT - another writer won this version, retry needed
[worker 7] CONFLICT - another writer won this version, retry needed
[worker 3] CONFLICT - another writer won this version, retry needed
[worker 1] OK - inserted 5 rows
[worker 4] CONFLICT - another writer won this version, retry needed
[worker 16] OK - inserted 5 rows
[worker 13] CONFLICT - another writer won this version, retry needed
[worker 15] CONFLICT - another writer won this version, retry needed
[worker 11] CONFLICT - another writer won this version, retry needed
[worker 14] CONFLICT - another writer won this version, retry needed
[worker 12] OK - inserted 5 rows
[worker 9] CONFLICT - another writer won this version, retry needed
[worker 10] CONFLICT - another writer won this version, retry needed
[worker 17] CONFLICT - another writer won this version, retry needed
[worker 20] CONFLICT - another writer won this version, retry needed
[worker 18] OK - inserted 5 rows
[worker 19] CONFLICT - another writer won this version, retry needed
```

Here we see 5 successful writes, and 15 signaled conflicts. Let's confirm in
the data:

```sql
SELECT count() AS total_rows FROM my_catalog.my_schema.concurrent_tbl;
```

```text
┌────────────┐
│ total_rows │
│   int64    │
├────────────┤
│         35 │
└────────────┘
```

10 seeded rows + (5 writes × 5 rows each) = 35 total rows. (In a real workload,
you would retry the conflicted writes and land all 20 inserts.) Catalog Managed
Table commits gave us clear signal and semantics during highly concurrent
writes, as promised.

### Travel in Time, Faster

DuckDB's Delta snapshot loading is getting a speed boost: snapshots
will load incrementally when possible, making time travel across nearby
versions significantly faster. Consider a table where some initial queries are
made against version 16:

```sql
ATTACH './path/to/table' AS t (TYPE delta, VERSION 16);
SELECT count() FROM t;  -- → 17
```

And now some work needs to be done against version 20. If we peek under the
hood (warning: sneaky code follows), we'll see that none of the previously
loaded Delta log metadata files were re-loaded:

```sql
SET enable_logging = true;
SET delta_kernel_logging = true;
CALL enable_logging('DeltaKernel', level = 'trace');

ATTACH './path/to/table' AS t (TYPE delta, VERSION 20);
SELECT count() FROM t;  -- → 21

-- Delta kernel logs 'Provisionally selecting ... <version>.json'
-- whenever it reads a log file from scratch. We search for any such
-- message referencing a zero-padded log filename; zero matches
-- means the cached v16 snapshot was reused rather than rebuilt.
SELECT count() FROM duckdb_logs
WHERE type = 'DeltaKernel'
  AND message LIKE '%00000000000000000%.json%';
-- → 0
```

In Delta lakes with thousands or millions of snapshots, incremental loading
provides a big win when working across multiple versions.

> At time of writing, incremental snapshot loading is supported in nightly builds.
> You can install it using:
>
> ```sql
> FORCE INSTALL delta FROM core_nightly;
> ```
>
> Please be aware that nightly builds are not intended for production use.
> The implementation will be included in the next stable release,
> [v1.5.3]({% link release_calendar.md %}).

## Conclusions

A year ago, DuckDB could read Delta tables. Today it can insert data into them,
travel through their history, and query and write through a governed catalog —
without the experimental caveat on any of it. The combination of Delta for open
storage, Unity Catalog for governance and coordination, and DuckDB for fast
analytical queries is a stack you can build on.

There's more to come: DDL support to create and manage tables directly,
delete/update/merge support, and multi-table atomicity for writes that span
more than one table. In the meantime, the playground image linked above has
everything you need to kick the tires. As always, feedback and bug reports
are welcome on [GitHub](https://github.com/duckdb/duckdb-delta).
