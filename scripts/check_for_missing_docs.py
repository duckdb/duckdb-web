#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from re import escape

import duckdb
from ripgrepy import Ripgrepy

docs_root = str(Path(__file__).parent.parent / "docs")

ignored_functions = {
    # difficult to check for docs for
    "*",
    "+",
    "-",
    "/",
    "||",
    "|",
    "~",
    "^",
    "**",
    # part of extensions
    "dsdgen",
    "dbgen",
    "tpch_queries",
    "tpcds_answers",
    "tpcds_queries",
    "tpch_answers",
    # only used in python bindings
    "pandas_scan",
    "python_map_function",
    # only used in JDBC bindings
    "arrow_scan_dumb",
}

functions = duckdb.default_connection.execute(
    "select distinct function_name from duckdb_functions()",
).fetchall()

functions = sorted(list({function for (function,) in functions} - ignored_functions))


def check_function(function):
    run = Ripgrepy(f"\\W{escape(function)}\\W", docs_root).json().run()
    return function, bool(run.as_dict)


for function, good in ThreadPoolExecutor(10).map(check_function, functions):
    if not good:
        print(function)
