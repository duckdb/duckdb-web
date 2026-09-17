---
layout: post
title: "dbt Without the Warehouse (or the Bill): DuckDB End to End"
author: "Hannes Mühleisen"
excerpt: ""
tags: ["talk"]
labels: [core]
venue: "The Cosmopolitan, Las Vegas"
---

Hannes Mühleisen, co-creator of DuckDB, will give a talk at [dbt Summit](https://www.getdbt.com/dbt-summit) (formerly Coalesce), dbt Labs' annual conference for the analytics engineering community. The talk is scheduled for 10:00 AM PT on Friday, September 18, 2026, in Level 3, Gracia 4.

## Venue

The Cosmopolitan of Las Vegas, 3708 Las Vegas Blvd S, Las Vegas, NV 89109.

## Abstract

Somewhere along the way we all agreed that transforming a few gigabytes of data requires renting a distributed system by the second. Every dbt run becomes a round-trip you didn't need to take: slow, metered, and queued behind your colleagues' CI jobs. If your whole project fits in a few hundred GB, this is a strange way to live, and you can stop. DuckDB is a free, MIT-licensed, in-process analytical database — no server, no account, no invoice — and it now runs in public beta on the dbt Fusion engine. That means sub-second model iteration on your laptop, full-project CI in seconds on a plain GitHub runner, and Python models that run in-process without your data going anywhere. Add DuckDB's native readers for Parquet, Iceberg, and Postgres, DuckLake for publishing your output tables in open formats, and DuckDB-WASM for querying them straight from the browser, and the warehouse becomes optional at every stage, not just development. This talk features a real dbt project developed, tested, deployed, and served entirely on DuckDB, live on stage, on more data than you'd think reasonable. Your data is not that big. Your bill doesn't have to be either.
