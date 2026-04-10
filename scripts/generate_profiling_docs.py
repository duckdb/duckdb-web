import argparse
import os
import sys
from pathlib import Path

from jinja2.optimizer import Optimizer
from tabulate import tabulate

REPO_ROOT = Path(__file__).resolve().parents[1]
METRIC_TOOLS_PATH = Path("scripts") / "metrics"
METRICS_DOC_PATH = REPO_ROOT / "docs" / "current" / "dev" / "metrics.md"
METRICS_DOC_TEMPLATE = REPO_ROOT / "scripts" / "metrics.md.template"

METRICS_MARKER = "<!-- METRICS_TABLE -->"
END_METRICS_MARKER = "<!-- END_METRICS_TABLE -->"
GROUPS_MARKER = "<!-- GROUPS -->"
END_GROUPS_MARKER = "<!-- END_GROUPS -->"
OPTIMIZER_MARKER = "<!-- OPTIMIZER_METRICS -->"
END_OPTIMIZER_MARKER = "<!-- END_OPTIMIZER_METRICS -->"
CUMULATIVE_MARKER = "<!-- CUMULATIVE_METRICS -->"
END_CUMALATIVE_MARKER = "<!-- END_CUMULATIVE_METRICS -->"
EXAMPLES_MARKER = "<!-- EXAMPLES -->"
END_EXAMPLES_MARKER = "<!-- END_EXAMPLES -->"

CPU_TIME_NOTE = f"""`CPU_TIME` measures the cumulative operator timings.
It does not include time spent in other stages, like parsing, query planning, etc.
Thus, for some queries, the `LATENCY` in the `QUERY_ROOT` can be greater than the `CPU_TIME`.
"""


def _write_heading(f, heading):
    f.write(f"\n{heading}\n\n")


def _write_individual_metric(f, metric):
    is_operator_node = metric.group == "operator"
    is_query_node = metric.query_root

    if metric.query_root is False and metric.group != "operator":
        is_query_node = True
        is_operator_node = True

    _write_heading(f, f"#### `{metric.name}`")
    f.write("<div class=\"nostroke_table\"></div>\n\n")

    table = f"| **Description** | {metric.description} |\n"
    table += f"| **Type** | {metric.type} |\n"
    table += f"| **Unit** | {metric.unit} |\n" if metric.unit != "--" else ""
    table += f"| **Default** | ✅ |\n" if metric.is_default else ''
    table += f"| **Query Node** | ✅ |\n" if is_query_node else ''
    table += f"| **Operator Node** | ✅ |\n" if is_operator_node else ''
    table += (
        f"| **[Cumulative](#cumulative-metrics)** | ✅ |\n"
        if metric.collection_method and "cumulative" in metric.collection_method.lower()
        else ''
    )
    table += f"| **Child** | {metric.child} |\n" if metric.child else ''
    f.write(table + "\n")

    if metric.name == "CPU_TIME":
        f.write(f"**Note:**\n\n{CPU_TIME_NOTE}\n\n")


def _write_section_from_template(f, metrics, section):
    f.write(section)
    for metric in metrics:
        _write_individual_metric(f, metric)


def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation for DuckDB profiling metrics based on the definitions in duckdb/src/common/enums/metric_type.json"
    )

    parser.add_argument(
        "--duckdb-path",
        required=True,
        type=str,
        help="Path to the DuckDB repository (used to read metric definitions and optimizer types)",
    )

    args = parser.parse_args()
    base_path = REPO_ROOT / args.duckdb_path
    metrics_package_path = base_path / "scripts"
    sys.path.append(str(metrics_package_path))

    try:
        from metrics.inputs import (
            load_metrics_json,
            retrieve_optimizers,
            retrieve_template,
            START_OF_FILE,
        )
        from metrics.model import build_all_metrics
        from metrics.paths import (
            METRICS_JSON,
            OPTIMIZER_HPP,
        )
        from metrics.writer import IndentedFileWriter
    except ImportError as e:
        print(
            f"Error: Could not find profiling metric tools in {metrics_package_path / 'metrics'}."
        )
        print(f"DuckDB path provided: {args.duckdb_path}")
        print(f"Resolved base path: {base_path}")
        print(
            "Please ensure the DuckDB path is correct and points to a DuckDB repository with the required scripts in scripts/metrics."
        )
        print(f"Original error: {e}")
        sys.exit(1)

    metrics_json = load_metrics_json(METRICS_JSON)
    optimizers = retrieve_optimizers(OPTIMIZER_HPP)
    metric_index = build_all_metrics(metrics_json, optimizers)

    with IndentedFileWriter(METRICS_DOC_PATH) as f:
        f.write(
            retrieve_template(
                METRICS_DOC_TEMPLATE, START_OF_FILE, METRICS_MARKER
            ).lstrip('\n')
        )

        # Generate metrics table
        metrics_table = []

        for metric in metric_index.defs:
            if metric.group == "optimizer":
                continue
            metrics_table.append(
                [
                    f"[`{metric.name}`](#{metric.name.lower().replace(' ', '_')})",
                    f"[{metric.group}](#{metric.group}-metrics)",
                    metric.description,
                ]
            )

        metric_table_headers = ["Name", "Group", "Description"]
        f.write(
            tabulate(metrics_table, headers=metric_table_headers, tablefmt="github")
        )
        f.write("\n\n")

        f.write(
            retrieve_template(METRICS_DOC_TEMPLATE, GROUPS_MARKER, END_GROUPS_MARKER)
        )
        for group in metric_index.group_names:
            if group not in ("all", "default"):
                f.write(f"- [`{group.upper()}`](#{group}-metrics)\n")

        f.write("\n")
        optimizers = []
        cumulative_metrics = []

        for group in metric_index.group_names:
            if group in ("all", "default", "optimizer"):
                continue

            group_metrics = [m for m in metric_index.defs if m.group == group]

            _write_heading(f, f"### {group.capitalize()} Metrics")
            f.write(metric_index.group_description(group) + "\n\n")

            for metric in group_metrics:
                if (
                    metric.collection_method
                    and "cumulative" in metric.collection_method.lower()
                ):
                    cumulative_metrics.append(metric)

                if "optimizer" in metric.name.lower():
                    optimizers.append(metric)

                _write_individual_metric(f, metric)

        # write optimizer metrics
        f.write(
            retrieve_template(
                METRICS_DOC_TEMPLATE, OPTIMIZER_MARKER, END_OPTIMIZER_MARKER
            )
        )
        for metric in optimizers:
            f.write(f"- [`{metric.name}`](#{metric.name.lower().replace(' ', '_')})\n")

        # write cumulative metrics
        f.write(
            retrieve_template(
                METRICS_DOC_TEMPLATE, CUMULATIVE_MARKER, END_CUMALATIVE_MARKER
            )
        )
        for metric in cumulative_metrics:
            f.write(f"- [`{metric.name}`](#{metric.name.lower().replace(' ', '_')})\n")

        # write examples
        f.write(
            retrieve_template(
                METRICS_DOC_TEMPLATE, EXAMPLES_MARKER, END_EXAMPLES_MARKER
            )
        )


if __name__ == "__main__":
    main()
