#!/usr/bin/env python3
"""Generate the casting operations matrix on the Typecasting documentation page.

The matrix used to be a static image (images/typecasting-matrix.png), which was
hard to read, not accessible to screen readers, could not be searched or copied,
and had drifted out of sync with the engine. This script derives the matrix
directly from a DuckDB binary so it can be regenerated in CI and always matches
the documented version.

For every ordered pair of source and target types it determines whether:

* the cast is added *implicitly* by the system, via `can_cast_implicitly()`; or
* the cast is only available *explicitly* (with `CAST` / `::`), detected by
  attempting the cast on a representative value and checking whether the engine
  reports `Unimplemented type for cast`; or
* the cast is not supported at all.

The generated table is written into the page between the
`<!-- BEGIN GENERATED TYPECASTING MATRIX -->` and
`<!-- END GENERATED TYPECASTING MATRIX -->` markers.

Usage:
    python3 scripts/generate_typecasting_matrix.py [/path/to/duckdb] [/path/to/typecasting.md]
"""

import os
import subprocess
import sys

# (full type name, short column label, a representative non-NULL literal of that type)
TYPES = [
    ("BOOLEAN", "BOOL", "true::BOOLEAN"),
    ("TINYINT", "I8", "1::TINYINT"),
    ("SMALLINT", "I16", "1::SMALLINT"),
    ("INTEGER", "I32", "1::INTEGER"),
    ("BIGINT", "I64", "1::BIGINT"),
    ("HUGEINT", "I128", "1::HUGEINT"),
    ("UTINYINT", "U8", "1::UTINYINT"),
    ("USMALLINT", "U16", "1::USMALLINT"),
    ("UINTEGER", "U32", "1::UINTEGER"),
    ("UBIGINT", "U64", "1::UBIGINT"),
    ("UHUGEINT", "U128", "1::UHUGEINT"),
    ("FLOAT", "F32", "1.5::FLOAT"),
    ("DOUBLE", "F64", "1.5::DOUBLE"),
    ("DECIMAL(18, 3)", "DEC", "1.5::DECIMAL(18, 3)"),
    ("VARCHAR", "STR", "'1'::VARCHAR"),
    ("BLOB", "BLOB", "'\\xAA'::BLOB"),
    ("BIT", "BIT", "'101'::BIT"),
    ("UUID", "UUID", "'00000000-0000-0000-0000-000000000000'::UUID"),
    ("DATE", "DATE", "DATE '2020-01-01'"),
    ("TIME", "TIME", "TIME '12:00:00'"),
    ("TIMESTAMP", "TS", "TIMESTAMP '2020-01-01 12:00:00'"),
    ("TIMESTAMP WITH TIME ZONE", "TSTZ", "TIMESTAMPTZ '2020-01-01 12:00:00'"),
    ("TIME WITH TIME ZONE", "TTZ", "TIME WITH TIME ZONE '12:00:00'"),
    ("INTERVAL", "IVL", "INTERVAL 1 DAY"),
]

IMPLICIT = "I"
EXPLICIT = "E"
NONE = ""

BEGIN_MARKER = "<!-- BEGIN GENERATED TYPECASTING MATRIX -->"
END_MARKER = "<!-- END GENERATED TYPECASTING MATRIX -->"


def run(db_path, query):
    """Run a query, returning (returncode, stdout, stderr)."""
    res = subprocess.run(
        [db_path, "-batch", "-init", os.devnull, "-c", query],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (
        res.returncode,
        res.stdout.decode("utf8", "replace"),
        res.stderr.decode("utf8", "replace"),
    )


def implicit_matrix(db_path):
    """Return a set of (source, target) pairs for which an implicit cast exists."""
    selects = []
    for si, (s_type, _, _) in enumerate(TYPES):
        for ti, (t_type, _, _) in enumerate(TYPES):
            selects.append(
                f"SELECT {si} AS s, {ti} AS t, "
                f"can_cast_implicitly(NULL::{s_type}, NULL::{t_type}) AS ok"
            )
    query = "\nUNION ALL\n".join(selects) + " ORDER BY s, t;"
    res = subprocess.run(
        [db_path, "-batch", "-init", os.devnull, "-list", "-noheader", "-c", query],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    code, out, err = (
        res.returncode,
        res.stdout.decode("utf8", "replace"),
        res.stderr.decode("utf8", "replace"),
    )
    if code != 0:
        print("Failed to compute implicit casts:\n" + err, file=sys.stderr)
        sys.exit(1)
    implicit = set()
    for line in out.strip().splitlines():
        s, t, ok = line.split("|")
        if ok == "true":
            implicit.add((int(s), int(t)))
    return implicit


def explicit_supported(db_path, value, target_type):
    """Whether an explicit cast of `value` to `target_type` is supported at all."""
    code, _, err = run(db_path, f"SELECT CAST({value} AS {target_type});")
    if code == 0:
        return True
    # A missing cast reports "Unimplemented type for cast"; any other error
    # (out of range, parse failure, ...) means the cast exists but this
    # particular value could not be converted.
    return "Unimplemented type for cast" not in err


def build_matrix(db_path):
    implicit = implicit_matrix(db_path)
    rows = []
    for si, (s_type, _, s_value) in enumerate(TYPES):
        cells = []
        for ti, (t_type, _, _) in enumerate(TYPES):
            if si == ti:
                cells.append(IMPLICIT)
            elif (si, ti) in implicit:
                cells.append(IMPLICIT)
            elif explicit_supported(db_path, s_value, t_type):
                cells.append(EXPLICIT)
            else:
                cells.append(NONE)
        rows.append(cells)
    return rows


def render(rows):
    labels = [short for _, short, _ in TYPES]
    header = "| From \\ To | " + " | ".join(labels) + " |"
    sep = "|" + "---|" * (len(labels) + 1)
    lines = [header, sep]
    for (full, _, _), cells in zip(TYPES, rows):
        lines.append("| `" + full + "` | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def legend():
    items = ", ".join(f"`{short}` ({full})" for full, short, _ in TYPES)
    return (
        "In the matrix below, rows are the source type and columns are the target type. "
        f"`{IMPLICIT}` marks a cast the system also performs *implicitly*; "
        f"`{EXPLICIT}` marks a cast that is only available *explicitly* (with `CAST` or `::`); "
        "an empty cell marks an unsupported cast. "
        "Even where a cast is supported, it may still fail at runtime for a particular value "
        "(for example, out of range or unparseable input).\n\n"
        "Column abbreviations: " + items + "."
    )


def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else "duckdb"
    doc_file = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "docs/preview/sql/data_types/typecasting.md"
    )

    rows = build_matrix(db_path)
    block = legend() + "\n\n<div class=\"monospace_table\"></div>\n\n" + render(rows)

    with open(doc_file, "r") as f:
        text = f.read()

    if BEGIN_MARKER not in text or END_MARKER not in text:
        print(f"Could not find generation markers in {doc_file}", file=sys.stderr)
        sys.exit(1)

    before = text.split(BEGIN_MARKER)[0]
    after = text.split(END_MARKER)[1]
    text = before + BEGIN_MARKER + "\n\n" + block + "\n\n" + END_MARKER + after

    with open(doc_file, "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()
