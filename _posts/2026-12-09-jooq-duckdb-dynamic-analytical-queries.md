---
layout: post
title: "Building Dynamic Analytical Queries in Java with jOOQ and DuckDB"
authors:
  - Lukas Eder
  - Geertjan Wielenga
  - Tim Cox
thumb: "/images/blog/thumbs/jooq.svg"
image: "/images/blog/thumbs/jooq.png"
excerpt: "[jOOQ](https://www.jooq.org/) lets Java, Kotlin and Scala developers write SQL as type-safe code instead of strings. Its creator, Lukas Eder, added DuckDB as a supported dialect when few people had heard of it, and the open-source edition supports it for free. He explains why the combination fits analytical applications, where queries change with every user request."
tag: case-study
---

> Quote
>
> jOOQ will give you type safety on top of DuckDB inside of your Java program.
>
> — Lukas Eder, creator of [jOOQ](https://www.jooq.org/)
{: .quote-large}

Tools such as [DataGrip]({% post_url 2026-11-05-jetbrains-datagrip %}) and [QStudio]({% post_url 2026-11-03-bringing-local-analytics-to-the-quants-desktop %}) ship DuckDB inside the product as their query engine. [jOOQ](https://www.jooq.org/) is different. **"jOOQ isn't using DuckDB, it's just integrating with it,"** says its creator, Lukas Eder. DuckDB lives in the developer's own application, and jOOQ sits on top of it, giving developers on the JVM (Java Virtual Machine) a type-safe way to write the SQL that DuckDB runs, in Java, Kotlin or Scala.

## From Oracle SQL to an Open-Source Business

Before jOOQ, Lukas wrote Oracle SQL for an e-banking integrator in Switzerland. He became deeply specialized in this work and found it compelling. SQL has been his focus ever since.

jOOQ started as a side project. It is an internal domain-specific language: it models the SQL language in Java, so that developers can embed type-safe SQL directly in their programs. Lukas first tried to sell it to his employer and to other companies. When that did not work, he open-sourced it. Once large companies started to use it, he founded a business around it in 2013.

Today jOOQ supports around 30 SQL dialects. Developers write against one API in what is mostly standard SQL, and jOOQ translates it into each vendor's syntax. The business model follows the database: commercial databases such as Oracle and SQL Server need a commercial jOOQ license, while open-source databases, DuckDB among them, work with the free open-source edition. Some advanced features, such as client-side emulation of row-level security, are commercial only.

## Adding DuckDB Early

Lukas cannot remember whether anyone asked for DuckDB support. He thinks he may have added it simply because it was interesting. It looked like it would sit in the same space as SQLite, embedded and in-process, but built for analytics. He ran jOOQ's integration tests against it, most of them passed without much effort, and he decided to support it early, well before DuckDB gained widespread adoption.

**"Things have changed, and I'm glad I already have supported DuckDB for a long time,"** he says.

He has also watched DuckDB mature. In his experience the earliest releases had problems, including with transaction consistency. Over the years, the transactional side stabilized too. **"It's really reliable now,"** Lukas says.

## How the Pieces Fit Together

The architecture is simple. jOOQ talks to databases through JDBC, and the [DuckDB Java client]({% link docs/2.0/clients/java/overview.md %}) is a JDBC driver that contains the embedded database. **"jOOQ uses JDBC, and the DuckDB database is embedded in the form of a JDBC driver,"** Lukas says. **"So that's all you need."**

An application needs two dependencies, both available from Maven Central:

```xml
<dependency>
  <groupId>org.duckdb</groupId>
  <artifactId>duckdb_jdbc</artifactId>
</dependency>
<dependency>
  <groupId>org.jooq</groupId>
  <artifactId>jooq</artifactId>
</dependency>
```

The application builds queries with jOOQ's API. jOOQ renders them as DuckDB SQL and sends them through the JDBC driver, and DuckDB executes them. DuckDB does not know or care where a query came from. **"It's just always JDBC,"** Lukas says.

jOOQ also has a code generator. It reads the database schema and generates Java classes for its tables and columns. Queries written against those classes are checked by the Java compiler, so a misspelled column or a comparison between incompatible types fails the build instead of failing in production.

## Why Analytical Queries Benefit Most

Lukas's main argument is about dynamic SQL. Transactional applications tend to run the same few queries over and over. Analytical applications build their queries from user input: a filter here, a different grouping there, an extra time range. **"If you're writing an application against an analytical database, then you're gonna have a ton of dynamic SQL,"** he says.

Without a library like jOOQ, dynamic SQL means building strings. **"If it's dynamic, then you have to concatenate strings, and it's just ugly and error-prone,"** Lukas says. A missing space between two fragments is enough to break a query. In his experience, teams that go this way end up writing their own query builder. It handles `SELECT`, `FROM` and `WHERE` and a few `AND` and `OR` combinations, and stops there.

With jOOQ, every part of the query is an object. The application can add conditions, choose columns and change the grouping, and the result is still a single, well-formed query, with bind values instead of concatenated input. The sketch below uses classes generated from a `trips` table:

```java
Condition where = DSL.noCondition();
if (filter.region() != null) {
    where = where.and(TRIPS.REGION.eq(filter.region()));
}
if (filter.since() != null) {
    where = where.and(TRIPS.PICKUP_TIME.ge(filter.since()));
}

Field<String> dimension = switch (filter.groupBy()) {
    case REGION -> TRIPS.REGION;
    case VENDOR -> TRIPS.VENDOR;
};

try (Connection connection = DriverManager.getConnection("jdbc:duckdb:analytics.duckdb")) {
    Result<?> result = DSL.using(connection, SQLDialect.DUCKDB)
        .select(dimension, DSL.count(), DSL.avg(TRIPS.FARE))
        .from(TRIPS)
        .where(where)
        .groupBy(dimension)
        .orderBy(DSL.count().desc())
        .fetch();
}
```

Every filter is optional, and the grouping column is chosen at runtime, but each column reference is checked when the code compiles.

Because jOOQ holds the whole query as an object model, it can also transform queries before they run. Lukas gives row-level security as an example. A developer writes what looks like a static query, and jOOQ adds the extra predicates behind the scenes. This is a commercial jOOQ feature, but it works on any database, DuckDB included.

Lukas compares this with ORMs like Hibernate, the most popular persistence framework in Java. An ORM can help load data into an analytical database, he says, but it does little for querying it. For that you write SQL, either as static strings or, when the queries are dynamic, with a tool like jOOQ. The same pattern applies to other analytical databases. Many jOOQ users run it on Snowflake for the same reason.

jOOQ runs anywhere on the JVM. Lukas notes that it is particularly popular with Kotlin developers.

## Ad Hoc SQL and Application SQL

Lukas is candid about which parts of DuckDB's [friendly SQL]({% link docs/2.0/sql/dialect/friendly_sql.md %}) matter to him. DuckDB lets you skip `SELECT` and start a query with `FROM`. That is handy in the terminal. In application code, Lukas thinks it makes little difference. **"This is very useful for ad hoc SQL,"** he says, in the same way that `SELECT *` is fine at the command line but something you should never write in an application.

The distinction is a useful one. The [DuckDB CLI]({% link docs/2.0/clients/cli/overview.md %}) is built for exploration. A Java service that runs thousands of generated queries needs something else: structure, reuse and checks at compile time. jOOQ provides those.

## Keeping Up with a Dialect

To support a database, Lukas relies on jOOQ's test suite. **"There's a huge integration test suite that runs all the queries on all the database products,"** he explains. When he adds a dialect, he runs the suite, sees what fails and adapts how jOOQ renders SQL for that database. Standard syntax such as joins usually works unchanged. JSON support and functions differ in almost every database.

Not everything is covered yet. DuckDB's [`PIVOT` syntax]({% link docs/2.0/sql/statements/pivot.md %}) differs from Oracle's and SQL Server's, and jOOQ does not support it yet, because nobody has asked for it.

Integrating DuckDB also gives Lukas ideas. He is considering [`ASOF JOIN`]({% link docs/2.0/guides/sql_features/asof_join.md %}), DuckDB's fuzzy temporal join, for jOOQ, and possibly emulating it on databases that lack it. An idea that starts with one database can end up as a feature for all of them.

## What Comes Next

Developers today rarely need to ask Lukas for help getting started. AI coding assistants have learned jOOQ from its documentation, and Lukas uses Claude himself every day to write jOOQ code. **"The documentation of jOOQ is really good,"** he says.

Lukas expects the combination with DuckDB to grow as DuckDB becomes more common inside Java applications. Until recently, he says, DuckDB was more popular as a standalone tool at the console than embedded in a Java program. Once that changes, people will pick up jOOQ along with it. The DuckDB Java client keeps gaining features for exactly that kind of use, such as [table functions written in Java]({% post_url 2026-08-25-table-functions-in-java %}).

If you use jOOQ with DuckDB, we would like to hear from you, and so would Lukas.

We would like to thank Lukas for the conversation. jOOQ is available at [jooq.org](https://www.jooq.org/), and the open-source edition supports DuckDB. If you use DuckDB and want to share your story, email [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).
