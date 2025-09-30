---
layout: docu
title: DuckDB Docker Container
---

DuckDB has an [official Docker image](https://github.com/duckdb/duckdb-docker), which supports both the arm64 (AArch64) and x86_64 (AMD64) architectures.

## Usage

To use the DuckDB Docker image, run:

```batch
docker run --rm -it -v "$(pwd):/workspace" -w /workspace duckdb/duckdb
```

## Using the DuckDB UI with Docker

To use the [DuckDB UI]({% link docs/preview/core_extensions/ui.md %}) with Docker, enable host networking.

> This setting forwards all ports from the container, so exercise caution and avoid it in secure environments.

```batch
docker run --rm -it -v "$(pwd):/workspace" -w /workspace --net host duckdb/duckdb
```

Then, launch the UI as follows:

```plsql
CALL start_ui();
```

To enable host networking in Docker Desktop, follow the instructions on the [Host network driver](https://docs.docker.com/engine/network/drivers/host/#docker-desktop) page.
