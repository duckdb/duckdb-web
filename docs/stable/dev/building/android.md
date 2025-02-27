---
layout: docu
redirect_from:
- /docs/dev/building/android
title: Android
---

DuckDB has experimental support for Android. Please use the latest `main` branch of DuckDB instead of the stable versions.

## Building the DuckDB Library Using the Android NDK

We provide build instructions for setups using macOS and Android Studio. For other setups, please adjust the steps accordingly.

1. Open [Android Studio](https://developer.android.com/studio).
   Select the **Tools** menu and pick **SDK Manager**.
   Select the SDK Tools tab and tick the **NDK (Side by side)** option.
   Click **OK** to install.

1. Set the Android NDK's location. For example:

   ```batch
   ANDROID_NDK=~/Library/Android/sdk/ndk/28.0.12433566/
   ```

1. Set the [Android ABI](https://developer.android.com/ndk/guides/abis). For example:

   ```batch
   ANDROID_ABI=arm64-v8a
   ```

   Or:

   ```batch
   ANDROID_ABI=x86_64
   ```

1. If you would like to use the [Ninja build system]({% link docs/stable/dev/building/overview.md %}#prerequisites), make sure it is installed and available on the `PATH`.

1. Set the list of DuckDB extensions to build. These will be statically linked in the binary. For example:

   ```batch
   DUCKDB_EXTENSIONS="icu;json;parquet"
   ```

1. Navigate to DuckDB's directory and run the build as follows:

   ```batch
   PLATFORM_NAME="android_${ANDROID_ABI}"
   BUILDDIR=./build/${PLATFORM_NAME}
   mkdir -p ${BUILDDIR}
   cd ${BUILDDIR}
   cmake \
       -G "Ninja" \
       -DEXTENSION_STATIC_BUILD=1 \
       -DDUCKDB_EXTRA_LINK_FLAGS="-llog" \
       -DBUILD_EXTENSIONS=${DUCKDB_EXTENSIONS} \
       -DENABLE_EXTENSION_AUTOLOADING=1 \
       -DENABLE_EXTENSION_AUTOINSTALL=1 \
       -DCMAKE_VERBOSE_MAKEFILE=on \
       -DANDROID_PLATFORM=${ANDROID_PLATFORM} \
       -DLOCAL_EXTENSION_REPO="" \
       -DOVERRIDE_GIT_DESCRIBE="" \
       -DDUCKDB_EXPLICIT_PLATFORM=${PLATFORM_NAME} \
       -DBUILD_UNITTESTS=0 \
       -DBUILD_SHELL=1 \
       -DANDROID_ABI=${ANDROID_ABI} \
       -DCMAKE_TOOLCHAIN_FILE=${ANDROID_NDK}/build/cmake/android.toolchain.cmake \
       -DCMAKE_BUILD_TYPE=Release ../..
   cmake \
       --build . \
       --config Release
   ```

1. For the `arm64-v8a` ABI, the build will produce the `build/android_arm64-v8a/duckdb` and `build/android_arm64-v8a/src/libduckdb.so` binaries.

## Building the CLI in Termux

1. To build the [command line client]({% link docs/stable/clients/cli/overview.md %}) in the [Termux application](https://termux.dev/), install the following packages:

   ```batch
   pkg install -y git ninja clang cmake python3
   ```

1. Set the list of DuckDB extensions to build. These will be statically linked in the binary. For example:

   ```batch
   DUCKDB_EXTENSIONS="icu;json"
   ```

1. Build DuckDB as follows:

   ```batch
   mkdir build
   cd build
   export LDFLAGS="-llog"
   cmake \
      -G "Ninja" \
      -DBUILD_EXTENSIONS="${DUCKDB_EXTENSIONS}" \
      -DDUCKDB_EXPLICIT_PLATFORM=linux_arm64_android \
      -DCMAKE_BUILD_TYPE=Release \
      ..
   cmake --build . --config Release
   ```

Note that you can also use the Python client on Termux:

```batch
pip install --pre --upgrade duckdb
```

## Troubleshooting

### Log Library Is Missing

**Problem:**
The build throws the following error:

```console
ld.lld: error: undefined symbol: __android_log_write
```

**Solution:**
Make sure the log library is linked:

```batch
export LDFLAGS="-llog"
```
