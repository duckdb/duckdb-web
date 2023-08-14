# Contributing

## Code of Conduct

This project and everyone participating in it is governed by a [Code of Conduct](code_of_conduct.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [quack@duckdb.org](mailto:quack@duckdb.org).

## Eligibility

Before submitting a contribution, please check whether your contribution is eligible.

1. Before creating a new page, please [search the existing documentation](https://duckdb.org/docs/search) for similar pages.
2. In general, guides for third-party tools using DuckDB should not be included in the DuckDB documentation. Rather, these tools and their documentation should be collected in the [`awesome-duckdb` community repository](https://github.com/davidgasquez/awesome-duckdb).

## Adding a new page

Thank you for contributing to the DuckDB documentation!

Each new page requires at least 2 edits:
* The creation of a new Markdown page with the documentation. Please follow the format of another `.md` file in the `docs` folder.
* Add a link to the new page within `_data/menu_docs_dev.json`. This populates the dropdown menus.

The addition of a new guide requires one additional edit:
* Add a link to the new page within the Guides landing page: `docs/guides/index.md`

**Please test your changes using the steps listed in the [Building](building.md) guide.**

**When creating a PR, please check the box to "Allow edits from maintainers".**

## Style guide

Please adhere the following style guide when submitting a pull request.

### Syntax

* Use [GitHub's Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) for formatting.
* Do not hard-wrap lines in blocks of text.
* Enclose code in blocks that are tagged with the appropriate language (e.g., \`\`\`sql CODE HERE \`\`\`). To display blocks of text without a language (e.g., console outputs), use \`\`\`text ... \`\`\`.
* Quoted blocks (lines starting with `>`) are rendered as [a "Note" box](https://duckdb.org/docs/archive/0.8.1/guides/python/filesystems).
* Always format SQL code, variable names, function names, etc. as code. For example, when talking about the `CREATE TABLE` statement, the keywords should be formatted as code.

### Headers

* The title of the page should be encoded in the front matter's `title` property. The body of the page should not start with a repetition of this title.
* In the body of the page, restrict the use of headers to the following levels: h2 (`##`), h3 (`###`), and h4 (`####`).

### SQL style

* Use SQL uppercase keywords, e.g., `SELECT ... FROM ...`.
* Employing DuckDB's syntax extensions, e.g., the [`FROM-first` syntax](https://duckdb.org/docs/archive/0.8.1/sql/query_syntax/from) and [`GROUP BY ALL`](https://duckdb.org/docs/sql/query_syntax/groupby#group-by-all), is allowed but use them sparingly when introducing new features.
* Use **4 spaces** for indentation.

### Spelling

* Use [American English (en-US) spelling](https://en.wikipedia.org/wiki/Oxford_spelling#Language_tag_comparison),

## Examples

* Examples that illustrate the use of features are very welcome. Where applicable, consider starting the page with a few simple examples that demonstrate the most common uses of the feature described.
* All examples should be self-contained and reproducible if possible, meaning that any example tables must be created as a part of the documentation.

## Cross-references

* Where applicable, add cross-references to relevant other pages in the documentation.
* Use descriptive links:
    * :white_check_mark: ```see [the `COPY` statement](../../sql/statements/copy)```
    * :x: `see [here](../../sql/statements/copy)`
* Use relative URLs without the `.html` extension:
    * :white_check_mark: `../../sql/statements/copy`
    * :x: `../../sql/statements/copy.html`
    * :x: `/docs/sql/statements/copy`
    * :x: `https://duckdb.org/docs/sql/statements/copy`
* Reference a specific section when possible:
    * :white_check_mark: `../../sql/statements/copy#copy-from`
* Do **not** link related GitHub issues/discussions. This allows the documentation to be self-contained.

## Achive and generated pages

* The archive pages (e.g., <https://duckdb.org/docs/archive/0.5.1/>) contain documentation for old versions. Do not edit these pages.
* Many of the documentation's pages are auto-generated. Before editing, please check the [`scripts/generate_all_docs.sh`](scripts/generate_all_docs.sh) script. Do not edit the generated content, instead, edit the source files (often found in the [`duckdb` repository](https://github.com/duckdb/duckdb)).

## Notice

We reserve full and final discretion over whether or not we will merge a pull request. Adhering to these guidelines is not a guarantee that your pull request will be merged.
