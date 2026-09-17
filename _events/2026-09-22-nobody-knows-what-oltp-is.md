---
layout: post
title: "Nobody Knows What OLTP Is: DuckDB Moves to the Middle"
author: "Hannes Mühleisen"
excerpt: ""
tags: ["talk"]
labels: [core]
venue: "Contemporary Jewish Museum, San Francisco"
---

Hannes Mühleisen, co-creator of DuckDB, will give a talk at the [Rows & Columns Summit](https://rowsandcolumnssummit.com/), a practitioner-focused, single-track conference exploring the architecture question that won't go away: OLTP and OLAP, together or apart? The talk is scheduled for 1:30 PM on September 22, 2026.

## Venue

Contemporary Jewish Museum, 736 Mission Street, San Francisco, CA 94105.

## Abstract

The common wisdom in the endless OLTP versus OLAP debate goes like this: Postgres is OLTP, DuckDB is OLAP, and somewhere in the middle sits the elusive HTAP that nobody has actually seen. This is wrong. Postgres is not really an OLTP system, real transaction engines like TigerBeetle run circles around it. Postgres is a general-purpose system, not great at any single task but good enough for most, and that is exactly why it sits in the middle. DuckDB, the friendliest SQL database, is an in-process analytical engine that runs anywhere from a browser tab to a battery to space, and it started out firmly on the analytics end. But now with concurrent transactions, concurrent checkpointing, and Quack, our new DuckDB-to-DuckDB client-server protocol, DuckDB is slowly moving toward the middle too, from the other side, without making anything slower. In this talk, Hannes discusses the trade-offs and future directions we are thinking about to make this a reality. And who knows, maybe we get HTAP after all (spoiler alert, we won't).
