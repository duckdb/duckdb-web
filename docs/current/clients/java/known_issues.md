---
layout: docu
redirect_from:
- /docs/clients/java/known_issues
- /docs/preview/clients/java/known_issues
- /docs/stable/clients/java/known_issues
title: Troubleshoot
---

## Overview

This page collects common issues encountered when using the DuckDB JDBC driver, together with their workarounds. If you run into a problem that is not covered here, search the [driver's issue tracker](https://github.com/duckdb/duckdb-java/issues) on GitHub.

## Driver Class Not Found

This error occurs when the DuckDB JDBC driver is not on the application's classpath, typically because the build tool has not resolved the dependency. If the Java application is unable to find the DuckDB driver, it may throw the following error:

```console
Exception in thread "main" java.sql.SQLException: No suitable driver found for jdbc:duckdb:
    at java.sql/java.sql.DriverManager.getConnection(DriverManager.java:706)
    at java.sql/java.sql.DriverManager.getConnection(DriverManager.java:252)
    ...
```

And when trying to load the class manually, it may result in this error:

```console
Exception in thread "main" java.lang.ClassNotFoundException: org.duckdb.DuckDBDriver
    at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641)
    at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188)
    at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:520)
    at java.base/java.lang.Class.forName0(Native Method)
    at java.base/java.lang.Class.forName(Class.java:375)
    ...
```

These errors stem from the DuckDB [Maven](https://maven.apache.org/)/[Gradle](https://gradle.org/) dependency not being detected. To ensure that it is detected, force refresh the Maven configuration in your IDE.

## Parquet String Column Returns a Blob

Parquet files written by some legacy writers do not set the `UTF8` flag on string columns, so DuckDB reads them as `BLOB`. `ResultSet.getObject()` then returns a `DuckDBBlobResult` and `ResultSet.getString()` returns the bytes rendered as an escaped string rather than the expected text. Enable the [`binary_as_string`]({% link docs/current/data/parquet/overview.md %}) setting to read these columns as `VARCHAR`:

```java
try (Statement stmt = conn.createStatement()) {
    stmt.execute("SET binary_as_string = true;");
}
```

The same option can be passed to `read_parquet` directly, for example `read_parquet('file.parquet', binary_as_string = true)`.
