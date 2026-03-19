---
layout: docu
redirect_from:
- /docs/preview/dev/building/unofficial_and_unsupported_platforms
title: Unofficial and Unsupported Platforms
---

> Warning The platforms listed on this page are not officially supported.
> The build instructions are provided on a best-effort basis.
> Community contributions are very welcome.

DuckDB is built and distributed for several platforms with [different levels of support]({% link docs/current/dev/building/overview.md %}).
DuckDB _can be built_ for other platforms with varying levels of success.
This page provides an overview of these with the intent to clarify which platforms can be expected to work.

## 32-bit Architectures

[32-bit architectures](https://en.wikipedia.org/wiki/32-bit_computing) are officially not supported but it is possible to build DuckDB manually for some of these platforms.
For example, see the build instructions for [32-bit Raspberry Pi boards]({% link docs/current/dev/building/raspberry_pi.md %}#raspberry-pi-32-bit).

Note that 32-bit platforms are limited to using 4 GiB RAM due to the amount of addressable memory.

## Big-Endian Architectures

[Big-endian architectures](https://en.wikipedia.org/wiki/Endianness) (such as PowerPC) are [not supported](https://duckdblabs.com/community_support_policy#architectures) by DuckDB.
While DuckDB can likely be built on such architectures,
the resulting binary may exhibit [correctness](https://github.com/duckdb/duckdb/issues/5548) [errors](https://github.com/duckdb/duckdb/issues/9714) on certain operations.
Therefore, its use is not recommended.

## RISC-V Architectures

### Native Build (Recommended)

DuckDB builds natively on RISC-V 64-bit boards without any special flags. Tested on a [BananaPi F3](https://wiki.banana-pi.org/Banana_Pi_BPI-F3) ([SpacemiT K1](https://www.spacemit.com/key-stone-k1), rv64gc, 8 cores @ 1.6 GHz, 16 GB RAM) running Debian Trixie:

```bash
sudo apt-get update
sudo apt-get install -y git g++ cmake ninja-build
git clone --depth=1 https://github.com/duckdb/duckdb
cd duckdb
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

Build time is approximately 2 hours on an 8-core SpacemiT K1. The resulting binary works out of the box:

```bash
./duckdb -c “SELECT 'Hello from RISC-V' AS message;”
```

```text
┌───────────────────┐
│      message      │
│      varchar      │
├───────────────────┤
│ Hello from RISC-V │
└───────────────────┘
```

Aggregation queries work as expected:

```bash
./duckdb -c “CREATE TABLE test AS SELECT range AS id, range * 3.14 AS value FROM range(1000);
SELECT count(*) AS cnt, round(avg(value), 2) AS avg_val FROM test;”
```

```text
┌───────┬─────────┐
│  cnt  │ avg_val │
│ int64 │ double  │
├───────┼─────────┤
│  1000 │ 1568.43 │
└───────┴─────────┘
```

The DuckDB Python package also builds successfully from source on riscv64:

```bash
pip install duckdb --no-binary duckdb
```

### Build with RVV (RISC-V Vector Extension)

On boards with [RVV 1.0](https://github.com/riscvarchive/riscv-v-spec) support (e.g., [SpacemiT K3](https://www.spacemit.com/key-stone-k3) with vlen 256), you can enable vector instructions for better performance. The user [“LivingLinux” on Bluesky](https://bsky.app/profile/livinglinux.bsky.social) [built DuckDB](https://bsky.app/profile/livinglinux.bsky.social/post/3lak5q7mmg42j) with RVV and [published a video about it](https://www.youtube.com/watch?v=G6uVDH3kvNQ):

```bash
GEN=ninja \
    CC='gcc-14 -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CXX='g++-14 -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    BUILD_EXTENSIONS='fts' \
    make
```

### Cross-Compilation

For those who do not have RISC-V hardware, you can cross-compile DuckDB using the [riscv-gnu-toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain):

```bash
GEN=ninja \
    CC='riscv64-linux-gnu-gcc -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    CXX='riscv64-linux-gnu-g++ -march=rv64gcv_zicsr_zifencei_zihintpause_zvl256b' \
    make
```

For more reference information on DuckDB RISC-V cross-compiling, see the [mocusez/duckdb-riscv-ci](https://github.com/mocusez/duckdb-riscv-ci) and [DuckDB Pull Request #16549](https://github.com/duckdb/duckdb/pull/16549).
