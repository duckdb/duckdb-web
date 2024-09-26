

# Note, this may not handle all special characters
shell_link_stub = "https://shell.duckdb.org/#queries=v0,"
# sql = """
#     install tpch;
#     load tpch;
#     call dbgen(sf=0.1);
#     pragma tpch(7);
# """

sql = """
CREATE OR REPLACE TABLE business_metrics (
    product_line VARCHAR, product VARCHAR, year INTEGER, quarter VARCHAR, revenue integer, cost integer
);
INSERT INTO business_metrics VALUES
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q1', 100, 100),
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q2', 200, 100),
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q3', 300, 100),
    ('Waterfowl watercraft', 'Duck boats', 2022, 'Q4', 400, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q1', 500, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q2', 600, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q3', 700, 100),
    ('Waterfowl watercraft', 'Duck boats', 2023, 'Q4', 800, 100),

    ('Duck Duds', 'Duck suits', 2022, 'Q1', 10, 10),
    ('Duck Duds', 'Duck suits', 2022, 'Q2', 20, 10),
    ('Duck Duds', 'Duck suits', 2022, 'Q3', 30, 10),
    ('Duck Duds', 'Duck suits', 2022, 'Q4', 40, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q1', 50, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q2', 60, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q3', 70, 10),
    ('Duck Duds', 'Duck suits', 2023, 'Q4', 80, 10),

    ('Duck Duds', 'Duck neckties', 2022, 'Q1', 1, 1),
    ('Duck Duds', 'Duck neckties', 2022, 'Q2', 2, 1),
    ('Duck Duds', 'Duck neckties', 2022, 'Q3', 3, 1),
    ('Duck Duds', 'Duck neckties', 2022, 'Q4', 4, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q1', 5, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q2', 6, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q3', 7, 1),
    ('Duck Duds', 'Duck neckties', 2023, 'Q4', 8, 1),
;

FROM business_metrics;

INSTALL pivot_table from community;
LOAD 'https://community-extensions.duckdb.org/v1.1.1/wasm_eh/pivot_table.duckdb_extension.wasm';

DROP TYPE IF EXISTS columns_parameter_enum;

CREATE TYPE columns_parameter_enum AS ENUM (FROM build_my_enum(['business_metrics'], ['year', 'quarter'], []));

FROM pivot_table(['business_metrics'],['sum(revenue)', 'sum(cost)'], ['product_line', 'product'], ['year', 'quarter'], [], subtotals := 1, grand_totals := 1, values_axis := 'rows');
"""

statements = sql.strip().split(sep=";")

encoded_statements = []

for statement in statements:
    trimmed = statement.strip()
    no_hyphens = trimmed.replace('-', '%2D')
    no_spaces = no_hyphens.replace('\n',' ').replace(' ', '-')
    encoded = (
        no_spaces.replace(',','%2C')
        .replace('=','%3D')
        .replace(':','%3A')
        .replace(r'/','%2F')
        .replace('%2D',' ')
    )
    encoded_statements.append(encoded)

combined = shell_link_stub + '~,'.join(encoded_statements)

print(combined)
