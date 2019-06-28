---
layout: default
title: Installation
selected: Documentation/Installation
---
# Installation From Source
The source code of DuckDB can be found [here](https://github.com/cwida/duckdb).

## Requirements
DuckDB requires CMake to be installed and a C++11 compliant compiler. GCC 4.9 and newer, Clang 3.9 and newer and VisualStudio 2017 are tested on each revision.
## Compiling
Run ``make`` in the root directory to compile the sources. For development, use ``make debug`` to build a non-optimized debug version. You may run make unit and make allunit to verify that your version works properly after making changes.

On systems without GNU Make (e.g. Windows), you can directly use ``CMake`` to generate project files for your compiler or IDE of choice (e.g. Visual Studio).
## Usage
A command line utility based on sqlite3 can be found in either build/release/tools/shell/shell (release, the default) or build/debug/tools/shell/shell (debug).

## Embedding
As DuckDB is an embedded database, there is no database server to launch or client to connect to a running server. However, the database server can be embedded directly into an application using the C or C++ bindings. The main build process creates the shared library build/release/src/libduckdb.[so|dylib|dll] that can be linked against. A static library is built as well.

For examples on how to embed DuckDB into your application, see the [examples](https://github.com/cwida/duckdb/tree/master/examples) folder in the repository.
