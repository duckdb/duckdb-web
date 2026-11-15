---
layout: post
title: Local Analytics Doesn’t Need a Database Server
authors:
  - Ilya Boyandin
  - Geertjan Wielenga
  - Tim Cox
thumb: /images/blog/thumbs/local-analytics-without-a-database-server.svg
image: /images/blog/thumbs/local-analytics-without-a-database-server.png
excerpt: From interactive maps to graph exploration, DuckDB makes it possible to analyze data without a database server. Ilya Boyandin shares how this approach led to SQLRooms, a toolkit for building analytics applications that bring data, visualizations, and AI-assisted analysis together on the user’s machine.
tag: case-study
---

> Quote
>
> You should own your data. It can live on your computer, not everything has to live in the Cloud. It can be synced via the cloud, but you decide when to keep it local and when not.
>
> — Ilya Boyandin, creator of [SQLRooms](https://sqlrooms.org)
{: .quote-large}

[Ilya Boyandin](https://www.linkedin.com/in/ilyabo/) is a software engineer, the creator of [SQLRooms](https://sqlrooms.org), [FlowmapBlue](https://flowmap.blue), and [Flowmap City](https://flowmap.city/). He worked on geospatial data analytics at Unfolded, the company founded by the team behind the open-source data visualization projects [deck.gl](https://deck.gl) and [kepler.gl](https://kepler.gl), which was later acquired by Foursquare.

## How DuckDB Entered the Picture

Ilya first used DuckDB in [Flowmap City](https://flowmap.city/), a side project for [visualizing mobility flows](https://ilya.boyandin.me/p/flowmap-city) that he still maintains.
Working with a small budget, Ilya wanted to keep Flowmap City easy to operate with minimal infrastructure. DuckDB’s [WebAssembly build]({% link docs/2.0/clients/wasm/overview.md %}) lets the app run analytical queries in the user’s browser without a database server. Uploaded datasets are stored as Parquet files in S3. When someone opens a project, the app loads the data into DuckDB-Wasm through [presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html).

As users pan, zoom, or change filters in Flowmap City, DuckDB-Wasm runs SQL queries in the browser to update the map. A single interaction can trigger a number of queries preparing the data for the current viewport:

<div class="video-container">
<video src="https://blobs.duckdb.org/videos/flowmap-city.mp4" controls muted loop playsinline></video>
</div>

Ilya explains: **“We can now do much of the analysis and visualization in the browser. This keeps infrastructure requirements low and can be faster because queries don’t need a round trip to the server.”**

## From a Side Project to SQLRooms

Much of Flowmap City’s data-loading and interface code was useful beyond mobility analysis. Ilya extracted those pieces into SQLRooms, which he continues to develop as an open-source project.

[SQLRooms](https://sqlrooms.org/) is a modular toolkit for building DuckDB-powered analytics applications in React. It provides building blocks for loading data, writing SQL, displaying tables, creating visualizations, and integrating AI assistants. Developers can combine these pieces with their own components.

These components work together within a _Room_: a workspace containing datasets, analysis artifacts such as saved queries, charts, maps, and documents, and the application state that connects them. SQLRooms handles query execution through a shared DuckDB connection, so developers can focus on how users explore their data and build on their work.

DuckDB can run directly in the browser through WebAssembly or natively on the user’s machine in a desktop application, allowing data analysis without a remote database server.

Ilya’s interest in local-first software shaped the framework. **“You should own your data. It can live on your computer, not everything has to live in the Cloud. It can be synced via the cloud, but you decide when to keep it local and when not.”**

## Putting SQLRooms to Work at Foursquare

At Foursquare, Ilya’s team has been developing [Foursquare Spatial Desktop](https://ilya.boyandin.me/p/fsq-spatial-desktop), a desktop application for exploring geospatial data built with SQLRooms. It combines DuckDB’s analytical engine with [kepler.gl](https://kepler.gl/)’s visualization tools. The app builds on the team’s experience with kepler.gl and [Foursquare Studio](https://studio.foursquare.com), its cloud-hosted geospatial analytics platform.

Ilya explains: **“For this particular product, DuckDB embedded into the desktop app is just the perfect fit. It enables analysis workflows which users can execute locally.”** SQLite is embeddable too, he says, but it is not column-oriented and was not designed for analytics on larger datasets.

![Foursquare Spatial Desktop](/images/blog/local-analytics/fsq-spatial-desktop-earthquakes.webp)

Modern laptops have substantial computing power and GPUs well suited to visualization, Ilya adds. **“I’m seeing renewed interest in applications that keep data and computation on the user’s own machine.”**

### Dynamic Tiling in Spatial Desktop

Spatial Desktop uses [deck.gl](https://deck.gl/) to render maps, but drawing millions of features at once can slow things down. The app addresses this with dynamic tiling powered by DuckDB’s [spatial extension]({% link docs/2.0/core_extensions/spatial/overview.md %}).

Map tiles are often prepared in advance for fast loading. Spatial Desktop can also generate tiles from users’ own datasets on demand, using the local DuckDB database, so users can start exploring without preparing a tileset first. For each requested tile, it selects nearby features and takes a random sample to keep dense tiles manageable. It also simplifies lines and polygons according to the zoom level, retaining more detail as the user zooms in.

<div class="video-container">
<video src="https://blobs.duckdb.org/videos/fsq-spatial-desktop-dynamic-tiling-4-1500.mp4" controls muted loop playsinline></video>
</div>

The following simplified query shows the main steps. It assumes the source geometries are already in Web Mercator coordinates (`EPSG:3857`). The tile width determines both a small buffer around the search area and a simplification tolerance equivalent to roughly half a pixel:

```sql
WITH tile AS (
    SELECT
        ST_TileEnvelope(⟨z⟩, ⟨x⟩, ⟨y⟩) AS bounds,
        (ST_XMax(bounds) - ST_XMin(bounds)) / 256.0 AS meters_per_pixel
),
candidates AS (
    SELECT
        f.id, f.geometry, tile.bounds,
        GREATEST(meters_per_pixel * 0.5, 0.1) AS tolerance
    FROM features f, tile
    WHERE ST_Intersects_Extent(
        f.geometry,
        ST_Buffer(tile.bounds, meters_per_pixel * 16)
    )
),
sampled AS (
    SELECT *
    FROM candidates
    USING SAMPLE reservoir(50000 ROWS)
),
encoded AS (
    SELECT
        id,
        ST_AsMVTGeom(
            ST_SimplifyPreserveTopology(geometry, tolerance),
            ST_Extent(bounds)
        ) AS geom
    FROM sampled
)
SELECT ST_AsMVT(encoded, 'features') AS tile
FROM encoded
WHERE geom IS NOT NULL;
```

`ST_AsMVTGeom` converts the simplified geometries to tile coordinates and clips them; [`ST_AsMVT`]({% link docs/2.0/core_extensions/spatial/functions.md %}#st_asmvt) packages them and their attributes into a Mapbox Vector Tile (MVT). The production implementation also handles invalid geometries, filters out very small lines and polygons, and caches generated tiles.

An HTTP server running locally as part of the Electron desktop app serves the tiles requested by the map.

## Graph Analytics on the Fly with Cosmograph

SQLRooms also powers the analytical workspace in [Cosmograph](https://cosmograph.app), a browser-based graph exploration tool developed by [Nikita Rokotyan](https://rokotyan.com/) and Thor Whalen. Ilya helped integrate SQLRooms into the application, which can visualize graphs with millions of edges.

<div class="video-container">
<video src="https://blobs.duckdb.org/videos/cosmograph-2.0.mp4" controls muted loop playsinline></video>
</div>

Cosmograph has been tested with datasets ranging from tens of thousands of points to several million. DuckDB-Wasm handles data loading and SQL queries in a background worker, helping keep the interface responsive. It lets the app filter and summarize data as users explore, while columnar query results reduce the conversion work needed to prepare data for visualization.

## When the Agent Writes the SQL

SQLRooms also supports AI-assisted analysis. **“The combination of SQL and AI agents is actually quite powerful,”** Ilya says. **“SQL has a long history, there are many documents on the web explaining how to use it, so LLMs are pretty good at generating it.”**

Users can ask questions in natural language. The assistant generates SQL queries and chart specifications, which the application executes and renders locally. The source dataset can stay on the user’s machine, while database schemas and selected query results can be shared with the AI provider to help answer questions.

In the Spatial Desktop example below, the assistant generates SQL to retrieve data from available sources and calculate a combined score for wine-growing suitability across Italy. The resulting map is accompanied by AI-generated regional analysis:

![Foursquare Spatial Desktop showing a wine-growing suitability map of Italy alongside AI-generated regional analysis](/images/blog/local-analytics/italy-wine-suitability-with-sidebar.webp)

## Where SQLRooms Goes Next

Ilya is extending SQLRooms’ workspace model so users can bring their analysis together in interactive documents. These documents combine text with blocks such as charts or SQL queries, letting users explain their findings alongside the analysis that produced them.

<div class="video-container">
<video src="https://blobs.duckdb.org/videos/sqlrooms-cars-document.mp4" controls muted loop playsinline></video>
</div>

Ilya is also exploring other ways to work with these analytical projects. At [DuckCon #7]({% link _events/2026-06-24-duckcon7.html %}) in Amsterdam, he demonstrated a SQLRooms command-line tool with a notebook-style interface. It saves both the data and the analysis artifacts in a single DuckDB database file. The goal is to let users continue the same project through a graphical application or the command line. The CLI design is still evolving.

## Learn More

Ilya’s [five-minute talk](https://www.youtube.com/watch?v=fV1LXnPl4ng) from DuckCon #7 gives a short tour of this direction.

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/fV1LXnPl4ng" title="YouTube video player" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

SQLRooms is open source and available at [sqlrooms.org](https://sqlrooms.org). Its [examples page](https://sqlrooms.org/examples) is a good place to start. [Flowmap City](https://flowmap.city/), [Foursquare Spatial Desktop](https://foursquare.com/products/spatial-desktop/), and [Cosmograph](https://cosmograph.app) are free to try.

We would like to thank Ilya for the conversation. You can follow his writing on DuckDB and SQLRooms on [his website](https://ilya.boyandin.me/). And if you are reading this, are using DuckDB, and would like to share your story, drop us a line at [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).
