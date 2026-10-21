---
layout: docu
redirect_from:
- /docs/dev/building/windows
- /docs/stable/dev/building/windows
- /docs/current/dev/building/windows
- /docs/lts/dev/building/windows
- /docs/preview/dev/building/windows
title: Windows
---

On Windows, DuckDB requires the [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) both as a build-time and runtime dependency. Note that unlike the build process on UNIX-like systems, the Windows builds directly call CMake.

## Clang-cl

To build DuckDB on Windows, we recommend using the [`clang-cl` compiler](https://clang.llvm.org/docs/MSVCCompatibility.html) with the Visual Studio build tools (MSVC toolchain, Windows SDK and linker). This is the setup used by DuckDB's [CI workflow](https://github.com/duckdb/duckdb/blob/d54cbbe3df17e8e5ce68312f483b4155836112aa/.github/workflows/Windows.yml#L30).

1. Install [Visual Studio](https://visualstudio.microsoft.com/downloads/) (or the Build Tools for Visual Studio) with the “Desktop development with C++” workload and the “C++ Clang Compiler for Windows” component. You also need Python, CMake, Ninja and a Bash shell with GNU Make (e.g., Git Bash with `make` installed).
2. Open a shell where the Visual Studio environment variables are set (e.g., the “x64 Native Tools Command Prompt” or a shell started from it).
3. Run the following commands in a Bash shell from the root of the DuckDB repository:

   ```bash
   export GEN=ninja
   export CC=clang-cl
   export CXX=clang-cl
   python scripts/windows_ci.py
   make windows_release
   ```

The `make windows_release` target invokes CMake with the bundled extensions configuration (`.github/config/bundled_extensions.cmake`) and builds DuckDB in `Release` mode.

## MSYS2 and MinGW64

DuckDB on Windows can also be built with [MSYS2](https://www.msys2.org/) and [MinGW64](https://www.mingw-w64.org/).
Note that this build is only supported for compatibility reasons and should only be used if the `clang-cl` build is not feasible on a given platform.
To build DuckDB with MinGW64, install the required dependencies using Pacman.
When prompted with `Enter a selection (default=all)`, select the default option by pressing `Enter`.

```bash
pacman -Syu git mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake mingw-w64-x86_64-ninja
git clone https://github.com/duckdb/duckdb
cd duckdb
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DBUILD_EXTENSIONS="icu;parquet;json"
cmake --build . --config Release
```

Once the build finishes successfully, you can find the `duckdb.exe` binary in the repository's directory:

```bash
./duckdb.exe
```

## Building the Go Client

Building on Windows may result in the following error:

```batch
go build
```

```console
collect2.exe: error: ld returned 5 exit status
```

GitHub user [vdmitriyev](https://github.com/vdmitriyev) shared instructions for [building the DuckDB Go client on Windows](https://github.com/marcboeker/go-duckdb/issues/4#issuecomment-2176409066):

1. Get four files (`.dll, .lib, .hpp, .h`) from the `libduckdb-windows-amd64.zip` archive.

2. Place them to, e.g.,: `C:\duckdb-go\libs\`.

3. Install the dependencies following the [`duckdb-go` project](https://github.com/duckdb/duckdb-go).

4. Build your project using the following instructions:

   ```bash
   set PATH=C:\duckdb-go\libs\;%PATH%
   set CGO_CFLAGS=-IC:\duckdb-go\libs\
   set CGO_LDFLAGS=-LC:\duckdb-go\libs\ -lduckdb
   go build
   ```
