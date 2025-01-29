---
layout: docu
title: Raspberry Pi
---

## Raspberry Pi (64-bit)

DuckDB can be built for 64-bit Raspberry Pi boards. First, install the required build packages:

```batch
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build
```

Then, clone and build it as follows:

```bash
git clone https://github.com/duckdb/duckdb
cd duckdb
GEN=ninja CORE_EXTENSIONS="icu;json" make
```

Finally, run it:

```batch
build/release/duckdb
```

## Raspberry Pi 32-bit

On 32-bit Raspberry Pi boards, you need to add the [`-latomic` link flag](https://github.com/duckdb/duckdb/issues/13855#issuecomment-2341539339).
As extensions are not distributed for this platform, it's recommended to also include them in the build.
For example:

```batch
mkdir build
cd build
cmake .. \
    -DCORE_EXTENSIONS="httpfs;json;parquet" \
    -DDUCKDB_EXTRA_LINK_FLAGS="-latomic"
make -j4
```
