# DuckDB reformat table script

As one would expect, this script uses DuckDB to reformat the function tables in DuckDB documentation.
Prior to the reformatting, tables have 3-5 columns, which often makes for a cramped look.
After reformatting the tables, they have 2 column and functions are spelled out in their own sections.

## Usage

Run the script with:

```bash
./create-function-sections.sh
```

Then, paste the resulting entries into their original files under `docs/sql/functions`.

Note: Nome entries need special handling, these can be found in the `_exceptions.md` file. Add these manually after the previous steps.
