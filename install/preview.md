---
layout: default
title: DuckDB Preview (Alpha/Nightly) Installation
excerpt: DuckDB preview installation page
body_class: blog_typography nightly_install
max_page_width: medium
redirect_from:
  - /preview
  - /nightly
  - /nightlies
  - /install/nightly
  - /install/nightlies
---

<div class="wrap pagetitle pagetitle--small">
  <div class="pagetitle-heading" role="heading" aria-level="1">DuckDB Preview (Alpha/Nightly) Installation</div>
</div>

> Alpha releases currently cannot load [community extensions]({% link community_extensions/index.md %}).

The preview (nightly) builds provide development versions of DuckDB. As such, they are constantly in flux and they are less suitable for production use than the stable releases of DuckDB. You should only use these releases if you are looking for [recent bugfixes](https://github.com/duckdb/duckdb/pulls?q=is%3Apr+is%3Amerged) or optimizations.

There are currently the following DuckDB versions under development:

* v1.5: a regular release with extended support to allow users sufficient time to transition to v2.0.
* v2.0: an LTS release.
* v2.1: the upcoming DuckDB version, in an early stage of the development.

Note that for most users, we recommend the [stable DuckDB releases]({% link docs/2.0/installation.html %}).

## Python

For Python, we distribute different nightly builds. Note that not all of them are available at all times and a few days can be skipped when nightly builds fail.


### Python v1.5-dev

```batch
pip install "duckdb<1.6.0" --pre --upgrade
```

### Python v2.0-dev

```batch
pip install "duckdb<2.1.0" --pre --upgrade
```

### Python v2.1-dev

```batch
pip install duckdb --pre --upgrade
```

## Command Line Interface (CLI) Client

### CLI v1.5-dev

To download the v1.5-dev command line client, use the following links:

| Platform | Architecture       | v1.5-dev CLI client                                                                |
| -------- | ------------------ | ---------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-arm64.zip) |
| Linux    | `x86_64`           | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-amd64.zip) |
| macOS    | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-osx.zip)         |
| Windows  | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-windows.zip)     |

### CLI v2.0-dev

#### v2.0-dev macOS and Linux Install Script

To install the preview build on Linux and macOS, run:

```bash
curl https://install.duckdb.org | DUCKDB_VERSION=alpha bash
```

#### v2.0-dev Windows PowerShell Script

To install the preview build on Windows, run:

```powershell
$env:DUCKDB_VERSION = "alpha"; irm https://install.duckdb.org/install.ps1 | iex
```

#### v2.0-dev CLI Packages

To download the v2.0-dev command line client, use the following links:

| Platform | Architecture       | v2.0-dev CLI client                                                                    |
| -------- | ------------------ | -------------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-cli-linux-arm64.tar.gz)   |
| Linux    | `x86_64`           | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-cli-linux-amd64.tar.gz)   |
| macOS    | `arm64` / `x86_64` | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-cli-osx-universal.tar.gz) |
| Windows  | `arm64`            | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-cli-windows-arm64.tar.gz) |
| Windows  | `x86_64`           | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-cli-windows-amd64.tar.gz) |

### CLI v2.1-dev

To download the v2.1-dev command line client, use the following links:

| Platform | Architecture       | v2.1-dev CLI client                                                         |
| -------- | ------------------ | --------------------------------------------------------------------------- |
| Linux    | `arm64`            | [tar.gz](https://artifacts.duckdb.org/main/duckdb-cli-linux-arm64.tar.gz)   |
| Linux    | `x86_64`           | [tar.gz](https://artifacts.duckdb.org/main/duckdb-cli-linux-amd64.tar.gz)   |
| macOS    | `arm64` / `x86_64` | [tar.gz](https://artifacts.duckdb.org/main/duckdb-cli-osx-universal.tar.gz) |
| Windows  | `arm64`            | [tar.gz](https://artifacts.duckdb.org/main/duckdb-cli-windows-arm64.tar.gz) |
| Windows  | `x86_64`           | [tar.gz](https://artifacts.duckdb.org/main/duckdb-cli-windows-amd64.tar.gz) |

## Java

The following snippets import the latest preview builds of the Java package.
To determine the version number, please visit the [latest CI builds](https://github.com/duckdb/duckdb-java/actions/workflows/Java.yml) and search for a _Java JDBC_ task that succeeded on the `v2.0-cyanoptera` branch (for v2.0-dev) or the `main` branch (for v2.1-dev).
In that job, consult the _Maven S3 Deploy_ job's _Deploy snapshot to S3_ task and find the version tag, e.g., `{{ site.latest_duckdb_java_dev_version }}`.

### Java v2.0-dev

#### Maven

```xml
<dependencies>
    <dependency>
        <groupId>org.duckdb</groupId>
        <artifactId>duckdb_jdbc</artifactId>
        <version>{{ site.latest_duckdb_java_dev_version }}</version>
    </dependency>
</dependencies>

<repositories>
    <repository>
        <id>duckdb</id>
        <url>https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/</url>
    </repository>
</repositories>
```

#### Gradle (Groovy)

```groovy
repositories {
    maven {
        url 'https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/'
    }
}

dependencies {
    implementation 'org.duckdb:duckdb_jdbc:{{ site.latest_duckdb_java_dev_version }}'
}
```

#### Gradle (Kotlin)

```kotlin
repositories {
    maven {
        url = uri("https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/")
    }
}

dependencies {
    implementation("org.duckdb:duckdb_jdbc:{{ site.latest_duckdb_java_dev_version }}")
}
```

#### Direct Download

<a href="https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/org/duckdb/duckdb_jdbc/{{ site.latest_duckdb_java_dev_version }}/duckdb_jdbc-{{ site.latest_duckdb_java_dev_version }}.jar" class="download-btn">duckdb_jdbc-{{ site.latest_duckdb_java_dev_version }}.jar</a>

### Java v2.1-dev

The Java v2.1-dev release is currently not available.

{% comment %}
#### Maven

```xml
<dependencies>
    <dependency>
        <groupId>org.duckdb</groupId>
        <artifactId>duckdb_jdbc</artifactId>
        <version>{{ site.next_duckdb_java_dev_version }}</version>
    </dependency>
</dependencies>

<repositories>
    <repository>
        <id>duckdb</id>
        <url>https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/</url>
    </repository>
</repositories>
```

#### Gradle (Groovy)

```groovy
repositories {
    maven {
        url 'https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/'
    }
}

dependencies {
    implementation 'org.duckdb:duckdb_jdbc:{{ site.next_duckdb_java_dev_version }}'
}
```

#### Gradle (Kotlin)

```kotlin
repositories {
    maven {
        url = uri("https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/")
    }
}

dependencies {
    implementation("org.duckdb:duckdb_jdbc:{{ site.next_duckdb_java_dev_version }}")
}
```

#### Direct Download

<a href="https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven/org/duckdb/duckdb_jdbc/{{ site.next_duckdb_java_dev_version }}/duckdb_jdbc-{{ site.next_duckdb_java_dev_version }}.jar" class="download-btn">duckdb_jdbc-{{ site.next_duckdb_java_dev_version }}.jar</a>
{% endcomment %}

## ODBC

For ODBC, the preview builds are based on the `main` branch of the [`duckdb/duckdb-odbc` repository](https://github.com/duckdb/duckdb-odbc/).

| Platform | Architecture | ODBC client                                                                 |
| -------- | ------------ | --------------------------------------------------------------------------- |
| Linux    | `arm64`      | [zip](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-linux-arm64.zip)   |
| Linux    | `x86_64`     | [zip](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-linux-amd64.zip)   |
| macOS    | `arm64`      | [zip](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-macos-arm64.zip)   |
| macOS    | `x86_64`     | [zip](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-macos-amd64.zip)   |
| Windows  | `arm64`      | [zip](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-windows-arm64.zip) |
| Windows  | `x86_64`     | [zip](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-windows-amd64.zip) |

## R

In R, run the following to install the latest DuckDB from source based on the `main` branch of the [`duckdb/duckdb-r` repository](https://github.com/duckdb/duckdb-r/).

```R
install.packages("pak")
pak::pak("duckdb/duckdb-r")
```

## C/C++ Libraries

### v1.5-dev C/C++ Libraries

To download the C/C++ libraries, use the following links:

| Platform | Architecture       | v1.5-dev C/C++ library                                                             |
| -------- | ------------------ | ---------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-arm64.zip) |
| Linux    | `x86_64`           | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-amd64.zip) |
| macOS    | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-osx.zip)         |
| Windows  | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-windows.zip)     |


### v2.0-dev C/C++ Libraries

To download the v2.0-dev C/C++ libraries, use the following links:

| Platform | Architecture       | v2.0-dev C/C++ library                                                                         |
| -------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-shared-libs-linux-arm64.tar.gz)   |
| Linux    | `x86_64`           | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-shared-libs-linux-amd64.tar.gz)   |
| macOS    | `arm64` / `x86_64` | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-shared-libs-osx-universal.tar.gz) |
| Windows  | `arm64`            | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-shared-libs-windows-arm64.tar.gz) |
| Windows  | `x86_64`           | [tar.gz](https://artifacts.duckdb.org/v2.0-cyanoptera/duckdb-shared-libs-windows-amd64.tar.gz) |

## Node.js (Neo)

For the DuckDB Node Neo driver, the nightly release is currently not available.
