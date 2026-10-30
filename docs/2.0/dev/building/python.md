---
layout: docu
redirect_from:
- /docs/dev/building/python
- /docs/stable/dev/building/python
- /docs/current/dev/building/python
- /docs/lts/dev/building/python
- /docs/preview/dev/building/python
title: Python
---

The DuckDB Python package has its own repository at [`duckdb/duckdb-python`](https://github.com/duckdb/duckdb-python) and uses [nanobind](https://nanobind.readthedocs.io/) 3 to create Python bindings with DuckDB.

## Prerequisites

This guide assumes:

1. You have a full clone of the DuckDB Python package source, including its git submodule
2. You have [Astral UV](https://docs.astral.sh/uv/) version >= 0.8.0 installed
3. You run commands from the root of the `duckdb-python` source

We are opinionated about using **Astral UV** for Python environment and dependency management. While using pip for a development environment with an editable install without build isolation is possible, we don't provide guidance for that approach in this guide.

We use **CLion** as our IDE. This guide doesn't include specific instructions for other IDEs, but the setup should be similar.

### 1. DuckDB Python Repository

Start by [forking `duckdb-python`](https://github.com/duckdb/duckdb-python/fork) into a personal repository, then clone your fork:

```bash
git clone --recurse-submodules YOUR_FORK_URL
cd duckdb-python
git remote add upstream https://github.com/duckdb/duckdb-python.git
git fetch --all
```

If you've already cloned without submodules:

```bash
git submodule update --init --recursive
git remote add upstream https://github.com/duckdb/duckdb-python.git
git fetch --all
```

**Important notes:**
* DuckDB is vendored as a git submodule and must be initialized, otherwise the build fails with `RuntimeError: Duckdb submodule not initialized`
* The package version is the `release_version` in `pyproject.toml` followed by `.dev` and the time of the latest commit across the repository and the submodule, as `yymmddhhmm` in UTC, for example `2.0.0.dev2610201323`. No git tags are read. The DuckDB version is computed from the number of commits in the submodule, so do not make a shallow clone

### 2. Install Astral uv

[Install uv](https://docs.astral.sh/uv/getting-started/installation/) version >= 0.8.0.

## Development Environment Setup

### 1. Platform-Specific Setup

#### All Platforms

* Python 3.11 or later; free-threaded builds of CPython are not supported
* uv >= 0.8.0 required
* CMake, Ninja, nanobind, and the NumPy headers (installed via UV)
* C++ compiler toolchain

#### Linux

On Ubuntu, install the following packages:

```bash
sudo apt-get update
sudo apt-get install ccache gcc-16 g++-16
```

On Fedora, Red Hat, Amazon Linux, etc., run:

```bash
sudo dnf install ccache gcc gcc-c++
```

Make sure the compiler are set using:

```bash
export CC=gcc-16
export CXX=g++-16
```

#### macOS

Make sure that you have Xcode command line tools installed:

```bash
xcode-select --install
```

#### Windows

Ensure you have the following installed:

* Visual Studio 2019+ with C++ support
* Git for Windows

### 2. Install Dependencies and Build

Set up the development environment in two steps:

```bash
# Install the build dependencies without building the project
uv sync --only-group build --no-install-project -p 3.13

# Build and install the project without build isolation
uv sync --no-build-isolation -v --reinstall -p 3.13
```

The result is an editable Debug build in `build/debug/`. Editable builds use the full CPython API; only wheels use the stable ABI.

**Why two steps?**
* `uv sync` performs editable installs by default with scikit-build-core using a persistent build-dir
* The build happens in an isolated, ephemeral environment where cmake's paths point to non-existing directories
* Installing dependencies first, then building without isolation ensures proper cmake integration

### 3. Enable Pre-Commit Hooks

We run a number of linting, formatting, and type-checking in CI. You can run all of these manually, but to make your life easier you can install the exact same checks we run in CI as git hooks with [pre-commit](https://pre-commit.com). Install it pinned to Python 3.12, so the hooks do not depend on your build interpreter:

```bash
uv tool install --python 3.12 pre-commit
pre-commit install
```

This will run all required checks before letting your commit pass. To run them across the tree, use `pre-commit run --all-files`.

You can also install a post-checkout hook that always runs `git submodule update --init --recursive`. When you change branches between main and a bugfix branch, this makes sure the `duckdb` submodule is always correctly initialized:

```bash
pre-commit install --hook-type post-checkout
```

### 4. Verify Installation

```bash
uv run python -c "import duckdb; print(duckdb.sql('SELECT 42').fetchall())"
```

## Development Workflow

### Running Tests

Run all tests:

```bash
uv run --no-build-isolation pytest ./tests --verbose
```

Run fast tests only (excludes slow directory):

```bash
uv run --no-build-isolation pytest ./tests --verbose --ignore=./tests/slow
```

### Test Coverage

Build with coverage (compiles the extension with `--coverage` into `build/coverage/` for C++ coverage), then run the tests under coverage:

```bash
COVERAGE=1 uv sync --no-build-isolation -v --reinstall -p 3.13
COVERAGE=1 uv run --no-build-isolation coverage run -m pytest ./tests --verbose
```

Check Python coverage:

```bash
uv run coverage html -d htmlcov-python
uv run coverage report --format=markdown
```

Check C++ coverage:

```bash
uv run gcovr \
  --gcov-ignore-errors all \
  --gcov-ignore-parse-errors=negative_hits.warn_once_per_file \
  --root "$PWD" \
  --filter "${PWD}/src" \
  --exclude '.*/\.cache/.*' \
  --gcov-exclude '.*/\.cache/.*' \
  --gcov-exclude '.*/external/.*' \
  --gcov-exclude '.*/site-packages/.*' \
  --exclude-unreachable-branches \
  --exclude-throw-branches \
  --html --html-details -o coverage-cpp.html \
  build/coverage/src \
  --print-summary
```

### Building Wheels

Build an sdist and a wheel for your system:

```bash
uv build
```

On CPython 3.12 and later, the wheel is tagged `cp312-abi3`: it uses the stable ABI and serves 3.12 and every later version. On CPython 3.11, the wheel is specific to that version. Build for a specific Python version:

```bash
uv build -p 3.11
```

To install the wheel, run:

```bash
uv pip install dist/duckdb-*.whl
```

### Cleaning Build Artifacts

```bash
uv cache clean
rm -rf build .venv uv.lock
```

## IDE Setup (CLion)

For CLion users, the project can be configured for C++ debugging of the Python extension:

### CMake Profile Configuration

In **Settings** → **Build, Execution, Deployment** → **CMake**, create a Debug profile:

* **Name:** Debug
* **Build type:** Debug
* **Generator:** Ninja
* **CMake Options:**
  ```text
  -DCMAKE_PREFIX_PATH=$CMakeProjectDir$/.venv;$CMAKE_PREFIX_PATH
  ```

### Python Debug Configuration

Create a **CMake Application** run configuration:

* **Name:** Python Debug
* **Target:** `All targets`
* **Executable:** `⟨PROJECT_DIR⟩/.venv/bin/python3`{:.language-sql .highlight}
* **Program arguments:** `$FilePath$`
* **Working directory:** `$ProjectFileDir$`

This allows setting C++ breakpoints and debugging Python scripts that use the DuckDB extension.

## Debugging

### Command Line Debugging

Set breakpoints and debug with lldb:

```bash
# Example Python script (test.py)
# import duckdb
# print(duckdb.sql("SELECT * FROM range(1000)").df())

lldb -- .venv/bin/python3 test.py
```

In lldb:

```bash
# Set breakpoint (library loads when imported)
(lldb) br s -n duckdb::DuckDBPyResult::FetchDF
(lldb) r
```

## Cross-Platform Testing

You can run the Packaging workflow manually on your fork for any branch via the GitHub Actions web interface. Its inputs choose a minimal set of wheels or all of them, the test suite to run (none, fast, or all), the commits of the package and of the DuckDB submodule to build, and a forced package or DuckDB version.

## Troubleshooting

### Build Issues

**Missing submodule:** If the build fails with `RuntimeError: Duckdb submodule not initialized`, initialize the submodule:

```bash
git submodule update --init --recursive
```
