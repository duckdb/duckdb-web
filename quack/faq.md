---
layout: default
title: Frequently Asked Questions for Quack
body_class: faq
toc: false
---

<!-- ################################################################################# -->
<!-- ################################################################################# -->
<!-- ################################################################################# -->

<div class="wrap pagetitle">
  <h1>FAQ for Quack</h1>
</div>

## Overview

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What is Quack?

<div class="answer" markdown="1">

Quack allows DuckDB to connect to a DuckDB server through the `quack:` protocol. You can think of Quack as a Remote Procedure Call (RPC) protocol for DuckDB. Quack enables DuckDB instances to talk to each other, effectively turning DuckDB into a client-server database management system, where both the client and the server are DuckDB instances.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Why is it called Quack?

<div class="answer" markdown="1">

Mallard ducks communicate by [quacking](https://en.wikipedia.org/wiki/Duck#Communication), so it's only fair that DuckDB instances communicate through the protocol `quack`.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### When should I use Quack?

<div class="answer" markdown="1">

Quack can be beneficial in a number of scenarios, including the following:

* You need concurrent read-write access to the same DuckDB database.
* Your data is on a server and you want to move the computation as close to the data as possible.
* You have a powerful server that can process the data but would like to see the results on your local computer.
* And many more – we are excited to see what the community comes up with.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Can I use DuckDB with Quack for transactional (OLTP) workloads?

<div class="answer" markdown="1">

Yes. DuckDB with Quack can handle a few thousand writes per second on a server with 8 CPUs and 32 GB RAM. See [the benchmarks in our announcement blog post](https://duckdb.org/2026/05/12/quack-remote-protocol).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Can I still run DuckDB as an in-process database?

<div class="answer" markdown="1">

Yes, DuckDB as an in-process database will continue working just as it did before, and we will treat the in-process deployment model as a first-class citizen in the DuckDB ecosystem.

</div>

</div>

## Using Quack

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How do I get started with using Quack?

<div class="answer" markdown="1">

Please follow the [installation instructions](https://duckdb.org/quack) and the [documentation](https://duckdb.org/docs/current/quack/overview).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How does Quack work?

<div class="answer" markdown="1">

Quack uses HTTP v2.0 for communication. This allows Quack to work in environments with firewalls, load balancers, etc. You can provide your own encryption – see the [“Reserve Proxy” guide]({% link docs/current/quack/setup/reverse_proxy.md %}).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Can I already use Quack?

<div class="answer" markdown="1">

Yes, Quack is available in DuckDB v1.5.2 as a beta release. To install and load it, run:

```sql
INSTALL quack FROM core_nightly;
LOAD quack;
```

</div>

</div>

## Features

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is the Quack protocol fast?

<div class="answer" markdown="1">

Yes, we designed Quack to be a high-performance protocol for both bulk operations and small changes. We worked on minimizing the number of round-trips required. See [the benchmarks in our announcement blog post](https://duckdb.org/2026/05/12/quack-remote-protocol).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How to set up a secure Quack server?

<div class="answer" markdown="1">

Please consult the Quack documentation's [Security](https://duckdb.org/docs/current/quack/security) page and the [Securing Quack with a Reverse Proxy](http://duckdb.org/docs/current/quack/setup/reverse_proxy) page.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Does Quack support the full DuckDB SQL dialect?

<div class="answer" markdown="1">

Yes. By default, you can use all SQL features of the remote DuckDB server. It is possible to limit these features using custom authorization functions.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Does DuckDB with Quack support distributed query processing?

<div class="answer" markdown="1">

Currently, DuckDB with Quack does not support distributed query processing.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### I have a production use case that requires feature X in Quack. How do I proceed?

<div class="answer" markdown="1">

Please consult the DuckDB FAQ's [“I would like feature X to be implemented in DuckDB. How do I proceed?”](https://duckdb.org/faq#i-would-like-feature-x-to-be-implemented-in-duckdb-how-do-i-proceed) entry. If you think a feature is missing from Quack, please [start a new discussion in the main DuckDB repository](https://github.com/duckdb/duckdb/discussions/new/choose).

</div>

</div>

## Development

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Is Quack production-ready?

<div class="answer" markdown="1">

Not yet. Quack is currently in a beta state. You can use Quack for prototyping but it is still in development, and breaking changes are expected to happen. These may include the protocol, function names and default settings. We expect Quack to mature over the next few months and plan to release it as a stable protocol as part of [DuckDB v2.0](https://duckdb.org/release_calendar) in September 2026\.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### How can I contribute to Quack?

<div class="answer" markdown="1">

The code is available in the [`duckdb-quack` repository](https://github.com/duckdb/duckdb-quack). You are welcome to open issues and propose new features through a [discussion in the main DuckDB repository](https://github.com/duckdb/duckdb/discussions/new/choose).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### I found a bug in Quack. Where do I report it?

<div class="answer" markdown="1">

Please [submit an issue in the `duckdb-quack` repository](https://github.com/duckdb/duckdb-quack/issues/new).

</div>

</div>

## Quack in the DuckDB Ecosystem

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What's the relation of Quack to third-party solutions for remotely accessing DuckDB?

<div class="answer" markdown="1">

There are several third-party solutions providing remote access to DuckDB (e.g., the [airport extension](https://duckdb.org/community_extensions/extensions/airport) and [GizmoSQL](https://github.com/gizmodata/gizmosql) using the [Arrow Flight Protocol](https://arrow.apache.org/docs/format/Flight.html)). Quack is a clean slate implementation from the core DuckDB team. Quack, in the spirit of the DuckDB project, does not have any third-party dependencies.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What is the relationship between Quack and DuckLake?

<div class="answer" markdown="1">

Quack is a remote protocol for DuckDB that enables client-server use of DuckDB. DuckLake is an open lakehouse format supported by different data management systems, including DuckDB itself but also Apache Spark, Apache DataFusion and Trino.

Quack and DuckLake share a few similarities:

* Both are available in DuckDB as an extension.
* Both of them unlock the “multiplayer DuckDB” experience by allowing multiple writers to access the same database.

However, Quack and DuckLake are also fundamentally different.

**Relation to DuckDB:**
  * Quack is exclusive to DuckDB as it allows DuckDB processes to communicate. 
  * The DuckLake format is not exclusive to DuckDB: DuckLakes can be [created, read and updated via different clients](https://ducklake.select/docs/stable/#list-of-ducklake-clients).
* **Storage:**
  * Quack allows you to run a DuckDB server that uses DuckDB's native database format for storage. This allows you to scale up to a few terabytes.
  * DuckLake stores the data on object storage, which allows it to store huge, potentially petabyte-scale datasets.
* **Setup:**
  * The setup of Quack only requires installing the Quack extension on both the client and the server.
  * DuckLake requires a central catalog database. A typical DuckLake setup includes object storage (where the data is stored in Parquet format) and a catalog database.

Quack and DuckLake can be combined in different combinations. For example, if you have a huge database or need time travel capabilities, consider using DuckLake as that is served through a DuckDB instance through Quack.

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### Can I use DuckDB with Quack as the catalog database for DuckLake?

<div class="answer" markdown="1">

Yes, we have [experimental support for using DuckDB with Quack as a catalog database](https://github.com/duckdb/ducklake/pull/1151).

</div>

</div>

<!-- ----- ----- ----- ----- ----- ----- Q&A entry ----- ----- ----- ----- ----- ----- -->

<div class="qa-wrap" markdown="1">

### What is the relationship between Quack and MotherDuck?

<div class="answer" markdown="1">

Quack is a protocol that allows remote access to a DuckDB server. It's an MIT-licensed open-source solution that you can run in a self-hosted environment or in the cloud.

MotherDuck provides a fully managed database-as-a-service in the cloud. As such, it also allows remote access among other features of a managed database (central user management, backups, etc.) and other advanced features such as [dual execution](https://motherduck.com/docs/key-tasks/running-hybrid-queries/) (a feature that is currently not supported by Quack).
MotherDuck uses DuckDB both on the client side and on the server side but it employs its own protocol for communication.
When building Quack, [we incorporated lessons from the MotherDuck team learned](http://duckdb.org/2026/05/12/quack-remote-protocol#acknowledgements) into building our protocol.
To learn about MotherDuck's plans with Quack, check out the “Quacking On” section of the [their blog post on Quack](https://motherduck.com/blog/duckdb-client-server/#quacking-on)

</div>

</div>
