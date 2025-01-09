---
layout: community_extension_doc
title: Community Extension Development
---

## Building

DuckDB provides a C++ based [Extension Template](https://github.com/duckdb/extension-template) which comes batteries-included.
The template is configured with the package manager [vcpkg](https://vcpkg.io/), a SQL-based testing framework, and a GitHub Actions based CI/CD toolchain.
The CI/CD chain will automatically build your extension for all supported DuckDB platforms including Linux, MacOS, Windows and WASM.

## Publishing

To publish an extension in the DuckDB Community Repository, a Pull Request can be opened in the [Community Repository](https://github.com/duckdb/community-extensions). In the PR,
a descriptor file needs to be specified containing all the relevant information of the extension, such as its source repository and version. Checkout the [already existing community extensions](https://github.com/duckdb/community-extensions/tree/main/extensions) for examples.

The Community Repository builds extensions using DuckDB's [CI toolchain](https://github.com/duckdb/extension-ci-tools), this means that
for your extension needs to be buildable with this toolchain. Fortunately, this is the exact same toolchain as is used by the Extension Template, so
for extensions based on the template, this works out of the box.

## Developer Documentation

With DuckDB's Community Extensions being a [relatively new]({% post_url 2024-07-05-community-extensions %}) addition to the DuckDB ecosystem, there is currently limited developer documentation available. Information can be found in the following places:

* READMEs in the [DuckDB repository](https://github.com/duckdb/duckdb)
* [CI toolchain](https://github.com/duckdb/extension-ci-tools)
* [extension template](https://github.com/duckdb/extension-template)
* [Community Extensions Repository](https://github.com/duckdb/community-extensions)

However, because of the batteries-included nature of the extension template and the [large]({% link community_extensions/index.md %}) [amount]({% link docs/extensions/core_extensions.md %}) or example extensions, extension development should be relatively straightforward.

## Supported DuckDB Version and How to Maintain an Extension Through Releases

At this moment, community extensions aim to be built and distributed only for latest stable DuckDB release.
This means that users on any but the latest stable release will see community extensions as frozen in time, with no more updates being served.

When the next DuckDB release is near (see the [release calendar]({% link docs/dev/release_calendar.md %})), the [`duckdb/community-extensions` repository](https://github.com/duckdb/community-extensions/) switches to test extensions both versus the latest stable release *and* the current `main` branch.
If an extension is compatible both the latest stable release *and* the current `main` branch, the extension should not be impacted by new release.
This is the hopefully common case.

If an extension *not* compatible with both branches at the same time, the recommended path to update is the following:

1. Have two separate branches, one targeting the latest stable release and one targeting the `main` branch.
2. Provide the hash of the latest commit on the branch targeting stable as `ref` and the one from targeting main duckdb branch as `ref_next`.
3. This allows extension to be tested both versus latest stable *and* against current `main`.
4. Once a release hash is set, community extensions will be built for that DuckDB hash and `ref_next` (if present) swapped for `ref`.

See for example the descriptor for [`hannes/duckdb_avro`](https://github.com/hannes/duckdb_avro) that was published a few weeks before DuckDB v1.2.0.
It changed in <https://github.com/duckdb/community-extensions/pull/252/files> from:

```yaml
repo:
  github: hannes/duckdb_avro
  ref: e5ed59b6ccf915c65e17eb6286b9a64f3ab09f59
```

to:

```yaml
repo:
  github: hannes/duckdb_avro
  ref: e5ed59b6ccf915c65e17eb6286b9a64f3ab09f59
  ref_next: c8941c92ec103f7825eb88207c04512f8a714b23
```

Here `ref`, the commit is compatible with DuckDB version v1.1.3, and `ref_next` is compatible with current main.

Note that being compatible with current main can't guarantee compatibility with v1.2.0, since changes affecting the extension might still land, but it should allow to iterate early before a new stable DuckDB release.

## Getting Help

For extension development related questions, there is a dedicated channel in the [DuckDB Discord server](https://discord.com/invite/tcvwpjfnZx). The Discord server is
a great place to get help from other extension developers and the core DuckDB team. If you've found a bug or another type of issue with DuckDB, the extension template, or CI toolchain, please do just open an issue in the respective repository describing your issue.
Of course if you're not sure, you can always first check in the Discord channel if it's a real issue or just you [holding it wrong](https://www.wired.com/2010/06/iphone-4-holding-it-wrong/).
