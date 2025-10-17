---
layout: default
title: DuckDB Preview (Nightly) Installation
excerpt: DuckDB preview installation page
redirect_from:
- install/nightly
- install/nightlies
---

## DuckDB Preview (Nightly) Installation

### Command Line Interface (CLI)

| Platform | Architecture   | Download                                                                        |
| -------- | -------------- | ------------------------------------------------------------------------------- |
| Linux    | x86_64         | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-linux-amd64.zip) |
| Linux    | arm64          | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-linux-arm64.zip) |
| macOS    | arm64 / x86_64 | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-osx.zip)         |
| Windows  | arm64 / x86_64 | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-windows.zip)     |

### Python

```batch
pip install duckdb --pre --upgrade
```

### R

```R
install.packages("pak")
pak::pak("duckdb/duckdb-r")
```

### Java

Maven:

```xml
<dependencies>
  <dependency>
    <groupId>org.duckdb</groupId>
    <artifactId>duckdb_jdbc</artifactId>
    <version>1.5.0-SNAPSHOT</version>
  </dependency>
</dependencies>
<repositories>
  <repository>
    <id>oss-sonatype</id>
    <name>oss-sonatype</name>
    <url>https://oss.sonatype.org/content/repositories/snapshots/</url>
    <snapshots>
      <enabled>true</enabled>
    </snapshots>
  </repository>
</repositories>
```

[Direct Download (JAR)](https://artifacts.duckdb.org/duckdb-java/latest/java-jars.zip)

### Node.js

```batch
npm install duckdb@next
```

> The nightly release of the Node.js driver installs the old (deprecated) Node.js driver and not DuckDB Node Neo. For the Node Neo driver, the nightly release is currently not available.

### C / C++

| Platform | Architecture   | Download                                                                        |
| -------- | -------------- | ------------------------------------------------------------------------------- |
| Linux    | x86_64         | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-linux-amd64.zip) |
| Linux    | arm64          | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-linux-arm64.zip) |
| macOS    | arm64 / x86_64 | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-osx.zip)         |
| Windows  | arm64 / x86_64 | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-windows.zip)     |

### ODBC

| Platform | Architecture   | Download                                                                          |
| -------- | -------------- | --------------------------------------------------------------------------------- |
| Linux    | x86_64         | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-linux-amd64.zip)    |
| Linux    | arm64          | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-linux-arm64.zip)    |
| macOS    | arm64 / x86_64 | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-osx-universal.zip)  |
| Windows  | arm64 / x86_64 | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-windows-amd64.zip') |
