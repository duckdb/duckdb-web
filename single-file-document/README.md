# Single-file DuckDB documentation

## Prerequisites

* `pandoc` with XeLaTeX
* Python packages in `requirements.txt`

## Generate document

```bash
single-file-document/generate_single_file_documentation.sh
```

## Generate PDF with Docker

Navigate to the repository root and run Docker:

```bash
cd $(git rev-parse --show-toplevel)
docker run \
     --volume "$(pwd):/data" \
     --workdir /data/single-file-document \
     pandoc/extra \
     --defaults pandoc-configuration.yaml
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
