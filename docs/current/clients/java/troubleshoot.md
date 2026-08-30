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

This behavior is tracked in [duckdb-java issue #113](https://github.com/duckdb/duckdb-java/issues/113).

## Native Image: `NoSuchMethodError` When Opening a Connection

In a [GraalVM Native Image]({% link docs/current/clients/java/deploy_native_image.md %}) executable, opening the first connection may fail with:

```console
Exception in thread "main" java.lang.ExceptionInInitializerError
    ...
Caused by: java.lang.NoSuchMethodError: ⟨class and method⟩
    at com.oracle.svm.core.jni.functions.JNIFunctions$Support.getMethodID(JNIFunctions.java)
    ...
```

The driver resolves its entire JNI surface eagerly when its native library initializes, so a single class, method, or field missing from the reachability metadata fails the whole initialization. This indicates that the metadata compiled into the image is missing or older than the driver: upgrade to a driver version that ships its own metadata, or regenerate the metadata with the tracing agent against the exact driver version in use.

The error is sometimes wrapped in a misleading message:

```console
java.lang.UnsatisfiedLinkError: Unsupported JNI version 0xffffffff, required by ⟨path⟩/libduckdb_java.⟨suffix⟩
```

This is what the library's `JNI_OnLoad` reports when an internal lookup failed, and the cause is the same missing metadata, not a JNI version problem.

## Native Image: `UnsatisfiedLinkError: Can't load library`

In a Native Image executable, the first connection may fail with:

```console
java.lang.UnsatisfiedLinkError: Can't load library: duckdb_java | java.library.path = [.]
    ...
Caused by: java.io.FileNotFoundException: DuckDB JNI library not found, path: '⟨path⟩/libduckdb_java.⟨suffix⟩'
```

The shared library was neither embedded in the executable nor found next to it. Either add a resource entry for your platform's library or place the library file beside the executable. Both options are described on the [Deploy as Native Image]({% link docs/current/clients/java/deploy_native_image.md %}) page.

## Warning about a Restricted Method in `java.lang.System`

On JDK 24 and later, loading the driver prints:

```console
WARNING: A restricted method in java.lang.System has been called
WARNING: java.lang.System::load has been called by org.duckdb.DuckDBNative ...
WARNING: Use --enable-native-access=ALL-UNNAMED to avoid a warning for callers in this module
```

This is the JDK's [native access integrity check](https://openjdk.org/jeps/472) and is harmless. Silence it by running the JVM with `--enable-native-access=ALL-UNNAMED`, or the module name of the driver if you place it on the module path. Future JDK releases will turn this warning into an error, so adding the flag is recommended.

## Further Reading

* [Deploy as Native Image]({% link docs/current/clients/java/deploy_native_image.md %}) — building standalone executables with GraalVM, including both ways to provide the shared library.
* [Java (JDBC) Client]({% link docs/current/clients/java/overview.md %}) — installing the driver from Maven Central, the fix for the driver-not-found errors above.
* [Define Connections]({% link docs/current/clients/java/connecting.md %}) — driver registration, configuration options, and instance behavior behind many connection-time errors.
* [Parquet Files]({% link docs/current/data/parquet/overview.md %}) — the `binary_as_string` setting and other options for reading Parquet string columns correctly.
