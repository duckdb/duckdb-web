---
layout: docu
railroad: statements/indexes.js
title: PEG Parser
---

DuckDB v1.5 shipped an experimental parser based on PEG (Parser Expression Grammars).
The new parser enables better suggestions, improved error messages, and allows extensions to extend the grammar.
The PEG parser is currently disabled by default but you can opt-in using:

```sql
CALL enable_peg_parser();
```

The PEG parser is already used for generating suggestions. You can cycle through the options using `TAB`.

```sql
«animals_db» D FROM ducks WHERE habitat IS 
IS           ISNULL       ILIKE        ⌊IN⌋           INTERSECT    LIKE
```

We are planning to make the switch to the new parser in the [DuckDB v2.0]({% link release_calendar.md %}) release.

> As a tradeoff, the parser has a slight performance overhead, however, this is in the range of milliseconds and is thus negligible for analytical queries. For more details on the rationale for using a PEG parser and benchmark results, please refer to the [CIDR 2026 paper]({% link _library/2025-01-19-runtime-extensible-parsers.md %}) by Hannes Mühleisen and Mark Raasveldt, or their [blog post]({% post_url 2024-11-22-runtime-extensible-parsers %}) summarizing the paper.
