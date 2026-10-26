---
layout: docu
redirect_from:
- /docs/dev/building/openharmony
- /docs/stable/dev/building/openharmony
- /docs/current/dev/building/openharmony
- /docs/lts/dev/building/openharmony
- /docs/preview/dev/building/openharmony
title: OpenHarmony
---

DuckDB supports building for OpenHarmony (OHOS) AArch64 (ARM64) on a best-effort basis.
On this platform, DuckDB reports the platform name `openharmony_arm64`.
Prebuilt binaries and extensions are not distributed for this platform.

## Prerequisites

DuckDB needs CMake, Ninja, and a C++17 compiler on the build host, plus the OpenHarmony SDK.
The Linux x64 SDK from the OpenHarmony release page can be used for cross-compilation.
The repository ships a toolchain file that handles both the Linux x64 SDK layout and the
on-device SDK layout.

Set `OHOS_SDK` to the `native` directory of the SDK:

```bash
export OHOS_SDK=/path/to/ohos-sdk/linux/native
```

## Cross-Compiling

Configure with the OpenHarmony toolchain file:

```bash
cmake -G Ninja -B build/openharmony \
    -DCMAKE_TOOLCHAIN_FILE="$PWD/scripts/ohos-toolchain.cmake" \
    -DCMAKE_BUILD_TYPE=Release \
    -DDUCKDB_EXPLICIT_PLATFORM=openharmony_arm64

cmake --build build/openharmony --parallel
```

`DUCKDB_EXPLICIT_PLATFORM` is required when cross-compiling because the platform probe
binary cannot run on the build host.
The resulting `build/openharmony/duckdb` is an AArch64 musl binary.

## Building on an OpenHarmony Device

On a device, CMake detects the OpenHarmony toolchain and the platform probe runs natively,
so `DUCKDB_EXPLICIT_PLATFORM` is not required:

```bash
cmake -G Ninja -B build/openharmony \
    -DCMAKE_TOOLCHAIN_FILE="$PWD/scripts/ohos-toolchain.cmake" \
    -DCMAKE_BUILD_TYPE=Release

cmake --build build/openharmony --parallel
./build/openharmony/duckdb -c "PRAGMA platform;"
```

## Notes

- The shell must not be stripped on OpenHarmony: the OS verifies the ELF `.codesign`
  section on exec.
- No prebuilt extensions are distributed for `openharmony_arm64`; build the extensions you
  need from source. `INSTALL <extension>` reports that no extension is available for this
  platform.
- The unittest binary is linked against the static DuckDB library on OpenHarmony because
  the shared library does not export the internal symbols used by the test helpers.
