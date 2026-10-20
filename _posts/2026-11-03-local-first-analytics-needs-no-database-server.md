---
layout: post
title: "Local-First Analytics Needs No Database Server"
authors:
  - Ilya Boyandin in conversation with Geertjan Wielenga & Tim Cox
thumb: "/images/blog/thumbs/spatial-joins.svg"
image: "/images/blog/thumbs/spatial-joins.png"
excerpt: "Ilya Boyandin first used DuckDB in a geospatial side project that analyzed data in the browser with no database backend. He later turned that setup into SQLRooms, an open-source framework for local-first analytical applications, and Foursquare's Spatial Desktop is the largest application built on it so far."
tag: using-duckdb
---

TL;DR: Ilya Boyandin first used DuckDB in a geospatial side project that analyzed data in the browser with no database backend. He later turned that setup into [SQLRooms](https://sqlrooms.org), an open-source framework for local-first analytical applications. Foursquare's Spatial Desktop is the largest application built on it so far.

[Ilya Boyandin](https://www.linkedin.com/in/ilyabo/) is a software engineer and the creator of SQLRooms. He has a PhD in geospatial data visualization. He worked on urban mobility analytics at Teralytics before joining Unfolded, the company behind the open-source projects [deck.gl](https://deck.gl) and [kepler.gl](https://kepler.gl). Foursquare later acquired Unfolded, and he has worked there since.

## How DuckDB Entered the Picture

At Teralytics, Ilya's team used ClickHouse. Like DuckDB, it is columnar and built for analytics, but it usually runs on provisioned servers in a cluster. **“ClickHouse can be used locally, but it's not really meant for that, unlike DuckDB.”**

He first used DuckDB in [Flowmap.city](https://www.flowmap.city/), a side project for [visualizing mobility flows](https://ilya.boyandin.me/p/flowmap-city) that he still maintains. He had little budget for infrastructure, and DuckDB already had a [WebAssembly build]({% link docs/current/clients/wasm/overview.md %}) that runs in the browser. In Flowmap.city, users upload files to object storage, which is cheap or often free. When someone opens a project, DuckDB-Wasm starts in the browser and loads the files from the bucket over the [`s3://`]({% link docs/current/core_extensions/httpfs/s3api.md %}) protocol:

```sql
SELECT *
FROM 's3://⟨bucket⟩/⟨project⟩/flows.parquet';
```

**“They can do all the analytics and visualization in the browser,”** Ilya says, **“which is very convenient and has very low requirements on the infrastructure.”**

Flowmap.city showed him that an analytical application could work with no database server behind it.

## From a Side Project to SQLRooms

For Flowmap.city, Ilya had built a table view, a SQL editor, a schema tree and query execution in the browser. None of it was specific to mobility data. He extracted these pieces into a standalone framework called [SQLRooms](https://ilya.boyandin.me/p/sqlrooms), which he continues to develop as open source.

SQLRooms is a set of building blocks for creating DuckDB-backed analytics applications in React. Developers combine only the packages and state slices their app needs. At its center is the Room, a self-contained workspace that holds the data along with the analysis done on it. Each Room is connected to its own DuckDB instance, running natively on a device or as WebAssembly in a browser. The framework's DuckDB wrapper handles file loading, so data can be queried as soon as it is added. All computation happens on the user's own machine, whether that is a browser tab or a desktop app. The framework also has built-in support for AI agents that write and run SQL.

The quickest way in is the [minimal example](https://sqlrooms.org/examples), a small Vite and React app that loads a CSV file and runs SQL queries against it:

```sql
SELECT *
FROM 'sales.csv'
LIMIT 10;
```

Developers outside Foursquare have built on the framework as well. Amar Harolikar customized SQLRooms to analyze an 11-million-row, 1.6 GB CSV file in natural language, entirely in the browser. [Cosmograph](https://ilya.boyandin.me/p/cosmograph), a tool for visualizing large network graphs and machine learning embeddings built by Nikita Rokotyan and his team, is another application built on the framework.

Ilya's interest in local-first software shaped the framework. **“You should own your data. It should live on your computer, not in the Cloud. It can be synced via the cloud, but you decide when to keep it local and when not.”**

## One Database File, One Analytical Project

In SQLRooms applications, DuckDB can store the project along with the data. In Spatial Desktop, **“the project file you create is actually a DuckDB database file, in which we store both the data users add to the project and all the artifacts they create within it.”** Opening a project is a single `ATTACH`:

```sql
ATTACH 'project.duckdb';
```

A whole project then lives in one file that a user can move around like any other document. Ilya's current work on SQLRooms builds on this idea (see below).

## Putting SQLRooms to Work at Foursquare

The largest application built on SQLRooms so far is [Foursquare Spatial Desktop](https://ilya.boyandin.me/p/fsq-spatial-desktop), a free desktop application for visualizing geospatial data. Anyone can register and use it with their own data. Only the embedded AI agent is paid. Foursquare also uses SQLRooms for internal analysis tools.

Spatial Desktop followed kepler.gl, the free client-only tool, and Foursquare Studio, the commercial version hosted in the cloud. It was the first of these to use DuckDB, which Ilya proposed. **“For this particular product, I think DuckDB was just a perfect fit,”** he says. **“I wouldn't say we considered alternatives.”** SQLite is embeddable too, he says, but it is not column-oriented and was not designed for analytics on larger datasets.

DuckDB ships with the application, so users install nothing extra. Ilya acknowledges that a desktop application makes it harder to share projects and edit them together. In exchange, queries don't wait on the network and the data stays on the user's machine. Foursquare also has no database servers to run. Modern laptops are powerful, he adds, and their GPUs are good at visualization. **“There is a bit of a resurrection of desktop applications right now.”**

Foursquare also has a browser version of its geospatial agent that reads data through [MotherDuck]({% link docs/current/core_extensions/motherduck.md %}). Since MotherDuck is DuckDB in the cloud, the team reuses most of the agent's instructions for generating SQL.

## When the Agent Writes the SQL

Work on Spatial Desktop started around the time AI agents became usable. **“This combination of SQL and AI agents is actually quite powerful,”** Ilya says. **“SQL has such a long history, so many documents on the web explaining how to use it, and LLMs are pretty good at generating it.”** Users ask a question and the agent writes and runs the DuckDB queries, so they don't need to know SQL.

The interface changed as a result. **“In the very first version the SQL editor was very prominent in the app. Then we started doing more with the agent, and now it's hidden by default.”** The queries are still there. Users can open them to check what the agent did, and they can also write their own.

## Geospatial Processing on the Fly

Spatial Desktop has been tested with datasets from tens of thousands of points up to several gigabytes. It renders maps with deck.gl, which slows down once a map holds hundreds of thousands of objects. The team got around this with dynamic tiling built on DuckDB's [spatial extension]({% link docs/current/core_extensions/spatial/overview.md %}).

Web maps usually load pre-generated tiles for the area in view at the current zoom level. Spatial Desktop generates those tiles at query time instead. A query filters the features to the viewport. As the user zooms out, it simplifies polygons, and it samples the data where needed. The spatial extension's [`ST_AsMVT`]({% link docs/current/core_extensions/spatial/functions.md %}#st_asmvt) function then encodes the result as a binary tile in MVT, a widely supported format:

```sql
INSTALL spatial;
LOAD spatial;

SELECT ST_AsMVT({
    'geometry': ST_AsMVTGeom(
        geometry,
        ST_Extent(ST_TileEnvelope(⟨z⟩, ⟨x⟩, ⟨y⟩)),
        4096,
        256,
        false
    ),
    'id': id
}) AS tile
FROM features
WHERE ST_Intersects(geometry, ST_TileEnvelope(⟨z⟩, ⟨x⟩, ⟨y⟩));
```

Ilya says this lets the app **“show even more data than deck.gl can render at once.”**

## Where SQLRooms Goes Next

The project file in Spatial Desktop points to a broader idea that Ilya is developing in SQLRooms, where the DuckDB file carries the analysis as well as the data. He is building a Canvas module with SQL query cells and Vega-Lite chart cells, alongside a Notebooks module. An engine underneath tracks how cells depend on each other and reruns downstream cells when the data changes.

He is also adding real-time collaboration based on the [Loro CRDT](https://loro.dev/) library. Because DuckDB treats the data as read-only, only the interface state needs to be synchronized between collaborators. That state can itself be stored in DuckDB, either on a shared server or on a local machine for offline work.

At [DuckCon #7]({% link _events/2026-06-24-duckcon7.html %}) in Amsterdam, Ilya showed a SQLRooms command-line tool that works with a DuckDB database and presents the analysis in a notebook-like style. The direction is a single DuckDB file that holds an entire analytical workspace, which someone can open elsewhere and continue. The design is still changing.

## Watch the DuckCon Talk

Ilya's five-minute talk from DuckCon #7 gives a short tour of this direction.

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/fV1LXnPl4ng" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

SQLRooms is open source and available at [sqlrooms.org](https://sqlrooms.org), where the example apps are a good place to start. [Flowmap.city](https://www.flowmap.city/) and [Foursquare Spatial Desktop](https://location.foursquare.com/products/spatial/) are free to try.

We would like to thank Ilya for the conversation. You can follow his writing on DuckDB and SQLRooms on [his blog](https://ilya.boyandin.me/). And if you are reading this, are using DuckDB, and would like to share your story, drop us a line at [quack@duckdb.org](mailto:quack@duckdb.org).
