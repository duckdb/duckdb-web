---
layout: post
title: "How JetBrains Built Cross-Database Queries into DataGrip with DuckDB"
authors:
  - Ilia Epelbaum in conversation with Geertjan Wielenga and Tim Cox
thumb: "/images/blog/thumbs/jetbrains-datagrip.svg"
image: "/images/blog/thumbs/jetbrains-datagrip.png"
excerpt: "JetBrains users had long asked to join data across different database connections in a single query. Rather than build its own cross-database query engine, JetBrains embedded DuckDB in DataGrip, using DuckDB's custom table functions to connect it to the IDE's existing query execution. This is why DuckDB won out over the alternatives, and where the integration goes next."
tag: using-duckdb
---

When [JetBrains](https://www.jetbrains.com/) set out to let developers join data across different database connections in a single query, it chose not to build its own cross-database query engine. Instead, [DataGrip](https://www.jetbrains.com/datagrip/), its database IDE, embeds DuckDB to execute those queries, and exposes DuckDB's SQL dialect directly to the developers writing them.

> Quote DuckDB turned out to be the simplest option to integrate.
>
> -- Ilia Epelbaum, DataGrip, JetBrains

## Querying Across Data Sources

DataGrip is JetBrains' IDE for working with databases and writing SQL, developed since 2015. The same database functionality is also available as a plugin inside the other JetBrains IDEs, so the feature reaches well beyond DataGrip itself.

For a long time, users had been asking for one thing in particular: the ability to run a single query across more than one data source. The most common request was to join data from different database connections in one query. DataGrip could already execute queries against each connection, but nothing tied the results together, so the team needed an engine that could.

## Choosing DuckDB over Building Its Own

JetBrains explored several approaches. It considered [Apache Calcite](https://calcite.apache.org/), handling the queries itself using PSI (the internal code representation JetBrains uses across its IDEs), and DuckDB.

DuckDB won on ease of integration. **"DuckDB turned out to be the simplest option to integrate,"** says Ilia Epelbaum, who works on the DataGrip team. The deciding feature was the ability to register a custom table function: it gave JetBrains a straightforward way to connect DuckDB to the query-execution functionality DataGrip already had. DuckDB was also preferred over lighter alternatives such as H2 because it brought more capabilities, including query optimizations like projection pushdown.

Maxim Sobolevskiy, Head of Database Ecosystem at JetBrains, puts the result in concrete terms. **"With DuckDB and its support for custom table functions, cross-database queries have finally become practical in DataGrip,"** he says. **"Users can join data from PostgreSQL, MySQL, MongoDB, or any other supported database in one query, without setting up extra infrastructure."** The embedded alternatives the team evaluated could not do this, because **"extending them required either native code or a complicated implementation."**

Epelbaum came to the project knowing the territory. He had been a database developer working on [Trino](https://trino.io/) before moving into database tooling, and already knew how flexible DuckDB was. That background is part of why the team reached for it rather than writing and maintaining a cross-database query engine of its own.

## DuckDB in Plain Sight

Developers know DuckDB is there. Because a cross-source join runs through a DuckDB table function, the query itself is written in DuckDB's SQL dialect, and DataGrip tells developers so. **"We highlight that it's DuckDB,"** Epelbaum says, so that someone writing a join across connections knows they are writing a DuckDB query.

JetBrains has gone further and supports DuckDB as a first-class dialect in its own right, not only as the engine behind cross-source joins. Epelbaum contributed syntax highlighting for DuckDB, including the syntax introduced in [DuckDB 2.0]({% post_url 2026-10-21-announcing-duckdb-200 %}).

## An Initial Solution, Still Evolving

This is still a first version. **"We've built the initial solution, and we want to see how users actually use it in practice,"** Epelbaum says. Only after that does it plan to layer on more of DuckDB's optimizations.

Two directions are on the roadmap. The first is to take fuller advantage of DuckDB's query optimizations. The second is to use DuckDB for file-based data sources, reading files the way it already reads across connections. Epelbaum also singled out DuckDB's [friendly SQL]({% link docs/2.0/sql/dialect/friendly_sql.md %}) as something the team values in day-to-day use.

For now, DuckDB sits at the core of a feature that JetBrains users had wanted for years, letting them join across their databases without JetBrains having to become a query-engine vendor to make it happen.

## About JetBrains and DataGrip

JetBrains builds professional developer tools, including IntelliJ IDEA, PyCharm, and the Kotlin language, that have served millions of programmers for more than 20 years. [DataGrip](https://www.jetbrains.com/datagrip/), its database IDE, helps developers and data engineers query, explore, and manage multiple databases from a single environment.
