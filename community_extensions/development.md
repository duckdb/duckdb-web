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
With DuckDB's Community Extensions being a [relatively new](https://duckdb.org/2024/07/05/community-extensions.html) addition to the DuckDB ecosystem, developer documentation is currently
spread a little thin and mainly exists of READMEs in the [DuckDB repository](https://github.com/duckdb/duckdb), the [CI toolchain](https://github.com/duckdb/extension-ci-tools), the [extension template](https://github.com/duckdb/extension-template), and the [Community Repository](https://github.com/duckdb/community-extensions). 
However, because of the batteries-included nature of the extension template and the [large](/community_extensions.html) [amount](https://duckdb.org/docs/extensions/core_extensions.html) or example extensions,
extension development should be relatively straightforward.

## Getting Help
For extension development related questions, there is a dedicated channel in the [DuckDB Discord server](https://discord.com/invite/tcvwpjfnZx). The Discord server is
a great place to get help from other extension developers and the core DuckDB team. If you've found a bug or another type of issue with DuckDB, the extension template, or CI toolchain, please do just open an issue in the respective repository describing your issue.
Of course if you're not sure, you can always first check in the Discord channel if it's a real issue or just you [holding it wrong](https://www.wired.com/2010/06/iphone-4-holding-it-wrong/).
