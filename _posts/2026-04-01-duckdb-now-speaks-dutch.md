---
layout: post
title: "DuckDB Now Speaks Dutch!"
author: "Daniël ten Wolde"
thumb: "/images/blog/thumbs/duckdb-now-speaks-dutch.svg"
image: "/images/blog/thumbs/duckdb-now-speaks-dutch.png"
excerpt: "DuckDB now speaks Dutch! Load the EendDB community extension and start writing your queries in het Nederlands."
tags: ["extensions"]
---

Historically speaking, SQL queries have always been formulated in English. The initial name of the language was even Structured **English** Query Language (SEQUEL), before it became SQL. Now, what if the Dutch hadn't traded away New Amsterdam (present-day New York)? Would we all have been writing SQL in Dutch instead?

Well, wonder no longer. Today we're releasing [**EendDB**]({% link community_extensions/extensions/eenddb.md %}): a DuckDB extension that brings you the **Gestructureerde Zoektaal,** or GZT for short.

Want joins? We've got `SAMENVOEGEN`. Aggregates? `GROEP PER`. Window functions? Those work too — though you'll have to look up the Dutch keywords in the repository yourself.

You can try it out right now in [DuckDB v1.5.1]({% post_url 2026-03-23-announcing-duckdb-151 %}):

```sql
INSTALL eenddb FROM community;
LOAD eenddb;
CALL enable_dutch_parser();

MAAK TABEL eend (
    id        GEHEEL_GETAL,
    naam      TEKST,
    leeftijd  GEHEEL_GETAL,
    gewicht   KOMMAGETAL,
    soort     TEKST
);

TOEVOEGEN AAN eend WAARDEN
    (1, 'Donald',  29, 1.2, 'Wilde eend'),
    (2, 'Daffy',   35, 1.5, 'Zwarte eend'),
    (3, 'Daisy',   27, 1.1, 'Wilde eend'),
    (4, 'Scrooge', 75, 1.8, 'Wilde eend');

SELECTEER *
VAN eend
WAARBIJ gewicht > 1.2 EN naam ZOALS '%D%'
VOLGORDE PER leeftijd;
```

```text
┌───────┬─────────┬──────────┬─────────┬─────────────┐
│  id   │  naam   │ leeftijd │ gewicht │    soort    │
│ int32 │ varchar │  int32   │  float  │   varchar   │
├───────┼─────────┼──────────┼─────────┼─────────────┤
│     2 │ Daffy   │       35 │     1.5 │ Zwarte eend │
└───────┴─────────┴──────────┴─────────┴─────────────┘
```

Of course, no query language is complete without joins and aggregates. Let's create a second table and count the ducks per _soort:_

```sql
MAAK TABEL soorten (soort TEKST, leefgebied TEKST);

TOEVOEGEN AAN soorten WAARDEN
    ('Wilde eend',  'Meren en rivieren'),
    ('Zwarte eend', 'Kustgebieden');

SELECTEER s.leefgebied, count(*) ALS aantal_eenden
VAN eend ALS e
LINKS SAMENVOEGEN soorten ALS s OP e.soort = s.soort
GROEP PER s.leefgebied
VOLGORDE PER aantal_eenden AFLOPEND;
```
```text
┌───────────────────┬───────────────┐
│    leefgebied     │ aantal_eenden │
│      varchar      │     int64     │
├───────────────────┼───────────────┤
│ Meren en rivieren │             3 │
│ Kustgebieden      │             1 │
└───────────────────┴───────────────┘
```

After we are done playing around, we obviously have to clean up after ourselves. Rather than `DROP` a table, in Dutch we like to throw it away (“weggooien”):

```sql
GOOI_WEG TABEL eend;
GOOI_WEG TABEL soorten;
```

Under the hood, the parser is using DuckDB's [new experimental parser]({% post_url 2026-03-09-announcing-duckdb-150 %}#peg-parser), based on [Parsing Expression Grammar]({% post_url 2024-11-22-runtime-extensible-parsers %}).

For more examples, check out the [repository on GitHub](https://github.com/Dtenwolde/eenddb/).
