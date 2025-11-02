---
layout: docu
redirect_from:
- /docs/dev/building/python
title: Python
---

The DuckDB Python package has its own repository at [`duckdb/duckdb-python`](https://github.com/duckdb/duckdb-python) and uses [pybind11](https://pybind11.readthedocs.io/en/stable/) to create Python bindings with DuckDB.

## Prerequisites

This guide assumes:

1. You have a working copy of the DuckDB Python package source (including git submodules and tags)
2. You have [Astral UV](https://docs.astral.sh/uv/) version >= 0.8.0 installed
3. You run commands from the root of the `duckdb-python` source

We are opinionated about using **Astral UV** for Python environment and dependency management. While using pip for a development environment with an editable install without build isolation is possible, we don't provide guidance for that approach in this guide.

We use **CLion** as our IDE. This guide doesn't include specific instructions for other IDEs, but the setup should be similar.

### 1. DuckDB Python Repository

Start by [forking `duckdb-python`](https://github.com/duckdb/duckdb-python/fork) into a personal repository, then clone your fork:

```bash
git clone --recurse-submodules ⟨YOUR_FORK_URL⟩
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
- DuckDB is vendored as a git submodule and must be initialized
- DuckDB version determination depends on local availability of git tags
- If switching between branches with different submodule refs, add the git hooks:

```bash
git config --local core.hooksPath .githooks/
```

### 2. Install Astral uv

[Install uv](https://docs.astral.sh/uv/getting-started/installation/) version >= 0.8.0.

## Development Environment Setup

### 1. Platform-Specific Setup

**All Platforms:**
- Python 3.9+ supported
- uv >= 0.8.0 required
- CMake and Ninja (installed via UV)
- C++ compiler toolchain

**Linux (Ubuntu 24.04):**

```bash
sudo apt-get update
sudo apt-get install ccache
```

**macOS:**

```bash
# Xcode command line tools
xcode-select --install
```

**Windows:**
- Visual Studio 2019+ with C++ support
- Git for Windows

### 2. Install Dependencies and Build

Set up the development environment in two steps:

```bash
# Install all development dependencies without building the project
uv sync --no-install-project

# Build and install the project without build isolation
uv sync --no-build-isolation
```

**Why two steps?**
- `uv sync` performs editable installs by default with scikit-build-core using a persistent build-dir
- The build happens in an isolated, ephemeral environment where cmake's paths point to non-existing directories
- Installing dependencies first, then building without isolation ensures proper cmake integration

### 3. Enable Pre-Commit Hooks

We run a number of linting, formatting and type-checking in CI. You can run all of these manually, but to make your life easier you can install the exact same checks we run in CI as git hooks with pre-commit, which is already installed as part of the dev dependencies:

```bash
uvx pre-commit install
```

This will run all required checks before letting your commit pass.

You can also install a post-checkout hook that always runs `git submodule update --init --recursive`. When you change branches between main and a bugfix branch, this makes sure the duckdb submodule is always correctly initialized:

```bash
uvx pre-commit install --hook-type post-checkout
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

Run with coverage (compiles extension with `--coverage` for C++ coverage):

```bash
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
  --root "$PWD" \
  --filter "${PWD}/src/duckdb_py" \
  --exclude '.*/\.cache/.*' \
  --gcov-exclude '.*/\.cache/.*' \
  --gcov-exclude '.*/external/.*' \
  --gcov-exclude '.*/site-packages/.*' \
  --exclude-unreachable-branches \
  --exclude-throw-branches \
  --html --html-details -o coverage-cpp.html \
  build/coverage/src/duckdb_py \
  --print-summary
```

### Building Wheels

Build wheel for your system:

```bash
uv build
```

Build for specific Python version:

```bash
uv build -p 3.9
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

- **Name:** Debug
- **Build type:** Debug  
- **Generator:** Ninja
- **CMake Options:**
  ```text
  -DCMAKE_PREFIX_PATH=$CMakeProjectDir$/.venv;$CMAKE_PREFIX_PATH
  ```

### Python Debug Configuration  

Create a **CMake Application** run configuration:

- **Name:** Python Debug
- **Target:** `All targets`
- **Executable:** `[PROJECT_DIR]/.venv/bin/python3`
- **Program arguments:** `$FilePath$`
- **Working directory:** `$ProjectFileDir$`

This allows setting C++ breakpoints and debugging Python scripts that use the DuckDB extension.

## Debugging

### Command Line Debugging

Set breakpoints and debug with lldb:

```bash
# Example Python script (test.py)
# import duckdb
# print(duckdb.sql("select * from range(1000)").df())

lldb -- .venv/bin/python3 test.py
```

In lldb:

```bash
# Set breakpoint (library loads when imported)
(lldb) br s -n duckdb::DuckDBPyRelation::FetchDF
(lldb) r
```

## Cross-Platform Testing

You can run the packaging workflow manually on your fork for any branch, choosing platforms and test suites via the GitHub Actions web interface.

## Troubleshooting

### Build Issues

**Missing git tags:** If you forked DuckDB Python, ensure you have the upstream tags:

```bash
git remote add upstream https://github.com/duckdb/duckdb-python.git
git fetch --tags upstream
git push --tags
```

### Platform-Specific Issues

**Windows compilation:** Ensure you have Visual Studio 2019+ with C++ support installed.
