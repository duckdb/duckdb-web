---
layout: docu
title: Deploy as Native Image
---

## Overview

The JDBC driver runs inside [GraalVM Native Image](https://www.graalvm.org/latest/reference-manual/native-image/) executables. Graal Native Image compiles a Java application ahead of time into a standalone binary that starts in milliseconds and requires no JVM on the target machine, which suits command line tools, serverless functions, and small containers.

Recent driver versions ship the JNI reachability metadata that `native-image` needs, and the build picks it up automatically from the class path. 

Two things remain for the application to configure: native access and the location of DuckDB's shared library.

> Driver versions up to and including 1.5.5 do not ship this metadata. For those versions, generate it by running the application once on the JVM with the [tracing agent](https://www.graalvm.org/latest/reference-manual/native-image/metadata/AutomaticMetadataCollection/):
>
> ```bash
> java -agentlib:native-image-agent=config-output-dir=⟨config_dir⟩ -cp ⟨classpath⟩ ⟨MainClass⟩
> ```
>
> Next, pass the directory to the build with `-H:ConfigurationFileDirectories=⟨config_dir⟩`.

## Requirements

GraalVM for JDK 22 or later is required. Older GraalVM releases initialize the driver's classes at image build time, which bakes a build machine path into the executable and fails at run time with `UnsatisfiedLinkError`.

Pass `--enable-native-access=ALL-UNNAMED` to `native-image`, or add it as a build argument in the [Native Build Tools](https://graalvm.github.io/native-build-tools/latest/index.html) Maven or Gradle plugin.

Load the driver explicitly before opening the first connection:

```java
Class.forName("org.duckdb.DuckDBDriver");
```

Driver auto-registration through `ServiceLoader` is not always visible to Graal Native Image's closed world analysis, and the explicit load makes registration deterministic.

## Providing the Shared Library

DuckDB's engine is a native library bundled inside the driver JAR, one file per platform. Choose one of two ways to make it available to the executable.

### Option 1: Embed the Library in the Executable

Add a resource entry naming your platform's library, either in a configuration directory passed via `-H:ConfigurationFileDirectories` or under `META-INF/native-image` in your own project:

```json
{ "resources": { "includes": [ { "pattern": "libduckdb_java\\.so_linux_amd64" } ] } }
```

The bundled library names are `libduckdb_java.so_linux_amd64`, `libduckdb_java.so_linux_arm64`, `libduckdb_java.so_osx_universal`, and `libduckdb_java.so_windows_amd64`. 

Name the one for your target platform explicitly. A wildcard matching all of them adds roughly 260 MB to the executable.

This option produces a single self contained file, around 120 MB. The driver extracts the library to a temporary directory when the first connection opens, which adds up to a second of startup time and requires a writable temporary directory.

### Option 2: Ship the Library Next to the Executable

Build without any resource entry and place the shared library in the same directory as the executable. The file works under its bundled name, for example `libduckdb_java.so_linux_amd64`, or under the platform convention: `libduckdb_java.so` on Linux, `libduckdb_java.dylib` on macOS, `duckdb_java.dll` on Windows. The lookup is anchored to the executable rather than the working directory, so the program runs correctly from anywhere.

This option produces a small executable, under 20 MB for a simple application, with no extraction cost when connections open. The library can be extracted from the driver JAR, or taken from the `-nolib` distribution together with its separate library artifact.

## Building

A minimal build, with the driver JAR in the current directory:

```bash
javac -cp duckdb_jdbc-⟨version⟩.jar App.java
native-image --no-fallback --enable-native-access=ALL-UNNAMED \
    -cp duckdb_jdbc-⟨version⟩.jar:. -o app App
```

`--no-fallback` makes the build fail outright instead of producing an image that still requires a JVM. For Maven and Gradle projects, the [Native Build Tools](https://graalvm.github.io/native-build-tools/latest/index.html) plugins wrap the same build and run it during `mvn package` or `gradle nativeCompile`.

## Further Reading

* [Troubleshoot]({% link docs/current/clients/java/troubleshoot.md %}) — the Native Image errors that indicate missing metadata or a missing shared library.
* [Define Connections]({% link docs/current/clients/java/connecting.md %}) — driver registration and connection configuration.
* [Java (JDBC) Client]({% link docs/current/clients/java/overview.md %}) — installing the driver from Maven Central.