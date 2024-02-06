# Contributing

- [Contributing](#contributing)
  - [Code of Conduct](#code-of-conduct)
  - [Contributing to the DuckDB Documentation](#contributing-to-the-duckdb-documentation)
  - [Eligibility](#eligibility)
  - [Adding a New Page](#adding-a-new-page)
  - [Style Guide](#style-guide)
    - [Formatting](#formatting)
    - [Headers](#headers)
    - [SQL Style](#sql-style)
    - [Python Style](#python-style)
    - [Links](#links)
    - [Spelling](#spelling)
  - [Example Code Snippets](#example-code-snippets)
  - [Cross-References](#cross-references)
  - [Achive and Generated Pages](#achive-and-generated-pages)
  - [Notice](#notice)

## Code of Conduct

This project and everyone participating in it is governed by a [Code of Conduct](code_of_conduct.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [quack@duckdb.org](mailto:quack@duckdb.org).

## Contributing to the DuckDB Documentation

Contributions to the [DuckDB Documentation](https://duckdb.org/) are welcome. To submit a contribution, please open a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) in the [`duckdb/duckdb-web`](https://github.com/duckdb/duckdb-web) repository.

## Eligibility

Before submitting a contribution, please check whether your contribution is eligible.

1. Before creating a new page, please [search the existing documentation](https://duckdb.org/docs/search) for similar pages.
2. In general, guides for third-party tools using DuckDB should not be included in the DuckDB documentation. Rather, these tools and their documentation should be collected in the [Awesome DuckDB community repository](https://github.com/davidgasquez/awesome-duckdb).

## Adding a New Page

Thank you for contributing to the DuckDB documentation!

Each new page requires at least 2 edits:
* Create new Markdown file (using the `snake_case` naming convention). Please follow the format of another `.md` file in the `docs` folder.
* Add a link to the new page within `_data/menu_docs_dev.json`. This populates the dropdown menus.

The addition of a new guide requires one additional edit:
* Add a link to the new page within the Guides landing page: `docs/guides/index.md`

Before creating a pull request, please perform the following steps:
* Preview your changes in the browser using the [site build guide](BUILDING.md).
* Run the linters with `scripts/lint.sh` to show potential issues and run `scripts/lint.sh -f` to perform the fixes for markdownlint.

When creating a PR, please check the box to "Allow edits from maintainers".

## Style Guide

Please adhere the following style guide when submitting a pull request.

Some of this style guide is automated with GitHub Actions, but feel free to run [`scripts/lint.sh`](scripts/lint.sh) to run them locally.

### Formatting

* Use [GitHub's Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) for formatting.
* Do not hard-wrap lines in blocks of text.
* Format code blocks with the appropriate language (e.g., \`\`\`sql CODE HERE \`\`\`).
* To display blocks of text without a language (e.g., output of a script), use \`\`\`text OUTPUT HERE \`\`\`.
* Quoted blocks (lines starting with `>`) are rendered as [a "Note" box](https://duckdb.org/docs/archive/0.8.1/guides/python/filesystems).
* Always format SQL code, variable names, function names, etc. as code. For example, when talking about the `CREATE TABLE` statement, the keywords should be formatted as code.
* When presenting SQL statements, do not include the DuckDB prompt (`D `).
* SQL statements should end with a semicolon (`;`) to allow readers to quickly paste them into a SQL console.
* Narrow tables should be prepended with an empty div that has the `narrow` table class: `<div class="narrow_table"></div>`.

### Headers

* The title of the page should be encoded in the front matter's `title` property. The body of the page should not start with a repetition of this title.
* In the body of the page, restrict the use of headers to the following levels: h2 (`##`), h3 (`###`), and h4 (`####`).
* Use headline capitalization as defined in the [Chicago Manual of Style](https://headlinecapitalization.com/).

### SQL Style

* Use **4 spaces** for indentation.
* Use uppercase SQL keywords, e.g., `SELECT 42 AS x, 'hello world' AS y FROM ...;`.
* Use lowercase function names, e.g., `SELECT cos(pi()), date_part('year', DATE '1992-09-20');`.
* Use snake case (lowercase with underscore separators) for table and column names, e.g. `SELECT departure_time FROM train_services;`
* Add spaces around commas and operators, e.g. `SELECT FROM tbl WHERE x > 42;`.
* Add a semicolon to the end of each SQL statement, e.g., `SELECT 42 AS x;`.
* Commas should be placed at the end of each line.
* _Do not_ add clauses or expressions purely for aligning lines. For exampe, avoid adding `WHERE 1 = 1` and `WHERE true`.
* _Do not_ include the DuckDB prompt. For example, avoid the following: `D SELECT 42;`.
* Employing DuckDB's syntax extensions, e.g., the [`FROM-first` syntax](https://duckdb.org/docs/sql/query_syntax/from) and [`GROUP BY ALL`](https://duckdb.org/docs/sql/query_syntax/groupby#group-by-all), is allowed but use them sparingly when introducing new features.
* The returned tables should be formatted using the DuckDB CLI's duckbox mode (`.mode duckbox`) and marked with the `text` language tag, e.g.:

    ````
    ```text
    ┌───────┐
    │   x   │
    │ int32 │
    ├───────┤
    │    42 │
    └───────┘
    ```
    ````    

### Python Style

* Use **4 spaces** for indentation.
* Use double quotes (`"`) by default for strings.

### Links

* Please avoid using the term "here" for links (e.g., "for more details, click [here](https://example.org/)" should be avoided). For the rationale, see a [detailed explanation on why your links should never say "click here"](https://uxmovement.com/content/why-your-links-should-never-say-click-here/).

### Spelling

* Use [American English (en-US) spelling](https://en.wikipedia.org/wiki/Oxford_spelling#Language_tag_comparison).

## Example Code Snippets

* Examples that illustrate the use of features are very welcome. Where applicable, consider starting the page with a few simple examples that demonstrate the most common uses of the feature described.
* If possible, examples should be self-contained and reproducible. For example, the tables used in the example must be created as a part of the example code snippet.

## Cross-References

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

## Achive and Generated Pages

* The archive pages (e.g., <https://duckdb.org/docs/archive/0.8.1/>) contain documentation for old versions of DuckDB. In general, we do not accept contributions to these pages – please target the latest version of the page when submitting your contributions.
* Many of the documentation's pages are auto-generated. Before editing, please check the [`scripts/generate_all_docs.sh`](scripts/generate_all_docs.sh) script. Do not edit the generated content, instead, edit the source files (often found in the [`duckdb` repository](https://github.com/duckdb/duckdb)).

## Notice

We reserve full and final discretion over whether or not we will merge a pull request. Adhering to these guidelines is not a guarantee that your pull request will be merged.
