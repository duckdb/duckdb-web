---
layout: post
title: "DuckDB v2.0: Your Database Deserves a Better Parser"
author: "Daniël ten Wolde"
thumb: "/images/blog/thumbs/duckdb-20-peg-parser.svg"
image: "/images/blog/thumbs/duckdb-20-peg-parser.png"
excerpt: "DuckDB 2.0 replaces its PostgreSQL-derived SQL parser with a PEG-based parser that is easier to evolve and can be extended at runtime."
tags: ["release"]
---

At DuckDB, one of our goals is to make working with a database system as easy as possible. Users interact with the system through the widely understood Structured Query Language (SQL). Previous blog posts have covered DuckDB’s Friendly SQL, including `GROUP BY ALL` and column selection using `SELECT * EXCLUDE (...)`. Before DuckDB can execute a query using these features, however, it first has to determine whether its syntax is valid. That is the job of the *parser*, and in DuckDB v2.0 we are completely replacing it without you noticing.

## What is the Role of a Parser?

At a high level, DuckDB processes a SQL query through the following stages: 

**SQL text → Tokenizer → Parser → ParseResult tree → Transformer → DuckDB AST** → Binder → Logical Plan → Optimizer → Physical Plan → Execution

In this blog, we focus on the tokenizer, parser, and transformer:

* Tokenizer: This is the first step and is responsible for splitting up the raw input string into *tokens*. These can be of various categories, for example: `KEYWORD`, `NUMBER`, or `IDENTIFIER`. It is also where comments, in SQL denoted with either `--` or `/* */`, are recognized and skipped.
* Parser: The parser determines whether these tokens follow DuckDB's grammar and produces a `ParseResult` tree.
* Transformer: Converts the generic parse results into DuckDB’s internal abstract syntax tree (AST), forming structures such as `SQLStatement`, `TableRef`, and `ParsedExpression`. The resulting AST is passed on to the binder.

The parser determines whether a query is syntactically valid, while the binder determines whether the tables, columns, and functions it refers to actually exist.

Consider the following query:

```sql
SELECT *
WHERE true
FROM range(1);
```

```console
Parser Error:
syntax error at or near "FROM"

LINE 3: FROM range(1);
        ^^^^
```

Every individual *token* in this query is valid, but the clauses occur in an order that DuckDB’s grammar does not accept. Friendly SQL allows both `SELECT`-first and `FROM`-first syntax, but it does not allow the clauses to appear in an arbitrary order.

By comparison, the following query is syntactically valid, so it passes the parser and transformer. However, it fails later in the binder because the table `missing_table` does not exist. 

```sql
FROM missing_table;
```

```console
Catalog Error:
Table with name missing_table does not exist!

LINE 1: FROM missing_table;
             ^^^^^^^^^^^^^
```

## The DuckDB SQL Dialect

Although a SQL standard exists, database systems support different parts of the standard and add their own syntax and behavior. The resulting variants are commonly referred to as SQL dialects. Examples include the dialects supported by PostgreSQL, Oracle, GoogleSQL for BigQuery, MySQL, MariaDB, SQLite, Spark SQL, and, of course, DuckDB.

DuckDB’s SQL closely follows PostgreSQL conventions, but it has evolved considerably over the years. We have added features of our own, such as `GROUP BY ALL`, as well as features inspired by other database systems. At the same time, DuckDB does not implement every aspect of PostgreSQL’s behavior. DuckDB therefore speaks its own SQL dialect, which we will refer to as **DuckSQL** in this post, even though it remains strongly influenced by PostgreSQL.

This distinction is important when talking about the parser. The SQL dialect that DuckDB accepts and the implementation used to parse that SQL are two separate things. For DuckDB `2.0`, we are replacing the parser implementation and rewriting its grammar. What we are **not** replacing is DuckSQL itself.


## Outgrowing the PostgreSQL-derived parser

When DuckDB started out, it made a lot of sense to use the PostgreSQL-derived parser and grammar. This parser was already part of the [first commit](https://github.com/duckdb/duckdb/commit/ba75d81601913782d28a3878707d135319f38bdd) to DuckDB in 2018. It gave DuckDB a mature, battle-tested SQL grammar based on syntax that many users were already familiar with. We adapted the parser to our needs and added a `Transformer` that converted the resulting PostgreSQL-style parse tree into DuckDB’s internal AST.

However, over the years this parser also came with some downsides. Extending DuckSQL meant modifying the underlying YACC/Bison grammar. Because Bison generates an LALR(1) parser, seemingly small additions to the grammar can interact with existing rules and introduce `shift/reduce` or `reduce/reduce` conflicts. As DuckSQL grew, making changes to the grammar therefore became increasingly difficult.

This was one of the motivations behind our earlier blog post on runtime-extensible SQL parsers. In that post and the accompanying CIDR paper, we explored whether Parsing Expression Grammars (PEGs) could provide a better foundation for an extensible database parser. At the time, the PEG parser was still an experimental prototype capable of parsing only a subset of SQL. 

## A Primer on PEG Parsers

Before looking at how we turned the prototype into a production parser, let us briefly revisit how a PEG describes a language.

A PEG consists of named rules that describe how an input should be matched. Consider the following rules from DuckDB’s new grammar:

```text
SelectFrom <- SelectFromClause / FromSelectClause
SelectFromClause <- SelectClause FromClause?
FromSelectClause <- FromClause SelectClause?
```

The `<-` operator defines a rule, `/` specifies a choice between alternatives, and `?` makes an element optional. Together, these rules state that DuckSQL accepts both a traditional `SELECT`-first query:

```sql
SELECT *
FROM range(1);
```

And DuckDB’s Friendly SQL `FROM`-first equivalent:

```sql
FROM range(1)
SELECT *;
```

A PEG evaluates alternatives in order. When matching `SelectFrom`, the parser first attempts `SelectFromClause`. If that does not match, it attempts `FromSelectClause`. The first successful alternative is selected. As a result, PEG grammars do not have the same `shift/reduce` and `reduce/reduce` conflicts as LALR grammars. Instead, alternatives are ordered explicitly, and that order forms part of the grammar’s behavior.

In DuckDB, these rules operate on the tokens produced by the tokenizer. The matcher applies the grammar rules to those tokens and constructs a generic `ParseResult` tree, which is subsequently transformed into DuckDB’s internal AST.

## Going from Prototype to Production

The research prototype demonstrated that a PEG-based SQL parser was feasible. Replacing DuckDB’s existing parser, however, required considerably more than parsing a representative subset of SQL. The new parser had to accept all of DuckSQL and produce the same AST expected by DuckDB’s binder.

The PEG grammar first reached users in DuckDB v1.2, where it handled autocomplete in the CLI. Later, in DuckDB v1.5 we introduced the complete PEG parser as an experimental, opt-in feature. Since then, the grammar, matcher, and transformer have been steadily improved to make the PEG parser the default for DuckDB v2.0.

Among other things, the parser had to support:

* **Every statement and expression type:** Supporting the complete DuckSQL dialect includes both common syntax and the less frequently used statements.
* **Operator precedence and associativity:** For example, `SELECT true OR true AND false;` must be interpreted as `(true OR (true AND false))`, because `AND` binds more tightly than `OR`.
* **Correct keyword classification:** Some keywords, such as `SELECT`, are `RESERVED` and cannot be used as unquoted table or column names. Other keywords may be used as identifiers depending on their context.
* **Compatibility with DuckDB’s internal AST:** The PEG transformer must produce the same DuckDB AST structures as the transformer for the PostgreSQL-derived parse nodes wherever the language behavior is intended to remain unchanged.
* **Correct error reporting:** For an invalid query, the parser should report where parsing failed and, where possible, provide context and a useful indication what went wrong. Ideally without point to a [manual](https://duckdb.org/2024/11/22/runtime-extensible-parsers#:~:text=You%20have%20an%20error%20in%20your%20SQL%20syntax%3B%20check%20the%20manual%20that%20corresponds%20to%20your%20MySQL%20server%20version%20for%20the%20right%20syntax%20to%20use%20near%20%27SELEXT%27%20at%20line%201%2E).
* **Performance on unusual inputs:** Besides keeping normal parsing fast, we also had to make sure that malformed queries do not suddenly take a long time to parse.

### Avoiding Repeated Work with Packrat Parsing

One issue we encountered was repeated work during backtracking. A naïve PEG matcher can evaluate the same grammar rule at the same token position many times while trying different alternatives. For certain malformed inputs, the amount of repeated work can grow exponentially.

We encountered this with queries containing a large number of unmatched opening parentheses:

```sql
SELECT ((((((((((((((((((;
```

With the experimental PEG parser shipped in v1.5, adding one more opening parenthesis approximately doubled the parsing time:

```text
18 opening parentheses:  5.303 seconds
19 opening parentheses: 10.640 seconds
```

We addressed this using **packrat parsing**, a memoization technique commonly used with PEG parsers. For each memoized matcher, we store the result of applying it at a particular token position. If the parser later attempts the same matcher at the same position, it reuses the cached result instead of evaluating it again.

With packrat parsing enabled, the same malformed query was rejected almost instantly:

```text
19 opening parentheses: 0.001 seconds
```

As a result, a memoized matcher is evaluated at most once at a particular token position, removing the repeated work that caused the exponential behavior in this example. This requires additional memory while parsing, but that is a worthwhile trade-off for avoiding cases such as this.

Turning the prototype into a production parser involved much more than translating the grammar. The new parser had to cover the complete DuckSQL dialect, preserve DuckDB’s existing AST, remain compatible with existing queries, and handle both valid and malformed input efficiently.

The resulting architecture replaces the PostgreSQL-derived parser front end, while the binder and the remainder of DuckDB’s query-processing pipeline continue to operate on the same internal AST.

-- todo: Add figure of old vs. new architecture

## Evolving DuckSQL

With the PEG parser now in place for DuckDB v2.0, we have also continued to extend DuckSQL with new syntax for DuckDB v2.0.

One example is the new expression-statement syntax. Until now, executing a query consisting only of expressions always required writing a `SELECT`:

```sql
SELECT date: current_date(), time: current_localtime();
```

With an expression statement, the `SELECT` can be omitted:

```sql
date: current_date(), time: current_localtime();
```

As a bonus, this also works with prefix aliases.

Another example is the new `CONNECT` statement, introduced for Quack. It allows you to connect to a remote database and route subsequent queries to it until `DISCONNECT` is called:

```sql
CONNECT 'postgres://localhost/mydb';
SELECT count(*) FROM orders; -- Runs on the PostgreSQL server
DISCONNECT;
```

We have also extended `COPY TO` with `PARTITION BY` and `ORDER BY` syntax:

```sql
COPY orders TO 'orders'
(
    FORMAT parquet,
    PARTITION BY (year, month),
    ORDER BY (order_date)
);
```

These additions would also have been possible with the old PostgreSQL-derived parser, but adding them would have been considerably more cumbersome. The PEG grammar makes it easier for us to continue evolving DuckSQL.

So far, these rules are all part of DuckSQL itself. The next step is allowing extensions to add rules of their own.

## Extending the Parser

Extensions are a central part of DuckDB. They can already add scalar and table functions, optimizer rules, query-plan rewrites, and even custom physical operators. 

Extensions that add new syntax already exist, such as [`psql`](https://duckdb.org/community_extensions/extensions/psql) and [`duckpgq`](https://duckdb.org/community_extensions/extensions/duckpgq), but under the hood they work as fallback parsers. DuckDB first tries to parse the query itself and only calls the extension if that fails. This works well for self-contained syntax, but an extension that wants to add syntax inside SQL also has to parse the surrounding SQL itself. These fallback parsers also make it impossible to combine the syntax of multiple extensions. 

With the PEG parser, extensions can instead extend individual parts of DuckDB’s parser. They can extend the tokenizer, add grammar rules, and register custom matchers while continuing to reuse the rest of DuckSQL.

> Warning The API shown below is still a preview and may change before [DuckDB v2.0]({% post_url 2026-08-17-duckdb-20-highlights %}).

To make this concrete, we use Google’s [pipe query syntax](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax). This is an extension to SQL that adds piped data flow syntax. Pipe syntax expresses a query as a sequence of operators, where each operator consumes the result of the previous one.

```sql
FROM produce
  |> WHERE
        item != 'bananas'
        AND category IN ('fruit', 'nut')
  |> AGGREGATE COUNT(*) AS num_items, SUM(sales) AS total_sales
     GROUP BY item
  |> ORDER BY item DESC;
```

A simplified PEG grammar for this needs a handful of rules:

```sql
PipeSelectAtom <- PipeSource PipeStage+
PipeSource <- FromClause / SelectStatementType / SelectParens
PipeStage <- '|>' PipeOperator
PipeOperator <- PipeAggregate / PipeAggregateGroupOnly / PipeWhere / PipeSelect / PipeExtend / PipeDistinct / PipeOrderBy / PipeLimit
PipeWhere <- WhereClause
PipeSelect <- 'SELECT' TargetList
PipeExtend <- 'EXTEND' TargetList
PipeDistinct <- 'DISTINCT'
PipeOrderBy <- OrderByClause
PipeLimit <- LimitClause OffsetClause?
PipeAggregate <- 'AGGREGATE' TargetList GroupByClause?
PipeAggregateGroupOnly <- 'AGGREGATE' GroupByClause
```

Here, `+` means that `PipeStage` must occur one or more times, so a pipe query must contain at least one pipe operator.

This grammar can reuse existing rules, such as `GroupByClause`, to reduce the amount of grammar the extension needs to define. An extension can still define its own rule where DuckDB’s existing syntax does not fit. 

### Registering the Grammar

Defining just the PEG rules does not yet make them part of DuckDB’s grammar. The extension must also specify (1) the existing grammar rule it wants to extend and (2) the transformer rules that convert the new syntax into DuckDB’s AST. 

In the current prototype, certain grammar rules expose extension points. Pipe SQL registers `PipeSelectAtom` as an additional alternative for `SelectAtom`, together with the new keywords `AGGREGATE` and `EXTEND`.

```cpp
static void LoadInternal(ExtensionLoader &loader) {
    ParserExtension extension;
    extension.grammar_extension.grammar = PIPE_SQL_GRAMMAR;
    extension.grammar_extension.select_atom_rule = "PipeSelectAtom";

    extension.grammar_extension.RegisterSelectAtomTransformer(
        "PipeSelectAtom",
        TransformPipeSelectAtom
    );
    
    loader.RegisterKeyword(
        "aggregate",
            ExtensionKeywordCategory::RESERVED
        );
        loader.RegisterKeyword(
            "extend",
            ExtensionKeywordCategory::RESERVED
        );

        loader.RegisterParserExtension(std::move(extension));
}
```

By registering this alternative, the resulting grammar is effectively:

```cpp
SelectAtom <-
    PipeSelectAtom /
    SelectParens /
    SelectStatementType
```

The extension alternative is now tried first. If no pipe syntax is present, it fails without consuming any tokens and the query is parsed with the built-in alternatives. 

### Transforming the Result

Adding a grammar rule only gets us as far as a `ParseResult`. The extension still needs to transform that result into the DuckDB AST that is expected by the binder. Since `PipeSelectAtom` extends `SelectAtom`, its transformer returns a `SelectStatement`:

```cpp
static unique_ptr<SelectStatement> TransformPipeSelectAtom(
    ParserExtensionInfo *info,
    PEGTransformer &transformer,
    ParseResult &parse_result
);
```

Inside this function, the extension only needs to transform the new pipe-specific rules it introduced. For DuckDB grammar rules that the extension reuses, it can also reuse the existing transformations. For example, because the pipe grammar uses DuckDB’s existing `GroupByClause`, the extension does not need to parse or transform `GROUP BY` itself.

This is an important difference from the fallback parsers that are available today. An extension no longer needs to implement expressions, table references, `GROUP BY` clauses, and the rest of SQL itself. Instead, it can add only the syntax it needs and reuse DuckDB’s grammar and transformations for everything else.

### Executing Pipe SQL

With the extension registered, DuckDB can now execute queries using the new pipe syntax. For example, we can combine the pipe operators added by the extension with existing DuckSQL features such as `range()` and prefix aliases:

```sql
FROM range(6) t(i) 
  |> WHERE i % 2 = 0 
  |> SELECT i, doubled: i * 2 
  |> ORDER BY i DESC;
```

```text
┌───────┬─────────┐
│   i   │ doubled │
│ int64 │  int64  │
├───────┼─────────┤
│     4 │       8 │
│     2 │       4 │
│     0 │       0 │
└───────┴─────────┘
```

The extension only defines the pipe-specific structure. Expressions, table references, `WHERE`, `SELECT`, `ORDER BY`, and other reused rules are still parsed and transformed by DuckDB itself. This means that new syntax can be combined with DuckSQL without the extension having to implement the rest of SQL again.

## What’s Next?

With DuckDB 2.0, the PEG parser is planned to completely replace the PostgreSQL-derived parser. The goal is for existing DuckSQL queries to continue working as before, while giving us a parser that is easier to evolve and designed to be extended at runtime.

The runtime grammar extension API shown in this post is still a work in progress and may change before v2.0 is released. However, the underlying idea is already working: extensions can add their own syntax while reusing the existing DuckDB grammar and transformations instead of implementing a complete SQL parser themselves.

If you do find an existing query that behaves differently with the PEG parser, please let us know by filing an issue.
