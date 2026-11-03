---
layout: docu
redirect_from:
- /docs/guides/python/install
- /docs/stable/guides/python/install
- /docs/current/guides/python/install
- /docs/lts/guides/python/install
- /docs/preview/guides/python/install
title: Installing the Python Client
how_to_topic: python
---

## Installing via Pip

The Python client requires Python 3.11 or later. On Python 3.10, `pip` does not report an error: it installs a 1.x release instead, and with `--pre` a 1.x development build.

The latest release of the Python client can be installed using `pip`.

```batch
pip install duckdb
```

The pre-release Python client (known as the “preview” or “nightly” build) can be installed using `--pre`.

```batch
pip install duckdb --upgrade --pre
```

## Installing from Source

Follow the [Python build guide]({% link docs/2.0/dev/building/python.md %}).
