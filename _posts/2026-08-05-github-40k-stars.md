---
layout: post
title: "Thank You for 40&nbsp;000 Stars on GitHub"
author: The DuckDB team
thumb: "/images/blog/thumbs/github-40k-stars.svg"
image: "/images/blog/thumbs/github-40k-stars.jpg"
tags: ["release"]
excerpt: "DuckDB just reached 40&nbsp;000 stars on GitHub! Here's what happened since the last 10&nbsp;000-star milestone."
---

The [`duckdb/duckdb` GitHub repository](https://github.com/duckdb/duckdb) has just passed 40&nbsp;000 stars!

![Star history]({% link images/blog/star-history-20260805-dark.png %}){: .darkmode-img }
![Star history]({% link images/blog/star-history-20260805-light.png %}){: .lightmode-img }

We’d like to use this milestone to stop for a moment and revisit recent developments in the DuckStack ecosystem since last summer (2025), when we surpassed [30 000 stars](https://duckdb.org/2025/06/06/github-30k-stars).

## Releases

* Since the last milestone, the DuckLabs team has released [DuckDB 1.4.0](https://duckdb.org/2025/09/16/announcing-duckdb-140), our first long-term support release, and [DuckDB 1.5.0](https://duckdb.org/2026/03/09/announcing-duckdb-150). Both releases are packed with many new features, performance optimizations, and bugfixes.
* The DuckLabs team also published the [DuckLake 1.0](https://ducklake.select/2026/04/13/ducklake-10/) standard, our production-ready format for SQL-as-a-lakehouse.
* Finally, we released [the Quack remote protocol](https://duckdb.org/2026/05/12/quack-remote-protocol), which lets you run DuckDB in a client-server setup with multiple concurrent writers. That’s right: DuckDB instances can now talk to each other!

## Community Metrics

Besides the GitHub stars, the DuckDB community has also experienced a lot of growth in other metrics:

* Each month, `duckdb.org` receives traffic from over 8 million unique visitors – more than double last summer’s numbers. We also see over 2 PB (!) in traffic from millions of extension downloads. [Thanks again to Cloudflare](https://duckdb.foundation/#technical-sponsors) for sponsoring the project.
* DuckDB now has [50M+ monthly downloads in PyPI](https://pypistats.org/packages/duckdb), more than double the 20M we reported last time.

*(As usual, we’d like to emphasize that while we’re happy to see these metrics grow, we are not glorifying them and they are not a target per se in accordance with [Goodhart’s law](https://en.wikipedia.org/wiki/Goodhart%27s_law).)*

## Events

Since 30 000 stars, we ran DuckDB meetups in [Amsterdam](https://duckdb.org/events/2025/09/17/duckdb-amsterdam-meetup-3/), [Berlin](https://duckdb.org/events/2025/06/26/duckdb-berlin-meetup/), and [London](https://duckdb.org/events/2025/09/04/duckdb-science-and-education-london-meetup/). We also hosted a [Developer Meeting](https://duckdb.org/events/2026/01/30/duckdb-developer-meeting-1/) focused on DuckDB internals and extension development. 

Finally, we hosted [DuckCon #7](https://duckdb.org/events/2026/06/24/duckcon7/), our largest DuckCon so far, which we also streamed online. These events allowed us to connect with our community of engineers, builders, and scientists, and learn about the many ways they are using DuckDB.

Next up, we'll host the [DuckDB Paris meetup](https://luma.com/p9n5hkvf) with [Altertable](https://altertable.ai/) and we are setting up a
[meetup in Boston]({% link _events/2026-09-03-duckdb-boston-meetup.md %}).
Stay tuned!

## DuckDB in the Wild

Here are just a few of the projects, extensions, and announcements that happened in the DuckDB community since the last 10 000-star milestone:

* **Blog:** Petrica Leuca shows you [how to use DuckDB for keyword, full-text, and semantic similarity search](https://duckdb.org/2025/06/13/text-analytics) with embeddings for lightweight text analytics.
* **Video:** GizmoEdge: [A distributed DuckDB engine for IoT](https://www.youtube.com/watch?v=xlvjN_eFJvM) (from the first DuckDB Developer Meeting) by Philip Moore.
* **Blog:** [DuckDB for streaming analytics?](https://duckdb.org/2025/10/13/duckdb-streaming-patterns) Yes, says Guillermo Sanchez, you can use DuckDB to refresh your data at near real-time speed.
* **Use Case Walkthrough:** Uncovering [Financial Crime with DuckDB and SQL/PGQ](https://duckdb.org/2025/10/22/duckdb-graph-queries-duckpgq) graph syntax that's part of SQL:2023 by Daniël ten Wolde.
* **For Fun:** DuckDB co-creator Hannes Mühleisen shows you [how to store and even process video in DuckDB](https://duckdb.org/2025/10/27/movies-in-databases).
* **Blog:** [Iceberg in the Browser](https://duckdb.org/2025/12/16/iceberg-in-the-browser): learn how to read and write tables in Iceberg catalogs without needing to manage any infrastructure – directly from your browser!
* **Presentation:** Denis Hirn from University of Tübingen introduces you to DuckPL: [A procedural language in DuckDB](https://www.youtube.com/watch?v=cjmtEBz_hSc).
* **Hardware benchmarks:** Hannes Mühleisen tests [DuckDB on a Loongson CPU](https://duckdb.org/2026/01/06/duckdb-on-loongarch-morefine) and Gábor Szárnyas put [DuckDB to work on a MacBook Neo](https://duckdb.org/2026/03/11/big-data-on-the-cheapest-macbook).
* **Video:** Barry Smart walks you through 20 years of wind data while [auditing UK energy policy without a cluster](https://www.youtube.com/watch?v=7dUEgMLuUcI) (DuckCon).
* **Blog:** Interested in [building DuckDB extensions in C#](https://duckdb.org/2026/03/20/duckdb-extensionkit-csharp)? Giorgi Dalakishvili shows you how to build DuckDB extensions in C# with DuckDB.ExtensionKit.
* **Talk:** Kian Mehrabani takes you on a tour of [how Spotify is using DuckDB](https://www.youtube.com/watch?v=-9GY1CCJG5o) as a SQL layer over user listening history in this video from DuckCon.
* **Preview:** In DuckDB v2.0, scheduled for fall 2026, DuckDB will support async reads of Parquet and CSV files. Pedro Holanda walks you through the details of [asynchronous I/O](https://duckdb.org/2026/07/31/asynchronous-io).

## Closing Thoughts

We would like to extend a heartfelt **thank you** to the DuckDB community of users and contributors. We look forward to growing the community around the “DuckStack” and hope the GitHub stars follow. We'll report back when we reach 50 000 stars.
