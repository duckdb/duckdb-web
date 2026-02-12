from dataclasses import dataclass, field


@dataclass
class PythonRelAPIParamDetails:
    # configure param details
    parameter_name: str = None
    parameter_type: list[str] = None
    parameter_default: str | None = None
    parameter_description: str | None = None


@dataclass
class PythonRelAPIDetails:
    # Configure details for each method
    additional_description: str = ""  # text to be appended to the method description
    aliases: list[str] = None  # list of methods the methods is alias of
    parameters: list[PythonRelAPIParamDetails] = None  # method parameter description
    example: str = (
        None  # either an entire example code, either the code to be placed in DEFAULT_EXAMPLE
    )
    use_default_example: bool = (
        True  # True if it the example should be used in DEFAULT_EXAMPLE
    )
    result: str = None  # the result of the example code execution
    result_type: str = "text"  # how the result to be presented (text, sql)


DEFAULT_EXAMPLE = '''```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

{code_example}
```
'''

PLACEHOLDER_EXAMPLE = "```python\n{code_example}\n```"
PLACEHOLDER_RESULT = "```{result_type}\n{result}\n```"

CREATION_METHODS_MAP = {
    "from_arrow": PythonRelAPIDetails(
        example="""
import duckdb
import pyarrow as pa

ids = pa.array([1], type=pa.int8())
texts = pa.array(['a'], type=pa.string())
example_table = pa.table([ids, texts], names=["id", "text"])

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_arrow(example_table)

rel.show()
""",
        result="""
┌──────┬─────────┐
│  id  │  text   │
│ int8 │ varchar │
├──────┼─────────┤
│    1 │ a       │
└──────┴─────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="arrow_object",
                parameter_type=["pyarrow.Table", "pyarrow.RecordBatch"],
                parameter_description="Arrow object to create a relation from",
            )
        ],
    ),
    "from_csv_auto": PythonRelAPIDetails(
        example="""
import csv
import duckdb

duckdb_conn = duckdb.connect()

with open('code_example.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '1', 'text': 'a'})

rel = duckdb_conn.from_csv_auto("code_example.csv")

rel.show()
""",
        result="""
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        use_default_example=False,
        aliases=["read_csv"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="path_or_buffer",
                parameter_type=["Union[str, StringIO, TextIOBase]"],
                parameter_description="Path to the CSV file or buffer to read from.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="header",
                parameter_type=["Optional[bool], Optional[int]"],
                parameter_default=None,
                parameter_description="Row number(s) to use as the column names, or None if no header.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Compression type (e.g., 'gzip', 'bz2').",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sep",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Delimiter to use; defaults to comma.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="delimiter",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Alternative delimiter to use.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="dtype",
                parameter_type=["Optional[Dict[str, str]], Optional[List[str]]"],
                parameter_default=None,
                parameter_description="Data types for columns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="na_values",
                parameter_type=["Optional[str], Optional[List[str]]"],
                parameter_default=None,
                parameter_description="Additional strings to recognize as NA/NaN.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="skiprows",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Number of rows to skip at the start.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="quotechar",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character used to quote fields.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="escapechar",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character used to escape delimiter or quote characters.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="encoding",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Encoding to use for UTF when reading/writing.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="parallel",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Enable parallel reading.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="date_format",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Format to parse dates.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="timestamp_format",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Format to parse timestamps.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sample_size",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Number of rows to sample for schema inference.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="all_varchar",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Treat all columns as VARCHAR.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="normalize_names",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Normalize column names to lowercase.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="null_padding",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Enable null padding for rows with missing columns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="names",
                parameter_type=["Optional[List[str]]"],
                parameter_default=None,
                parameter_description="List of column names to use.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="lineterminator",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character to break lines on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="columns",
                parameter_type=["Optional[Dict[str, str]]"],
                parameter_default=None,
                parameter_description="Column mapping for schema.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="auto_type_candidates",
                parameter_type=["Optional[List[str]]"],
                parameter_default=None,
                parameter_description="List of columns for automatic type inference.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="max_line_size",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Maximum line size in bytes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="ignore_errors",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Ignore parsing errors.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="store_rejects",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Store rejected rows.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="rejects_table",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Table name to store rejected rows.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="rejects_scan",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Scan to use for rejects.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="rejects_limit",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Limit number of rejects stored.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="force_not_null",
                parameter_type=["Optional[List[str]]"],
                parameter_default=None,
                parameter_description="List of columns to force as NOT NULL.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="buffer_size",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Buffer size in bytes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="decimal",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character to recognize as decimal point.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="allow_quoted_nulls",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Allow quoted NULL values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="filename",
                parameter_type=["Optional[bool], Optional[str]"],
                parameter_default=None,
                parameter_description="Add filename column or specify filename.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_partitioning",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Enable Hive-style partitioning.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="union_by_name",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Union files by column name instead of position.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_types",
                parameter_type=["Optional[Dict[str, str]]"],
                parameter_default=None,
                parameter_description="Hive types for columns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_types_autocast",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Automatically cast Hive types.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="connection",
                parameter_type=["DuckDBPyConnection"],
                parameter_description="DuckDB connection to use.",
            ),
        ],
    ),
    "from_df": PythonRelAPIDetails(
        example="""
import duckdb
import pandas as pd

df = pd.DataFrame(data = {'id': [1], "text":["a"]})

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_df(df)

rel.show()
""",
        result="""
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="df",
                parameter_type=["pandas.DataFrame"],
                parameter_description="A pandas DataFrame to be converted into a DuckDB relation.",
            )
        ],
    ),
    "from_parquet": PythonRelAPIDetails(
        example="""
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ids = pa.array([1], type=pa.int8())
texts = pa.array(['a'], type=pa.string())
example_table = pa.table([ids, texts], names=["id", "text"])

pq.write_table(example_table, "code_example.parquet")

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_parquet("code_example.parquet")

rel.show()
""",
        result="""
┌──────┬─────────┐
│  id  │  text   │
│ int8 │ varchar │
├──────┼─────────┤
│    1 │ a       │
└──────┴─────────┘
""",
        use_default_example=False,
        aliases=["read_parquet"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="file_glob",
                parameter_type=["str"],
                parameter_description="File path or glob pattern pointing to Parquet files to be read.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="binary_as_string",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Interpret binary columns as strings instead of blobs.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="file_row_number",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Add a column containing the row number within each file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="filename",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Add a column containing the name of the file each row came from.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_partitioning",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Enable automatic detection of Hive-style partitions in file paths.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="union_by_name",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Union Parquet files by matching column names instead of positions.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["object"],
                parameter_description="Optional compression codec to use when reading the Parquet files.",
            ),
        ],
    ),
    "from_query": PythonRelAPIDetails(
        additional_description="""

> **Warning.** Passing `params` to this method is [discouraged]({% link docs/stable/clients/python/known_issues.md %}#parameterized-queries-in-relational-api) due to significant performance overhead. Use [`execute()`]({% link docs/stable/clients/python/dbapi.md %}#prepared-statements) for parameterized queries instead.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_query("from range(1,2) tbl(id)")

rel.show()
""",
        result="""
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        use_default_example=False,
        aliases=["query", "sql"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="query",
                parameter_type=["object"],
                parameter_description="The SQL query or subquery to be executed and converted into a relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="alias",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional alias name to assign to the resulting relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="params",
                parameter_type=["object"],
                parameter_description="Optional query parameters. **Discouraged** due to [significant performance overhead]({% link docs/stable/clients/python/known_issues.md %}#parameterized-queries-in-relational-api). Use [`execute()`]({% link docs/stable/clients/python/dbapi.md %}#prepared-statements) for parameterized queries instead.",
            ),
        ],
    ),
    "query": PythonRelAPIDetails(
        additional_description="""

> **Warning.** Passing `params` to this method is [discouraged]({% link docs/stable/clients/python/known_issues.md %}#parameterized-queries-in-relational-api) due to significant performance overhead. Use [`execute()`]({% link docs/stable/clients/python/dbapi.md %}#prepared-statements) for parameterized queries instead.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.query("from range(1,2) tbl(id)")

rel.show()
""",
        result="""
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        use_default_example=False,
        aliases=["from_query", "sql"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="query",
                parameter_type=["object"],
                parameter_description="The SQL query or subquery to be executed and converted into a relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="alias",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional alias name to assign to the resulting relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="params",
                parameter_type=["object"],
                parameter_description="Optional query parameters. **Discouraged** due to [significant performance overhead]({% link docs/stable/clients/python/known_issues.md %}#parameterized-queries-in-relational-api). Use [`execute()`]({% link docs/stable/clients/python/dbapi.md %}#prepared-statements) for parameterized queries instead.",
            ),
        ],
    ),
    "read_csv": PythonRelAPIDetails(
        example="""
import csv
import duckdb

duckdb_conn = duckdb.connect()

with open('code_example.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '1', 'text': 'a'})

rel = duckdb_conn.read_csv("code_example.csv")

rel.show()
""",
        result="""
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        use_default_example=False,
        aliases=["from_csv_auto"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="path_or_buffer",
                parameter_type=["Union[str, StringIO, TextIOBase]"],
                parameter_description="Path to the CSV file or buffer to read from.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="header",
                parameter_type=["Optional[bool], Optional[int]"],
                parameter_default=None,
                parameter_description="Row number(s) to use as the column names, or None if no header.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Compression type (e.g., 'gzip', 'bz2').",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sep",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Delimiter to use; defaults to comma.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="delimiter",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Alternative delimiter to use.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="dtype",
                parameter_type=["Optional[Dict[str, str]], Optional[List[str]]"],
                parameter_default=None,
                parameter_description="Data types for columns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="na_values",
                parameter_type=["Optional[str], Optional[List[str]]"],
                parameter_default=None,
                parameter_description="Additional strings to recognize as NA/NaN.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="skiprows",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Number of rows to skip at the start.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="quotechar",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character used to quote fields.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="escapechar",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character used to escape delimiter or quote characters.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="encoding",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Encoding to use for UTF when reading/writing.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="parallel",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Enable parallel reading.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="date_format",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Format to parse dates.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="timestamp_format",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Format to parse timestamps.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sample_size",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Number of rows to sample for schema inference.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="all_varchar",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Treat all columns as VARCHAR.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="normalize_names",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Normalize column names to lowercase.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="null_padding",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Enable null padding for rows with missing columns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="names",
                parameter_type=["Optional[List[str]]"],
                parameter_default=None,
                parameter_description="List of column names to use.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="lineterminator",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character to break lines on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="columns",
                parameter_type=["Optional[Dict[str, str]]"],
                parameter_default=None,
                parameter_description="Column mapping for schema.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="auto_type_candidates",
                parameter_type=["Optional[List[str]]"],
                parameter_default=None,
                parameter_description="List of columns for automatic type inference.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="max_line_size",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Maximum line size in bytes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="ignore_errors",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Ignore parsing errors.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="store_rejects",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Store rejected rows.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="rejects_table",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Table name to store rejected rows.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="rejects_scan",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Scan to use for rejects.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="rejects_limit",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Limit number of rejects stored.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="force_not_null",
                parameter_type=["Optional[List[str]]"],
                parameter_default=None,
                parameter_description="List of columns to force as NOT NULL.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="buffer_size",
                parameter_type=["Optional[int]"],
                parameter_default=None,
                parameter_description="Buffer size in bytes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="decimal",
                parameter_type=["Optional[str]"],
                parameter_default=None,
                parameter_description="Character to recognize as decimal point.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="allow_quoted_nulls",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Allow quoted NULL values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="filename",
                parameter_type=["Optional[bool], Optional[str]"],
                parameter_default=None,
                parameter_description="Add filename column or specify filename.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_partitioning",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Enable Hive-style partitioning.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="union_by_name",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Union files by column name instead of position.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_types",
                parameter_type=["Optional[Dict[str, str]]"],
                parameter_default=None,
                parameter_description="Hive types for columns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_types_autocast",
                parameter_type=["Optional[bool]"],
                parameter_default=None,
                parameter_description="Automatically cast Hive types.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="connection",
                parameter_type=["DuckDBPyConnection"],
                parameter_description="DuckDB connection to use.",
            ),
        ],
    ),
    "read_json": PythonRelAPIDetails(
        example="""
import duckdb
import json

with open("code_example.json", mode="w") as f:
    json.dump([{'id': 1, "text":"a"}], f)
    
duckdb_conn = duckdb.connect()

rel = duckdb_conn.read_json("code_example.json")

rel.show()
""",
        result="""
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="path_or_buffer",
                parameter_type=["object"],
                parameter_description="File path or file-like object containing JSON data to be read.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="columns",
                parameter_type=["object"],
                parameter_description="Optional list of column names to project from the JSON data.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sample_size",
                parameter_type=["object"],
                parameter_description="Number of rows to sample for inferring JSON schema.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="maximum_depth",
                parameter_type=["object"],
                parameter_description="Maximum depth to which JSON objects should be parsed.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="records",
                parameter_type=["str"],
                parameter_description="Format string specifying whether JSON is in records mode.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="format",
                parameter_type=["str"],
                parameter_description="Format of the JSON data (e.g., 'auto', 'newline_delimited').",
            ),
            PythonRelAPIParamDetails(
                parameter_name="date_format",
                parameter_type=["object"],
                parameter_description="Format string for parsing date fields.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="timestamp_format",
                parameter_type=["object"],
                parameter_description="Format string for parsing timestamp fields.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["object"],
                parameter_description="Compression codec used on the JSON data (e.g., 'gzip').",
            ),
            PythonRelAPIParamDetails(
                parameter_name="maximum_object_size",
                parameter_type=["object"],
                parameter_description="Maximum size in bytes for individual JSON objects.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="ignore_errors",
                parameter_type=["object"],
                parameter_description="If True, skip over JSON records with parsing errors.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="convert_strings_to_integers",
                parameter_type=["object"],
                parameter_description="If True, attempt to convert strings to integers where appropriate.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="field_appearance_threshold",
                parameter_type=["object"],
                parameter_description="Threshold for inferring optional fields in nested JSON.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="map_inference_threshold",
                parameter_type=["object"],
                parameter_description="Threshold for inferring maps from JSON object patterns.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="maximum_sample_files",
                parameter_type=["object"],
                parameter_description="Maximum number of files to sample for schema inference.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="filename",
                parameter_type=["object"],
                parameter_description="If True, include a column with the source filename for each row.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_partitioning",
                parameter_type=["object"],
                parameter_description="If True, enable Hive partitioning based on directory structure.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="union_by_name",
                parameter_type=["object"],
                parameter_description="If True, align JSON columns by name instead of position.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_types",
                parameter_type=["object"],
                parameter_description="If True, use Hive types from directory structure for schema.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_types_autocast",
                parameter_type=["object"],
                parameter_description="If True, automatically cast data types to match Hive types.",
            ),
        ],
    ),
    "read_parquet": PythonRelAPIDetails(
        example="""
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ids = pa.array([1], type=pa.int8())
texts = pa.array(['a'], type=pa.string())
example_table = pa.table([ids, texts], names=["id", "text"])

pq.write_table(example_table, "code_example.parquet")

duckdb_conn = duckdb.connect()

rel = duckdb_conn.read_parquet("code_example.parquet")

rel.show()
""",
        result="""
┌──────┬─────────┐
│  id  │  text   │
│ int8 │ varchar │
├──────┼─────────┤
│    1 │ a       │
└──────┴─────────┘
""",
        use_default_example=False,
        aliases=["from_parquet"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="file_glob",
                parameter_type=["str"],
                parameter_description="File path or glob pattern pointing to Parquet files to be read.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="binary_as_string",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Interpret binary columns as strings instead of blobs.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="file_row_number",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Add a column containing the row number within each file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="filename",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Add a column containing the name of the file each row came from.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="hive_partitioning",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Enable automatic detection of Hive-style partitions in file paths.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="union_by_name",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Union Parquet files by matching column names instead of positions.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["object"],
                parameter_description="Optional compression codec to use when reading the Parquet files.",
            ),
        ],
    ),
    "sql": PythonRelAPIDetails(
        additional_description="""

> **Warning.** Passing `params` to this method is [discouraged]({% link docs/stable/clients/python/known_issues.md %}#parameterized-queries-in-relational-api) due to significant performance overhead. Use [`execute()`]({% link docs/stable/clients/python/dbapi.md %}#prepared-statements) for parameterized queries instead.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("from range(1,2) tbl(id)")

rel.show()
""",
        result="""
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        use_default_example=False,
        aliases=["from_query", "query"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="query",
                parameter_type=["object"],
                parameter_description="The SQL query or subquery to be executed and converted into a relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="alias",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional alias name to assign to the resulting relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="params",
                parameter_type=["object"],
                parameter_description="Optional query parameters. **Discouraged** due to [significant performance overhead]({% link docs/stable/clients/python/known_issues.md %}#parameterized-queries-in-relational-api). Use [`execute()`]({% link docs/stable/clients/python/dbapi.md %}#prepared-statements) for parameterized queries instead.",
            ),
        ],
    ),
    "table": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("create table code_example as select * from range(1,2) tbl(id)")

rel = duckdb_conn.table("code_example")

rel.show()
""",
        result="""
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="table_name",
                parameter_type=["str"],
                parameter_description="Name of the table to create a relation from.",
            )
        ],
    ),
    "table_function": PythonRelAPIDetails(
        example='''
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
    create macro get_record_for(x) as table
    select x*range from range(1,2)
""")

rel = duckdb_conn.table_function(name="get_record_for", parameters=[1])

rel.show()
''',
        result="""
┌───────────────┐
│ (1 * "range") │
│     int64     │
├───────────────┤
│             1 │
└───────────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="name",
                parameter_type=["str"],
                parameter_description="Name of the table function to call.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="parameters",
                parameter_type=["object"],
                parameter_description="Optional parameters to pass to the table function.",
            ),
        ],
    ),
    "values": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.values([1, 'a'])

rel.show()
""",
        result="""
┌───────┬─────────┐
│ col0  │  col1   │
│ int32 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        use_default_example=False,
    ),
    "view": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("create table code_example as select * from range(1,2) tbl(id)")

rel = duckdb_conn.view("code_example")

rel.show()
""",
        result="""
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="view_name",
                parameter_type=["str"],
                parameter_description="Name of the view to create a relation from.",
            )
        ],
    ),
}

DEFINITION_METHODS_MAP = {
    "columns": PythonRelAPIDetails(
        example="rel.columns",
        result=" ['id', 'description', 'value', 'created_timestamp']",
    ),
    "describe": PythonRelAPIDetails(
        example="rel.describe()",
        result="""
┌─────────┬──────────────────────────────────────┬─────────────────┬────────────────────┬────────────────────────────┐
│  aggr   │                  id                  │   description   │       value        │     created_timestamp      │
│ varchar │               varchar                │     varchar     │       double       │          varchar           │
├─────────┼──────────────────────────────────────┼─────────────────┼────────────────────┼────────────────────────────┤
│ count   │ 9                                    │ 9               │                9.0 │ 9                          │
│ mean    │ NULL                                 │ NULL            │                5.0 │ NULL                       │
│ stddev  │ NULL                                 │ NULL            │ 2.7386127875258306 │ NULL                       │
│ min     │ 08fdcbf8-4e53-4290-9e81-423af263b518 │ value is even   │                1.0 │ 2025-04-09 15:41:20.642+02 │
│ max     │ fb10390e-fad5-4694-91cb-e82728cb6f9f │ value is uneven │                9.0 │ 2025-04-09 15:49:20.642+02 │
│ median  │ NULL                                 │ NULL            │                5.0 │ NULL                       │
└─────────┴──────────────────────────────────────┴─────────────────┴────────────────────┴────────────────────────────┘ 
""",
    ),
    "description": PythonRelAPIDetails(
        example="rel.description",
        result="""
[('id', 'UUID', None, None, None, None, None),
 ('description', 'STRING', None, None, None, None, None),
 ('value', 'NUMBER', None, None, None, None, None),
 ('created_timestamp', 'DATETIME', None, None, None, None, None)]  
""",
    ),
    "dtypes": PythonRelAPIDetails(
        example="rel.dtypes",
        result=" [UUID, VARCHAR, BIGINT, TIMESTAMP WITH TIME ZONE]",
        aliases=["types"],
    ),
    "explain": PythonRelAPIDetails(
        example="rel.explain()",
        result="""
┌───────────────────────────┐\n│         PROJECTION        │\n│    ────────────────────   │\n│             id            │\n│        description        │\n│           value           │\n│     created_timestamp     │\n│                           │\n│          ~9 Rows          │\n└─────────────┬─────────────┘\n┌─────────────┴─────────────┐\n│           RANGE           │\n│    ────────────────────   │\n│      Function: RANGE      │\n│                           │\n│          ~9 Rows          │\n└───────────────────────────┘\n\n
""",
    ),
    "query-1": PythonRelAPIDetails(
        example='rel.query(virtual_table_name="rel_view", sql_query="from rel")\n\nduckdb_conn.sql("show rel_view")',
        result="""
┌───────────────────┬──────────────────────────┬─────────┬─────────┬─────────┬─────────┐
│    column_name    │       column_type        │  null   │   key   │ default │  extra  │
│      varchar      │         varchar          │ varchar │ varchar │ varchar │ varchar │
├───────────────────┼──────────────────────────┼─────────┼─────────┼─────────┼─────────┤
│ id                │ UUID                     │ YES     │ NULL    │ NULL    │ NULL    │
│ description       │ VARCHAR                  │ YES     │ NULL    │ NULL    │ NULL    │
│ value             │ BIGINT                   │ YES     │ NULL    │ NULL    │ NULL    │
│ created_timestamp │ TIMESTAMP WITH TIME ZONE │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────────┴──────────────────────────┴─────────┴─────────┴─────────┴─────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="virtual_table_name",
                parameter_type=["str"],
                parameter_description="The name to assign to the current relation when referenced in the SQL query.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sql_query",
                parameter_type=["str"],
                parameter_description="The SQL query string that uses the virtual table name to query the relation.",
            ),
        ],
    ),
    "set_alias": PythonRelAPIDetails(
        example="rel.set_alias('abc').select('abc.id')",
        result="In the SQL query, the alias will be `abc`",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="alias",
                parameter_type=["str"],
                parameter_description="The alias name to assign to the relation.",
            )
        ],
    ),
    "alias": PythonRelAPIDetails(
        example="rel.alias", result="unnamed_relation_43c808c247431be5"
    ),
    "shape": PythonRelAPIDetails(example="rel.shape", result="(9, 4)"),
    "show": PythonRelAPIDetails(
        example="rel.show()",
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 642ea3d7-793d-4867-a759-91c1226c25a0 │ value is uneven │     1 │ 2025-04-09 15:41:20.642+02 │
│ 6817dd31-297c-40a8-8e40-8521f00b2d08 │ value is even   │     2 │ 2025-04-09 15:42:20.642+02 │
│ 45143f9a-e16e-4e59-91b2-3a0800eed6d6 │ value is uneven │     3 │ 2025-04-09 15:43:20.642+02 │
│ fb10390e-fad5-4694-91cb-e82728cb6f9f │ value is even   │     4 │ 2025-04-09 15:44:20.642+02 │
│ 111ced5c-9155-418e-b087-c331b814db90 │ value is uneven │     5 │ 2025-04-09 15:45:20.642+02 │
│ 66a870a6-aef0-4085-87d5-5d1b35d21c66 │ value is even   │     6 │ 2025-04-09 15:46:20.642+02 │
│ a7e8e796-bca0-44cd-a269-1d71090fb5cc │ value is uneven │     7 │ 2025-04-09 15:47:20.642+02 │
│ 74908d48-7f2d-4bdd-9c92-1e7920b115b5 │ value is even   │     8 │ 2025-04-09 15:48:20.642+02 │
│ 08fdcbf8-4e53-4290-9e81-423af263b518 │ value is uneven │     9 │ 2025-04-09 15:49:20.642+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="max_width",
                parameter_type=["int"],
                parameter_description="Maximum display width for the entire output in characters.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="max_rows",
                parameter_type=["int"],
                parameter_description="Maximum number of rows to display.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="max_col_width",
                parameter_type=["int"],
                parameter_description="Maximum number of characters to display per column.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="null_value",
                parameter_type=["str"],
                parameter_description="String to display in place of NULL values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="render_mode",
                parameter_type=["object"],
                parameter_description="Render mode for displaying the output.",
            ),
        ],
    ),
    "sql_query": PythonRelAPIDetails(
        example="rel.sql_query()",
        result="""SELECT 
    gen_random_uuid() AS id, 
    concat('value is ', CASE  WHEN ((mod("range", 2) = 0)) THEN ('even') ELSE 'uneven' END) AS description, 
    "range" AS "value", 
    (now() + CAST(concat("range", ' ', 'minutes') AS INTERVAL)) AS created_timestamp 
FROM "range"(1, 10)
""",
        result_type="sql",
    ),
    "type": PythonRelAPIDetails(example="rel.type", result="QUERY_RELATION"),
    "types": PythonRelAPIDetails(
        example="rel.types",
        result="[UUID, VARCHAR, BIGINT, TIMESTAMP WITH TIME ZONE]",
        aliases=["dtypes"],
    ),
}

TRANSFORMATION_METHODS_MAP = {
    "aggregate": PythonRelAPIDetails(
        example="rel = rel.aggregate('max(value)')",
        result="""
┌──────────────┐
│ max("value") │
│    int64     │
├──────────────┤
│            9 │
└──────────────┘
        """,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="aggr_expr",
                parameter_type=["str", "list[Expression]"],
                parameter_description="The list of columns and aggregation functions.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="group_expr",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="The list of columns to be included in `group_by`. If `None`, `group by all` is applied.",
            ),
        ],
    ),
    "apply": PythonRelAPIDetails(
        example="""
rel.apply(
    function_name="count", 
    function_aggr="id", 
    group_expr="description",
    projected_columns="description"
)
""",
        result="""
┌─────────────────┬───────────┐
│   description   │ count(id) │
│     varchar     │   int64   │
├─────────────────┼───────────┤
│ value is uneven │         5 │
│ value is even   │         4 │
└─────────────────┴───────────┘
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="function_name",
                parameter_type=["str"],
                parameter_description="Name of the function to apply over the relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="function_aggr",
                parameter_type=["str"],
                parameter_description="The list of columns to apply the function over.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="group_expr",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional SQL expression for grouping.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="function_parameter",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional parameters to pass into the function.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "cross": PythonRelAPIDetails(
        example='rel.cross(other_rel=rel.set_alias("other_rel"))',
        result="""
┌─────────────────────────────┬─────────────────┬───────┬───────────────────────────┬──────────────────────────────────────┬─────────────────┬───────┬───────────────────────────┐
│             id              │   description   │ value │     created_timestamp     │                  id                  │   description   │ value │     created_timestamp     │
│            uuid             │     varchar     │ int64 │ timestamp with time zone  │                 uuid                 │     varchar     │ int64 │ timestamp with time zone  │
├─────────────────────────────┼─────────────────┼───────┼───────────────────────────┼──────────────────────────────────────┼─────────────────┼───────┼───────────────────────────┤
│ cb2b453f-1a06-4f5e-abe1-b…  │ value is uneven │     1 │ 2025-04-10 09:53:29.78+02 │ cb2b453f-1a06-4f5e-abe1-bfd413581bcf │ value is uneven │     1 │ 2025-04-10 09:53:29.78+02 │
...
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="other_rel",
                parameter_type=["_duckdb.DuckDBPyRelation"],
                parameter_description="Another relation to perform a cross product with.",
            )
        ],
    ),
    "except_": PythonRelAPIDetails(
        example='rel.except_(other_rel=rel.set_alias("other_rel"))',
        result="""
The relation query is executed twice, therefore generating different ids and timestamps:
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ f69ed6dd-a7fe-4de2-b6af-1c2418096d69 │ value is uneven │     3 │ 2025-04-10 11:43:05.711+02 │
│ 08ad11dc-a9c2-4aaa-9272-760b27ad1f5d │ value is uneven │     7 │ 2025-04-10 11:47:05.711+02 │
...
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="other_rel",
                parameter_type=["_duckdb.DuckDBPyRelation"],
                parameter_description="The relation to subtract from the current relation (set difference).",
            )
        ],
    ),
    "filter": PythonRelAPIDetails(
        example='rel.filter("value = 2")',
        result="""
┌──────────────────────────────────────┬───────────────┬───────┬───────────────────────────┐
│                  id                  │  description  │ value │     created_timestamp     │
│                 uuid                 │    varchar    │ int64 │ timestamp with time zone  │
├──────────────────────────────────────┼───────────────┼───────┼───────────────────────────┤
│ b0684ab7-fcbf-41c5-8e4a-a51bdde86926 │ value is even │     2 │ 2025-04-10 09:54:29.78+02 │
└──────────────────────────────────────┴───────────────┴───────┴───────────────────────────┘
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="filter_expr",
                parameter_type=["str", "Expression"],
                parameter_description="The filter expression to apply over the relation.",
            )
        ],
    ),
    "insert": PythonRelAPIDetails(
        example='''
import duckdb

from datetime import datetime
from uuid import uuid4

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
).to_table("code_example")

rel = duckdb_conn.table("code_example")

rel.insert(
    (
        uuid4(), 
        'value is even',
        10, 
        datetime.now()
    )
)

rel.filter("value = 10")
''',
        result="""
┌──────────────────────────────────────┬───────────────┬───────┬───────────────────────────────┐
│                  id                  │  description  │ value │       created_timestamp       │
│                 uuid                 │    varchar    │ int64 │   timestamp with time zone    │
├──────────────────────────────────────┼───────────────┼───────┼───────────────────────────────┤
│ c6dfab87-fae6-4213-8f76-1b96a8d179f6 │ value is even │    10 │ 2025-04-10 10:02:24.652218+02 │
└──────────────────────────────────────┴───────────────┴───────┴───────────────────────────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="values",
                parameter_type=["object"],
                parameter_description="A tuple of values matching the relation column list, to be inserted.",
            )
        ],
    ),
    "insert_into": PythonRelAPIDetails(
        example='''
import duckdb

from datetime import datetime
from uuid import uuid4

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
        select
            gen_random_uuid() as id,
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value,
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
).to_table("code_example")

rel = duckdb_conn.values(
    [
        uuid4(),
        'value is even',
        10,
        datetime.now()
    ]
)

rel.insert_into("code_example")

duckdb_conn.table("code_example").filter("value = 10")
    ''',
        result="""
┌──────────────────────────────────────┬───────────────┬───────┬───────────────────────────────┐
│                  id                  │  description  │ value │       created_timestamp       │
│                 uuid                 │    varchar    │ int64 │   timestamp with time zone    │
├──────────────────────────────────────┼───────────────┼───────┼───────────────────────────────┤
│ 271c5ddd-c1d5-4638-b5a0-d8c7dc9e8220 │ value is even │    10 │ 2025-04-10 14:29:18.616379+02 │
└──────────────────────────────────────┴───────────────┴───────┴───────────────────────────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="table_name",
                parameter_type=["str"],
                parameter_description="The table name to insert the data into. The relation must respect the column order of the table.",
            )
        ],
    ),
    "intersect": PythonRelAPIDetails(
        example='rel.intersect(other_rel=rel.set_alias("other_rel"))',
        result="""
The relation query is executed once with `rel` and once with `other_rel`,
therefore generating different ids and timestamps:

┌──────┬─────────────┬───────┬──────────────────────────┐
│  id  │ description │ value │    created_timestamp     │
│ uuid │   varchar   │ int64 │ timestamp with time zone │
├──────┴─────────────┴───────┴──────────────────────────┤
│                        0 rows                         │
└───────────────────────────────────────────────────────┘
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="other_rel",
                parameter_type=["_duckdb.DuckDBPyRelation"],
                parameter_description="The relation to intersect with the current relation (set intersection).",
            )
        ],
    ),
    "join": PythonRelAPIDetails(
        example="""
rel = rel.set_alias("rel").join(
    other_rel=rel.set_alias("other_rel"), 
    condition="rel.id = other_rel.id",
    how="left"
)

rel.count("*")
""",
        result="""
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            9 │
└──────────────┘
""",
        use_default_example=True,
        additional_description="""

Depending on how the `condition` parameter is provided, the JOIN clause generated is:
- `USING`

```python
import duckdb

duckdb_conn = duckdb.connect()

rel1 = duckdb_conn.sql("select range as id, concat('dummy 1', range) as text from range(1,10)")
rel2 = duckdb_conn.sql("select range as id, concat('dummy 2', range) as text from range(5,7)")

rel1.join(rel2, condition="id", how="inner").sql_query()
```
with following SQL:

```sql
SELECT * 
FROM (
        SELECT "range" AS id, 
            concat('dummy 1', "range") AS "text" 
        FROM "range"(1, 10)
    ) AS unnamed_relation_41bc15e744037078 
INNER JOIN (
        SELECT "range" AS id, 
        concat('dummy 2', "range") AS "text" 
        FROM "range"(5, 7)
    ) AS unnamed_relation_307e245965aa2c2b 
USING (id)
```
- `ON`

```python
import duckdb

duckdb_conn = duckdb.connect()

rel1 = duckdb_conn.sql("select range as id, concat('dummy 1', range) as text from range(1,10)")
rel2 = duckdb_conn.sql("select range as id, concat('dummy 2', range) as text from range(5,7)")

rel1.join(rel2, condition=f"{rel1.alias}.id = {rel2.alias}.id", how="inner").sql_query()
```

with the following SQL:

```sql
SELECT * 
FROM (
        SELECT "range" AS id, 
            concat('dummy 1', "range") AS "text" 
        FROM "range"(1, 10)
    ) AS unnamed_relation_41bc15e744037078 
INNER JOIN (
        SELECT "range" AS id, 
        concat('dummy 2', "range") AS "text" 
        FROM "range"(5, 7)
    ) AS unnamed_relation_307e245965aa2c2b 
ON ((unnamed_relation_41bc15e744037078.id = unnamed_relation_307e245965aa2c2b.id))
```

> `NATURAL`, `POSITIONAL` and `ASOF` joins are not provided by the relational API.
> `CROSS` joins are provided through the [cross method](#cross). 
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="other_rel",
                parameter_type=["_duckdb.DuckDBPyRelation"],
                parameter_description="The relation to join with the current relation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="condition",
                parameter_type=["object"],
                parameter_description="The join condition, typically a SQL expression or the duplicated column name to join on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="how",
                parameter_type=["str"],
                parameter_default="'inner'",
                parameter_description="The type of join to perform: 'inner', 'left', 'right', 'outer', 'semi' and 'anti'.",
            ),
        ],
    ),
    "limit": PythonRelAPIDetails(
        example="rel.limit(1)",
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 4135597b-29e7-4cb9-a443-41f3d54f25df │ value is uneven │     1 │ 2025-04-10 10:52:03.678+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="n",
                parameter_type=["int"],
                parameter_description="The maximum number of rows to return.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="offset",
                parameter_type=["int"],
                parameter_default="0",
                parameter_description="The number of rows to skip before starting to return rows.",
            ),
        ],
    ),
    "map": PythonRelAPIDetails(
        example="""
import duckdb
from pandas import DataFrame

def multiply_by_2(df: DataFrame):
    df["id"] = df["id"] * 2
    return df

duckdb_conn = duckdb.connect()
rel = duckdb_conn.sql("select range as id, 'dummy' as text from range(1,3)")

rel.map(multiply_by_2, schema={"id": int, "text": str})
""",
        result="""
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     2 │ dummy   │
│     4 │ dummy   │
└───────┴─────────┘
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="map_function",
                parameter_type=["Callable"],
                parameter_description="A Python function that takes a DataFrame and returns a transformed DataFrame.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="schema",
                parameter_type=["object"],
                parameter_default="None",
                parameter_description="Optional schema describing the structure of the output relation.",
            ),
        ],
    ),
    "order": PythonRelAPIDetails(
        example='rel.order("value desc").limit(1, offset=4)',
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 55899131-e3d3-463c-a215-f65cb8aef3bf │ value is uneven │     5 │ 2025-04-10 10:56:03.678+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="order_expr",
                parameter_type=["str"],
                parameter_description="SQL expression defining the ordering of the result rows.",
            )
        ],
    ),
    "project": PythonRelAPIDetails(
        example='rel.project("description").limit(1)',
        result="""
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is uneven │
└─────────────────┘
""",
        use_default_example=True,
        aliases=["select"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            )
        ],
    ),
    "select": PythonRelAPIDetails(
        example='rel.select("description").limit(1)',
        result="""
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is uneven │
└─────────────────┘
""",
        use_default_example=True,
        aliases=["project"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            )
        ],
    ),
    "sort": PythonRelAPIDetails(
        example='rel.sort("description")',
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 5e0dfa8c-de4d-4ccd-8cff-450dabb86bde │ value is even   │     6 │ 2025-04-10 16:52:15.605+02 │
│ 95f1ad48-facf-4a84-a971-0a4fecce68c7 │ value is even   │     2 │ 2025-04-10 16:48:15.605+02 │
...
""",
        use_default_example=True,
    ),
    "union": PythonRelAPIDetails(
        example='rel = rel.union(union_rel=rel)\n\nrel.count("*")',
        result="""
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           18 │
└──────────────┘
""",
        use_default_example=True,
        additional_description="\n>The union is `union all`. In order to retrieve distinct values, apply [distinct](#distinct).",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="union_rel",
                parameter_type=["_duckdb.DuckDBPyRelation"],
                parameter_description="The relation to union with the current relation (set union).",
            )
        ],
    ),
    "update": PythonRelAPIDetails(
        example='''
import duckdb

from duckdb import ColumnExpression

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
).to_table("code_example")

rel = duckdb_conn.table("code_example")

rel.update(set={"description":None}, condition=ColumnExpression("value") == 1)

# the update is executed on the table, but not reflected on the relationship
# the relationship has to be recreated to retrieve the modified data
rel = duckdb_conn.table("code_example")

rel.show()
''',
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 66dcaa14-f4a6-4a55-af3b-7f6aa23ab4ad │ NULL            │     1 │ 2025-04-10 16:54:49.317+02 │
│ c6a18a42-67fb-4c95-827b-c966f2f95b88 │ value is even   │     2 │ 2025-04-10 16:55:49.317+02 │
...
""",
        use_default_example=False,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="set",
                parameter_type=["object"],
                parameter_description="Mapping of columns to new values for the update operation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="condition",
                parameter_type=["object"],
                parameter_default="None",
                parameter_description="Optional condition to filter which rows to update.",
            ),
        ],
    ),
}

FUNCTION_METHODS_MAP = {
    "any_value": PythonRelAPIDetails(
        example="rel.any_value('id')",
        result="""
┌──────────────────────────────────────┐
│            any_value(id)             │
│                 uuid                 │
├──────────────────────────────────────┤
│ 642ea3d7-793d-4867-a759-91c1226c25a0 │
└──────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name from which to retrieve any value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "arg_max": PythonRelAPIDetails(
        example='rel.arg_max(arg_column="value", value_column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────────────┐
│   description   │ arg_max("value", "value") │
│     varchar     │           int64           │
├─────────────────┼───────────────────────────┤
│ value is uneven │                         9 │
│ value is even   │                         8 │
└─────────────────┴───────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="arg_column",
                parameter_type=["str"],
                parameter_description="The column name for which to find the argument maximizing the value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="value_column",
                parameter_type=["str"],
                parameter_description="The column name containing values used to determine the maximum.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "arg_min": PythonRelAPIDetails(
        example='rel.arg_min(arg_column="value", value_column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────────────┐
│   description   │ arg_min("value", "value") │
│     varchar     │           int64           │
├─────────────────┼───────────────────────────┤
│ value is even   │                         2 │
│ value is uneven │                         1 │
└─────────────────┴───────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="arg_column",
                parameter_type=["str"],
                parameter_description="The column name for which to find the argument minimizing the value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="value_column",
                parameter_type=["str"],
                parameter_description="The column name containing values used to determine the minimum.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "avg": PythonRelAPIDetails(
        example="rel.avg('value')",
        result="""
┌──────────────┐
│ avg("value") │
│    double    │
├──────────────┤
│          5.0 │
└──────────────┘
 """,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the average on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "bit_and": PythonRelAPIDetails(
        example="""
rel = rel.select("description, value::bit as value_bit")

rel.bit_and(column="value_bit", groups="description", projected_columns="description")
""",
        result="""
┌─────────────────┬──────────────────────────────────────────────────────────────────┐
│   description   │                        bit_and(value_bit)                        │
│     varchar     │                               bit                                │
├─────────────────┼──────────────────────────────────────────────────────────────────┤
│ value is uneven │ 0000000000000000000000000000000000000000000000000000000000000001 │
│ value is even   │ 0000000000000000000000000000000000000000000000000000000000000000 │
└─────────────────┴──────────────────────────────────────────────────────────────────┘    
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to perform the bitwise AND aggregation on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "bit_or": PythonRelAPIDetails(
        example="""
rel = rel.select("description, value::bit as value_bit")

rel.bit_or(column="value_bit", groups="description", projected_columns="description")
""",
        result="""
┌─────────────────┬──────────────────────────────────────────────────────────────────┐
│   description   │                        bit_or(value_bit)                         │
│     varchar     │                               bit                                │
├─────────────────┼──────────────────────────────────────────────────────────────────┤
│ value is uneven │ 0000000000000000000000000000000000000000000000000000000000001111 │
│ value is even   │ 0000000000000000000000000000000000000000000000000000000000001110 │
└─────────────────┴──────────────────────────────────────────────────────────────────┘    
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to perform the bitwise OR aggregation on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "bit_xor": PythonRelAPIDetails(
        example="""
rel = rel.select("description, value::bit as value_bit")

rel.bit_xor(column="value_bit", groups="description", projected_columns="description")
""",
        result="""
┌─────────────────┬──────────────────────────────────────────────────────────────────┐
│   description   │                        bit_xor(value_bit)                        │
│     varchar     │                               bit                                │
├─────────────────┼──────────────────────────────────────────────────────────────────┤
│ value is even   │ 0000000000000000000000000000000000000000000000000000000000001000 │
│ value is uneven │ 0000000000000000000000000000000000000000000000000000000000001001 │
└─────────────────┴──────────────────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to perform the bitwise XOR aggregation on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "bitstring_agg": PythonRelAPIDetails(
        example='rel.bitstring_agg(column="value", groups="description", projected_columns="description", min=1, max=9)',
        result="""
┌─────────────────┬────────────────────────┐
│   description   │ bitstring_agg("value") │
│     varchar     │          bit           │
├─────────────────┼────────────────────────┤
│ value is uneven │ 101010101              │
│ value is even   │ 010101010              │
└─────────────────┴────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to aggregate as a bitstring.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="min",
                parameter_type=["object"],
                parameter_default="None",
                parameter_description="Optional minimum bitstring value for aggregation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="max",
                parameter_type=["object"],
                parameter_default="None",
                parameter_description="Optional maximum bitstring value for aggregation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "bool_and": PythonRelAPIDetails(
        example="""
rel = rel.select("description, mod(value,2)::boolean as uneven")

rel.bool_and(column="uneven", groups="description", projected_columns="description")
""",
        result="""
┌─────────────────┬──────────────────┐
│   description   │ bool_and(uneven) │
│     varchar     │     boolean      │
├─────────────────┼──────────────────┤
│ value is even   │ false            │
│ value is uneven │ true             │
└─────────────────┴──────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to perform the boolean AND aggregation on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "bool_or": PythonRelAPIDetails(
        example="""
rel = rel.select("description, mod(value,2)::boolean as uneven")

rel.bool_or(column="uneven", groups="description", projected_columns="description")
""",
        result="""
┌─────────────────┬─────────────────┐
│   description   │ bool_or(uneven) │
│     varchar     │     boolean     │
├─────────────────┼─────────────────┤
│ value is even   │ false           │
│ value is uneven │ true            │
└─────────────────┴─────────────────┘                
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to perform the boolean OR aggregation on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "count": PythonRelAPIDetails(
        example='rel.count("id")',
        result="""
┌───────────┐
│ count(id) │
│   int64   │
├───────────┤
│         9 │
└───────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to perform count on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "cume_dist": PythonRelAPIDetails(
        example='rel.cume_dist(window_spec="over (partition by description order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬──────────────────────────────────────────────────────────────┐
│   description   │ value │ cume_dist() OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │ int64 │                            double                            │
├─────────────────┼───────┼──────────────────────────────────────────────────────────────┤
│ value is uneven │     1 │                                                          0.2 │
│ value is uneven │     3 │                                                          0.4 │
│ value is uneven │     5 │                                                          0.6 │
│ value is uneven │     7 │                                                          0.8 │
│ value is uneven │     9 │                                                          1.0 │
│ value is even   │     2 │                                                         0.25 │
│ value is even   │     4 │                                                          0.5 │
│ value is even   │     6 │                                                         0.75 │
│ value is even   │     8 │                                                          1.0 │
└─────────────────┴───────┴──────────────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "dense_rank": PythonRelAPIDetails(
        example=' rel.dense_rank(window_spec="over (partition by description order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬───────────────────────────────────────────────────────────────┐
│   description   │ value │ dense_rank() OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │ int64 │                             int64                             │
├─────────────────┼───────┼───────────────────────────────────────────────────────────────┤
│ value is even   │     2 │                                                             1 │
│ value is even   │     4 │                                                             2 │
│ value is even   │     6 │                                                             3 │
│ value is even   │     8 │                                                             4 │
│ value is uneven │     1 │                                                             1 │
│ value is uneven │     3 │                                                             2 │
│ value is uneven │     5 │                                                             3 │
│ value is uneven │     7 │                                                             4 │
│ value is uneven │     9 │                                                             5 │
└─────────────────┴───────┴───────────────────────────────────────────────────────────────┘
""",
        aliases=["rank_dense"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "distinct": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("select range from range(1,4)")

rel = rel.union(union_rel=rel)

rel.distinct().order("range")
""",
        result="""
┌───────┐
│ range │
│ int64 │
├───────┤
│     1 │
│     2 │
│     3 │
└───────┘
""",
        use_default_example=False,
    ),
    "favg": PythonRelAPIDetails(
        example='rel.favg(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────┐
│   description   │ favg("value") │
│     varchar     │    double     │
├─────────────────┼───────────────┤
│ value is uneven │           5.0 │
│ value is even   │           5.0 │
└─────────────────┴───────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the average on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "first": PythonRelAPIDetails(
        example='rel.first(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────┐
│   description   │ "first"("value") │
│     varchar     │      int64       │
├─────────────────┼──────────────────┤
│ value is even   │                2 │
│ value is uneven │                1 │
└─────────────────┴──────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name from which to retrieve the first value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "first_value": PythonRelAPIDetails(
        example='rel.first_value(column="value", window_spec="over (partition by description order by value)", projected_columns="description").distinct()',
        result="""
┌─────────────────┬───────────────────────────────────────────────────────────────────────┐
│   description   │ first_value("value") OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │                                 int64                                 │
├─────────────────┼───────────────────────────────────────────────────────────────────────┤
│ value is even   │                                                                     2 │
│ value is uneven │                                                                     1 │
└─────────────────┴───────────────────────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name from which to retrieve the first value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "fsum": PythonRelAPIDetails(
        example='rel.fsum(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────┐
│   description   │ fsum("value") │
│     varchar     │    double     │
├─────────────────┼───────────────┤
│ value is even   │          20.0 │
│ value is uneven │          25.0 │
└─────────────────┴───────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the sum on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "geomean": PythonRelAPIDetails(
        example='rel.geomean(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────┐
│   description   │ geomean("value")  │
│     varchar     │      double       │
├─────────────────┼───────────────────┤
│ value is uneven │ 3.936283427035351 │
│ value is even   │ 4.426727678801287 │
└─────────────────┴───────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the geometric mean on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "histogram": PythonRelAPIDetails(
        example='rel.histogram(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────────────┐
│   description   │    histogram("value")     │
│     varchar     │   map(bigint, ubigint)    │
├─────────────────┼───────────────────────────┤
│ value is uneven │ {1=1, 3=1, 5=1, 7=1, 9=1} │
│ value is even   │ {2=1, 4=1, 6=1, 8=1}      │
└─────────────────┴───────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the histogram on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "lag": PythonRelAPIDetails(
        example='rel.lag(column="description", window_spec="over (order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬───────────────────────────────────────────────────┐
│   description   │ value │ lag(description, 1, NULL) OVER (ORDER BY "value") │
│     varchar     │ int64 │                      varchar                      │
├─────────────────┼───────┼───────────────────────────────────────────────────┤
│ value is uneven │     1 │ NULL                                              │
│ value is even   │     2 │ value is uneven                                   │
│ value is uneven │     3 │ value is even                                     │
│ value is even   │     4 │ value is uneven                                   │
│ value is uneven │     5 │ value is even                                     │
│ value is even   │     6 │ value is uneven                                   │
│ value is uneven │     7 │ value is even                                     │
│ value is even   │     8 │ value is uneven                                   │
│ value is uneven │     9 │ value is even                                     │
└─────────────────┴───────┴───────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to apply the lag function on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="offset",
                parameter_type=["int"],
                parameter_default="1",
                parameter_description="The number of rows to lag behind.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="default_value",
                parameter_type=["str"],
                parameter_default="'NULL'",
                parameter_description="The default value to return when the lag offset goes out of bounds.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="ignore_nulls",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether to ignore NULL values when computing the lag.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "last": PythonRelAPIDetails(
        example='rel.last(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬─────────────────┐
│   description   │ "last"("value") │
│     varchar     │      int64      │
├─────────────────┼─────────────────┤
│ value is even   │               8 │
│ value is uneven │               9 │
└─────────────────┴─────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name from which to retrieve the last value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "last_value": PythonRelAPIDetails(
        example='rel.last_value(column="value", window_spec="over (order by description)", projected_columns="description").distinct()',
        result="""
┌─────────────────┬─────────────────────────────────────────────────┐
│   description   │ last_value("value") OVER (ORDER BY description) │
│     varchar     │                      int64                      │
├─────────────────┼─────────────────────────────────────────────────┤
│ value is uneven │                                               9 │
│ value is even   │                                               8 │
└─────────────────┴─────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name from which to retrieve the last value within the window.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "lead": PythonRelAPIDetails(
        example='rel.lead(column="description", window_spec="over (order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬────────────────────────────────────────────────────┐
│   description   │ value │ lead(description, 1, NULL) OVER (ORDER BY "value") │
│     varchar     │ int64 │                      varchar                       │
├─────────────────┼───────┼────────────────────────────────────────────────────┤
│ value is uneven │     1 │ value is even                                      │
│ value is even   │     2 │ value is uneven                                    │
│ value is uneven │     3 │ value is even                                      │
│ value is even   │     4 │ value is uneven                                    │
│ value is uneven │     5 │ value is even                                      │
│ value is even   │     6 │ value is uneven                                    │
│ value is uneven │     7 │ value is even                                      │
│ value is even   │     8 │ value is uneven                                    │
│ value is uneven │     9 │ NULL                                               │
└─────────────────┴───────┴────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to apply the lead function on.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="offset",
                parameter_type=["int"],
                parameter_default="1",
                parameter_description="The number of rows to lead ahead.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="default_value",
                parameter_type=["str"],
                parameter_default="'NULL'",
                parameter_description="The default value to return when the lead offset goes out of bounds.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="ignore_nulls",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether to ignore NULL values when computing the lead.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "list": PythonRelAPIDetails(
        example='rel.list(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬─────────────────┐
│   description   │  list("value")  │
│     varchar     │     int64[]     │
├─────────────────┼─────────────────┤
│ value is even   │ [2, 4, 6, 8]    │
│ value is uneven │ [1, 3, 5, 7, 9] │
└─────────────────┴─────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to aggregate values into a list.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "max": PythonRelAPIDetails(
        example=' rel.max(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────┐
│   description   │ max("value") │
│     varchar     │    int64     │
├─────────────────┼──────────────┤
│ value is even   │            8 │
│ value is uneven │            9 │
└─────────────────┴──────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the maximum value of.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "mean": PythonRelAPIDetails(
        example='rel.mean(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────┐
│   description   │ avg("value") │
│     varchar     │    double    │
├─────────────────┼──────────────┤
│ value is even   │          5.0 │
│ value is uneven │          5.0 │
└─────────────────┴──────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the mean value of.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "median": PythonRelAPIDetails(
        example='rel.median(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬─────────────────┐
│   description   │ median("value") │
│     varchar     │     double      │
├─────────────────┼─────────────────┤
│ value is even   │             5.0 │
│ value is uneven │             5.0 │
└─────────────────┴─────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the median value of.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "min": PythonRelAPIDetails(
        example='rel.min(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────┐
│   description   │ min("value") │
│     varchar     │    int64     │
├─────────────────┼──────────────┤
│ value is uneven │            1 │
│ value is even   │            2 │
└─────────────────┴──────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the min value of.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "mode": PythonRelAPIDetails(
        example='rel.mode(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬─────────────────┐
│   description   │ "mode"("value") │
│     varchar     │      int64      │
├─────────────────┼─────────────────┤
│ value is uneven │               1 │
│ value is even   │               2 │
└─────────────────┴─────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the mode (most frequent value) of.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "n_tile": PythonRelAPIDetails(
        example='rel.n_tile(window_spec="over (partition by description)", num_buckets=2, projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬──────────────────────────────────────────┐
│   description   │ value │ ntile(2) OVER (PARTITION BY description) │
│     varchar     │ int64 │                  int64                   │
├─────────────────┼───────┼──────────────────────────────────────────┤
│ value is uneven │     1 │                                        1 │
│ value is uneven │     3 │                                        1 │
│ value is uneven │     5 │                                        1 │
│ value is uneven │     7 │                                        2 │
│ value is uneven │     9 │                                        2 │
│ value is even   │     2 │                                        1 │
│ value is even   │     4 │                                        1 │
│ value is even   │     6 │                                        2 │
│ value is even   │     8 │                                        2 │
└─────────────────┴───────┴──────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="num_buckets",
                parameter_type=["int"],
                parameter_description="The number of buckets to divide the rows into.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "nth_value": PythonRelAPIDetails(
        example='rel.nth_value(column="value", window_spec="over (partition by description)", projected_columns="description", offset=1)',
        result="""
┌─────────────────┬───────────────────────────────────────────────────────┐
│   description   │ nth_value("value", 1) OVER (PARTITION BY description) │
│     varchar     │                         int64                         │
├─────────────────┼───────────────────────────────────────────────────────┤
│ value is even   │                                                     2 │
│ value is even   │                                                     2 │
│ value is even   │                                                     2 │
│ value is even   │                                                     2 │
│ value is uneven │                                                     1 │
│ value is uneven │                                                     1 │
│ value is uneven │                                                     1 │
│ value is uneven │                                                     1 │
│ value is uneven │                                                     1 │
└─────────────────┴───────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name from which to retrieve the nth value within the window.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="offset",
                parameter_type=["int"],
                parameter_description="The position of the value to retrieve within the window (1-based index).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="ignore_nulls",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether to ignore NULL values when computing the nth value.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "percent_rank": PythonRelAPIDetails(
        example='rel.percent_rank(window_spec="over (partition by description order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬─────────────────────────────────────────────────────────────────┐
│   description   │ value │ percent_rank() OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │ int64 │                             double                              │
├─────────────────┼───────┼─────────────────────────────────────────────────────────────────┤
│ value is even   │     2 │                                                             0.0 │
│ value is even   │     4 │                                              0.3333333333333333 │
│ value is even   │     6 │                                              0.6666666666666666 │
│ value is even   │     8 │                                                             1.0 │
│ value is uneven │     1 │                                                             0.0 │
│ value is uneven │     3 │                                                            0.25 │
│ value is uneven │     5 │                                                             0.5 │
│ value is uneven │     7 │                                                            0.75 │
│ value is uneven │     9 │                                                             1.0 │
└─────────────────┴───────┴─────────────────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "product": PythonRelAPIDetails(
        example='rel.product(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────┐
│   description   │ product("value") │
│     varchar     │      double      │
├─────────────────┼──────────────────┤
│ value is uneven │            945.0 │
│ value is even   │            384.0 │
└─────────────────┴──────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the product of.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "quantile": PythonRelAPIDetails(
        example='rel.quantile(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────────────────┐
│   description   │ quantile_disc("value", 0.500000) │
│     varchar     │              int64               │
├─────────────────┼──────────────────────────────────┤
│ value is uneven │                                5 │
│ value is even   │                                4 │
└─────────────────┴──────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to compute the quantile for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="q",
                parameter_type=["object"],
                parameter_default="0.5",
                parameter_description="The quantile value to compute (e.g., 0.5 for median).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "quantile_cont": PythonRelAPIDetails(
        example='rel.quantile_cont(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────────────────┐
│   description   │ quantile_cont("value", 0.500000) │
│     varchar     │              double              │
├─────────────────┼──────────────────────────────────┤
│ value is even   │                              5.0 │
│ value is uneven │                              5.0 │
└─────────────────┴──────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to compute the continuous quantile for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="q",
                parameter_type=["object"],
                parameter_default="0.5",
                parameter_description="The quantile value to compute (e.g., 0.5 for median).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "quantile_disc": PythonRelAPIDetails(
        example='rel.quantile_disc(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────────────────┐
│   description   │ quantile_disc("value", 0.500000) │
│     varchar     │              int64               │
├─────────────────┼──────────────────────────────────┤
│ value is even   │                                4 │
│ value is uneven │                                5 │
└─────────────────┴──────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to compute the discrete quantile for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="q",
                parameter_type=["object"],
                parameter_default="0.5",
                parameter_description="The quantile value to compute (e.g., 0.5 for median).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "rank": PythonRelAPIDetails(
        example='rel.rank(window_spec="over (partition by description order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬─────────────────────────────────────────────────────────┐
│   description   │ value │ rank() OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │ int64 │                          int64                          │
├─────────────────┼───────┼─────────────────────────────────────────────────────────┤
│ value is uneven │     1 │                                                       1 │
│ value is uneven │     3 │                                                       2 │
│ value is uneven │     5 │                                                       3 │
│ value is uneven │     7 │                                                       4 │
│ value is uneven │     9 │                                                       5 │
│ value is even   │     2 │                                                       1 │
│ value is even   │     4 │                                                       2 │
│ value is even   │     6 │                                                       3 │
│ value is even   │     8 │                                                       4 │
└─────────────────┴───────┴─────────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "rank_dense": PythonRelAPIDetails(
        example=' rel.rank_dense(window_spec="over (partition by description order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬───────────────────────────────────────────────────────────────┐
│   description   │ value │ dense_rank() OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │ int64 │                             int64                             │
├─────────────────┼───────┼───────────────────────────────────────────────────────────────┤
│ value is uneven │     1 │                                                             1 │
│ value is uneven │     3 │                                                             2 │
│ value is uneven │     5 │                                                             3 │
│ value is uneven │     7 │                                                             4 │
│ value is uneven │     9 │                                                             5 │
│ value is even   │     2 │                                                             1 │
│ value is even   │     4 │                                                             2 │
│ value is even   │     6 │                                                             3 │
│ value is even   │     8 │                                                             4 │
└─────────────────┴───────┴───────────────────────────────────────────────────────────────┘
""",
        aliases=["dense_rank"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "row_number": PythonRelAPIDetails(
        example='rel.row_number(window_spec="over (partition by description order by value)", projected_columns="description, value")',
        result="""
┌─────────────────┬───────┬───────────────────────────────────────────────────────────────┐
│   description   │ value │ row_number() OVER (PARTITION BY description ORDER BY "value") │
│     varchar     │ int64 │                             int64                             │
├─────────────────┼───────┼───────────────────────────────────────────────────────────────┤
│ value is uneven │     1 │                                                             1 │
│ value is uneven │     3 │                                                             2 │
│ value is uneven │     5 │                                                             3 │
│ value is uneven │     7 │                                                             4 │
│ value is uneven │     9 │                                                             5 │
│ value is even   │     2 │                                                             1 │
│ value is even   │     4 │                                                             2 │
│ value is even   │     6 │                                                             3 │
│ value is even   │     8 │                                                             4 │
└─────────────────┴───────┴───────────────────────────────────────────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "select_dtypes": PythonRelAPIDetails(
        example="rel.select_dtypes(types=[duckdb.sqltypes.VARCHAR]).distinct()",
        result="""
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is even   │
│ value is uneven │
└─────────────────┘
""",
        aliases=["select_types"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="types",
                parameter_type=["object"],
                parameter_description="Data type(s) to select columns by. Can be a single type or a collection of types.",
            )
        ],
    ),
    "select_types": PythonRelAPIDetails(
        example="rel.select_types(types=[duckdb.sqltypes.VARCHAR]).distinct()",
        result="""
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is even   │
│ value is uneven │
└─────────────────┘
""",
        aliases=["select_dtypes"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="types",
                parameter_type=["object"],
                parameter_description="Data type(s) to select columns by. Can be a single type or a collection of types.",
            )
        ],
    ),
    "std": PythonRelAPIDetails(
        example='rel.std(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────┐
│   description   │ stddev_samp("value") │
│     varchar     │        double        │
├─────────────────┼──────────────────────┤
│ value is uneven │   3.1622776601683795 │
│ value is even   │    2.581988897471611 │
└─────────────────┴──────────────────────┘
""",
        aliases=["stddev", "stddev_samp"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the standard deviation for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "stddev": PythonRelAPIDetails(
        example='rel.stddev(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────┐
│   description   │ stddev_samp("value") │
│     varchar     │        double        │
├─────────────────┼──────────────────────┤
│ value is even   │    2.581988897471611 │
│ value is uneven │   3.1622776601683795 │
└─────────────────┴──────────────────────┘
""",
        aliases=["std", "stddev_samp"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the standard deviation for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "stddev_pop": PythonRelAPIDetails(
        example='rel.stddev_pop(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬─────────────────────┐
│   description   │ stddev_pop("value") │
│     varchar     │       double        │
├─────────────────┼─────────────────────┤
│ value is even   │    2.23606797749979 │
│ value is uneven │  2.8284271247461903 │
└─────────────────┴─────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the standard deviation for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "stddev_samp": PythonRelAPIDetails(
        example='rel.stddev_samp(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────┐
│   description   │ stddev_samp("value") │
│     varchar     │        double        │
├─────────────────┼──────────────────────┤
│ value is even   │    2.581988897471611 │
│ value is uneven │   3.1622776601683795 │
└─────────────────┴──────────────────────┘
""",
        aliases=["stddev", "std"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the standard deviation for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "string_agg": PythonRelAPIDetails(
        example='rel.string_agg(column="value", sep=",", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────────────┐
│   description   │ string_agg("value", ',') │
│     varchar     │         varchar          │
├─────────────────┼──────────────────────────┤
│ value is even   │ 2,4,6,8                  │
│ value is uneven │ 1,3,5,7,9                │
└─────────────────┴──────────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to concatenate values from.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sep",
                parameter_type=["str"],
                parameter_default="','",
                parameter_description="Separator string to use between concatenated values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "sum": PythonRelAPIDetails(
        example='rel.sum(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────┐
│   description   │ sum("value") │
│     varchar     │    int128    │
├─────────────────┼──────────────┤
│ value is even   │           20 │
│ value is uneven │           25 │
└─────────────────┴──────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the sum for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "unique": PythonRelAPIDetails(
        example='rel.unique(unique_aggr="description")',
        result="""
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is even   │
│ value is uneven │
└─────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="unique_aggr",
                parameter_type=["str"],
                parameter_description="The column to get the distinct values for.",
            )
        ],
    ),
    "value_counts": PythonRelAPIDetails(
        example='rel.value_counts(column="description", groups="description")',
        result="""
┌─────────────────┬────────────────────┐
│   description   │ count(description) │
│     varchar     │       int64        │
├─────────────────┼────────────────────┤
│ value is uneven │                  5 │
│ value is even   │                  4 │
└─────────────────┴────────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to count values from.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
        ],
    ),
    "var": PythonRelAPIDetails(
        example='rel.var(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────┐
│   description   │ var_samp("value") │
│     varchar     │      double       │
├─────────────────┼───────────────────┤
│ value is even   │ 6.666666666666667 │
│ value is uneven │              10.0 │
└─────────────────┴───────────────────┘
""",
        aliases=["variance", "var_samp"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the sample variance for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "var_pop": PythonRelAPIDetails(
        example='rel.var_pop(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬──────────────────┐
│   description   │ var_pop("value") │
│     varchar     │      double      │
├─────────────────┼──────────────────┤
│ value is even   │              5.0 │
│ value is uneven │              8.0 │
└─────────────────┴──────────────────┘
""",
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the population variance for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "var_samp": PythonRelAPIDetails(
        example='rel.var_samp(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────┐
│   description   │ var_samp("value") │
│     varchar     │      double       │
├─────────────────┼───────────────────┤
│ value is even   │ 6.666666666666667 │
│ value is uneven │              10.0 │
└─────────────────┴───────────────────┘
""",
        aliases=["variance", "var"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the sample variance for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
    "variance": PythonRelAPIDetails(
        example='rel.variance(column="value", groups="description", projected_columns="description")',
        result="""
┌─────────────────┬───────────────────┐
│   description   │ var_samp("value") │
│     varchar     │      double       │
├─────────────────┼───────────────────┤
│ value is even   │ 6.666666666666667 │
│ value is uneven │              10.0 │
└─────────────────┴───────────────────┘
""",
        aliases=["var", "var_samp"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="column",
                parameter_type=["str"],
                parameter_description="The column name to calculate the sample variance for.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="groups",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the `group by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="window_spec",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Optional window specification for window functions, provided as `over (partition by ... order by ...)`",
            ),
            PythonRelAPIParamDetails(
                parameter_name="projected_columns",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Comma-separated list of columns to include in the result.",
            ),
        ],
    ),
}

OUTPUT_METHODS_MAP = {
    "arrow": PythonRelAPIDetails(
        example="pa_table = rel.arrow()\n\npa_table",
        result="""
pyarrow.Table
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: [["3ac9e0ba-8390-4a02-ad72-33b1caea6354","8b844392-1404-4bbc-b731-120f42c8ca27","ca5584ca-8e97-4fca-a295-ae3c16c32f5b","926d071e-5f64-488f-ae02-d19e315f9f5c","aabeedf0-5783-4eff-9963-b3967a6ea5d8","1f20db9a-bee8-4b65-b7e8-e7c36b5b8fee","795c678e-3524-4b52-96ec-7b48c24eeab1","9ffbd403-169f-4fe4-bc41-09751066f1f1","8fdb0a60-29f0-4f5b-afcc-c736a03cd083"]]
description: [["value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven"]]
value: [[1,2,3,4,5,6,7,8,9]]
created_timestamp: [[2025-04-10 09:07:12.614000Z,2025-04-10 09:08:12.614000Z,2025-04-10 09:09:12.614000Z,2025-04-10 09:10:12.614000Z,2025-04-10 09:11:12.614000Z,2025-04-10 09:12:12.614000Z,2025-04-10 09:13:12.614000Z,2025-04-10 09:14:12.614000Z,2025-04-10 09:15:12.614000Z]]
""",
        use_default_example=True,
        aliases=["fetch_arrow_table", "to_arrow_table"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="batch_size",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The batch size of writing the data to the Arrow table",
            )
        ],
    ),
    # 'close': PythonRelAPIDetails(example=  '', result=  '', use_default_example=False)
    "create": PythonRelAPIDetails(
        example='rel.create("table_code_example")\n\nduckdb_conn.table("table_code_example").limit(1)',
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 3ac9e0ba-8390-4a02-ad72-33b1caea6354 │ value is uneven │     1 │ 2025-04-10 11:07:12.614+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        use_default_example=True,
        aliases=["to_table"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="table_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the table to be created. There shouldn't be any other table with the same name.",
            )
        ],
    ),
    "create_view": PythonRelAPIDetails(
        example='rel.create_view("view_code_example", replace=True)\n\nduckdb_conn.table("view_code_example").limit(1)',
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 3ac9e0ba-8390-4a02-ad72-33b1caea6354 │ value is uneven │     1 │ 2025-04-10 11:07:12.614+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        use_default_example=True,
        aliases=["to_view"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="view_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the view to be created.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="replace",
                parameter_type=["bool"],
                parameter_default="True",
                parameter_description="If the view should be created with `CREATE OR REPLACE`. When set to `False`, there shouldn't be another view with the same `view_name`.",
            ),
        ],
    ),
    "df": PythonRelAPIDetails(
        example="rel.df()",
        result="""
                                     id      description  value                created_timestamp
0  3ac9e0ba-8390-4a02-ad72-33b1caea6354  value is uneven      1 2025-04-10 11:07:12.614000+02:00
1  8b844392-1404-4bbc-b731-120f42c8ca27    value is even      2 2025-04-10 11:08:12.614000+02:00
2  ca5584ca-8e97-4fca-a295-ae3c16c32f5b  value is uneven      3 2025-04-10 11:09:12.614000+02:00
...
""",
        use_default_example=True,
        aliases=["fetchdf", "to_df"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="date_as_object",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="If the date columns should be interpreted as Python date objects.",
            )
        ],
    ),
    "execute": PythonRelAPIDetails(
        example="rel.execute()",
        result="""
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 3ac9e0ba-8390-4a02-ad72-33b1caea6354 │ value is uneven │     1 │ 2025-04-10 11:07:12.614+02 │
│ 8b844392-1404-4bbc-b731-120f42c8ca27 │ value is even   │     2 │ 2025-04-10 11:08:12.614+02 │
│ ca5584ca-8e97-4fca-a295-ae3c16c32f5b │ value is uneven │     3 │ 2025-04-10 11:09:12.614+02 │
""",
        use_default_example=True,
    ),
    "fetch_arrow_reader": PythonRelAPIDetails(
        example="pa_reader = rel.fetch_arrow_reader(batch_size=1)\n\npa_reader.read_next_batch()",
        result="""
pyarrow.RecordBatch
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: ["e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd"]
description: ["value is even"]
value: [2]
created_timestamp: [2025-04-10 09:25:51.259000Z]
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="batch_size",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The batch size for fetching the data.",
            )
        ],
    ),
    "fetch_arrow_table": PythonRelAPIDetails(
        example="rel.fetch_arrow_table()",
        result="""
pyarrow.Table
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: [["1587b4b0-3023-49fe-82cf-06303ca136ac","e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd","3f8ad67a-290f-4a22-b41b-0173b8e45afa","9a4e37ef-d8bd-46dd-ab01-51cf4973549f","12baa624-ebc9-45ae-b73e-6f4029e31d2d","56d41292-53cc-48be-a1b8-e1f5d6ca5581","1accca18-c950-47c1-9108-aef8afbd5249","56d8db75-72c4-4d40-90d2-a3c840579c37","e19f6201-8646-401c-b019-e37c42c39632"]]
description: [["value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven"]]
value: [[1,2,3,4,5,6,7,8,9]]
created_timestamp: [[2025-04-10 09:24:51.259000Z,2025-04-10 09:25:51.259000Z,2025-04-10 09:26:51.259000Z,2025-04-10 09:27:51.259000Z,2025-04-10 09:28:51.259000Z,2025-04-10 09:29:51.259000Z,2025-04-10 09:30:51.259000Z,2025-04-10 09:31:51.259000Z,2025-04-10 09:32:51.259000Z]]
""",
        use_default_example=True,
        aliases=["arrow", "to_arrow_table"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="batch_size",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The batch size for fetching the data.",
            )
        ],
    ),
    "fetch_record_batch": PythonRelAPIDetails(
        additional_description="\n\n> Deprecated `fetch_record_batch()` is deprecated since 1.4.0. Use [`record_batch()`](#record_batch) instead.",
        example="pa_reader = rel.fetch_record_batch(rows_per_batch=1)\n\npa_reader.read_next_batch()",
        result="""
pyarrow.RecordBatch
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: ["908cf67c-a086-4b94-9017-2089a83e4a6c"]
description: ["value is uneven"]
value: [1]
created_timestamp: [2025-04-10 09:52:55.249000Z]
""",
        use_default_example=True,
        aliases=["record_batch"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="rows_per_batch",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The number of rows per batch.",
            )
        ],
    ),
    "fetch_df_chunk": PythonRelAPIDetails(
        example="rel.fetch_df_chunk()",
        result="""
                                     id      description  value                created_timestamp
0  1587b4b0-3023-49fe-82cf-06303ca136ac  value is uneven      1 2025-04-10 11:24:51.259000+02:00
1  e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd    value is even      2 2025-04-10 11:25:51.259000+02:00
2  3f8ad67a-290f-4a22-b41b-0173b8e45afa  value is uneven      3 2025-04-10 11:26:51.259000+02:00
...
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="vectors_per_chunk",
                parameter_type=["int"],
                parameter_default="1",
                parameter_description="Number of data chunks to be processed before converting to dataframe.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="date_as_object",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="If the date columns should be interpreted as Python date objects.",
            ),
        ],
    ),
    "fetchall": PythonRelAPIDetails(
        example="rel.limit(1).fetchall()",
        result="""
[(UUID('1587b4b0-3023-49fe-82cf-06303ca136ac'),
  'value is uneven',
  1,
  datetime.datetime(2025, 4, 10, 11, 24, 51, 259000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
""",
        use_default_example=True,
    ),
    "fetchdf": PythonRelAPIDetails(
        example="rel.fetchdf()",
        result="""
                                     id      description  value                created_timestamp
0  1587b4b0-3023-49fe-82cf-06303ca136ac  value is uneven      1 2025-04-10 11:24:51.259000+02:00
1  e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd    value is even      2 2025-04-10 11:25:51.259000+02:00
2  3f8ad67a-290f-4a22-b41b-0173b8e45afa  value is uneven      3 2025-04-10 11:26:51.259000+02:00
...
""",
        use_default_example=True,
        aliases=["df", "to_df"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="date_as_object",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="If the date columns should be interpreted as Python date objects.",
            )
        ],
    ),
    "fetchmany": PythonRelAPIDetails(
        example="""
while res := rel.fetchmany(size=1):
    print(res)
""",
        result="""
[(UUID('cf4c5e32-d0aa-4699-a3ee-0092e900f263'), 'value is uneven', 1, datetime.datetime(2025, 4, 30, 16, 23, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('cec335ac-24ac-49a3-ae9a-bb35f71fc88d'), 'value is even', 2, datetime.datetime(2025, 4, 30, 16, 24, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('2423295d-9bb0-453c-a385-21bdacba03b6'), 'value is uneven', 3, datetime.datetime(2025, 4, 30, 16, 25, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('88806b21-192d-41e7-a293-c789aad636ba'), 'value is even', 4, datetime.datetime(2025, 4, 30, 16, 26, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('05837a28-dacf-4121-88a6-a374aefb8a07'), 'value is uneven', 5, datetime.datetime(2025, 4, 30, 16, 27, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('b9c1f7e9-6156-4554-b80e-67d3b5d810bb'), 'value is even', 6, datetime.datetime(2025, 4, 30, 16, 28, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('4709c7fa-d286-4864-bb48-69748b447157'), 'value is uneven', 7, datetime.datetime(2025, 4, 30, 16, 29, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('30e48457-b103-4fa5-95cf-1c7f0143335b'), 'value is even', 8, datetime.datetime(2025, 4, 30, 16, 30, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
[(UUID('036b7f4b-bd78-4ffb-a351-964d93f267b7'), 'value is uneven', 9, datetime.datetime(2025, 4, 30, 16, 31, 5, 310000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
""",
        use_default_example=True,
        additional_description='''
\n
>Warning Executing any operation during the retrieval of the data from an [aggregate](#aggregate) relation,
>will close the result set.
>```python
>import duckdb
>
>duckdb_conn = duckdb.connect()
>
>rel = duckdb_conn.sql("""
>       select 
>           gen_random_uuid() as id, 
>           concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
>           range as value, 
>           now() + concat(range,' ', 'minutes')::interval as created_timestamp
>       from range(1, 10)
>    """
>)
>
>agg_rel = rel.aggregate("value")
>
>while res := agg_rel.fetchmany(size=1):
>    print(res)
>    rel.show()
>```
''',
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="size",
                parameter_type=["int"],
                parameter_default="1",
                parameter_description="The number of records to be fetched.",
            )
        ],
    ),
    "fetchnumpy": PythonRelAPIDetails(
        example="rel.fetchnumpy()",
        result="""
{'id': array([UUID('1587b4b0-3023-49fe-82cf-06303ca136ac'),
        UUID('e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd'),
        UUID('3f8ad67a-290f-4a22-b41b-0173b8e45afa'),
        UUID('9a4e37ef-d8bd-46dd-ab01-51cf4973549f'),
        UUID('12baa624-ebc9-45ae-b73e-6f4029e31d2d'),
        UUID('56d41292-53cc-48be-a1b8-e1f5d6ca5581'),
        UUID('1accca18-c950-47c1-9108-aef8afbd5249'),
        UUID('56d8db75-72c4-4d40-90d2-a3c840579c37'),
        UUID('e19f6201-8646-401c-b019-e37c42c39632')], dtype=object),
 'description': array(['value is uneven', 'value is even', 'value is uneven',
        'value is even', 'value is uneven', 'value is even',
        'value is uneven', 'value is even', 'value is uneven'],
       dtype=object),
 'value': array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
 'created_timestamp': array(['2025-04-10T09:24:51.259000', '2025-04-10T09:25:51.259000',
        '2025-04-10T09:26:51.259000', '2025-04-10T09:27:51.259000',
        '2025-04-10T09:28:51.259000', '2025-04-10T09:29:51.259000',
        '2025-04-10T09:30:51.259000', '2025-04-10T09:31:51.259000',
        '2025-04-10T09:32:51.259000'], dtype='datetime64[us]')}
""",
        use_default_example=True,
    ),
    "fetchone": PythonRelAPIDetails(
        example="""
while res := rel.fetchone():
    print(res)
""",
        result="""
(UUID('fe036411-f4c7-4f52-9ddd-80cd2bb56613'), 'value is uneven', 1, datetime.datetime(2025, 4, 30, 12, 59, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('466c9b43-e9f0-4237-8f26-155f259a5b59'), 'value is even', 2, datetime.datetime(2025, 4, 30, 13, 0, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('5755cf16-a94f-41ef-a16d-21e856d71f9f'), 'value is uneven', 3, datetime.datetime(2025, 4, 30, 13, 1, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('05b52c93-bd68-45e1-b02a-a08d682c33d5'), 'value is even', 4, datetime.datetime(2025, 4, 30, 13, 2, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('cf61ef13-2840-4541-900d-f493767d7622'), 'value is uneven', 5, datetime.datetime(2025, 4, 30, 13, 3, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('033e7c68-e800-4ee8-9787-6cf50aabc27b'), 'value is even', 6, datetime.datetime(2025, 4, 30, 13, 4, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('8b8d6545-ff54-45d6-b69a-97edb63dfe43'), 'value is uneven', 7, datetime.datetime(2025, 4, 30, 13, 5, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('7da79dfe-b29c-462b-a414-9d5e3cc80139'), 'value is even', 8, datetime.datetime(2025, 4, 30, 13, 6, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
(UUID('f83ffff2-33b9-4f86-9d14-46974b546bab'), 'value is uneven', 9, datetime.datetime(2025, 4, 30, 13, 7, 8, 912000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
""",
        use_default_example=True,
        additional_description='''
\n
>Warning Executing any operation during the retrieval of the data from an [aggregate](#aggregate) relation,
>will close the result set.
>```python
>import duckdb
>
>duckdb_conn = duckdb.connect()
>
>rel = duckdb_conn.sql("""
>       select 
>           gen_random_uuid() as id, 
>           concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
>           range as value, 
>           now() + concat(range,' ', 'minutes')::interval as created_timestamp
>       from range(1, 10)
>    """
>)
>
>agg_rel = rel.aggregate("value")
>
>while res := agg_rel.fetchone():
>    print(res)
>    rel.show()
>```
''',
    ),
    "pl": PythonRelAPIDetails(
        example="rel.pl(batch_size=1)",
        result="""
shape: (9, 4)
┌─────────────────────────────────┬─────────────────┬───────┬────────────────────────────────┐
│ id                              ┆ description     ┆ value ┆ created_timestamp              │
│ ---                             ┆ ---             ┆ ---   ┆ ---                            │
│ str                             ┆ str             ┆ i64   ┆ datetime[μs, Europe/Amsterdam] │
╞═════════════════════════════════╪═════════════════╪═══════╪════════════════════════════════╡
│ b2f92c3c-9372-49f3-897f-2c86fc… ┆ value is uneven ┆ 1     ┆ 2025-04-10 11:49:51.886 CEST   │
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="batch_size",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The number of records to be fetched per batch.",
            )
        ],
    ),
    "record_batch": PythonRelAPIDetails(
        example="pa_batch = rel.record_batch(batch_size=1)\n\npa_batch.read_next_batch()",
        result="""
pyarrow.RecordBatch
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: ["908cf67c-a086-4b94-9017-2089a83e4a6c"]
description: ["value is uneven"]
value: [1]
created_timestamp: [2025-04-10 09:52:55.249000Z]
""",
        use_default_example=True,
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="batch_size",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The batch size for fetching the data.",
            )
        ],
    ),
    "tf": PythonRelAPIDetails(
        example='rel.select("description, value").tf()',
        result="""
{'description': <tf.Tensor: shape=(9,), dtype=string, numpy=
 array([b'value is uneven', b'value is even', b'value is uneven',
        b'value is even', b'value is uneven', b'value is even',
        b'value is uneven', b'value is even', b'value is uneven'],
       dtype=object)>,
 'value': <tf.Tensor: shape=(9,), dtype=int64, numpy=array([1, 2, 3, 4, 5, 6, 7, 8, 9])>}
""",
        use_default_example=True,
    ),
    "to_arrow_table": PythonRelAPIDetails(
        example="rel.to_arrow_table()",
        result="""
pyarrow.Table
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: [["86b2011d-3818-426f-a41e-7cd5c7321f79","07fa4f89-0bba-4049-9acd-c933332a66d5","f2f1479e-f582-4fe4-b82f-9b753b69634c","529d3c63-5961-4adb-b0a8-8249188fc82a","aa9eea7d-7fac-4dcf-8f32-4a0b5d64f864","4852aa32-03f2-40d3-8006-b8213904775a","c0127203-f2e3-4925-9810-655bc02a3c19","2a1356ba-5707-44d6-a492-abd0a67e5efb","800a1c24-231c-4dae-bd68-627654c8a110"]]
description: [["value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven"]]
value: [[1,2,3,4,5,6,7,8,9]]
created_timestamp: [[2025-04-10 09:54:24.015000Z,2025-04-10 09:55:24.015000Z,2025-04-10 09:56:24.015000Z,2025-04-10 09:57:24.015000Z,2025-04-10 09:58:24.015000Z,2025-04-10 09:59:24.015000Z,2025-04-10 10:00:24.015000Z,2025-04-10 10:01:24.015000Z,2025-04-10 10:02:24.015000Z]]
""",
        use_default_example=True,
        aliases=["fetch_arrow_table", "arrow"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="batch_size",
                parameter_type=["int"],
                parameter_default="1000000",
                parameter_description="The batch size for fetching the data.",
            )
        ],
    ),
    "to_csv": PythonRelAPIDetails(
        example='rel.to_csv("code_example.csv")',
        result="The data is exported to a CSV file, named code_example.csv",
        use_default_example=True,
        aliases=["write_csv"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="file_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the output CSV file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sep",
                parameter_type=["str"],
                parameter_default="','",
                parameter_description="Field delimiter for the output file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="na_rep",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Missing data representation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="header",
                parameter_type=["bool"],
                parameter_default="True",
                parameter_description="Whether to write column headers.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="quotechar",
                parameter_type=["str"],
                parameter_default="'\"'",
                parameter_description="Character used to quote fields containing special characters.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="escapechar",
                parameter_type=["str"],
                parameter_default="None",
                parameter_description="Character used to escape the delimiter if quoting is set to QUOTE_NONE.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="date_format",
                parameter_type=["str"],
                parameter_default="None",
                parameter_description="Custom format string for DATE values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="timestamp_format",
                parameter_type=["str"],
                parameter_default="None",
                parameter_description="Custom format string for TIMESTAMP values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="quoting",
                parameter_type=["int"],
                parameter_default="csv.QUOTE_MINIMAL",
                parameter_description="Control field quoting behavior (e.g., QUOTE_MINIMAL, QUOTE_ALL).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="encoding",
                parameter_type=["str"],
                parameter_default="'utf-8'",
                parameter_description="Character encoding for the output file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["str"],
                parameter_default="auto",
                parameter_description="Compression type (e.g., 'gzip', 'bz2', 'zstd').",
            ),
            PythonRelAPIParamDetails(
                parameter_name="overwrite",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When true, all existing files inside targeted directories will be removed (not supported on remote filesystems). Only has an effect when used with `partition_by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="per_thread_output",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When `true`, write one file per thread, rather than one file in total. This allows for faster parallel writing.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="use_tmp_file",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Write to a temporary file before renaming to final name to avoid partial writes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="partition_by",
                parameter_type=["list[str]"],
                parameter_default="None",
                parameter_description="List of column names to partition output by (creates folder structure).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="write_partition_columns",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether or not to write partition columns into files. Only has an effect when used with `partition_by`.",
            ),
        ],
    ),
    "to_df": PythonRelAPIDetails(
        example="rel.to_df()",
        result="""
                                     id      description  value                created_timestamp
0  e1f79925-60fd-4ee2-ae67-5eff6b0543d1  value is uneven      1 2025-04-10 11:56:04.452000+02:00
1  caa619d4-d79c-4c00-b82e-9319b086b6f8    value is even      2 2025-04-10 11:57:04.452000+02:00
2  64c68032-99b9-4e8f-b4a3-6c522d5419b3  value is uneven      3 2025-04-10 11:58:04.452000+02:00
...
""",
        use_default_example=True,
        aliases=["fetchdf", "df"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="date_as_object",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="If the date columns should be interpreted as Python date objects.",
            )
        ],
    ),
    "to_parquet": PythonRelAPIDetails(
        example='rel.to_parquet("code_example.parquet")',
        result="The data is exported to a Parquet file, named code_example.parquet",
        use_default_example=True,
        aliases=["write_parquet"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="file_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the output Parquet file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["str"],
                parameter_default="'snappy'",
                parameter_description="The compression format to use (`uncompressed`, `snappy`, `gzip`, `zstd`, `brotli`, `lz4`, `lz4_raw`).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="field_ids",
                parameter_type=["STRUCT"],
                parameter_default=None,
                parameter_description="The field_id for each column. Pass auto to attempt to infer automatically.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="row_group_size_bytes",
                parameter_type=["int"],
                parameter_default="row_group_size * 1024",
                parameter_description="The target size of each row group. You can pass either a human-readable string, e.g., 2MB, or an integer, i.e., the number of bytes. This option is only used when you have issued `SET preserve_insertion_order = false;`, otherwise, it is ignored.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="row_group_size",
                parameter_type=["int"],
                parameter_default="122880",
                parameter_description="The target size, i.e., number of rows, of each row group.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="overwrite",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="If True, overwrite the file if it exists.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="per_thread_output",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When `True`, write one file per thread, rather than one file in total. This allows for faster parallel writing.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="use_tmp_file",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Write to a temporary file before renaming to final name to avoid partial writes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="partition_by",
                parameter_type=["list[str]"],
                parameter_default="None",
                parameter_description="List of column names to partition output by (creates folder structure).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="write_partition_columns",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether or not to write partition columns into files. Only has an effect when used with `partition_by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="append",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When `True`, in the event a filename pattern is generated that already exists, the path will be regenerated to ensure no existing files are overwritten. Only has an effect when used with `partition_by`.",
            ),
        ],
    ),
    "to_table": PythonRelAPIDetails(
        example='rel.to_table("table_code_example")',
        result="A table, named table_code_example, is created with the data of the relation",
        use_default_example=True,
        aliases=["create"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="table_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the table to be created. There shouldn't be any other table with the same name.",
            )
        ],
    ),
    "to_view": PythonRelAPIDetails(
        example='rel.to_view("view_code_example", replace=True)',
        result="A view, named view_code_example, is created with the query definition of the relation",
        use_default_example=True,
        aliases=["create_view"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="view_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the view to be created.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="replace",
                parameter_type=["bool"],
                parameter_default="True",
                parameter_description="If the view should be created with `CREATE OR REPLACE`. When set to `False`, there shouldn't be another view with the same `view_name`.",
            ),
        ],
    ),
    "torch": PythonRelAPIDetails(
        example='rel.select("value").torch()',
        result="{'value': tensor([1, 2, 3, 4, 5, 6, 7, 8, 9])}",
        use_default_example=True,
    ),
    "write_csv": PythonRelAPIDetails(
        example='rel.write_csv("code_example.csv")',
        result="The data is exported to a CSV file, named code_example.csv",
        use_default_example=True,
        aliases=["to_csv"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="file_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the output CSV file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="sep",
                parameter_type=["str"],
                parameter_default="','",
                parameter_description="Field delimiter for the output file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="na_rep",
                parameter_type=["str"],
                parameter_default="''",
                parameter_description="Missing data representation.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="header",
                parameter_type=["bool"],
                parameter_default="True",
                parameter_description="Whether to write column headers.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="quotechar",
                parameter_type=["str"],
                parameter_default="'\"'",
                parameter_description="Character used to quote fields containing special characters.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="escapechar",
                parameter_type=["str"],
                parameter_default="None",
                parameter_description="Character used to escape the delimiter if quoting is set to QUOTE_NONE.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="date_format",
                parameter_type=["str"],
                parameter_default="None",
                parameter_description="Custom format string for DATE values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="timestamp_format",
                parameter_type=["str"],
                parameter_default="None",
                parameter_description="Custom format string for TIMESTAMP values.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="quoting",
                parameter_type=["int"],
                parameter_default="csv.QUOTE_MINIMAL",
                parameter_description="Control field quoting behavior (e.g., QUOTE_MINIMAL, QUOTE_ALL).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="encoding",
                parameter_type=["str"],
                parameter_default="'utf-8'",
                parameter_description="Character encoding for the output file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["str"],
                parameter_default="auto",
                parameter_description="Compression type (e.g., 'gzip', 'bz2', 'zstd').",
            ),
            PythonRelAPIParamDetails(
                parameter_name="overwrite",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When true, all existing files inside targeted directories will be removed (not supported on remote filesystems). Only has an effect when used with `partition_by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="per_thread_output",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When `true`, write one file per thread, rather than one file in total. This allows for faster parallel writing.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="use_tmp_file",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Write to a temporary file before renaming to final name to avoid partial writes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="partition_by",
                parameter_type=["list[str]"],
                parameter_default="None",
                parameter_description="List of column names to partition output by (creates folder structure).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="write_partition_columns",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether or not to write partition columns into files. Only has an effect when used with `partition_by`.",
            ),
        ],
    ),
    "write_parquet": PythonRelAPIDetails(
        example='rel.write_parquet("code_example.parquet")',
        result="The data is exported to a Parquet file, named code_example.parquet",
        use_default_example=True,
        aliases=["to_parquet"],
        parameters=[
            PythonRelAPIParamDetails(
                parameter_name="file_name",
                parameter_type=["str"],
                parameter_default=None,
                parameter_description="The name of the output Parquet file.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="compression",
                parameter_type=["str"],
                parameter_default="'snappy'",
                parameter_description="The compression format to use (`uncompressed`, `snappy`, `gzip`, `zstd`, `brotli`, `lz4`, `lz4_raw`).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="field_ids",
                parameter_type=["STRUCT"],
                parameter_default=None,
                parameter_description="The field_id for each column. Pass auto to attempt to infer automatically.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="row_group_size_bytes",
                parameter_type=["int"],
                parameter_default="row_group_size * 1024",
                parameter_description="The target size of each row group. You can pass either a human-readable string, e.g., 2MB, or an integer, i.e., the number of bytes. This option is only used when you have issued `SET preserve_insertion_order = false;`, otherwise, it is ignored.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="row_group_size",
                parameter_type=["int"],
                parameter_default="122880",
                parameter_description="The target size, i.e., number of rows, of each row group.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="overwrite",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="If True, overwrite the file if it exists.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="per_thread_output",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When `True`, write one file per thread, rather than one file in total. This allows for faster parallel writing.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="use_tmp_file",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Write to a temporary file before renaming to final name to avoid partial writes.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="partition_by",
                parameter_type=["list[str]"],
                parameter_default="None",
                parameter_description="List of column names to partition output by (creates folder structure).",
            ),
            PythonRelAPIParamDetails(
                parameter_name="write_partition_columns",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="Whether or not to write partition columns into files. Only has an effect when used with `partition_by`.",
            ),
            PythonRelAPIParamDetails(
                parameter_name="append",
                parameter_type=["bool"],
                parameter_default="False",
                parameter_description="When `True`, in the event a filename pattern is generated that already exists, the path will be regenerated to ensure no existing files are overwritten. Only has an effect when used with `partition_by`.",
            ),
        ],
    ),
}

DOCS_DETAILS_MAP = {
    **CREATION_METHODS_MAP,
    **DEFINITION_METHODS_MAP,
    **TRANSFORMATION_METHODS_MAP,
    **FUNCTION_METHODS_MAP,
    **OUTPUT_METHODS_MAP,
}
