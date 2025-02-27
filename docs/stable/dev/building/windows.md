---
layout: docu
redirect_from:
- /docs/dev/building/windows
title: Windows
---

On Windows, DuckDB requires the [Microsoft Visual C++ Redistributable package](https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist) both as a build-time and runtime dependency. Note that unlike the build process on UNIX-like systems, the Windows builds directly call CMake.

## Visual Studio

To build DuckDB on Windows, we recommend using the Visual Studio compiler.
To use it, follow the instructions in the [CI workflow](https://github.com/duckdb/duckdb/blob/52b43b166091c82b3f04bf8af15f0ace18207a64/.github/workflows/Windows.yml#L73):

```batch
python scripts/windows_ci.py
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_GENERATOR_PLATFORM=x64 \
    -DENABLE_EXTENSION_AUTOLOADING=1 \
    -DENABLE_EXTENSION_AUTOINSTALL=1 \
    -DDUCKDB_EXTENSION_CONFIGS="${GITHUB_WORKSPACE}/.github/config/bundled_extensions.cmake" \
    -DDISABLE_UNITY=1 \
    -DOVERRIDE_GIT_DESCRIBE="$OVERRIDE_GIT_DESCRIBE"
cmake --build . --config Release --parallel
```

## MSYS2 and MinGW64

DuckDB on Windows can also be built with [MSYS2](https://www.msys2.org/) and [MinGW64](https://www.mingw-w64.org/).
Note that this build is only supported for compatibility reasons and should only be used if the Visual Studio build is not feasible on a given platform.
To build DuckDB with MinGW64, install the required dependencies using Pacman.
When prompted with `Enter a selection (default=all)`, select the default option by pressing `Enter`.

```batch
pacman -Syu git mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake mingw-w64-x86_64-ninja
git clone https://github.com/duckdb/duckdb
cd duckdb
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DBUILD_EXTENSIONS="icu;parquet;json"
cmake --build . --config Release
```

Once the build finishes successfully, you can find the `duckdb.exe` binary in the repository's directory:

```batch
./duckdb.exe
```

## Building the Go Client

Building on Windows may result in the following error:

```bash
go build
```

```console
collect2.exe: error: ld returned 5 exit status
```

GitHub user [vdmitriyev](https://github.com/vdmitriyev) shared instructions for [building the DuckDB Go client on Windows](https://github.com/marcboeker/go-duckdb/issues/4#issuecomment-2176409066):

1. Get four files (`.dll, .lib, .hpp, .h`) from the `libduckdb-windows-amd64.zip` archive.

2. Place them to, e.g.,: `C:\DuckDB-Go\libs\`.

3. Install the dependencies following the [`go-duckdb` project](https://github.com/marcboeker/go-duckdb).

4. Build your project using the following instructions:

   ```batch
   set PATH=C:\DuckDB-Go\libs\;%PATH%
   set CGO_CFLAGS=-IC:\DuckDB-Go\libs\
   set CGO_LDFLAGS=-LC:\DuckDB-Go\libs\ -lduckdb
   go build
   ```
