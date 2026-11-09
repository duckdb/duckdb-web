---
layout: docu
title: DataGrip
how_to_topic: tools-meta
---

[DataGrip](https://www.jetbrains.com/datagrip/) is a JetBrains IDE for working with multiple databases, including DuckDB. This guide covers the quickest way to connect. For more detailed instructions on how to start working with DuckDB, check out the [DataGrip documentation](https://www.jetbrains.com/help/datagrip/duckdb.html).

> Quote
>
> DuckDB turned out to be the simplest option to integrate.
>
> – Ilia Epelbaum, DataGrip, JetBrains, from the [“How JetBrains Built Cross-Database Queries into DataGrip with DuckDB” blog post]({% post_url 2026-11-05-jetbrains-datagrip %})

## Installing DataGrip

Download DataGrip from the [official JetBrains website](https://www.jetbrains.com/datagrip/) and install it.

<img src="/images/guides/datagrip/download.png" alt="DataGrip Download Page" title="DataGrip Download Page"/>

## Creating a DuckDB Data Source

Go to *File* | *New* | *Data Source* and select *DuckDB*.
Alternatively, open the database explorer (⌘1), click *New* (+), and go to *Data Source* | *DuckDB*.

<img src="/images/guides/datagrip/new_data_source_menu.png" alt="DataGrip New Data Source Menu" title="DataGrip New Data Source Menu"/>

## Setting Up the Connection

On the *General* tab, choose a connection type:

* *Default*: a database file.
* *In-memory*
* *URL only*

For *Default*, click *Open* to select an existing database file, or *New* to create one.
DataGrip fills in the URL for you.

<img src="/images/guides/datagrip/connection_settings.png" alt="DataGrip Connection Settings" title="DataGrip Connection Settings"/>

## Getting the Driver and Testing the Connection

If you see the *Download missing driver files* link, click it.

<img src="/images/guides/datagrip/download_missing_driver_files.png" alt="DataGrip Download Missing Driver Files" title="DataGrip Download Missing Driver Files"/>

Then click *Test Connection*, and then *OK*.

<img src="/images/guides/datagrip/test_connection.png" alt="DataGrip Test Connection" title="DataGrip Test Connection"/>

## Running Queries

Select your data source in the database explorer and press ⌘↓ to open a query console.

<img src="/images/guides/datagrip/database_explorer.png" alt="DataGrip Database Explorer" title="DataGrip Database Explorer"/>

Write your SQL and run it. For demo purposes, we loaded data from the Sakila sample database.

Running `SELECT * FROM actor` shows the results in the *Database Output* pane, along with the row count and execution time.

<img src="/images/guides/datagrip/query_results.png" alt="DataGrip Query Results" title="DataGrip Query Results"/>

> Quote
>
> We highlight that it’s DuckDB.
>
> – Ilia Epelbaum, DataGrip, JetBrains, from the [“How JetBrains Built Cross-Database Queries into DataGrip with DuckDB” blog post]({% post_url 2026-11-05-jetbrains-datagrip %})

## Where to Learn More

> Quote
>
> With DuckDB and its support for custom table functions, cross-database queries have finally become practical in DataGrip. Users can join data from PostgreSQL, MySQL, MongoDB, or any other supported database in one query, without setting up extra infrastructure.
>
> – Maxim Sobolevskiy, Head of Database Ecosystem at JetBrains, from the [“How JetBrains Built Cross-Database Queries into DataGrip with DuckDB” blog post]({% post_url 2026-11-05-jetbrains-datagrip %})

This guide only describes how to get started with DuckDB in DataGrip.
To see everything DataGrip allows you to do, watch the videos in the DataGrip playlist on YouTube or explore the features overview page or the [DataGrip home page](https://www.jetbrains.com/datagrip/).
DataGrip is free for non-commercial projects, and a 30-day free trial is available to explore it yourself.
