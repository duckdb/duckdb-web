---
layout: community_extension_doc
title: Frequently Asked Questions
---


<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Are community extensions safe to install?

<div class="answer" markdown="1">

Similarly to other package management systems, DuckDB's Community Extensions repository contain community-contributed code,
therefore, there are no guarantees regarding the content of extensions.
The DuckDB Foundation and DuckDB Labs do not vet the code within community extensions and, therefore, cannot guarantee that DuckDB community extensions are safe to use.

For details on securing your DuckDB setup, please refer to the [Securing Extensions page]({% link docs/operations_manual/securing_duckdb/securing_extensions.md %}).
</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How can I secure my DuckDB setup when installing extensions?

<div class="answer" markdown="1">

The loading of community extensions can be explicitly disabled with the following one-way configuration option:

```sql
SET allow_community_extensions = false;
```

For details on securing your DuckDB setup, please refer to the [Securing Extensions page]({% link docs/operations_manual/securing_duckdb/securing_extensions.md %}).
</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Can I expose SQL macros as an extension?

<div class="answer" markdown="1">

Writing a DuckDB extension as a collection of SQL macro is already done be a few extensions. The [pivot_table]{% link community_extensions/extensions/pivot_table.md %} and [chsql]{% link community_extensions/extensions/chsql.md %} extensions for example follow this pattern.

Currently some C++ wrapper code is required, but this is possibly the simplest way to build a community extension AND the best way to package a set of utlity MACROs to be safely distributed.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Can I write extensions in Rust?

<div class="answer" markdown="1">

Writing a DuckDB extension in Rust is possible and [several](https://github.com/duckdb/community-extensions/blob/main/extensions/crypto/description.yml) [extensions](https://github.com/duckdb/community-extensions/blob/main/extensions/evalexpr_rhai/description.yml) [exist](https://github.com/duckdb/community-extensions/blob/main/extensions/prql/description.yml) [already](https://github.com/duckdb/duckdb_delta),
providing various examples to draw inspiration from.

Currently, writing a Rust-based DuckDB extension requires writing glue code in C++ and will force you to build through DuckDB's CMake & C++ based extension template.
We understand that this is not ideal and acknowledge the fact that Rust developers prefer to work on pure Rust codebases. For this (and many other) reason(s), a [C Extension API](https://github.com/duckdb/duckdb/pull/12682) is
in development that will allow DuckDB extensions written in pure Rust. As the C Extension API matures, a pure-Rust extension template will be made available.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### Can I write extensions in Go?

<div class="answer" markdown="1">

We are working on adding Go support for extensions.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How to write my extension in language X?

<div class="answer" markdown="1">

DuckDB's [Extension Template](https://github.com/duckdb/extension-template) is based on the DuckDB C++ API and uses DuckDB's CMake-based build system. The DuckDB team will currently only provide support for extensions written using this framework. However, note that CMake is pretty flexible: for example, several [Rust-based](#how-to-write-my-extension-in-rust) examples already exist.

Additionally, a new [C Extension API](https://github.com/duckdb/duckdb/pull/12682) is available since DuckDB v1.1.

</div>

</div>

<!-- Q&A entry -->

<div class="qa-wrap" markdown="1">

### How are naming collisions between extensions handled?

<div class="answer" markdown="1">

Currently, DuckDB extensions must have a uniquely name. For this reason, PRs that introduce naming collisions will not be accepted and will require
a rename. To resolve this, manual namespacing would be the solution, for example by prefixing your vendor name to the extension name: `⟨vendor⟩_⟨extname⟩`.

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
However, you should be warned that this could potentially lead to a more fragile build system with a corresponding increased maintainance load as DuckDB and its toolchain is updated.

</div>

</div>
