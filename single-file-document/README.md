# Single-file DuckDB documentation

## Prerequisites

* `pandoc` with XeLaTeX
* Python packages in `requirements.txt`

## Generate document

```bash
single-file-document/generate_single_file_documentation.sh
```

## Generate PDF with Docker

If you do not have Pandoc installed, you can build with Docker using:

```bash
single-file-document/generate_single_file_documentation.sh --docker
```

## Generate LaTeX code

To generate the intermediate LaTeX code produced by Pandoc, run:

```bash
pandoc --defaults pandoc-configuration.yaml --to=latex --output duckdb-docs.tex
```

## Notes

* Word wrapping:
  * Using code blocks without the language specified results in the LaTeX `verbatim` context, which does not support word wrapping.
  * If the language is specified, the LaTeX environment `Shaded`/`Highlighting` are used, which support word wrapping.
