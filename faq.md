---
layout: docu
title: Frequently Asked Questions
---

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How to write my extension in Rust?

<div class="answer" markdown="1">

Writing a DuckDB extension in Rust is possible and [several](https://github.com/duckdb/community-extensions/blob/main/extensions/crypto/description.yml) [extensions](https://github.com/duckdb/community-extensions/blob/main/extensions/evalexpr_rhai/description.yml) [exist](https://github.com/duckdb/community-extensions/blob/main/extensions/prql/description.yml) [already](https://github.com/duckdb/duckdb_delta),
providing various examples to draw inspiration from.

Currently, writing a Rust-based DuckDB extension requires writing glue code in C++ and will force you to build through DuckDB's CMake & C++ based extension template.
We understand that this is not ideal and acknowledge the fact that Rust developers prefer to work on pure Rust codebases. For this (and many other) reason(s), an [Extension C-API](https://github.com/duckdb/duckdb/pull/12682) is
in development that will allow DuckDB extensions written in pure Rust. As the Extension C-API matures, a pure-Rust extension template will be made available.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How to write my extension in language X?

<div class="answer" markdown="1">

DuckDB's [Extension Template](https://github.com/duckdb/extension-template) is based on the DuckDB C++ API and uses DuckDB's CMake-based build system. The DuckDB team will currently 
only provide support for extensions written using this framework. However, note that CMake is pretty flexible: for example, several [Rust-based](#how-to-write-my-extension-in-rust) examples already exist. 

Additionally, a new [Extension C-API](https://github.com/duckdb/duckdb/pull/12682) is in development that will open the doors to extend DuckDB in more ways.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How are naming collisions between extensions handled?

<div class="answer" markdown="1">

Currently, DuckDB extensions need to be uniquely named. For this reason, PRs that introduce naming collisions will not be accepted and will require
a rename. To resolve this, manual namespacing would be the solution, for example by prefixing your vendor name to the extension name: `<vendor>_<extname>`.

Note that in general the DuckDB team reserves the right to refuse extension names, or force an extension rename. For example, when an extension is no longer actively
maintained, the DuckDB team may decide to rename or even remove the extension to make the name available for another extension. Don't worry though, we will
always contact the extension maintainers before taking such drastic actions.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### The CI toolchain is missing dependency X, now what?

<div class="answer" markdown="1">

The [toolchain](https://github.com/duckdb/extension-ci-tools) used to compile DuckDB extensions may not contain all build-time
dependencies required to build your extension. If this is the case, please just open a PR adding toolchain components as [optional extras](https://github.com/duckdb/extension-ci-tools/pull/53).

Alternatively, you can try adding the installation of the required dependencies through the [Makefile](https://github.com/duckdb/extension-template/blob/main/Makefile) in your extension repository. 
However, you should be warned that this could potentially lead to a more fragile build system with a corresponding increased maintainance load as DuckDB and its toolchain
is updated.

</div>

</div>