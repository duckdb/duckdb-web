---
layout: docu
redirect_from:
- /docs/dev/building/python
title: Python
---

The DuckDB Python package lives in the main [DuckDB source on GitHub](https://github.com/duckdb/duckdb/) under the `/tools/pythonpkg/` folder. It uses [pybind11](https://pybind11.readthedocs.io/en/stable/) to create Python bindings with DuckDB.

## Prerequisites

For everything described on this page we make the following assumptions:

1. You have a working copy of the DuckDB source (including the git tags) and you run commands from the root of the source.
2. You have a suitable Python installation available in a dedicated virtual environment.

### 1. DuckDB Repository

Make sure you have checked out the [DuckDB source](https://github.com/duckdb/duckdb/) and that you are in its root. E.g.:

```batch
git clone https://github.com/duckdb/duckdb
...
cd duckdb
```

If you've _forked_ DuckDB, you may run into trouble when building the Python package when you haven't pulled in the tags.

```batch
# Check your remotes
git remote -v

# If you don't see upstream git@github.com:duckdb/duckdb.git, then add it
git remote add upstream git@github.com:duckdb/duckdb.git

# Now you can pull & push the tags
git fetch --tags upstream
git push --tags
```

### 2. Python Virtual Environment

For everything described here you will need a suitable Python installation. While you technically might be able to use your system Python, we **strongly** recommend you use a Python virtual environment. A virtual environment isolates dependencies and, depending on the tooling you use, gives you control over which Python interpreter you use. This way you don't pollute your system-wide Python with the different packages you need for your projects.

While we use Python's built-in `venv` module in our examples below, and technically this might (or might not!) work for you, we also **strongly** recommend use a tool like [astral uv](https://docs.astral.sh/uv/) (or Poetry, conda, etc.) that allows you to manage _both_ Python interpreter versions and virtual environments.

Create and activate a virtual env as follows:

```batch
# Create a virtual environment in the .venv folder (in the duckdb source root)
python3 -m venv --prompt duckdb .venv

# Activate the virtual env
source .venv/bin/activate
```

Make sure you have a modern enough version of `pip` available in your virtual env:

```batch
# Print pip's help
python3 -m pip install --upgrade pip
```

If that fails with `No module named pip` and you use `uv`, then run:

```batch
# Install pip
uv pip install pip
```

## Building from Source

Below are a number of options to build the Python library from source, with or without debug symbols, and with a default or custom set of [extensions]({% link docs/stable/extensions/overview.md %}). Make sure to check out the [DuckDB build documentation]({% link docs/stable/dev/building/overview.md %}) if you run into trouble building the DuckDB main library.

### Default Release, Debug Build or Cloud Storage

The following will build the package with the default set of extensions (json, parquet, icu and core_functions).

#### Release Build

```batch
GEN=ninja BUILD_PYTHON=1 make release
```

#### Debug Build

```batch
GEN=ninja BUILD_PYTHON=1 make debug
```

#### Verify

```batch
python3 -c "import duckdb; print(duckdb.sql('SELECT 42').fetchall())"
```

### Adding Extensions

Before thinking about statically linking extensions you should know that the Python package currently doesn't handle linked in extensions very well. If you don't really need to have an extension baked in than the advice is to just stick to [installing them at runtime]({% link docs/stable/extensions/installing_extensions.md %}). See `tools/pythonpkg/duckdb_extension_config.cmake` for the default list of extensions that are built with the Python package. Any other extension should be considered problematic.

Having said that, if you do want to give it a try, here's how.

> For more details on building DuckDB extensions look at the [documentation]({% link docs/stable/dev/building/building_extensions.md %}).

The DuckDB build process follows the following logic for building extensions:

1. First compose the complete set of extensions that might be included in the build.
1. Then compose the complete set of extensions that should be excluded from the build.
1. Assemble the final set of extensions to be compiled by subtracting the set of excluded extensions from the set of included extensions.

The following mechanisms add to the set of **_included_ extensions**:

| Mechanism                                                                        | Syntax / Example                                                                                                                                                         |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Built-in extensions enabled by default**                                       | `extension/extension_config.cmake` (≈30 built-ins)                                                                                                                       |
| **Python package extensions enabled by default**                                 | `tools/pythonpkg/duckdb_extension_config.cmake` (`json;parquet;icu`)                                                                                                     |
| **Semicolon-separated include list**                                             | `DUCKDB_EXTENSIONS=fts;tpch;json`                                                                                                                                        |
| **Flags**                                                                        | `BUILD_TPCH=1`, `BUILD_JEMALLOC=1`, `BUILD_FTS=1`, …                                                                                                                     |
| **Presets**                                                                      | `BUILD_ALL_EXT=1` - Build all in-tree extensions<br/>`BUILD_ALL_IT_EXT=1` - _Only_ build in-tree extensions<br/>`BUILD_ALL_OOT_EXT=1` - Build all out-of-tree extensions |
| **Custom config file(s)**                                                        | `DUCKDB_EXTENSION_CONFIGS=path/to/my.cmake`                                                                                                                              |
| **Core-only overrides** <br/>_only relevant with `DISABLE_BUILTIN_EXTENSIONS=1`_ | `CORE_EXTENSIONS=httpfs;fts`                                                                                                                                             |

---

The following mechanisms add to the set of **_excluded_ extensions**:

| Mechanism                                                                                                                                                            | Syntax / Example                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Semicolon-separated skip list**                                                                                                                                    | `SKIP_EXTENSIONS=parquet;jemalloc`                 |
| **Flags**                                                                                                                                                            | `DISABLE_PARQUET=1`, `DISABLE_CORE_FUNCTIONS=1`, … |
| **“No built-ins” switch** <br/>_Throws out *every* statically linked extension **except** `core_functions`.  Use `CORE_EXTENSIONS=…` to whitelist a subset back in._ | `DISABLE_BUILTIN_EXTENSIONS=1`                     |

---

### Show All Installed Extensions

```batch
python3 -c "import duckdb; print(duckdb.sql('SELECT extension_name, installed, description FROM duckdb_extensions();'))"
```

## Development Environment

This section walks you through the following steps:

* Creating a CMake profile for development
* Debugging the Python extension code with lldb

You can do this either on the CLI or from an IDE. The documentation below shows the configuration for CLion, but you should be able to get it to work with other IDEs like VSCode as well.

### Debugging From the CLI

Run this to configure the CMake profile needed to debug on the CLI:

```batch
GEN=ninja BUILD_PYTHON=1 PYTHON_DEV=1 make debug
```

This will take care of the following:

* Builds both the main DuckDB library and the Python library with debug symbols.
* Generates a `compile-commands.json` file that includes CPython and pybind11 headers so that intellisense and clang-tidy checks work in your IDE.
* Installs the required Python dependencies in your virtual env.

Once the build completes, do a sanity check to make sure everything works:

```batch
python3 -c "import duckdb; print(duckdb.sql('SELECT 42').fetchall())"
```

### Debugging

The basic recipe is to start `lldb` with your virtual env's Python interpreter and your script, then set a breakpoint and run your script.
For example, given a script `dataframe.df` with the following contents:

```python
import duckdb
print(duckdb.sql("select * from range(1000)").df())
```

The following should work:

```batch
lldb -- .venv/bin/python3 my_script.py
```

```batch
# Set a breakpoint
(lldb) br s -n duckdb::DuckDBPyRelation::FetchDF
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
# The above warning is harmless - the library hasn't been imported yet

# Run the script
(lldb) r
...
    frame #0: 0x000000013025833c duckdb.cpython-310-darwin.so`duckdb::DuckDBPyRelation::FetchDF(this=0x00006000012f8d20, date_as_object=false) at pyrelation.cpp:808:7
   805   }
   806
   807   PandasDataFrame DuckDBPyRelation::FetchDF(bool date_as_object) {
-> 808     if (!result) {
   809       if (!rel) {
   810         return py::none();
   811       }
Target 0: (python3) stopped.
```

### Debugging in an IDE / CLion

You should be able to get debugging going in an IDE that support `lldb`. Below are the instructions for CLion but you can copy the settings for your favorite IDE.

#### Configure a CMake Debug Profile

The following CMake profile enables Intellisense and clang-tidy by generating a `compile-commands.json` file so your IDE knows how to inspect the source code, and makes sure that the Python package will be built and installed in your Python virtual env.

Under **Settings** | **Build, Execution, Deployment** | **CMake**, add a profile and set the fields as follows:

* **Name**: Debug
* **Build type**: Debug
* **Generator**:  Ninja
* **CMake Options** (on a single line):

   ```console
   -DCMAKE_PREFIX_PATH=$CMakeProjectDir$/.venv;$CMAKE_PREFIX_PATH
   -DPython3_EXECUTABLE=$CMakeProjectDir$/.venv/bin/python3
   -DBUILD_PYTHON=1
   -DPYTHON_DEV=1
   ```

#### Create a Run Config for Debugging

Under **Run** | **Edit Configurations...** create a new **CMake Application**. Use the following values:

* **Name**: Python Debug
* **Target**: `All targets`
* **Executable**: `[ABS_PATH_TO_YOUR_VENV]/bin/python3` (careful: this is a symlink and sometimes an IDE might try and follow it and fill in the path to the actual executable, but that will not work)
* **Program arguments**: `$FilePath$`
* **Working directory**: `$ProjectFileDir$`
* **Before Launch**: `Build` (this should already be set)

That should be enough: save and close.

Now you can set a breakpoint in a C++ file. You then open your Python script in your editor and use this config and run `Python Debug` in debug mode.

### Development and Stubs

`*.pyi` stubs in `duckdb-stubs` are manually maintained. The connection-related stubs are generated using dedicated scripts in `tools/pythonpkg/scripts/`:

* `generate_connection_stubs.py`
* `generate_connection_wrapper_stubs.py`

These stubs are important for autocomplete in many IDEs, as static-analysis based language servers can't introspect `duckdb`'s binary module.

To verify the stubs match the actual implementation:

```batch
python3 -m pytest tests/stubs
```

If you add new methods to the DuckDB Python API, you'll need to manually add corresponding type hints to the stub files.

### What are py::objects and a py::handles?

These are classes provided by pybind11, the library we use to manage our interaction with the Python environment.
`py::handle` is a direct wrapper around a raw PyObject* and does not manage any references.
`py::object` is similar to py::handle but it can handle refcounts.

I say *can* because it doesn't have to, using `py::reinterpret_borrow<py::object>(...)` we can create a non-owning `py::object`, this is essentially just a py::handle but py::handle can't be used if the prototype requires a `py::object`.

`py::reinterpret_steal<py::object>(...)` creates an owning `py::object`, this will increase the refcount of the python object and will decrease the refcount when the `py::object` goes out of scope.

When directly interacting with python functions that return a `PyObject*`, such as `PyDateTime_DATE_GET_TZINFO`, you should generally wrap the call in `py::reinterpret_steal` to take ownership of the returned object.

## Troubleshooting

### Pip Fails with `No names found, cannot describe anything`

If you've forked DuckDB you may run into trouble when building the Python package when you haven't pulled in the tags.

```batch
# Check your remotes
git remote -v

# If you don't see upstream git@github.com:duckdb/duckdb.git, then add it
git remote add upstream git@github.com:duckdb/duckdb.git

# Now you can pull & push the tags
git fetch --tags upstream
git push --tags
```

### Building with the httpfs Extension Fails

The build fails on OSX when both the [`httpfs` extension]({% link docs/stable/extensions/httpfs/overview.md %}) and the Python package are included:

```console
ld: library not found for -lcrypto
clang: error: linker command failed with exit code 1 (use -v to see invocation)
error: command '/usr/bin/clang++' failed with exit code 1
ninja: build stopped: subcommand failed.
make: *** [release] Error 1
```

Linking in the httpfs extension is problematic. Please install it at runtime, if you can.

### Importing DuckDB Fails with `symbol not found in flat namespace`

If you seen an error that looks like this:

```console
ImportError: dlopen(/usr/bin/python3/site-packages/duckdb/duckdb.cpython-311-darwin.so, 0x0002): symbol not found in flat namespace '_MD5_Final'
```

... then you've probably tried to link in a problematic extension. As mentioned above: `tools/pythonpkg/duckdb_extension_config.cmake` contains the default list of extensions that are built with the Python package. Any other extension might cause problems.

### Python Fails with `No module named 'duckdb.duckdb'`

If you're in `tools/pythonpkg` and try to `import duckdb` you might see:

```console
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/duckdb/tools/pythonpkg/duckdb/__init__.py", line 4, in <module>
    import duckdb.functional as functional
  File "/duckdb/tools/pythonpkg/duckdb/functional/__init__.py", line 1, in <module>
    from duckdb.duckdb.functional import (
ModuleNotFoundError: No module named 'duckdb.duckdb'
```

This is because Python imported from the `duckdb` directory (i.e. `tools/pythonpkg/duckdb/`), rather than from the installed package. You should start your interpreter from a different directory instead.
