# Single-file DuckDB documentation

## Prerequisites

* `pandoc` with XeLaTeX
* Python packages in `requirements.txt`

## Generate document

```batch
single-file-document/generate_single_file_documentation.sh
```

The script generates two documents, each as a Markdown and a PDF file:

* `duckdb-docs.md` and `duckdb-docs.pdf` contain the 2.0 documentation (based on `docs/2.0` and `_data/menu_docs_20.json`).
* `duckdb-blog.md` and `duckdb-blog.pdf` contain the blog posts (based on `_posts`).

To use another version of the documentation, run `python3 concatenate_to_single_file.py --docs-version ⟨version⟩` in the `single-file-document` directory.

## Generate PDF with Docker

If you do not have Pandoc installed, you can build with Docker using:

```batch
single-file-document/generate_single_file_documentation.sh --docker
```

## Generate LaTeX code

To generate the intermediate LaTeX code produced by Pandoc, run:

```batch
single-file-document/generate_latex.sh
```

## Notes

* Word wrapping:
  * Using code blocks without the language specified results in the LaTeX `verbatim` context, which does not support word wrapping.
  * If the language is specified, the LaTeX environment `Shaded`/`Highlighting` are used, which support word wrapping.
