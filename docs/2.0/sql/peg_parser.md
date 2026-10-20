---
layout: docu
redirect_from:
- /docs/current/sql/peg_parser
- /docs/lts/sql/peg_parser
- /docs/preview/sql/peg_parser
title: PEG Parser
---

> New Starting with DuckDB 2.0, the PEG parser is the default parser. In earlier versions it was an experimental, opt-in feature enabled with `enable_peg_parser()`, which is no longer required or available.

DuckDB uses a parser based on PEG ([parsing expression grammars](https://en.wikipedia.org/wiki/Parsing_expression_grammar)).
It replaces the parser front end derived from PostgreSQL that earlier versions used.
The PEG parser enables better suggestions, improved error messages with precise source locations, and allows extensions to extend the grammar.

The PEG grammar was first introduced in DuckDB 1.2 to power autocomplete in the command line client. DuckDB 1.5 shipped a complete but experimental version, and DuckDB 2.0 made it the default.

Switching parsers does not change the SQL dialect. DuckDB 2.0 replaced the parser implementation and rewrote its grammar, but the dialect itself and the rest of the query pipeline, including the binder, continue to operate on the same internal syntax tree.

## Suggestions

The PEG parser is used to generate suggestions. You can cycle through the options using `TAB`:

```sql
«animals_db» D FROM ducks WHERE habitat IS 
IS           ISNULL       ILIKE        ⌊IN⌋           INTERSECT    LIKE
```

## Extensible Grammar

Because the grammar is part of the parser, extensions can extend the tokenizer, add grammar rules, and register custom matchers while reusing the rest of the DuckDB grammar. This makes it possible to combine the syntax of multiple extensions, and you can expect extensions that expose entirely new SQL syntax.

## Performance

The parser uses packrat parsing, which memoizes intermediate results to avoid exponential backtracking on deeply nested expressions. As a tradeoff, parsing uses additional memory and has a slight performance overhead. This is in the range of milliseconds and is thus negligible for analytical queries.

## Checking a Query

The `check_peg_parser` table function parses a query with the PEG parser and reports whether it parses successfully. This is useful for testing:

```sql
FROM check_peg_parser('SELECT 42');
```

## Legacy Parser

> New The `legacy_parser` extension was introduced in DuckDB 2.0.

For exceptional cases, DuckDB 2.0 can fall back to the legacy PostgreSQL-style parser through the [`legacy_parser` extension]({% link docs/2.0/core_extensions/legacy_parser.md %}). Setting the following option autoloads the extension and switches from the default PEG parser to the legacy parser:

```sql
SET enable_legacy_parser = true;
```

The legacy parser is intended as a bridge solution, for example to check a query on both parsers and determine whether a given behavior is tied to the parser or transformer rather than to downstream code. It provides a best-effort legacy experience and preserves several DuckDB 1.5 quirks:

* `~` and `!~` perform full regular expression matches, whereas DuckDB 2.0 defaults to partial matches.
* `B'0101'` is the `VARCHAR` value `'b0101'`, whereas DuckDB 2.0 interprets it as a bit-string literal.
* Rendered SQL qualifies built-in functions, for example `main.struct_pack(x := 1)` in view definitions.
* `ORDER BY true` is accepted, whereas DuckDB 2.0 rejects a non-integer literal.
* Column constraints on `ALTER TABLE ... ADD COLUMN`, such as `UNIQUE`, are rejected by the transformer.
* The `identifier_case_mode = 'uppercase'` option is a DuckDB 2.0 feature; the legacy grammar treats it as `preserve`.

> Warning Newer and more powerful syntax, such as [`INSTALL AND LOAD`]({% link docs/2.0/sql/statements/load_and_install.md %}), is rejected by the legacy parser.

## Further Reading

* [“A Preview of DuckDB v2.0”]({% post_url 2026-08-17-duckdb-20-highlights %}) blog post
* [“DuckDB v2.0: Your Database Deserves a Better Parser”]({% post_url 2026-08-20-duckdb-20-peg-parser %}) blog post
* [“Runtime-Extensible SQL Parsers Using PEG”]({% post_url 2024-11-22-runtime-extensible-parsers %}) blog post
* [“Runtime-Extensible Parsers”]({% link _library/2025-01-19-runtime-extensible-parsers.md %}) (CIDR 2026 paper) by Hannes Mühleisen and Mark Raasveldt
