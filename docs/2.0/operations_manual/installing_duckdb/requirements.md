---
layout: docu
redirect_from:
- /docs/current/operations_manual/installing_duckdb/requirements
- /docs/lts/operations_manual/installing_duckdb/requirements
- /docs/preview/operations_manual/installing_duckdb/requirements
title: Requirements
---

DuckDB is designed to be [portable]({% link why_duckdb.md %}#portable) and has very few runtime dependencies. Still, there are a few requirements to be aware of before installing or running DuckDB.

## Supported Platforms

DuckDB officially supports Linux, macOS and Windows on both x86_64 (AMD64) and AArch64 (ARM64) CPU architectures. Official binaries are distributed for these platforms for both the latest stable version and the preview version (nightly build).

| Platform name   | Operating system | Architecture    | CPU types                      | Support level |
| --------------- | ---------------- | --------------- | ------------------------------ | ------------- |
| `linux_amd64`   | Linux            | x86_64 (AMD64)  | Intel, AMD, etc.               | Full          |
| `linux_arm64`   | Linux            | AArch64 (ARM64) | AWS Graviton, Snapdragon, etc. | Full          |
| `osx_amd64`     | macOS 12+        | x86_64 (AMD64)  | Intel                          | Partial       |
| `osx_arm64`     | macOS 12+        | AArch64 (ARM64) | Apple Silicon M1, M2, etc.     | Full          |
| `windows_amd64` | Windows 10+      | x86_64 (AMD64)  | Intel, AMD, etc.               | Full          |
| `windows_arm64` | Windows 10+      | AArch64 (ARM64) | Copilot+ PC with Qualcomm CPU  | Full          |

> Warning macOS on Intel CPUs (`osx_amd64`) is only partially supported. DuckDB binaries and [core extensions]({% link docs/2.0/core_extensions/overview.md %}) are still distributed for this platform but, starting with DuckDB 2.0.0, [community extensions]({% link docs/2.0/extensions/community_extensions.md %}) are no longer built for it. DuckDB 2.1 will stop supporting `osx_amd64`.

DuckDB can also run on other platforms, such as Linux distributions using musl libc (e.g., Alpine Linux), Android and WebAssembly, with varying levels of support. For details, see the [list of platforms on the “Building DuckDB” page]({% link docs/2.0/dev/building/overview.md %}#platforms). For the platforms extensions are distributed for, see the [“Extension Distribution” page]({% link docs/2.0/extensions/extension_distribution.md %}#platforms).

## Linux

DuckDB's official Linux binaries require [glibc](https://www.gnu.org/software/libc/) 2.28 or newer. Since DuckDB 1.3.0, the official Linux binaries are [built using the `manylinux_2_28` image](https://github.com/duckdb/duckdb/pull/16956), which combines an older glibc with a newer compiler. As a result, extensions are no longer distributed for the `linux_amd64_gcc4` platform.

Most mainstream Linux distributions ship with [glibc 2.28](https://lists.gnu.org/archive/html/info-gnu/2018-08/msg00000.html) or newer, so no action is needed on these systems. If you need to run DuckDB on a system with an older glibc, you can [build DuckDB from source]({% link docs/2.0/dev/building/overview.md %}) against that version.
