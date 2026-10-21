from dataclasses import dataclass

from generate_python_relational_docs_methods import DUCKDB_DOC_VERSION


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
    alias_of: str = (
        None  # anchor of the entry this member is an alias of; its entry is then only a pointer
    )
    parameters: list[PythonRelAPIParamDetails] = None  # method parameter description
    example: str = (
        None  # either an entire example code, either the code to be placed in DEFAULT_EXAMPLE
    )
    use_default_example: bool = (
        True  # True if it the example should be used in DEFAULT_EXAMPLE
    )
    result_type: str = "text"  # how the result to be presented (text, sql)


DEFAULT_EXAMPLE = """\
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql(\"\"\"
    SELECT *
    FROM (VALUES
        (1, 'jeans', 'clothing', 20, TRUE),
        (2, 't-shirt', 'clothing', 8, FALSE),
        (3, 'jacket', 'clothing', 65, TRUE),
        (4, 'hammer', 'tools', 42, TRUE),
        (5, 'screwdriver', 'tools', 7, TRUE),
        (6, 'drill', 'tools', 89, TRUE)
    ) AS items(id, item, category, price, in_stock)
\"\"\")

{code_example}"""

PLACEHOLDER_EXAMPLE = "```python\n{code_example}\n```"
PLACEHOLDER_RESULT = "```{result_type}\n{result}\n```"


def _link(page):
    return "{% link docs/" + DUCKDB_DOC_VERSION + "/" + page + " %}"


def _param(name, types, description, default=None):
    return PythonRelAPIParamDetails(
        parameter_name=name,
        parameter_type=types,
        parameter_default=default,
        parameter_description=description,
    )


def _keyword(name, types, description, default=None):
    return _param(name, [*types, "keyword-only"], description, default)


# The stars are escaped because the page prints a parameter name in bold.
def _variadic(name, types, description):
    return _param("\\*" + name, types, description)


def _variadic_keywords(name, types, description):
    return _param("\\*\\*" + name, types, description)


_GROUPS = _param(
    "groups",
    ["str"],
    "Comma-separated list of columns to include in the `GROUP BY`.",
    "''",
)
_GROUPS_NOT_WINDOW = _param(
    "groups",
    ["str"],
    "Comma-separated list of columns to include in the `GROUP BY`; cannot be combined with `window_spec`.",
    "''",
)
_WINDOW_NOT_GROUPS = _param(
    "window_spec",
    ["str"],
    "Window specification, written as `OVER (PARTITION BY ... ORDER BY ...)`; cannot be combined with `groups`.",
    "''",
)
_OPTIONAL_WINDOW = _param(
    "window_spec",
    ["str"],
    "Window specification, written as `OVER (PARTITION BY ... ORDER BY ...)`.",
    "''",
)
_REQUIRED_WINDOW = _param(
    "window_spec",
    ["str"],
    "Window specification, written as `OVER (PARTITION BY ... ORDER BY ...)`.",
)
_PROJECTED_COLUMNS = _param(
    "projected_columns",
    ["str"],
    "Comma-separated list of columns to include in the result.",
    "''",
)


def _aggregate_parameters(expression_description, *between):
    return [
        _param("expression", ["str"], expression_description),
        *between,
        _GROUPS_NOT_WINDOW,
        _WINDOW_NOT_GROUPS,
        _PROJECTED_COLUMNS,
    ]


def _group_only_parameters(expression_description):
    return [
        _param("expression", ["str"], expression_description),
        _GROUPS,
        _PROJECTED_COLUMNS,
    ]


def _window_parameters():
    return [_REQUIRED_WINDOW, _PROJECTED_COLUMNS]


_QUANTILE = _param(
    "q",
    ["float", "list[float]"],
    "The quantile to compute, such as 0.5 for the median, or a list of quantiles.",
    "0.5",
)

_PATH_OR_BUFFER = _param(
    "path_or_buffer",
    ["str", "list[str]", "file-like object"],
    "Path to the file, a glob pattern, a list of paths or a file-like object such as `io.StringIO` or `io.BytesIO`.",
)

_MULTI_FILE_KEYWORDS = [
    _keyword(
        "filename",
        ["bool"],
        "Add a column `filename` with the path of the file each row came from.",
        "None",
    ),
    _keyword(
        "hive_partitioning",
        ["bool"],
        f"Interpret the path as a [Hive partitioned path]({_link('data/partitioning/hive_partitioning.md')}).",
        "None",
    ),
    _keyword(
        "union_by_name",
        ["bool"],
        "Align the columns of several files by name instead of by position.",
        "None",
    ),
    _keyword(
        "hive_types",
        ["dict[str, str]"],
        "Types of the Hive partition columns, as a dict of column name to type name.",
        "None",
    ),
    _keyword(
        "hive_types_autocast",
        ["bool"],
        "Whether to detect the types of the Hive partition columns.",
        "None",
    ),
]

_READ_CSV_PARAMETERS = [
    _PATH_OR_BUFFER,
    _keyword(
        "header",
        ["bool", "int"],
        "Whether the first line holds the column names; `0` means `True`. Detected when omitted.",
        "None",
    ),
    _keyword(
        "compression",
        ["str"],
        "Compression of the files: `'none'`, `'gzip'` or `'zstd'`. Detected from the file extension when omitted.",
        "None",
    ),
    _keyword(
        "sep",
        ["str"],
        "Delimiter between the columns, up to 4 bytes; cannot be combined with `delimiter`. Detected when omitted.",
        "None",
    ),
    _keyword("delimiter", ["str"], "Same as `sep`.", "None"),
    _keyword(
        "dtype",
        ["dict[str, str]", "list[str]"],
        "Column types, as a dict of column name to type or a list of types by position; a type is a type name or a `DuckDBPyType`.",
        "None",
    ),
    _keyword(
        "na_values",
        ["str", "list[str]"],
        "Strings that are read as `NULL`.",
        "None",
    ),
    _keyword(
        "skiprows",
        ["int"],
        "Number of lines to skip at the start of each file.",
        "None",
    ),
    _keyword("quotechar", ["str"], "Character used to quote values.", "None"),
    _keyword(
        "escapechar",
        ["str"],
        "Character that escapes the quote character inside a quoted value.",
        "None",
    ),
    _keyword(
        "comment",
        ["str"],
        "Character that starts a comment: a line is read only up to it, and a line that starts with it is skipped.",
        "None",
    ),
    _keyword(
        "thousands",
        ["str"],
        "Character that separates the thousands in numbers; it must differ from `decimal`.",
        "None",
    ),
    _keyword(
        "encoding",
        ["str"],
        "Only UTF-8 is accepted, written `'utf-8'` or `'utf8'`; any other encoding raises `BinderException`.",
        "None",
    ),
    _keyword("parallel", ["bool"], "Whether to use the parallel CSV reader.", "None"),
    _keyword(
        "date_format",
        ["str"],
        f"[Format]({_link('sql/functions/dateformat.md')}) used to parse dates.",
        "None",
    ),
    _keyword(
        "timestamp_format",
        ["str"],
        f"[Format]({_link('sql/functions/dateformat.md')}) used to parse timestamps.",
        "None",
    ),
    _keyword(
        "sample_size",
        ["int"],
        "Number of lines sampled to detect the dialect and the types.",
        "None",
    ),
    _keyword(
        "files_to_sniff",
        ["int"],
        "Number of files sampled to detect the schema when reading several files; `-1` samples all of them.",
        "None",
    ),
    _keyword(
        "auto_detect",
        ["bool"],
        "Whether to detect the dialect, the header and the types. Detected when omitted.",
        "None",
    ),
    _keyword(
        "all_varchar",
        ["bool"],
        "Read every column as `VARCHAR`, without detecting the types.",
        "None",
    ),
    _keyword(
        "normalize_names",
        ["bool"],
        "Normalize the column names; for example, `My Col` becomes `my_col`.",
        "None",
    ),
    _keyword(
        "null_padding",
        ["bool"],
        "Pad a line that lacks columns with `NULL` values on the right.",
        "None",
    ),
    _keyword(
        "strict_mode",
        ["bool"],
        "Whether to refuse a file that is not structurally valid CSV; with `False`, the reader tries to read it anyway.",
        "None",
    ),
    _keyword("names", ["list[str]"], "Column names, as a list.", "None"),
    _keyword(
        "lineterminator",
        ["str", "CSVLineTerminator"],
        "The line ending: one of `duckdb.CSVLineTerminator.LINE_FEED`, `duckdb.CSVLineTerminator.CARRIAGE_RETURN_LINE_FEED`, `'\\\\n'` and `'\\\\r\\\\n'`, the last two being escape text as written in Python; a string that holds the newline character itself, such as `'\\n'`, is refused.",
        "None",
    ),
    _keyword(
        "columns",
        ["dict[str, str]"],
        "Column names and types, as a dict of column name to type name; the types are then not detected.",
        "None",
    ),
    _keyword(
        "auto_type_candidates",
        ["list[str]"],
        "Types the reader may choose from when it detects the column types; `VARCHAR` is always one of them.",
        "None",
    ),
    _keyword(
        "max_line_size",
        ["int", "str"],
        "Maximum line size, in bytes.",
        "None",
    ),
    _keyword("ignore_errors", ["bool"], "Skip the lines that fail to parse.", "None"),
    _keyword(
        "store_rejects",
        ["bool"],
        f"Skip the lines with errors and store them in the [rejects table]({_link('data/csv/reading_faulty_csv_files.md')}).",
        "None",
    ),
    _keyword(
        "rejects_table",
        ["str"],
        "Name of the temporary table that holds the faulty lines.",
        "None",
    ),
    _keyword(
        "rejects_scan",
        ["str"],
        "Name of the temporary table that holds information on the scans that found faulty lines.",
        "None",
    ),
    _keyword(
        "rejects_limit",
        ["int"],
        "Maximum number of faulty lines stored for each file; `0` means no limit.",
        "None",
    ),
    _keyword(
        "force_not_null",
        ["list[str]"],
        "Columns whose values are never read as `NULL`.",
        "None",
    ),
    _keyword(
        "buffer_size",
        ["int"],
        "Size of the buffers used to read the files, in bytes.",
        "None",
    ),
    _keyword("decimal", ["str"], "Decimal separator of numbers.", "None"),
    _keyword(
        "allow_quoted_nulls",
        ["bool"],
        "Whether a quoted value can be read as `NULL`.",
        "None",
    ),
    *_MULTI_FILE_KEYWORDS,
]

_READ_CSV_DESCRIPTION = f"""

The options other than `path_or_buffer` are keyword arguments; an unknown one raises `InvalidInputException`. Most are the option of the same name of the SQL [`read_csv` function]({_link('data/csv/overview.md')}#parameters); `sep` and `delimiter` are `delim`, `dtype` is `dtypes`, `na_values` is `nullstr`, `skiprows` is `skip`, `quotechar` is `quote`, `escapechar` is `escape`, `date_format` is `dateformat`, `timestamp_format` is `timestampformat`, `lineterminator` is `new_line` and `decimal` is `decimal_separator`."""

_READ_PARQUET_DESCRIPTION = f"""

Each option is the option of the same name of the SQL [`read_parquet` function]({_link('data/parquet/overview.md')})."""

_READ_PARQUET_PARAMETERS = [
    _param(
        "path_or_buffer",
        ["str", "list[str]", "file-like object"],
        "Path to the Parquet file, a glob pattern, a list of paths or a file object opened in binary mode.",
    ),
    _param(
        "binary_as_string",
        ["bool"],
        "Read binary columns as strings, for files from writers that do not mark their strings as UTF-8.",
        "False",
    ),
    _keyword(
        "file_row_number",
        ["bool"],
        "Add a column `file_row_number` with the number of each row within its file.",
        "False",
    ),
    _keyword(
        "filename",
        ["bool"],
        "Add a column `filename` with the path of the file each row came from.",
        "False",
    ),
    _keyword(
        "hive_partitioning",
        ["bool"],
        f"Interpret the path as a [Hive partitioned path]({_link('data/partitioning/hive_partitioning.md')}).",
        "False",
    ),
    _keyword(
        "union_by_name",
        ["bool"],
        "Align the columns of several files by name instead of by position.",
        "False",
    ),
    _keyword(
        "compression",
        ["str"],
        "Accepted and ignored: a Parquet file records its own compression.",
        "None",
    ),
]

_SQL_PARAMETERS = [
    _param(
        "query",
        ["str"],
        "The SQL text; when it holds several statements, the ones before the last run at the call.",
    ),
    _keyword("alias", ["str"], "Alias of the relation.", "''"),
    _keyword(
        "params",
        ["list", "dict"],
        "Values of the query parameters: a list for `?` and `$1` markers, a dict for `$name` markers. The list or dict is copied at the call, as is any list, tuple or dict inside it; the values in it are converted each time the relation runs, so a `bytearray` changed in place afterwards is read changed.",
        "None",
    ),
]

_OVERWRITE_FILE = "Whether an existing file may be replaced. Omitted or `True`, an existing file is replaced; `False` refuses an existing file with `IOException`."
_WRITE_CSV_OVERWRITE = _keyword(
    "overwrite",
    ["bool"],
    _OVERWRITE_FILE
    + " With `partition_by`, only `True` writes into a directory that already holds files.",
    "None",
)
_WRITE_PARQUET_OVERWRITE = _keyword(
    "overwrite",
    ["bool"],
    _OVERWRITE_FILE
    + " With `partition_by`, `True` writes into a directory that already holds files, as `append=True` does.",
    "None",
)
_WRITE_COMMON = [
    _keyword(
        "per_thread_output",
        ["bool"],
        "Write one file per thread into the directory `file_name`, rather than one file.",
        "None",
    ),
    _keyword(
        "use_tmp_file",
        ["bool"],
        "Write to a temporary file first, so a cancelled write does not leave a broken file in place of an existing one.",
        "None",
    ),
    _keyword(
        "partition_by",
        ["list[str]"],
        f"Columns to partition the output by, written as [Hive partitioned]({_link('data/partitioning/partitioned_writes.md')}) directories under `file_name`.",
        "None",
    ),
    _keyword(
        "write_partition_columns",
        ["bool"],
        "Whether to also write the partition columns into the files; only has an effect with `partition_by`.",
        "None",
    ),
]

_WRITE_CSV_PARAMETERS = [
    _param(
        "file_name",
        ["str"],
        "Path of the CSV file to write; a directory with `partition_by` or `per_thread_output`.",
    ),
    _keyword(
        "sep", ["str"], "Delimiter between the columns; a comma when omitted.", "None"
    ),
    _keyword(
        "na_rep", ["str"], "Text written for `NULL` values; empty when omitted.", "None"
    ),
    _keyword(
        "header",
        ["bool"],
        "Whether to write a first line with the column names; written when omitted.",
        "None",
    ),
    _keyword(
        "quotechar",
        ["str"],
        'Character used to quote values; `"` when omitted.',
        "None",
    ),
    _keyword(
        "escapechar",
        ["str"],
        'Character written before a quote character inside a quoted value; `"` when omitted.',
        "None",
    ),
    _keyword(
        "date_format",
        ["str"],
        f"[Format]({_link('sql/functions/dateformat.md')}) used to write dates.",
        "None",
    ),
    _keyword(
        "timestamp_format",
        ["str"],
        f"[Format]({_link('sql/functions/dateformat.md')}) used to write timestamps.",
        "None",
    ),
    _keyword(
        "quoting",
        ["str", "int"],
        "Quote every value: pass `csv.QUOTE_ALL`, `'ALL'` or `'FORCE'`; any other value is refused. Values are quoted only where needed when omitted.",
        "None",
    ),
    _keyword(
        "encoding",
        ["str"],
        "Only UTF-8 is accepted, written `'utf-8'` or `'utf8'`.",
        "None",
    ),
    _keyword(
        "compression",
        ["str"],
        "Compression of the file: `'none'`, `'gzip'` or `'zstd'`. Chosen from the file extension when omitted.",
        "None",
    ),
    _WRITE_CSV_OVERWRITE,
    *_WRITE_COMMON,
]

_WRITE_PARQUET_PARAMETERS = [
    _param(
        "file_name",
        ["str"],
        "Path of the Parquet file to write; a directory with `partition_by`, `per_thread_output` or `file_size_bytes`.",
    ),
    _keyword(
        "compression",
        ["str"],
        "Compression codec: `'uncompressed'`, `'snappy'`, `'gzip'`, `'zstd'`, `'brotli'`, `'lz4'` or `'lz4_raw'`; `'snappy'` when omitted.",
        "None",
    ),
    _keyword(
        "field_ids",
        ["dict", "str"],
        "The Parquet `field_id` of each column, as a dict of column name to id, or `'auto'` to assign them.",
        "None",
    ),
    _keyword(
        "row_group_size_bytes",
        ["int", "str"],
        "Target size of each row group, as a number of bytes or a text such as `'2MB'`.",
        "None",
    ),
    _keyword(
        "row_group_size",
        ["int"],
        "Target number of rows of each row group; 122880 when omitted.",
        "None",
    ),
    _WRITE_PARQUET_OVERWRITE,
    *_WRITE_COMMON,
    _keyword(
        "append",
        ["bool"],
        "When a generated file name already exists, choose another name instead of overwriting the file; only has an effect when several files are written. Combined with `overwrite`, it raises `BinderException`.",
        "None",
    ),
    _keyword(
        "filename_pattern",
        ["str"],
        "Pattern of the names of the files written, where `{i}` is replaced by an index and `{uuid}` by a UUID; only has an effect when several files are written.",
        "None",
    ),
    _keyword(
        "file_size_bytes",
        ["int", "str"],
        "Start a new file in the directory `file_name` when a file grows past this size, given as a number of bytes or a text such as `'1MB'`.",
        "None",
    ),
]

_WRITE_CSV_DESCRIPTION = f"""

Most options are the option of the same name of the [`COPY ... TO` statement]({_link('sql/statements/copy.md')}); `sep` is `DELIMITER`, `na_rep` is `NULL`, `quotechar` is `QUOTE`, `escapechar` is `ESCAPE`, `quoting` sets `FORCE_QUOTE` for every column and `overwrite` is `OVERWRITE_OR_IGNORE`."""

_WRITE_PARQUET_DESCRIPTION = f"""

Each option is the option of the same name of the [`COPY ... TO` statement]({_link('sql/statements/copy.md')}), except `overwrite`, which is `OVERWRITE_OR_IGNORE`."""

_DATE_AS_OBJECT = _keyword(
    "date_as_object",
    ["bool"],
    "If the date columns should be interpreted as Python date objects.",
    "False",
)


_BATCH_SIZE = _param(
    "batch_size",
    ["int"],
    "The number of rows of each Arrow record batch.",
    "131072",
)


def _deprecated(name, replacement):
    return f"\n\n> Deprecated `{name}()` is deprecated. Use [`{replacement}()`](#{replacement}) instead."


_TABLE_NAME = (
    "The name of the table: `table`, `schema.table` or `catalog.schema.table`; a name of more parts raises "
    "`NotImplementedException`."
)

_CREATE_PARAMETERS = [
    _param(
        "table_name",
        ["str"],
        _TABLE_NAME + " There must not be a table of that name already.",
    )
]

_CREATE_VIEW_PARAMETERS = [
    _param("view_name", ["str"], "The name of the view to be created."),
    _param(
        "replace",
        ["bool"],
        "If the view should be created with `CREATE OR REPLACE`. When set to `False`, there must not be a view of that name already.",
        "True",
    ),
]

_CREATE_VIEW_DESCRIPTION = """

A view stores SQL text, so a relation over rows that DuckDB holds for it cannot become one: a relation from [`values()`](#values) or [`materialize()`](#materialize) or over a statement that ran at the call, such as an `INSERT`, raises `InvalidInputException`. Use [`create()`](#create) to store such rows in a table, or `con.register(name, rel)` for a temporary view that lasts as long as the connection."""

_SET_OPERATION_PARAMETER = (
    "The relation to combine with this one; it must have the same number of columns."
)

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
        use_default_example=False,
        parameters=[
            _param(
                "arrow_object",
                ["object"],
                "The Arrow object to create a relation from: a table, a record batch, a record batch reader, a dataset, a scanner, a polars DataFrame or an object that exports the Arrow PyCapsule interface.",
            )
        ],
    ),
    "from_csv_auto": PythonRelAPIDetails(alias_of="read_csv"),
    "from_df": PythonRelAPIDetails(
        example="""
import duckdb
import pandas as pd

df = pd.DataFrame(data = {'id': [1], "text":["a"]})

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_df(df)

rel.show()
""",
        use_default_example=False,
        parameters=[
            _param(
                "df",
                ["pandas.DataFrame"],
                "A pandas DataFrame to be converted into a DuckDB relation.",
            )
        ],
    ),
    "from_parquet": PythonRelAPIDetails(alias_of="read_parquet"),
    "from_query": PythonRelAPIDetails(alias_of="sql"),
    "query": PythonRelAPIDetails(alias_of="sql"),
    "read_csv": PythonRelAPIDetails(
        additional_description=_READ_CSV_DESCRIPTION,
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
        use_default_example=False,
        aliases=["from_csv_auto"],
        parameters=_READ_CSV_PARAMETERS,
    ),
    "read_json": PythonRelAPIDetails(
        additional_description=f"""

The options other than `path_or_buffer` are keyword arguments; an unknown one raises `TypeError`. Each is the option of the same name of the SQL [`read_json` function]({_link('data/json/loading_json.md')}).""",
        example="""
import duckdb
import json

with open("code_example.json", mode="w") as f:
    json.dump([{'id': 1, "text":"a"}], f)

duckdb_conn = duckdb.connect()

rel = duckdb_conn.read_json("code_example.json")

rel.show()
""",
        use_default_example=False,
        parameters=[
            _PATH_OR_BUFFER,
            _keyword(
                "columns",
                ["dict[str, str]"],
                "Key names and types, as a dict of key name to type name; the schema is then not detected.",
                "None",
            ),
            _keyword(
                "sample_size",
                ["int"],
                "Number of objects sampled to detect the types; `-1` samples all of them.",
                "None",
            ),
            _keyword(
                "maximum_depth",
                ["int"],
                "Maximum nesting depth to which the types are detected; `-1` detects all levels.",
                "None",
            ),
            _keyword(
                "records",
                ["str"],
                "`'true'` to read each object as a row of columns, `'false'` to read each as one value, `'auto'` to detect it.",
                "None",
            ),
            _keyword(
                "format",
                ["str"],
                "`'auto'`, `'unstructured'`, `'newline_delimited'` or `'array'`.",
                "None",
            ),
            _keyword(
                "date_format",
                ["str"],
                f"[Format]({_link('sql/functions/dateformat.md')}) used to parse dates.",
                "None",
            ),
            _keyword(
                "timestamp_format",
                ["str"],
                f"[Format]({_link('sql/functions/dateformat.md')}) used to parse timestamps.",
                "None",
            ),
            _keyword(
                "compression",
                ["str"],
                "Compression of the files: `'none'`, `'gzip'`, `'zstd'` or `'auto_detect'`. Detected from the file extension when omitted.",
                "None",
            ),
            _keyword(
                "maximum_object_size",
                ["int"],
                "Maximum size of a JSON object, in bytes.",
                "None",
            ),
            _keyword(
                "ignore_errors",
                ["bool"],
                "Read the objects that fail to parse as `NULL` rows; only with `format='newline_delimited'`.",
                "None",
            ),
            _keyword(
                "convert_strings_to_integers",
                ["bool"],
                "Whether strings that hold integers are read as numbers.",
                "None",
            ),
            _keyword(
                "field_appearance_threshold",
                ["float"],
                "When the fields of an object appear, on average, in a smaller fraction of the sampled objects than this, the object is read as a `MAP`.",
                "None",
            ),
            _keyword(
                "map_inference_threshold",
                ["int"],
                "An object with more fields than this is read as a `MAP` instead of a `STRUCT`; `-1` never reads a `MAP`.",
                "None",
            ),
            _keyword(
                "maximum_sample_files",
                ["int"],
                "Maximum number of files sampled to detect the schema.",
                "None",
            ),
            *_MULTI_FILE_KEYWORDS,
        ],
    ),
    "read_parquet": PythonRelAPIDetails(
        additional_description=_READ_PARQUET_DESCRIPTION,
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
        use_default_example=False,
        aliases=["from_parquet"],
        parameters=_READ_PARQUET_PARAMETERS,
    ),
    "sql": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("SELECT * FROM range(1, 4) tbl(id) WHERE id > $minimum", params={"minimum": 1})

rel.show()
""",
        use_default_example=False,
        aliases=["from_query", "query"],
        parameters=_SQL_PARAMETERS,
    ),
    "table": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("CREATE TABLE code_example AS SELECT * FROM range(1, 2) tbl(id)")

rel = duckdb_conn.table("code_example")

rel.show()
""",
        use_default_example=False,
        parameters=[
            _param(
                "table_name",
                ["str"],
                "Name of the table to create a relation from.",
            )
        ],
    ),
    "table_function": PythonRelAPIDetails(
        example='''
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
    CREATE MACRO get_record_for(x) AS TABLE
    SELECT x * range AS result FROM range(1, 2)
""")

rel = duckdb_conn.table_function(name="get_record_for", parameters=[1])

rel.show()
''',
        use_default_example=False,
        parameters=[
            _param("name", ["str"], "Name of the table function to call."),
            _param(
                "parameters",
                ["list"],
                "The arguments to pass to the table function, as a list.",
                "None",
            ),
        ],
    ),
    "values": PythonRelAPIDetails(
        additional_description="""

Python values are converted once, at the call, so a later change to the Python objects does not change the relation. Such a relation reads rows held in this process, which [`create_view()`](#create_view) refuses.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.values([1, 'a'])

rel.show()
""",
        use_default_example=False,
        parameters=[
            _variadic(
                "args",
                ["list", "tuple", "object"],
                "The rows: one list holding the values of one row, several tuples for several rows or the values of one row as separate arguments. A value is a Python value or an Expression.",
            )
        ],
    ),
    "view": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("CREATE VIEW code_example AS SELECT * FROM range(1, 2) tbl(id)")

rel = duckdb_conn.view("code_example")

rel.show()
""",
        use_default_example=False,
        parameters=[
            _param(
                "view_name",
                ["str"],
                "Name of the view to create a relation from.",
            )
        ],
    ),
}

DEFINITION_METHODS_MAP = {
    "alias": PythonRelAPIDetails(
        example='rel.set_alias("my_relation").alias',
    ),
    "columns": PythonRelAPIDetails(
        example="rel.columns",
    ),
    "describe": PythonRelAPIDetails(
        example="rel.describe()",
    ),
    "description": PythonRelAPIDetails(
        example="rel.description",
    ),
    "dtypes": PythonRelAPIDetails(alias_of="types"),
    "explain": PythonRelAPIDetails(
        additional_description=f"""

With `analyze=True` or with `type` set to `'analyze'` or `duckdb.ExplainType.ANALYZE`, the query runs and the plan shows the rows and the time of each operator, as [`EXPLAIN ANALYZE`]({_link('guides/meta/explain_analyze.md')}) does.""",
        example="print(rel.explain())",
        parameters=[
            _param(
                "type",
                ["str", "ExplainType"],
                "`'standard'` or `duckdb.ExplainType.STANDARD` for the plan, `'analyze'` or `duckdb.ExplainType.ANALYZE` to run the query and profile it.",
                "ExplainType.STANDARD",
            ),
            _param(
                "format",
                ["str"],
                "The output format, such as `'text'`, `'json'`, `'html'`, `'graphviz'` or `'yaml'`. The default draws the plan as text, and as HTML under Jupyter.",
                "None",
            ),
            _keyword(
                "analyze",
                ["bool"],
                "Run the query and profile it, as `type='analyze'` does.",
                "False",
            ),
        ],
    ),
    "preview": PythonRelAPIDetails(
        example="print(rel.preview(3))",
        parameters=[
            _param("limit", ["int"], "The number of rows to draw.", "10"),
        ],
    ),
    "query-1": PythonRelAPIDetails(
        example='rel.query(virtual_table_name="items", sql_query="SELECT max(price) AS max_price FROM items")',
        parameters=[
            _param(
                "virtual_table_name",
                ["str"],
                "The name under which `sql_query` reads the relation.",
            ),
            _param(
                "sql_query",
                ["str"],
                "The SQL query, a single statement, that reads the relation by the name `virtual_table_name`.",
            ),
        ],
    ),
    "set_alias": PythonRelAPIDetails(
        example='rel.set_alias("items").select("items.item, items.price")',
        parameters=[
            _param(
                "alias",
                ["str"],
                "The alias name to assign to the relation.",
            )
        ],
    ),
    "shape": PythonRelAPIDetails(
        example="rel.shape",
    ),
    "show": PythonRelAPIDetails(
        example="rel.show()",
        parameters=[
            _keyword(
                "max_width",
                ["int"],
                "Maximum display width for the entire output in characters.",
                "None",
            ),
            _keyword(
                "max_rows",
                ["int"],
                "Maximum number of rows to display.",
                "None",
            ),
            _keyword(
                "max_col_width",
                ["int"],
                "Maximum number of characters to display per column.",
                "None",
            ),
            _keyword(
                "null_value",
                ["str"],
                "String to display in place of NULL values.",
                "None",
            ),
            _keyword(
                "render_mode",
                ["RenderMode"],
                "`duckdb.RenderMode.ROWS` to draw a row per line, `duckdb.RenderMode.COLUMNS` to draw a column per line.",
                "None",
            ),
        ],
    ),
    "sql_query": PythonRelAPIDetails(
        example="print(rel.sql_query())",
        result_type="sql",
    ),
    "type": PythonRelAPIDetails(
        example="rel.type",
    ),
    "types": PythonRelAPIDetails(
        example="rel.types",
        aliases=["dtypes"],
    ),
}

TRANSFORMATION_METHODS_MAP = {
    "aggregate": PythonRelAPIDetails(
        example='rel.aggregate("category, max(price) AS max_price").order("category")',
        parameters=[
            _param(
                "aggr_expr",
                ["str", "list[Expression]"],
                "The columns and aggregates to compute: SQL text, or a list of Expressions, in which a string is a column name.",
            ),
            _param(
                "group_expr",
                ["str", "Expression", "None"],
                "The columns to group by, as SQL text or an Expression. `''` or `None` groups by every column of `aggr_expr` that is not an aggregate (`GROUP BY ALL`).",
                "''",
            ),
        ],
    ),
    "apply": PythonRelAPIDetails(
        example='rel.apply("max", "price", group_expr="category", projected_columns="category").order("category")',
        parameters=[
            _param(
                "function_name",
                ["str"],
                "Name of the function to apply over the relation.",
            ),
            _param(
                "function_aggr",
                ["str"],
                "The list of columns to apply the function over.",
            ),
            _param(
                "group_expr",
                ["str"],
                "Optional SQL expression for grouping.",
                "''",
            ),
            _param(
                "function_parameter",
                ["str"],
                "Optional parameters to pass into the function.",
                "''",
            ),
            _PROJECTED_COLUMNS,
        ],
    ),
    "cross": PythonRelAPIDetails(
        example="""
sizes = duckdb_conn.sql("SELECT * FROM (VALUES ('S'), ('M')) AS sizes(size)")

rel.filter("category = 'clothing'").select("item").cross(sizes).order("item, size")
""",
        parameters=[
            _param(
                "other_rel",
                ["DuckDBPyRelation"],
                "Another relation to perform a cross product with.",
            )
        ],
    ),
    "distinct": PythonRelAPIDetails(
        example='rel.select("category").distinct().order("category")',
        parameters=[
            _param(
                "on",
                ["str", "Expression", "list"],
                "A column name, an Expression or a list of them: keep one row for each distinct value of these columns, as SQL `DISTINCT ON` does. Omitted, only fully duplicate rows are removed.",
                "None",
            )
        ],
    ),
    "drop": PythonRelAPIDetails(
        example='rel.drop("id", "in_stock")',
        parameters=[
            _variadic(
                "columns",
                ["str"],
                "Names of the columns to remove; a name the relation does not have raises `BinderException`.",
            )
        ],
    ),
    "except_": PythonRelAPIDetails(
        additional_description="""

The difference is `EXCEPT ALL`, so duplicates count: a row that appears three times in this relation and once in `other_rel` appears twice in the result.""",
        example="""
categories = rel.select("category")
expensive = rel.filter("price > 30").select("category")

categories.except_(expensive).order("category")
""",
        parameters=[
            _param(
                "other_rel",
                ["DuckDBPyRelation"],
                _SET_OPERATION_PARAMETER,
            )
        ],
    ),
    "filter": PythonRelAPIDetails(
        example='rel.filter("price > 30")',
        parameters=[
            _param(
                "filter_expr",
                ["str", "Expression"],
                "The filter expression to apply over the relation.",
            )
        ],
    ),
    "group_by": PythonRelAPIDetails(
        additional_description="""

`group_by()` returns a grouped relation whose only method is `agg(*aggregates)`. `agg()` reads its arguments as [`aggregate()`](#aggregate) reads `aggr_expr`: one string is SQL text, which may list several aggregates; among several arguments, a string is a column name and an Expression is an aggregate. It returns a relation whose first columns are the group columns.""",
        example='rel.group_by("category").agg("sum(price) AS total, count(*) AS n").order("category")',
        parameters=[
            _variadic(
                "columns",
                ["str", "Expression"],
                "The columns to group by: column names or Expressions.",
            )
        ],
    ),
    "head": PythonRelAPIDetails(
        example="rel.head(3)",
        parameters=[
            _param("n", ["int"], "The number of rows to keep.", "5"),
        ],
    ),
    "insert": PythonRelAPIDetails(
        additional_description="""

The relation must read a table, as one from [`table()`](#table) does. The relation runs again on every read, so reading it afterwards shows the new rows.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("CREATE TABLE items (item VARCHAR, price INTEGER)")

rel = duckdb_conn.table("items")

rel.insert(("jeans", 20))
rel.insert(["hammer", 42])

rel.order("item")
""",
        use_default_example=False,
        parameters=[
            _param(
                "values",
                ["tuple", "list", "object"],
                "The values of one row in the order of the table's columns: a tuple, a list or, for a table of one column, a single value.",
            )
        ],
    ),
    "insert_into": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("CREATE TABLE items (item VARCHAR, price INTEGER)")

rel = duckdb_conn.values(("jeans", 20), ("hammer", 42))

rel.insert_into("items")

duckdb_conn.table("items").order("item")
""",
        use_default_example=False,
        parameters=[
            _param(
                "table_name",
                ["str"],
                _TABLE_NAME
                + " The table must exist, and the relation must have its columns in the table's column order.",
            )
        ],
    ),
    "intersect": PythonRelAPIDetails(
        additional_description="""

The intersection is `INTERSECT ALL`, so duplicates count: a row that appears three times in this relation and twice in `other_rel` appears twice in the result.""",
        example="""
categories = rel.select("category")
expensive = rel.filter("price > 30").select("category")

categories.intersect(expensive).order("category")
""",
        parameters=[
            _param(
                "other_rel",
                ["DuckDBPyRelation"],
                _SET_OPERATION_PARAMETER,
            )
        ],
    ),
    "join": PythonRelAPIDetails(
        additional_description=f"""

An `'inner'`, `'left'`, `'right'`, `'outer'`, `'full'`, `'semi'`, `'anti'` or `'asof'` join needs a `condition`, and raises `InvalidInputException` without one; a `'cross'`, `'positional'` or `'natural'` join takes none. The [joins section of the `FROM` clause]({_link('sql/query_syntax/from.md')}#joins) says what each join type does. A `CROSS` join is also provided through the [`cross()`](#cross) method.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

left = duckdb_conn.sql("SELECT * FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) AS t(id, name)")
right = duckdb_conn.sql("SELECT * FROM (VALUES (1, 'x'), (3, 'z'), (4, 'w')) AS t(id, name)")

print(left.join(right, "id").order("id"))

left.join(right, lambda a, b: a["id"] == b["id"], how="left", suffix="_right").order("id")
""",
        use_default_example=False,
        parameters=[
            _param(
                "other_rel",
                ["DuckDBPyRelation"],
                "The relation to join with the current relation.",
            ),
            _param(
                "condition",
                ["str", "list[str]", "Expression", "Callable"],
                "The join condition: SQL text such as `'a.id = b.id'`, a column name or a list of column names for a `USING` join, an Expression or a function that takes the two sides and returns an Expression, where `side['id']` is the column `id` of that side.",
                "None",
            ),
            _param(
                "how",
                ["str"],
                "The type of join: `'inner'`, `'left'`, `'right'`, `'outer'`, `'full'`, `'semi'`, `'anti'`, `'cross'`, `'positional'`, `'natural'` or `'asof'`.",
                "'inner'",
            ),
            _param(
                "suffix",
                ["str"],
                "Rename each column of the right side whose name the left side also has, by appending the suffix; the columns of a `USING` or natural join, which appear once, keep their names.",
                "None",
            ),
        ],
    ),
    "limit": PythonRelAPIDetails(
        additional_description="""

To read the first rows into Python, as `fetchone()` and `fetchmany()` did on a relation before DuckDB 2.0, use `rel.limit(1).fetchall()` and `rel.limit(n).fetchall()`. To read all the rows a batch at a time, use [`iter_rows()`](#iter_rows).""",
        example="rel.limit(1)",
        parameters=[
            _param(
                "n",
                ["int"],
                "The maximum number of rows to return.",
            ),
            _param(
                "offset",
                ["int"],
                "The number of rows to skip before starting to return rows.",
                "0",
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
rel = duckdb_conn.sql("SELECT range AS id, 'dummy' AS text FROM range(1, 3)")

rel.map(multiply_by_2, schema={"id": int, "text": str})
""",
        use_default_example=False,
        parameters=[
            _param(
                "map_function",
                ["Callable"],
                "A Python function that takes a DataFrame and returns a transformed DataFrame.",
            ),
            _keyword(
                "schema",
                ["dict"],
                "The columns of the output relation, as a dict of name to type. Without it, the function is called once on an empty DataFrame when the relation is built, to learn the columns it returns.",
                "None",
            ),
        ],
    ),
    "offset": PythonRelAPIDetails(
        example='rel.order("id").offset(4)',
        parameters=[
            _param("n", ["int"], "The number of rows to skip."),
        ],
    ),
    "order": PythonRelAPIDetails(
        example='rel.order("price DESC")',
        parameters=[
            _param(
                "order_expr",
                ["str", "Expression"],
                "The ordering of the rows: SQL text such as `'price DESC'`, or an Expression such as `col('price').desc()`.",
            )
        ],
    ),
    "pivot": PythonRelAPIDetails(
        additional_description=f"""

It runs a [`PIVOT`]({_link('sql/statements/pivot.md')}) with the values given; the columns not named in `column` or `aggregate` are the rows of the result.""",
        example="""
rel.select("in_stock, category, price").pivot("category", ["clothing", "tools"], "sum(price)").order("in_stock")
""",
        parameters=[
            _param(
                "column",
                ["str", "Expression"],
                "The column whose values become the new columns.",
            ),
            _param(
                "values",
                ["Iterable"],
                "The values of `column` that become columns, as Python values.",
            ),
            _param(
                "aggregate",
                ["str", "Expression"],
                "The aggregate each new column holds, as SQL text or an Expression.",
            ),
        ],
    ),
    "project": PythonRelAPIDetails(alias_of="select"),
    "rename": PythonRelAPIDetails(
        example='rel.rename(price="unit_price")',
        parameters=[
            _variadic_keywords(
                "columns",
                ["str"],
                "The columns to rename, as `old=new`; a name the relation does not have raises `BinderException`.",
            )
        ],
    ),
    "sample": PythonRelAPIDetails(
        additional_description=f"""

See [Samples]({_link('sql/samples.md')}) for the sampling methods. A fixed `seed` gives the same sample on every run only when DuckDB runs on one thread.""",
        example="""
duckdb_conn.sql("SET threads = 1")

rel.sample(3, seed=42).order("id")
""",
        parameters=[
            _param(
                "n",
                ["int"],
                "The number of rows to draw; give either `n` or `percent`.",
                "None",
            ),
            _keyword(
                "percent",
                ["float"],
                "The percentage of the rows to draw.",
                "None",
            ),
            _keyword(
                "seed",
                ["int"],
                "The seed of the random draw.",
                "None",
            ),
            _keyword(
                "method",
                ["str"],
                "`'reservoir'`, `'bernoulli'` or `'system'`; `'reservoir'` for `n` and `'bernoulli'` for `percent` when omitted.",
                "None",
            ),
        ],
    ),
    "select": PythonRelAPIDetails(
        example='rel.select("item, price")',
        aliases=["project"],
        parameters=[
            _variadic(
                "args",
                ["str", "Expression"],
                "The columns to keep, as strings or Expressions. A single string is SQL text, which may list several columns or expressions; among several arguments, each string names one column.",
            ),
            _keyword(
                "groups",
                ["str"],
                "Comma-separated list of columns to include in the `GROUP BY`.",
                "''",
            ),
        ],
    ),
    "select_dtypes": PythonRelAPIDetails(alias_of="select_types"),
    "select_types": PythonRelAPIDetails(
        example="rel.select_types([duckdb.sqltypes.VARCHAR])",
        aliases=["select_dtypes"],
        parameters=[
            _param(
                "types",
                ["list"],
                "The types of the columns to keep, as a list of `DuckDBPyType` values or type names such as `'VARCHAR'`.",
            )
        ],
    ),
    "sort": PythonRelAPIDetails(
        example='rel.sort("category", "price DESC")',
        parameters=[
            _variadic(
                "args",
                ["str", "Expression"],
                "The expressions to sort by, as SQL text such as `'price DESC'` or as Expressions.",
            )
        ],
    ),
    "union": PythonRelAPIDetails(
        additional_description="""

The union is `UNION ALL`, so it keeps duplicate rows. To keep only distinct rows, apply [`distinct()`](#distinct).""",
        example='rel.union(rel).count("*")',
        parameters=[
            _param(
                "union_rel",
                ["DuckDBPyRelation"],
                _SET_OPERATION_PARAMETER,
            )
        ],
    ),
    "union_by_name": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

first = duckdb_conn.sql("SELECT 1 AS id, 10 AS x")
second = duckdb_conn.sql("SELECT 20 AS y, 2 AS id")

first.union_by_name(second).order("id")
""",
        use_default_example=False,
        parameters=[
            _param(
                "other",
                ["DuckDBPyRelation"],
                "The relation to combine with this one; a column that only one of them has is `NULL` in the rows of the other.",
            ),
            _keyword(
                "all",
                ["bool"],
                "Keep duplicate rows (`UNION ALL BY NAME`); with `False`, keep only distinct rows (`UNION BY NAME`).",
                "True",
            ),
        ],
    ),
    "unnest": PythonRelAPIDetails(
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("SELECT 1 AS id, [10, 20] AS amounts UNION ALL SELECT 2, [30]")

rel.unnest("amounts").order("id, amounts")
""",
        use_default_example=False,
        parameters=[
            _variadic(
                "columns",
                ["str"],
                "Names of the list columns to expand; each keeps its name and holds one element per row.",
            )
        ],
    ),
    "unpivot": PythonRelAPIDetails(
        additional_description=f"""

It runs an [`UNPIVOT`]({_link('sql/statements/unpivot.md')}); the columns not named stay as they are, repeated for each new row.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("SELECT * FROM (VALUES ('north', 10, 20), ('south', 30, 40)) AS t(region, q1, q2)")

rel.unpivot("q1", "q2", name="quarter", value="amount").order("region, quarter")
""",
        use_default_example=False,
        parameters=[
            _variadic(
                "columns",
                ["str"],
                "Names of the columns to turn into rows.",
            ),
            _keyword(
                "name",
                ["str"],
                "Name of the new column that holds the names of the unpivoted columns.",
                "'name'",
            ),
            _keyword(
                "value",
                ["str"],
                "Name of the new column that holds their values.",
                "'value'",
            ),
        ],
    ),
    "update": PythonRelAPIDetails(
        additional_description="""

The relation must read a table, as one from [`table()`](#table) does. The relation runs again on every read, so reading it afterwards shows the updated rows.""",
        example="""
import duckdb
from duckdb import col, lit

duckdb_conn = duckdb.connect()

duckdb_conn.sql("CREATE TABLE items AS SELECT * FROM (VALUES (1, 'jeans', 20), (2, 'hammer', 42)) AS t(id, item, price)")

rel = duckdb_conn.table("items")

rel.update(set={"item": lit("claw hammer"), "price": col("price") + 5}, condition=col("id") == 2)

rel.order("id")
""",
        use_default_example=False,
        parameters=[
            _param(
                "set",
                ["dict"],
                "The new values, as a dict of column name to an Expression or a Python value. A string value raises `TypeError`: write `col('y')` for the column `y`, or `lit('y')` for the text.",
            ),
            _keyword(
                "condition",
                ["str", "Expression"],
                "Optional condition to filter which rows to update.",
                "None",
            ),
        ],
    ),
    "with_columns": PythonRelAPIDetails(
        example="""
from duckdb import col, lit

rel.with_columns(price=col("price") * 2, currency=lit("EUR"))
""",
        parameters=[
            _variadic_keywords(
                "columns",
                ["Expression", "object"],
                "The columns, as `name=value`, where a value is an Expression, a column name or a Python value; a column of the same name is replaced in place, any other is added at the end.",
            )
        ],
    ),
}

FUNCTION_METHODS_MAP = {
    "any_value": PythonRelAPIDetails(
        example='rel.any_value("item")',
        parameters=_aggregate_parameters(
            "The column or expression from which to retrieve any value."
        ),
    ),
    "arg_max": PythonRelAPIDetails(
        example='rel.arg_max("item", "price", groups="category", projected_columns="category").order("category")',
        parameters=[
            _param(
                "arg_column",
                ["str"],
                "The column whose value is returned, taken from the row where `value_column` is largest.",
            ),
            _param(
                "value_column",
                ["str"],
                "The column whose largest value picks the row.",
            ),
            _GROUPS_NOT_WINDOW,
            _WINDOW_NOT_GROUPS,
            _PROJECTED_COLUMNS,
        ],
    ),
    "arg_min": PythonRelAPIDetails(
        example='rel.arg_min("item", "price", groups="category", projected_columns="category").order("category")',
        parameters=[
            _param(
                "arg_column",
                ["str"],
                "The column whose value is returned, taken from the row where `value_column` is smallest.",
            ),
            _param(
                "value_column",
                ["str"],
                "The column whose smallest value picks the row.",
            ),
            _GROUPS_NOT_WINDOW,
            _WINDOW_NOT_GROUPS,
            _PROJECTED_COLUMNS,
        ],
    ),
    "avg": PythonRelAPIDetails(
        example='rel.avg("price")',
        aliases=["mean"],
        parameters=_aggregate_parameters(
            "The column or expression to calculate the average of."
        ),
    ),
    "bit_and": PythonRelAPIDetails(
        example='rel.bit_and("id", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to perform the bitwise AND aggregation on."
        ),
    ),
    "bit_or": PythonRelAPIDetails(
        example='rel.bit_or("id", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to perform the bitwise OR aggregation on."
        ),
    ),
    "bit_xor": PythonRelAPIDetails(
        example='rel.bit_xor("id", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to perform the bitwise XOR aggregation on."
        ),
    ),
    "bitstring_agg": PythonRelAPIDetails(
        example='rel.bitstring_agg("id", min=1, max=6, groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to aggregate as a bitstring.",
            _param(
                "min",
                ["int"],
                "The smallest value the bitstring can hold; give both `min` and `max`, or neither.",
                "None",
            ),
            _param(
                "max",
                ["int"],
                "The largest value the bitstring can hold; give both `min` and `max`, or neither.",
                "None",
            ),
        ),
    ),
    "bool_and": PythonRelAPIDetails(
        example='rel.bool_and("in_stock", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to perform the boolean AND aggregation on."
        ),
    ),
    "bool_or": PythonRelAPIDetails(
        example='rel.bool_or("in_stock", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to perform the boolean OR aggregation on."
        ),
    ),
    "count": PythonRelAPIDetails(
        example='rel.count("id")',
        parameters=_aggregate_parameters(
            "The column or expression to count the values of; `'*'` counts the rows."
        ),
    ),
    "cume_dist": PythonRelAPIDetails(
        example='rel.cume_dist(window_spec="OVER (PARTITION BY category ORDER BY price)", projected_columns="category, item, price").order("category, price")',
        parameters=_window_parameters(),
    ),
    "dense_rank": PythonRelAPIDetails(
        example='rel.dense_rank(window_spec="OVER (PARTITION BY category ORDER BY price)", projected_columns="category, item, price").order("category, price")',
        aliases=["rank_dense"],
        parameters=_window_parameters(),
    ),
    "favg": PythonRelAPIDetails(
        example='rel.favg("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the average of."
        ),
    ),
    "first": PythonRelAPIDetails(
        example='rel.first("item", groups="category", projected_columns="category").order("category")',
        parameters=_group_only_parameters(
            "The column or expression from which to retrieve the first value."
        ),
    ),
    "first_value": PythonRelAPIDetails(
        example='rel.first_value("item", window_spec="OVER (PARTITION BY category ORDER BY price)", projected_columns="category").distinct().order("category")',
        parameters=[
            _param(
                "expression",
                ["str"],
                "The column or expression from which to retrieve the first value within the window.",
            ),
            _OPTIONAL_WINDOW,
            _PROJECTED_COLUMNS,
        ],
    ),
    "fsum": PythonRelAPIDetails(
        example='rel.fsum("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the sum of."
        ),
    ),
    "geomean": PythonRelAPIDetails(
        example='rel.geomean("price", groups="category", projected_columns="category").order("category")',
        parameters=_group_only_parameters(
            "The column or expression to calculate the geometric mean of."
        ),
    ),
    "histogram": PythonRelAPIDetails(
        example='rel.histogram("in_stock", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the histogram of."
        ),
    ),
    "lag": PythonRelAPIDetails(
        example='rel.lag("item", window_spec="OVER (ORDER BY price)", projected_columns="item, price").order("price")',
        parameters=[
            _param(
                "expression",
                ["str"],
                "The column or expression to apply the lag function on.",
            ),
            _REQUIRED_WINDOW,
            _param(
                "offset",
                ["int"],
                "The number of rows to lag behind.",
                "1",
            ),
            _param(
                "default_value",
                ["str"],
                "The value, as SQL text, to return when the lag offset goes out of bounds.",
                "'NULL'",
            ),
            _param(
                "ignore_nulls",
                ["bool"],
                "Whether to ignore NULL values when computing the lag.",
                "False",
            ),
            _PROJECTED_COLUMNS,
        ],
    ),
    "last": PythonRelAPIDetails(
        example='rel.last("item", groups="category", projected_columns="category").order("category")',
        parameters=_group_only_parameters(
            "The column or expression from which to retrieve the last value."
        ),
    ),
    "last_value": PythonRelAPIDetails(
        example='rel.last_value("item", window_spec="OVER (PARTITION BY category ORDER BY price ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)", projected_columns="category").distinct().order("category")',
        parameters=[
            _param(
                "expression",
                ["str"],
                "The column or expression from which to retrieve the last value within the window.",
            ),
            _OPTIONAL_WINDOW,
            _PROJECTED_COLUMNS,
        ],
    ),
    "lead": PythonRelAPIDetails(
        example='rel.lead("item", window_spec="OVER (ORDER BY price)", projected_columns="item, price").order("price")',
        parameters=[
            _param(
                "expression",
                ["str"],
                "The column or expression to apply the lead function on.",
            ),
            _REQUIRED_WINDOW,
            _param(
                "offset",
                ["int"],
                "The number of rows to lead ahead.",
                "1",
            ),
            _param(
                "default_value",
                ["str"],
                "The value, as SQL text, to return when the lead offset goes out of bounds.",
                "'NULL'",
            ),
            _param(
                "ignore_nulls",
                ["bool"],
                "Whether to ignore NULL values when computing the lead.",
                "False",
            ),
            _PROJECTED_COLUMNS,
        ],
    ),
    "list": PythonRelAPIDetails(
        example='rel.list("item", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to aggregate values into a list."
        ),
    ),
    "max": PythonRelAPIDetails(
        example='rel.max("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the maximum value of."
        ),
    ),
    "mean": PythonRelAPIDetails(alias_of="avg"),
    "median": PythonRelAPIDetails(
        example='rel.median("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the median value of."
        ),
    ),
    "min": PythonRelAPIDetails(
        example='rel.min("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the min value of."
        ),
    ),
    "mode": PythonRelAPIDetails(
        example='''
import duckdb

duckdb_conn = duckdb.connect()

sales = duckdb_conn.sql("""
    SELECT *
    FROM (VALUES ('clothing', 20), ('clothing', 20), ('clothing', 8), ('tools', 42), ('tools', 7), ('tools', 7))
        AS sales(category, price)
""")

sales.mode("price", groups="category", projected_columns="category").order("category")
''',
        use_default_example=False,
        parameters=_aggregate_parameters(
            "The column or expression to calculate the mode (most frequent value) of."
        ),
    ),
    "n_tile": PythonRelAPIDetails(
        example='rel.n_tile(window_spec="OVER (PARTITION BY category ORDER BY price)", num_buckets=2, projected_columns="category, item, price").order("category, price")',
        parameters=[
            _REQUIRED_WINDOW,
            _param(
                "num_buckets",
                ["int"],
                "The number of buckets to divide the rows into.",
            ),
            _PROJECTED_COLUMNS,
        ],
    ),
    "nth_value": PythonRelAPIDetails(
        example='rel.nth_value("item", window_spec="OVER (PARTITION BY category ORDER BY price)", offset=2, projected_columns="category, item, price").order("category, price")',
        parameters=[
            _param(
                "expression",
                ["str"],
                "The column or expression from which to retrieve the nth value within the window.",
            ),
            _REQUIRED_WINDOW,
            _param(
                "offset",
                ["int"],
                "The position of the value to retrieve within the window (1-based index).",
            ),
            _param(
                "ignore_nulls",
                ["bool"],
                "Whether to ignore NULL values when computing the nth value.",
                "False",
            ),
            _PROJECTED_COLUMNS,
        ],
    ),
    "percent_rank": PythonRelAPIDetails(
        example='rel.percent_rank(window_spec="OVER (PARTITION BY category ORDER BY price)", projected_columns="category, item, price").order("category, price")',
        parameters=_window_parameters(),
    ),
    "product": PythonRelAPIDetails(
        example='rel.product("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the product of."
        ),
    ),
    "quantile": PythonRelAPIDetails(alias_of="quantile_disc"),
    "quantile_cont": PythonRelAPIDetails(
        example='rel.quantile_cont("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to compute the continuous quantile for.",
            _QUANTILE,
        ),
    ),
    "quantile_disc": PythonRelAPIDetails(
        example='rel.quantile_disc("price", groups="category", projected_columns="category").order("category")',
        aliases=["quantile"],
        parameters=_aggregate_parameters(
            "The column or expression to compute the discrete quantile for.",
            _QUANTILE,
        ),
    ),
    "rank": PythonRelAPIDetails(
        example='rel.rank(window_spec="OVER (PARTITION BY category ORDER BY price)", projected_columns="category, item, price").order("category, price")',
        parameters=_window_parameters(),
    ),
    "rank_dense": PythonRelAPIDetails(alias_of="dense_rank"),
    "row_number": PythonRelAPIDetails(
        example='rel.row_number(window_spec="OVER (PARTITION BY category ORDER BY price)", projected_columns="category, item, price").order("category, price")',
        parameters=_window_parameters(),
    ),
    "std": PythonRelAPIDetails(alias_of="stddev_samp"),
    "stddev": PythonRelAPIDetails(alias_of="stddev_samp"),
    "stddev_pop": PythonRelAPIDetails(
        example='rel.stddev_pop("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the standard deviation for."
        ),
    ),
    "stddev_samp": PythonRelAPIDetails(
        example='rel.stddev_samp("price", groups="category", projected_columns="category").order("category")',
        aliases=["std", "stddev"],
        parameters=_aggregate_parameters(
            "The column or expression to calculate the standard deviation for."
        ),
    ),
    "string_agg": PythonRelAPIDetails(
        example='rel.string_agg("item", sep=", ", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to concatenate values from.",
            _param(
                "sep",
                ["str"],
                "Separator string to use between concatenated values.",
                "','",
            ),
        ),
    ),
    "sum": PythonRelAPIDetails(
        example='rel.sum("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the sum for."
        ),
    ),
    "unique": PythonRelAPIDetails(
        example='rel.unique("category").order("category")',
        parameters=[
            _param(
                "unique_aggr",
                ["str"],
                "The column to get the distinct values for.",
            )
        ],
    ),
    "value_counts": PythonRelAPIDetails(
        example='rel.value_counts("in_stock", groups="in_stock").order("in_stock")',
        parameters=[
            _param(
                "expression",
                ["str"],
                "The column or expression to count values from.",
            ),
            _GROUPS,
        ],
    ),
    "var": PythonRelAPIDetails(alias_of="var_samp"),
    "var_pop": PythonRelAPIDetails(
        example='rel.var_pop("price", groups="category", projected_columns="category").order("category")',
        parameters=_aggregate_parameters(
            "The column or expression to calculate the population variance for."
        ),
    ),
    "var_samp": PythonRelAPIDetails(
        example='rel.var_samp("price", groups="category", projected_columns="category").order("category")',
        aliases=["var", "variance"],
        parameters=_aggregate_parameters(
            "The column or expression to calculate the sample variance for."
        ),
    ),
    "variance": PythonRelAPIDetails(alias_of="var_samp"),
}

OUTPUT_METHODS_MAP = {
    "arrow": PythonRelAPIDetails(
        alias_of="to_arrow_reader",
        additional_description="\n\n> We recommend using [`to_arrow_reader()`](#to_arrow_reader) instead.",
    ),
    "create": PythonRelAPIDetails(
        example="""
rel.filter("category = 'tools'").create("tools")

duckdb_conn.table("tools")
""",
        aliases=["to_table"],
        parameters=_CREATE_PARAMETERS,
    ),
    "create_view": PythonRelAPIDetails(
        additional_description=_CREATE_VIEW_DESCRIPTION,
        example="""
rel.filter("price > 30").create_view("expensive_items")

duckdb_conn.view("expensive_items")
""",
        aliases=["to_view"],
        parameters=_CREATE_VIEW_PARAMETERS,
    ),
    "df": PythonRelAPIDetails(
        example="rel.df()",
        aliases=["fetchdf", "to_df"],
        parameters=[_DATE_AS_OBJECT],
    ),
    "fetch_arrow_reader": PythonRelAPIDetails(
        alias_of="to_arrow_reader",
        additional_description=_deprecated("fetch_arrow_reader", "to_arrow_reader"),
    ),
    "fetch_arrow_table": PythonRelAPIDetails(
        alias_of="to_arrow_table",
        additional_description=_deprecated("fetch_arrow_table", "to_arrow_table"),
    ),
    "fetch_record_batch": PythonRelAPIDetails(
        alias_of="to_arrow_reader",
        additional_description=_deprecated("fetch_record_batch", "to_arrow_reader"),
    ),
    "fetchall": PythonRelAPIDetails(
        example="rel.limit(1).fetchall()",
    ),
    "fetchdf": PythonRelAPIDetails(alias_of="df"),
    "fetchnumpy": PythonRelAPIDetails(
        example="rel.fetchnumpy()",
    ),
    "iter_rows": PythonRelAPIDetails(
        additional_description="""

To read a relation row by row, as a loop over `fetchone()` or `fetchmany()` did before DuckDB 2.0, iterate over `iter_rows()`.""",
        example="""
for row in rel.iter_rows(batch_size=4):
    print(row)
""",
        parameters=[
            _param(
                "batch_size",
                ["int"],
                "The number of rows fetched at a time; it must be above zero.",
                "1024",
            )
        ],
    ),
    "materialize": PythonRelAPIDetails(
        additional_description="""

The returned relation reads the held rows, so it does not see later changes to the data, and [`create_view()`](#create_view) refuses it. `materialize()` takes the place of `execute()`, which relations no longer have since DuckDB 2.0.""",
        example="""
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("CREATE TABLE items AS SELECT range AS id FROM range(3)")

rel = duckdb_conn.table("items")
held = rel.materialize()

duckdb_conn.sql("INSERT INTO items VALUES (3)")

print(len(rel), len(held))
""",
        use_default_example=False,
    ),
    "pl": PythonRelAPIDetails(
        additional_description="\n\nNeeds the `polars` package.",
        example="rel.pl(batch_size=1)",
        parameters=[
            _BATCH_SIZE,
            _keyword(
                "lazy",
                ["bool"],
                "Return a polars `LazyFrame` instead of a `DataFrame`.",
                "False",
            ),
        ],
    ),
    "tf": PythonRelAPIDetails(
        additional_description="\n\nNeeds the `tensorflow` package.",
    ),
    "to_arrow_reader": PythonRelAPIDetails(
        additional_description="""

Until the reader is read to the end or closed, the connection refuses other queries with `ResourceInUseException`. A `with` block closes the reader when it ends, also when the loop stops early. The example sets a small `batch_size` only to show several batches. To read the rows a batch at a time, as `fetch_df_chunk()` did before DuckDB 2.0, read the batches of this reader.""",
        example="""
with rel.select("item, price").to_arrow_reader(batch_size=2) as reader:
    for batch in reader:
        print(batch.to_pydict())
""",
        aliases=["arrow", "fetch_arrow_reader", "fetch_record_batch"],
        parameters=[_BATCH_SIZE],
    ),
    "to_arrow_table": PythonRelAPIDetails(
        example="rel.to_arrow_table()",
        aliases=["fetch_arrow_table"],
        parameters=[_BATCH_SIZE],
    ),
    "to_csv": PythonRelAPIDetails(alias_of="write_csv"),
    "to_df": PythonRelAPIDetails(alias_of="df"),
    "to_dicts": PythonRelAPIDetails(
        example="rel.limit(2).to_dicts()",
    ),
    "to_parquet": PythonRelAPIDetails(alias_of="write_parquet"),
    "to_table": PythonRelAPIDetails(alias_of="create"),
    "to_view": PythonRelAPIDetails(alias_of="create_view"),
    "torch": PythonRelAPIDetails(
        additional_description="\n\nNeeds the `torch` package.",
    ),
    "write_csv": PythonRelAPIDetails(
        additional_description=_WRITE_CSV_DESCRIPTION,
        example='rel.write_csv("items.csv")',
        aliases=["to_csv"],
        parameters=_WRITE_CSV_PARAMETERS,
    ),
    "write_parquet": PythonRelAPIDetails(
        additional_description=_WRITE_PARQUET_DESCRIPTION,
        example='rel.write_parquet("items.parquet")',
        aliases=["to_parquet"],
        parameters=_WRITE_PARQUET_PARAMETERS,
    ),
}

DOCS_DETAILS_MAP = {
    **CREATION_METHODS_MAP,
    **DEFINITION_METHODS_MAP,
    **TRANSFORMATION_METHODS_MAP,
    **FUNCTION_METHODS_MAP,
    **OUTPUT_METHODS_MAP,
}
