---
layout: post
title: "From Precomputed Views to Ad Hoc SQL: How Spotify Uses DuckDB for Listening-History Queries"
authors:
  - Kian Mehrabani
  - John Kvarnefalk
  - Geertjan Wielenga
  - Tim Cox
thumb: "/images/blog/thumbs/spotify-listening-history.svg"
image: "/images/blog/thumbs/spotify-listening-history.png"
excerpt: "Spotify's personalization platform serves user-behavior data for hundreds of millions of listeners via precomputed materialized views. When agentic features required flexible, ad-hoc SQL access to individual listening histories, Spotify embedded DuckDB—choosing an in-process analytical engine that could query one listener's data (~1-2 GB) without building a separate backend service. For Spotify's internal teams, this dramatically accelerated experimentation."
tag: using-duckdb
---

Spotify's personalization platform is built around a fundamental insight: **understanding a listener's taste depends on their listening history**. The company serves this history to internal product teams via a platform of precomputed materialized views—over 300 of them—refreshed continuously and tuned for low latency (20–50 ms P99).

That architecture works well for known, precomputed questions. But when Spotify began investing in agentic features—where users can ask flexible, open-ended questions about their listening history—the old model broke down. An AI agent cannot predict every possible question a listener might ask. It needs flexible, ad-hoc SQL access to individual user histories.

The solution was unexpected: instead of building a centralized query backend, Spotify embedded DuckDB directly into their personalization service to run analytical queries in-process. This shifts the computational burden from a server to the user's request handler, and it works because—despite the aggregate scale being petabytes—a single listener's data is small enough to fit in memory.

## The Problem: Flexible Queries, Massive Scale

Spotify's listening-history infrastructure processes data for hundreds of millions of users. The aggregate dataset is on the order of petabytes. But here is the critical insight: **individual users are small**.

[John Kvarnefalk](https://www.linkedin.com/in/john-kvarnefalk/), a personalization engineer at Spotify, describes the operating model: **"We have hundreds of millions of tiny databases more or less."** A single user's listening history—even a heavy listener going back years—is roughly 1 to 2 GB.

The traditional solution was materialized views: precompute the queries downstream teams asked for, refresh them incrementally, and serve the precomputed results at request time. For Spotify's low-latency requirements and large user base, this made sense. Engineers write Java code, register it, the platform runs it periodically, and product teams query the results.

But this model assumes the questions are known in advance. Agentic features—like generating a playlist based on "what I listened to two years ago in the summer"—require a more flexible interface. An agent cannot know, when it starts, which specific queries it will need to run.

## Why an Embedded SQL Engine

Instead of building a separate analytical backend, Spotify considered embedded databases. [Kian Mehrabani](https://www.linkedin.com/in/kian-mehrabani/), a data engineer on the personalization team, explains the decision-making process:

**"We needed SQL or some kind of flexible query language for the agent. And we did think about SQLite, but I had been reading about DuckDB and had used it a little personally. I thought the ergonomics of DuckDB would work well for an early prototype, and I saw integrations with Java and compatibility with Arrow."**

DuckDB was chosen because:

1. **In-process execution:** No separate service; the query runs in the same Java process handling the user request.
2. **Rich integrations:** Apache Arrow support and JDBC driver made it compatible with Spotify's existing backend stack.
3. **SQL interface:** The vectorized analytical engine is built for complex historical queries, unlike SQLite's transactional model.
4. **Rapid prototyping:** The early proof of concept ran in Python; Spotify then integrated it into the Java/Kubernetes backend using JDBC.

## The Architecture: Protobuf to Arrow to DuckDB to SQL

When a request arrives for listening-history data, the flow is:

1. **Retrieve:** Spotify's personalization platform retrieves an individual user's history from Bigtable in Protocol Buffers (Protobuf) format.
2. **Convert:** The Protobufs are converted to Apache Arrow buffers in memory.
3. **Query:** DuckDB, embedded in the Java service and accessed via JDBC, executes SQL against the Arrow-backed data.
4. **Rewrite:** Apache Calcite parses and rewrites queries to support Spotify-specific table-valued functions and time-range selections.
5. **Return:** Query results are converted to JSON or text for downstream processing, including by agent tools.

This architecture avoids the overhead of a separate database service while providing the flexibility of SQL on individual user data.

## The Impact: Faster Experimentation

For Spotify's internal teams, the most significant benefit has been speed. John explains: **"It has unlocked faster experimentation and the validation speeds too."**

The workflow has changed from:
- Write Java code → register it → deploy it → wait → query the results

To:
- Write a SQL query → test it immediately → move to production views when ready

Kian adds: **"We're seeing an explosion of use. We've definitely seen more and more prototypes being built starting with the SQL-based system."** He notes that Spotify developers, including those using AI coding assistants like Claude, can now iterate on exploratory queries before deploying Java code.

This dual-layer approach—rapid SQL experimentation followed by materialized views for production—has become a pattern. Teams prototype with DuckDB, validate the idea quickly, and then productionize it in the established platform.

## Trade-offs and Technical Challenges

Running an embedded analytical engine inside a JVM-based microservice at scale presents genuine challenges:

- **Memory management:** Balancing memory between the Java heap, DuckDB's internal operations, and Arrow buffers in Kubernetes requires careful accounting.
- **Data conversion:** Converting from Protobuf to Arrow introduces copies that Kian identifies as a bottleneck. A potential optimization is native Java function integration to avoid extra copies.
- **Query rewriting:** Using Apache Calcite for dialect compatibility adds a layer. Kian notes friction from PostgreSQL-oriented dialect assumptions and would prefer direct access to DuckDB's abstract syntax tree (AST).
- **Observability:** Current profiling output is file-based JSON, which is cumbersome in a Java microservice. Real-time metrics integration would be more useful.

## Looking Ahead

Kian and John are exploring a unified model where validated SQL queries can be directly converted into materialized views without complete redevelopment. **"Everything is pretty nascent,"** Kian cautions. The agent strategy is still evolving, as is the broader integration of SQL into Spotify's personalization stack.

What is clear is that DuckDB filled a specific need: flexible, in-process analytical SQL for individual user histories without building a separate query backend.

## Learn More

* [DuckDB's Java API documentation](https://duckdb.org/docs/api/java.html)
* [Apache Arrow format](https://arrow.apache.org/)
* [Kian's DuckCon #7 presentation](https://www.youtube.com/watch?v=-9GY1CCJG5o) (June 2026)

We would like to thank Kian and John for the conversation. If you are using DuckDB and would like to share your story, reach out to us at [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).
