---
layout: docu
redirect_from:
- /dev/sqllogictest/test_configuration
- /docs/dev/sqllogictest/test_configuration
- /docs/preview/dev/sqllogictest/test_configuration
- /docs/stable/dev/sqllogictest/test_configuration
title: Unit Tester Configuration
---

There are three ways of setting options for the unit tester:

* [Command Line Arguments](#command-line-arguments)
* [Configuration File](#configuration-file)
* [Environment Variables](#environment-variables)
* [Configuration Options List](#configuration-options-list)

See the [Configuration Options List](#configuration-options-list) for the full list of available options.

## Command Line Arguments

See the [Configuration Options List](#configuration-options-list) for all available options.

```bash
# booleans
unittest --checkpoint-on-shutdown
unittest --no-checkpoint-on-shutdown

# other types
unittest --checkpoint-wal-size 100000
```

Command line options `--settings`, `--on-init` and `--init-script` can be used to specify [DuckDB configuration]({% link docs/current/configuration/overview.md %}).

## Configuration File

A JSON file that can be passed in using `--test-config`.
See the [Configuration Options List](#configuration-options-list) for all available options, replacing `-` with `_`.

Example:

```json
{
   "checkpoint_wal_size": 100000,
   "checkpoint_on_shutdown": "false"
}
```

The following additional options can also be used in the configuration file:

| Option | Description |
|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `extends` | List of config files to extend from |
| `inherit_skip_tests` | Path of config to inherit 'skip_tests' from |
| `skip_tests` | Tests to be skipped |

Example:

```json
{
    "extends": ["base_config.json"],
    "inherit_skip_tests": "test/configs/force_storage.json",
    "skip_tests": [
        {
            "reason": "Contains explicit use of the memory catalog.",
            "paths": [
                "test/sql/attach/attach_use_rollback.test",
                "test/sql/function/list/lambdas/arrow/warn_deprecated_arrow.test",
                "test/sql/cte/warn_deprecated_union_in_using_key.test"
            ]
        }
    ]
}
```

## Environment Variables

Most [Configuration Options](#configuration-options-list) can also be set as environment variables, prefixed with `DUCKDB_TEST_`, upper-cased with underscores:

Example:

```bash
DUCKDB_TEST_CHECKPOINT_ON_SHUTDOWN=1 unittest
```

## Configuration Options List

The following configuration options are available:

| Option | Description |
|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--autoloading <none|available|all>` | Loading strategy for extensions not bundled in |
| `--base-config <path>` | Config file to load and base initial settings on |
| `--block-size <num>` | Block Allocation Size; must be a power of 2 |
| `--checkpoint-on-shutdown`, `--no-checkpoint-on-shutdown` | Whether or not to checkpoint on database shutdown |
| `--checkpoint-wal-size <num>` | Size in bytes after which to trigger automatic checkpointing |
| `--comment <string>` | Extra free form comment line |
| `--data-dir <path>` | Root dir for test data; default WORKING_DIR/data. Relative values resolve per test cwd; absolute/remote (e.g. `az://...`) values are used verbatim. |
| `--database-destroy <on|off|on-success>` | Default on-success: keep on failure |
| `--description <string>` | Config description |
| `--emit-on-skip` | Print a `SKIP_TEST` marker per skipped test |
| `--emit-test-events` | Writes JSON with test events to stderr |
| `--force-reload` | Force reload the test framework |
| `--force-restart`, `--no-force-restart` | Force restart the database between runs |
| `--force-storage` | Test with persistent storage file |
| `--init-script <path>` | SQL script to execute on init |
| `--initial-db <path>` | Initial database path |
| `--keep-home` | Use `$HOME/USERPROFILE` instead of the sandboxed temp-dir home |
| `--max-test-threads <num>` | Max threads to be used by the test runner itself (for e.g. concurrent loop) |
| `--max-threads <num>` | Max threads to use during tests |
| `--on-cleanup <string>` | SQL statements to execute on test end |
| `--on-init <string>` | SQL statements to execute on init |
| `--on-load <string>` | SQL statements to execute on explicit load |
| `--on-new-connection <string>` | SQL statements to execute on connection |
| `--one-initialize` | Initialize buffers with all 1; also see `--zero-initialize` |
| `--require <extension_name>` | If the extension is missing: fail rather than skip tests that require it |
| `--run-id <'auto'|<string>>` | Override per-run identity; the `RUN_ID` path level; shared across a run's tests; auto = generate |
| `--select-tag <string>` | Select tests which match named tag (as singleton set; multiple sets are OR'd) |
| `--select-tag-set <comma-separated strings>` | Select tests which match _all_ named tags (multiple sets are OR'd) |
| `--settings <list[struct]>` | Set [DuckDB configuration]({% link docs/current/configuration/overview.md %}), struct should have keys name and value |
| `--skip-compiled`, `--no-skip-compiled` | Skip compiled tests |
| `--skip-error-messages <comma-separated strings>` | Skip rather than fail tests that fail with a message that contains any of these substrings |
| `--skip-tag <string>` | Skip tests which match named tag (as singleton set; multiple sets are OR'd) |
| `--skip-tag-set <comma-separated strings>` | Skip tests which match _all_ named tags (multiple sets are OR'd) |
| `--sort-style <none|rowsort|valuesort>` | Default sort style if none is configured in the test |
| `--statically-loaded-extensions <comma-separated strings>` | Extensions to be loaded (from the statically available ones) |
| `--stdin` | Read a single sqllogictest script from stdin |
| `--storage-fuzzer`, `--no-storage-fuzzer` | Run storage fuzzer tests |
| `--storage-version <string>` | Database storage version to use by default |
| `--summarize-failures`, `--no-summarize-failures` | Print a summary of all test failures after running |
| `--temp-dir-base <path>` | Override root of the temp-dir tree; may be local or remote (e.g. `s3://`) |
| `--temp-dir-create <never|on-absent|always>` | Default on-absent: mkdir -p, no clobber |
| `--temp-dir-destroy <never|on-success|always>` | Default on-success: keep on failure |
| `--temp-dir-run-id <on|off>` | Is RUN_ID a path level? (default on) |
| `--temp-dir-test-id <on|off>` | Is TEST_ID (the test name) a path level? (default on) |
| `--test-config <path>` | Path to a [configuration file](#configuration-file) |
| `--test-dir <path>` | Override default working directory of test runner, available in tests as {WORKING_DIRECTORY} |
| `--test-env <list[struct]>` | The test variables, struct should have keys env_name and env_value |
| `--test-memory-leaks`, `--no-test-memory-leaks` | Run memory leak tests |
| `--verify-vector <string>` | Run vector verification for a specific vector type (options: dictionary_expression, dictionary_operator, constant_operator, sequence_operator, nested_shuffle, variant_vector) |
| `--zero-initialize` | Initialize buffers with all 0; also see `--one-initialize` |
