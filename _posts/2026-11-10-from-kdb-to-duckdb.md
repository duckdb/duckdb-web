---
layout: post
title: "From kdb+ to DuckDB: Bringing Local Analytics to the Quant's Desktop"
authors:
  - Ryan Hamilton in conversation with Geertjan Wielenga and Tim Cox
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
excerpt: "TL;DR: After years building kdb+-based data platforms for banks and hedge funds, Ryan Hamilton wanted an analytical engine he could recommend to smaller teams without specialized infrastructure or expensive licensing. DuckDB gave him a small, embedded way to bring fast local analytics into QStudio and Pulse, and it is now shaping his next open-source project, PeachQ."
tag: using-duckdb
---

> Quote I like the simplicity of just a small thing running and working. And then you can get more complex.
>
> -- Ryan Hamilton, founder, [TimeStored](https://www.timestored.com/)

## Fifteen Years of Heavyweight Infrastructure

For about fifteen years, [Ryan Hamilton](https://www.linkedin.com/in/ryananthonyhamilton/) has built large market-data platforms for banks and hedge funds. Most of that work was in [kdb+](https://kx.com/), integrated with real-time messaging systems such as [Solace](https://solace.com/). He built much of the platform at UBS and almost all of it at Citi, contributed to Morgan Stanley's, and most recently worked at a hedge fund.

His users are typically teams of 10 to 15 quants. They are deep specialists in finance who spend anywhere from a tenth to more than half their time on technology. Ryan's job has been to store their data efficiently so they can get on with their work. Sometimes he leads a team to do that. Sometimes he builds it himself. Sometimes he talks quants out of building infrastructure on their own.

## Problems That Didn't Need a Heavyweight Answer

Alongside that work, startups, smaller tech firms and smaller funds kept asking Ryan the same question: what should we run this on? For years he had no good answer.

kdb+ was the natural technical fit, but under the licensing model he encountered, he couldn't recommend it to a small firm. He told KX that a startup-friendly license would pay off, since a firm that can't pay half a million today might pay millions once it grows. He also tried the alternatives. [MonetDB](https://www.monetdb.org/) didn't give him the simple embedded option he was looking for. [ClickHouse](https://clickhouse.com/), which he persuaded one firm to deploy, was more operationally involved than he wanted at the time. For some clients, the honest answer was that he would write something in C for their narrow use case.

## A Different Starting Point

DuckDB was different. It was small, embedded, reliable and analytically capable, and a team could start with it inside an application without standing up a server.

**“I like the simplicity of just a small thing running and working,”** Ryan says. **“And then you can get more complex.”**

That let him give smaller firms a straight recommendation. DuckDB might not scale to everything, but it would run well and serve them for a long time. For roughly 90% of use cases, he reasoned, it would carry a team for years. By the time they outgrew it, they would understand their workload well enough to choose what came next. In many cases, DuckDB has expanded quickly enough that they never needed to move.

## QStudio: a Local Analytical Sandbox

The clearest illustration is [QStudio](https://www.timestored.com/qstudio/), the analytics IDE Ryan released about 13 years ago. It was originally built for kdb+ and now connects to around 15 databases. He leaves database administration to tools like [DBeaver](https://dbeaver.io/) and focuses QStudio on analytics and charting.

DuckDB was the first deep integration, and it changed how quants work with expensive queries. The workflow runs like this. An analyst runs a heavy query against a remote database. Some of these take up to 20 minutes. QStudio captures the result locally to Parquet through DuckDB:

```sql
COPY (
    ⟨expensive_remote_query⟩
) TO 'results/trades_2026-11-10.parquet' (FORMAT parquet);
```

The next day, the analyst queries that saved result directly, without rerunning the original workload:

```sql
SELECT
    symbol,
    avg(price) AS avg_price,
    sum(volume) AS total_volume
FROM 'results/trades_2026-11-10.parquet'
GROUP BY ALL
ORDER BY total_volume DESC;
```

The result is a personal sandbox where quants can build on their own earlier work. It proved popular, and Ryan found its performance close to kdb+.

Because QStudio is a Java Swing desktop application deployed inside banks, the integration depends on DuckDB's [Java client]({% link docs/current/clients/java/overview.md %}). Ryan's early version relied on hacky workarounds to get appending working. Once a dedicated Java developer joined and rebuilt the [Appender]({% link docs/current/clients/java/data_import.md %}) properly, every kink was ironed out:

```java
DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
try (var appender = conn.createAppender(DuckDBConnection.DEFAULT_SCHEMA, "trades")) {
    appender.beginRow();
    appender.append("DUCK");
    appender.append(42.0);
    appender.append(1_000);
    appender.endRow();
}
```

**“It just worked,”** Ryan says, **“which is the highest praise I would give any engineering thing.”**

That experience became the basis of his DuckCon talk. His argument was that an open-source engine already beat a far more exotic and expensive stack in some areas. DuckDB has moved well ahead since then.

## Pulse: DuckDB by Default

QStudio never made much money directly, but it got a very small company onto the approved-vendor lists of some very large firms, which is hard for small vendors to do. When TimeStored launched [Pulse](https://www.timestored.com/pulse/), a real-time HTML visualization tool that is now Ryan's main product, that path into large firms already existed.

Ryan reached for DuckDB again. Pulse uses it to snapshot and cache data. What began as an integration experiment had become a repeated TimeStored architecture pattern. DuckDB sits in the embedded storage and query layer, and increasingly supports AI-assisted data exploration. Excel exports and similar user-facing features stay in the application's UI. That is partly to keep styling intact, and partly because bank users often can't install extensions at all.

## PeachQ: Back to q

Ryan's newest project is [PeachQ](https://peachq.org/), an open-source implementation of the q language. Ryan loves q as a language but thinks DuckDB is ahead as a database, so PeachQ separates the two.

The first release focuses on q compatibility and runs on the RayForce in-memory engine. DuckDB-backed storage is aimed at version two, which is still taking shape. That is where Ryan's recent work on C extensions is heading, along with experiments with newer formats such as [Vortex]({% link docs/current/core_extensions/vortex.md %}) and custom table formats. He credits DuckDB's [extension API]({% link docs/current/extensions/overview.md %}) with letting people add features cleanly, unlike the fragile workarounds he and others once built into closed systems. Often, he notes, DuckDB later builds those features itself.

## Further Reading

Ryan's DuckCon talk gives a short tour of this work.

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/viMXP_TG6tU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

You can explore QStudio, now open source, and try PeachQ at peachq.org.

We would like to thank Ryan for the conversation. You can follow his work on DuckDB, q and TimeStored at [timestored.com](https://www.timestored.com/). And if you are reading this, are using DuckDB, and would like to share your story, drop us a line at [quack@duckdb.org](mailto:quack@duckdb.org).
