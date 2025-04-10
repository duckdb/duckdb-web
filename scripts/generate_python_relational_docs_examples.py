DEFAULT_EXAMPLE = '''```python
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
)

{code_example}
```
'''

PLACEHOLDER_EXAMPLE = "```python\n{code_example}\n```"
PLACEHOLDER_RESULT = "```{result_type}\n{result}\n```"

CREATION_MEMBER_CODE_EXAMPLE_MAP = {
    'from_arrow': {
        'example': """
import duckdb
import pyarrow as pa

ids = pa.array([1], type=pa.int8())
texts = pa.array(['a'], type=pa.string())
example_table = pa.table([ids, texts], names=["id", "text"])

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_arrow(example_table)

rel.show()
""",
        'result': """
┌──────┬─────────┐
│  id  │  text   │
│ int8 │ varchar │
├──────┼─────────┤
│    1 │ a       │
└──────┴─────────┘
""",
        'default': False,
    },
    'from_csv_auto': {
        'example': """
import csv
import duckdb

duckdb_conn = duckdb.connect()

with open('code_example.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '1', 'text': 'a'})

rel = duckdb_conn.from_csv_auto("code_example.csv")

rel.show()
""",
        'result': """
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        'default': False,
    },
    'from_df': {
        'example': """
import duckdb
import pandas as pd

df = pd.DataFrame(data = {'id': [1], "text":["a"]})

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_df(df)

rel.show()
""",
        'result': """
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        'default': False,
    },
    'from_parquet': {
        'example': """
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ids = pa.array([1], type=pa.int8())
texts = pa.array(['a'], type=pa.string())
example_table = pa.table([ids, texts], names=["id", "text"])

pq.write_table(example_table, "code_example.parquet")

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_parquet("code_example.parquet")

rel.show()
""",
        'result': """
┌──────┬─────────┐
│  id  │  text   │
│ int8 │ varchar │
├──────┼─────────┤
│    1 │ a       │
└──────┴─────────┘
""",
        'default': False,
    },
    'from_query': {
        'example': """
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.from_query("from range(1,2) tbl(id)")

rel.show()
""",
        'result': """
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        'default': False,
    },
    'query': {
        'example': """
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.query("from range(1,2) tbl(id)")

rel.show()
""",
        'result': """
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        'default': False,
    },
    'read_csv': {
        'example': """
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
        'result': """
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        'default': False,
    },
    'read_json': {
        'example': """
import duckdb
import json

with open("code_example.json", mode="w") as f:
    json.dump([{'id': 1, "text":"a"}], f)
    
duckdb_conn = duckdb.connect()

rel = duckdb_conn.read_json("code_example.json")

rel.show()
""",
        'result': """
┌───────┬─────────┐
│  id   │  text   │
│ int64 │ varchar │
├───────┼─────────┤
│     1 │ a       │
└───────┴─────────┘
""",
        'default': False,
    },
    'read_parquet': {
        'example': """
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
        'result': """
┌──────┬─────────┐
│  id  │  text   │
│ int8 │ varchar │
├──────┼─────────┤
│    1 │ a       │
└──────┴─────────┘
""",
        'default': False,
    },
    'sql': {
        'example': """
import duckdb

duckdb_conn = duckdb.connect()

rel = duckdb_conn.sql("from range(1,2) tbl(id)")

rel.show()
""",
        'result': """
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        'default': False,
    },
    'table': {
        'example': """
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("create table code_example as select * from range(1,2) tbl(id)")

rel = duckdb_conn.table("code_example")

rel.show()
""",
        'result': """
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        'default': False,
    },
    'table_function': {
        'example': '''
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
    create macro get_record_for(x) as table
    select x*range from range(1,2)
""")

rel = duckdb_conn.table_function(name="get_record_for", parameters=[1])

rel.show()
''',
        'result': """
┌───────────────┐
│ (1 * "range") │
│     int64     │
├───────────────┤
│             1 │
└───────────────┘
""",
        'default': False,
    },
    # 'values': {'example': '', 'result': '', 'default': False},
    'view': {
        'example': """
import duckdb

duckdb_conn = duckdb.connect()

duckdb_conn.sql("create table code_example as select * from range(1,2) tbl(id)")

rel = duckdb_conn.view("code_example")

rel.show()
""",
        'result': """
┌───────┐
│  id   │
│ int64 │
├───────┤
│     1 │
└───────┘
""",
        'default': False,
    },
}

DEFINITION_MEMBER_CODE_EXAMPLE_MAP = {
    'columns': {
        'example': 'rel.columns',
        'result': " ['id', 'description', 'value', 'created_timestamp']",
    },
    'describe': {
        'example': 'rel.describe()',
        'result': """
┌─────────┬──────────────────────────────────────┬─────────────────┬────────────────────┬────────────────────────────┐
│  aggr   │                  id                  │   description   │       value        │     created_timestamp      │
│ varchar │               varchar                │     varchar     │       double       │          varchar           │
├─────────┼──────────────────────────────────────┼─────────────────┼────────────────────┼────────────────────────────┤
│ count   │ 9                                    │ 9               │                9.0 │ 9                          │
│ mean    │ NULL                                 │ NULL            │                5.0 │ NULL                       │
│ stddev  │ NULL                                 │ NULL            │ 2.7386127875258306 │ NULL                       │
│ min     │ 08fdcbf8-4e53-4290-9e81-423af263b518 │ value is even   │                1.0 │ 2025-04-09 15:41:20.642+02 │
│ max     │ fb10390e-fad5-4694-91cb-e82728cb6f9f │ value is uneven │                9.0 │ 2025-04-09 15:49:20.642+02 │
│ median  │ NULL                                 │ NULL            │                5.0 │ NULL                       │
└─────────┴──────────────────────────────────────┴─────────────────┴────────────────────┴────────────────────────────┘ 
""",
    },
    'description': {
        'example': 'rel.description',
        'result': """
[('id', 'UUID', None, None, None, None, None),
 ('description', 'STRING', None, None, None, None, None),
 ('value', 'NUMBER', None, None, None, None, None),
 ('created_timestamp', 'DATETIME', None, None, None, None, None)]  
""",
    },
    'dtypes': {
        'example': 'rel.dtypes',
        'result': ' [UUID, VARCHAR, BIGINT, TIMESTAMP WITH TIME ZONE]',
    },
    'explain': {
        'example': 'rel.explain()',
        'result': """
┌───────────────────────────┐\n│         PROJECTION        │\n│    ────────────────────   │\n│             id            │\n│        description        │\n│           value           │\n│     created_timestamp     │\n│                           │\n│          ~9 Rows          │\n└─────────────┬─────────────┘\n┌─────────────┴─────────────┐\n│           RANGE           │\n│    ────────────────────   │\n│      Function: RANGE      │\n│                           │\n│          ~9 Rows          │\n└───────────────────────────┘\n\n
""",
    },
    'query-1': {
        'example': 'rel.query(virtual_table_name="rel_view", sql_query="from rel")\n\nduckdb_conn.sql("show rel_view")',
        'result': """
┌───────────────────┬──────────────────────────┬─────────┬─────────┬─────────┬─────────┐
│    column_name    │       column_type        │  null   │   key   │ default │  extra  │
│      varchar      │         varchar          │ varchar │ varchar │ varchar │ varchar │
├───────────────────┼──────────────────────────┼─────────┼─────────┼─────────┼─────────┤
│ id                │ UUID                     │ YES     │ NULL    │ NULL    │ NULL    │
│ description       │ VARCHAR                  │ YES     │ NULL    │ NULL    │ NULL    │
│ value             │ BIGINT                   │ YES     │ NULL    │ NULL    │ NULL    │
│ created_timestamp │ TIMESTAMP WITH TIME ZONE │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────────┴──────────────────────────┴─────────┴─────────┴─────────┴─────────┘
""",
    },
    'set_alias': {
        'example': "rel.set_alias('abc').select('abc.id')",
        'result': 'In the SQL query, the alias will be `abc`',
    },
    'alias': {'example': 'rel.alias', 'result': 'unnamed_relation_43c808c247431be5'},
    'shape': {'example': 'rel.shape', 'result': '(9, 4)'},
    'show': {
        'example': 'rel.show()',
        'result': """
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 642ea3d7-793d-4867-a759-91c1226c25a0 │ value is uneven │     1 │ 2025-04-09 15:41:20.642+02 │
│ 6817dd31-297c-40a8-8e40-8521f00b2d08 │ value is even   │     2 │ 2025-04-09 15:42:20.642+02 │
│ 45143f9a-e16e-4e59-91b2-3a0800eed6d6 │ value is uneven │     3 │ 2025-04-09 15:43:20.642+02 │
│ fb10390e-fad5-4694-91cb-e82728cb6f9f │ value is even   │     4 │ 2025-04-09 15:44:20.642+02 │
│ 111ced5c-9155-418e-b087-c331b814db90 │ value is uneven │     5 │ 2025-04-09 15:45:20.642+02 │
│ 66a870a6-aef0-4085-87d5-5d1b35d21c66 │ value is even   │     6 │ 2025-04-09 15:46:20.642+02 │
│ a7e8e796-bca0-44cd-a269-1d71090fb5cc │ value is uneven │     7 │ 2025-04-09 15:47:20.642+02 │
│ 74908d48-7f2d-4bdd-9c92-1e7920b115b5 │ value is even   │     8 │ 2025-04-09 15:48:20.642+02 │
│ 08fdcbf8-4e53-4290-9e81-423af263b518 │ value is uneven │     9 │ 2025-04-09 15:49:20.642+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
    },
    'sql_query': {
        'example': 'rel.sql_query()',
        'result': """SELECT 
    gen_random_uuid() AS id, 
    concat('value is ', CASE  WHEN ((mod("range", 2) = 0)) THEN ('even') ELSE 'uneven' END) AS description, 
    "range" AS "value", 
    (now() + CAST(concat("range", ' ', 'minutes') AS INTERVAL)) AS created_timestamp 
FROM "range"(1, 10)
""",
        'result_type': "sql",
    },
    'type': {'example': 'rel.type', 'result': 'QUERY_RELATION'},
    'types': {
        'example': 'rel.types',
        'result': '[UUID, VARCHAR, BIGINT, TIMESTAMP WITH TIME ZONE]',
    },
}

TRANSFORMATION_MEMBER_CODE_EXAMPLE_MAP = {
    "aggregate": {
        "example": "rel = rel.aggregate('max(value)')",
        "result": """
┌──────────────┐
│ max("value") │
│    int64     │
├──────────────┤
│            9 │
└──────────────┘
        """,
    },
    'apply': {
        'example': """
rel.apply(
    function_name="count", 
    function_aggr="id", 
    group_expr="description",
    projected_columns="description"
)
""",
        'result': """
┌─────────────────┬───────────┐
│   description   │ count(id) │
│     varchar     │   int64   │
├─────────────────┼───────────┤
│ value is uneven │         5 │
│ value is even   │         4 │
└─────────────────┴───────────┘
""",
        'default': True,
    },
    'cross': {
        'example': 'rel.cross(other_rel=rel.set_alias("other_rel"))',
        'result': """
┌─────────────────────────────┬─────────────────┬───────┬───────────────────────────┬──────────────────────────────────────┬─────────────────┬───────┬───────────────────────────┐
│             id              │   description   │ value │     created_timestamp     │                  id                  │   description   │ value │     created_timestamp     │
│            uuid             │     varchar     │ int64 │ timestamp with time zone  │                 uuid                 │     varchar     │ int64 │ timestamp with time zone  │
├─────────────────────────────┼─────────────────┼───────┼───────────────────────────┼──────────────────────────────────────┼─────────────────┼───────┼───────────────────────────┤
│ cb2b453f-1a06-4f5e-abe1-b…  │ value is uneven │     1 │ 2025-04-10 09:53:29.78+02 │ cb2b453f-1a06-4f5e-abe1-bfd413581bcf │ value is uneven │     1 │ 2025-04-10 09:53:29.78+02 │
...
""",
        'default': True,
    },
    'except_': {
        'example': 'rel.except_(other_rel=rel.set_alias("other_rel"))',
        'result': """
The relation query is executed once with `rel` and once with `other_rel`,
therefore generating different ids and timestamps:

┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ f69ed6dd-a7fe-4de2-b6af-1c2418096d69 │ value is uneven │     3 │ 2025-04-10 11:43:05.711+02 │
│ 08ad11dc-a9c2-4aaa-9272-760b27ad1f5d │ value is uneven │     7 │ 2025-04-10 11:47:05.711+02 │
...
""",
        'default': True,
    },
    'filter': {
        'example': 'rel.filter("value = 2")',
        'result': """
┌──────────────────────────────────────┬───────────────┬───────┬───────────────────────────┐
│                  id                  │  description  │ value │     created_timestamp     │
│                 uuid                 │    varchar    │ int64 │ timestamp with time zone  │
├──────────────────────────────────────┼───────────────┼───────┼───────────────────────────┤
│ b0684ab7-fcbf-41c5-8e4a-a51bdde86926 │ value is even │     2 │ 2025-04-10 09:54:29.78+02 │
└──────────────────────────────────────┴───────────────┴───────┴───────────────────────────┘
""",
        'default': True,
    },
    'insert': {
        'example': '''
import duckdb

from datetime import datetime
from uuid import uuid4

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
        select 
            gen_random_uuid() as id, 
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value, 
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
).to_table("code_example")

rel = duckdb_conn.table("code_example")

rel.insert(
    (
        uuid4(), 
        'value is even',
        10, 
        datetime.now()
    )
)

rel.filter("value = 10")
''',
        'result': """
┌──────────────────────────────────────┬───────────────┬───────┬───────────────────────────────┐
│                  id                  │  description  │ value │       created_timestamp       │
│                 uuid                 │    varchar    │ int64 │   timestamp with time zone    │
├──────────────────────────────────────┼───────────────┼───────┼───────────────────────────────┤
│ c6dfab87-fae6-4213-8f76-1b96a8d179f6 │ value is even │    10 │ 2025-04-10 10:02:24.652218+02 │
└──────────────────────────────────────┴───────────────┴───────┴───────────────────────────────┘
""",
        'default': False,
    },
    'insert_into': {
        'example': '''
import duckdb

from datetime import datetime
from uuid import uuid4

duckdb_conn = duckdb.connect()

duckdb_conn.sql("""
        select
            gen_random_uuid() as id,
            concat('value is ', case when mod(range,2)=0 then 'even' else 'uneven' end) as description,
            range as value,
            now() + concat(range,' ', 'minutes')::interval as created_timestamp
        from range(1, 10)
    """
).to_table("code_example")

rel = duckdb_conn.values(
    [
        uuid4(),
        'value is even',
        10,
        datetime.now()
    ]
)

rel.insert_into("code_example")

duckdb_conn.table("code_example").filter("value = 10")
    ''',
        'result': """
┌──────────────────────────────────────┬───────────────┬───────┬───────────────────────────────┐
│                  id                  │  description  │ value │       created_timestamp       │
│                 uuid                 │    varchar    │ int64 │   timestamp with time zone    │
├──────────────────────────────────────┼───────────────┼───────┼───────────────────────────────┤
│ 271c5ddd-c1d5-4638-b5a0-d8c7dc9e8220 │ value is even │    10 │ 2025-04-10 14:29:18.616379+02 │
└──────────────────────────────────────┴───────────────┴───────┴───────────────────────────────┘
""",
        'default': False,
    },
    'intersect': {
        'example': 'rel.intersect(other_rel=rel.set_alias("other_rel"))',
        'result': """
The relation query is executed once with `rel` and once with `other_rel`,
therefore generating different ids and timestamps:

┌──────┬─────────────┬───────┬──────────────────────────┐
│  id  │ description │ value │    created_timestamp     │
│ uuid │   varchar   │ int64 │ timestamp with time zone │
├──────┴─────────────┴───────┴──────────────────────────┤
│                        0 rows                         │
└───────────────────────────────────────────────────────┘
""",
        'default': True,
    },
    'join': {
        'example': """
rel = rel.set_alias("rel").join(
    other_rel=rel.set_alias("other_rel"), 
    condition="rel.id = other_rel.id",
    how="left"
)

rel.count("*")
""",
        'result': """
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            9 │
└──────────────┘
""",
        'default': True,
        'additional_description': """

Depending on how the `condition` parameter is provided, the JOIN clause generated is:
- `USING`

    ```python
    import duckdb
    
    duckdb_conn = duckdb.connect()
    
    rel1 = duckdb_conn.sql("select range as id, concat('dummy 1', range) as text from range(1,10)")
    rel2 = duckdb_conn.sql("select range as id, concat('dummy 2', range) as text from range(5,7)")
    
    rel1.join(rel2, condition="id", how="inner").sql_query()
    ```
    with following SQL:
    ```sql
    SELECT * 
    FROM (
            SELECT "range" AS id, 
                concat('dummy 1', "range") AS "text" 
            FROM "range"(1, 10)
        ) AS unnamed_relation_41bc15e744037078 
    INNER JOIN (
            SELECT "range" AS id, 
            concat('dummy 2', "range") AS "text" 
            FROM "range"(5, 7)
        ) AS unnamed_relation_307e245965aa2c2b 
    USING (id)
    ```
- `ON`

    ```python
    import duckdb
    
    duckdb_conn = duckdb.connect()
    
    rel1 = duckdb_conn.sql("select range as id, concat('dummy 1', range) as text from range(1,10)")
    rel2 = duckdb_conn.sql("select range as id, concat('dummy 2', range) as text from range(5,7)")
    
    rel1.join(rel2, condition=f"{rel1.alias}.id = {rel2.alias}.id", how="inner").sql_query()
    ```
    with the following SQL:
    ```sql
    SELECT * 
    FROM (
            SELECT "range" AS id, 
                concat('dummy 1', "range") AS "text" 
            FROM "range"(1, 10)
        ) AS unnamed_relation_41bc15e744037078 
    INNER JOIN (
            SELECT "range" AS id, 
            concat('dummy 2', "range") AS "text" 
            FROM "range"(5, 7)
        ) AS unnamed_relation_307e245965aa2c2b 
    ON ((unnamed_relation_41bc15e744037078.id = unnamed_relation_307e245965aa2c2b.id))
    ```
""",
    },
    'limit': {
        'example': 'rel.limit(1)',
        'result': """
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 4135597b-29e7-4cb9-a443-41f3d54f25df │ value is uneven │     1 │ 2025-04-10 10:52:03.678+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        'default': True,
    },
    # 'map': {'example': '', 'result': '', 'default': False},
    'order': {
        'example': 'rel.order("value desc").limit(1, offset=4)',
        'result': """
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 55899131-e3d3-463c-a215-f65cb8aef3bf │ value is uneven │     5 │ 2025-04-10 10:56:03.678+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        'default': True,
    },
    'project': {
        'example': 'rel.project("description").limit(1)',
        'result': """
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is uneven │
└─────────────────┘
""",
        'default': True,
    },
    'select': {
        'example': 'rel.select("description").limit(1)',
        'result': """
┌─────────────────┐
│   description   │
│     varchar     │
├─────────────────┤
│ value is uneven │
└─────────────────┘
""",
        'default': True,
    },
    # 'sort': {'example': '', 'result': '', 'default': False},
    'union': {
        'example': 'rel = rel.union(union_rel=rel)\n\nrel.count("*")',
        'result': """
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│           18 │
└──────────────┘
""",
        'default': True,
    },
    # 'update': {'example': '', 'result': '', 'default': False},
}

FUNCTION_MEMBER_CODE_EXAMPLE_MAP = {
    'any_value': {
        'example': "rel.any_value('id')",
        'result': """
┌──────────────────────────────────────┐
│            any_value(id)             │
│                 uuid                 │
├──────────────────────────────────────┤
│ 642ea3d7-793d-4867-a759-91c1226c25a0 │
└──────────────────────────────────────┘
""",
    },
    'arg_max': {
        'example': 'rel.arg_max(arg_column="value", value_column="value", groups="description", projected_columns="description")',
        'result': """
┌─────────────────┬───────────────────────────┐
│   description   │ arg_max("value", "value") │
│     varchar     │           int64           │
├─────────────────┼───────────────────────────┤
│ value is uneven │                         9 │
│ value is even   │                         8 │
└─────────────────┴───────────────────────────┘
""",
    },
    'arg_min': {
        'example': 'rel.arg_min(arg_column="value", value_column="value", groups="description", projected_columns="description")',
        'result': """
┌─────────────────┬───────────────────────────┐
│   description   │ arg_min("value", "value") │
│     varchar     │           int64           │
├─────────────────┼───────────────────────────┤
│ value is even   │                         2 │
│ value is uneven │                         1 │
└─────────────────┴───────────────────────────┘
""",
    },
    'avg': {
        'example': "rel.avg('value')",
        'result': """
┌──────────────┐
│ avg("value") │
│    double    │
├──────────────┤
│          5.0 │
└──────────────┘
 """,
    },
    'bit_and': {
        'example': """
rel = rel.select("description, value::bit as value_bit")

rel.bit_and(column="value_bit", groups="description", projected_columns="description")
""",
        'result': """
┌─────────────────┬──────────────────────────────────────────────────────────────────┐
│   description   │                        bit_and(value_bit)                        │
│     varchar     │                               bit                                │
├─────────────────┼──────────────────────────────────────────────────────────────────┤
│ value is uneven │ 0000000000000000000000000000000000000000000000000000000000000001 │
│ value is even   │ 0000000000000000000000000000000000000000000000000000000000000000 │
└─────────────────┴──────────────────────────────────────────────────────────────────┘    
""",
    },
    'bit_or': {
        'example': """
rel = rel.select("description, value::bit as value_bit")

rel.bit_or(column="value_bit", groups="description", projected_columns="description")
""",
        'result': """
┌─────────────────┬──────────────────────────────────────────────────────────────────┐
│   description   │                        bit_or(value_bit)                         │
│     varchar     │                               bit                                │
├─────────────────┼──────────────────────────────────────────────────────────────────┤
│ value is uneven │ 0000000000000000000000000000000000000000000000000000000000001111 │
│ value is even   │ 0000000000000000000000000000000000000000000000000000000000001110 │
└─────────────────┴──────────────────────────────────────────────────────────────────┘    
""",
    },
    'bit_xor': {
        'example': """
rel = rel.select("description, value::bit as value_bit")

rel.bit_xor(column="value_bit", groups="description", projected_columns="description")
""",
        'result': """
┌─────────────────┬──────────────────────────────────────────────────────────────────┐
│   description   │                        bit_xor(value_bit)                        │
│     varchar     │                               bit                                │
├─────────────────┼──────────────────────────────────────────────────────────────────┤
│ value is even   │ 0000000000000000000000000000000000000000000000000000000000001000 │
│ value is uneven │ 0000000000000000000000000000000000000000000000000000000000001001 │
└─────────────────┴──────────────────────────────────────────────────────────────────┘
""",
    },
    'bitstring_agg': {
        'example': 'rel.bitstring_agg(column="value", groups="description", projected_columns="description", min=1, max=9)',
        'result': """
┌─────────────────┬────────────────────────┐
│   description   │ bitstring_agg("value") │
│     varchar     │          bit           │
├─────────────────┼────────────────────────┤
│ value is uneven │ 101010101              │
│ value is even   │ 010101010              │
└─────────────────┴────────────────────────┘
""",
    },
    'bool_and': {
        'example': """
rel = rel.select("description, mod(value,2)::boolean as uneven")

rel.bool_and(column="uneven", groups="description", projected_columns="description")
""",
        'result': """
┌─────────────────┬──────────────────┐
│   description   │ bool_and(uneven) │
│     varchar     │     boolean      │
├─────────────────┼──────────────────┤
│ value is even   │ false            │
│ value is uneven │ true             │
└─────────────────┴──────────────────┘
""",
    },
    'bool_or': {
        'example': """
rel = rel.select("description, mod(value,2)::boolean as uneven")

rel.bool_or(column="uneven", groups="description", projected_columns="description")
""",
        'result': """
┌─────────────────┬─────────────────┐
│   description   │ bool_or(uneven) │
│     varchar     │     boolean     │
├─────────────────┼─────────────────┤
│ value is even   │ false           │
│ value is uneven │ true            │
└─────────────────┴─────────────────┘                
""",
    },
    # 'count': {'example': 'rel.count()', 'result': ''},
    # 'cume_dist': {'example': 'rel.cume_dist()', 'result': ''},
    # 'dense_rank': {'example': 'rel.dense_rank()', 'result': ''},
    # 'distinct': {'example': 'rel.distinct()', 'result': ''},
    # 'favg': {'example': 'rel.favg()', 'result': ''},
    # 'first': {'example': 'rel.first()', 'result': ''},
    # 'first_value': {'example': 'rel.first_value()', 'result': ''},
    # 'fsum': {'example': 'rel.fsum()', 'result': ''},
    # 'geomean': {'example': 'rel.geomean()', 'result': ''},
    # 'histogram': {'example': 'rel.histogram()', 'result': ''},
    # 'lag': {'example': 'rel.lag()', 'result': ''},
    # 'last': {'example': 'rel.last()', 'result': ''},
    # 'last_value': {'example': 'rel.last_value()', 'result': ''},
    # 'lead': {'example': 'rel.lead()', 'result': ''},
    # 'list': {'example': 'rel.list()', 'result': ''},
    # 'max': {'example': 'rel.max()', 'result': ''},
    # 'mean': {'example': 'rel.mean()', 'result': ''},
    # 'median': {'example': 'rel.median()', 'result': ''},
    # 'min': {'example': 'rel.min()', 'result': ''},
    # 'mode': {'example': 'rel.mode()', 'result': ''},
    # 'n_tile': {'example': 'rel.n_tile()', 'result': ''},
    # 'nth_value': {'example': 'rel.nth_value()', 'result': ''},
    # 'percent_rank': {'example': 'rel.percent_rank()', 'result': ''},
    # 'product': {'example': 'rel.product()', 'result': ''},
    # 'quantile': {'example': 'rel.quantile()', 'result': ''},
    # 'quantile_cont': {'example': 'rel.quantile_cont()', 'result': ''},
    # 'quantile_disc': {'example': 'rel.quantile_disc()', 'result': ''},
    # 'rank': {'example': 'rel.rank()', 'result': ''},
    # 'rank_dense': {'example': 'rel.rank_dense()', 'result': ''},
    # 'row_number': {'example': 'rel.row_number()', 'result': ''},
    # 'select_dtypes': {'example': 'rel.select_dtypes()', 'result': ''},
    # 'select_types': {'example': 'rel.select_types()', 'result': ''},
    # 'std': {'example': 'rel.std()', 'result': ''},
    # 'stddev': {'example': 'rel.stddev()', 'result': ''},
    # 'stddev_pop': {'example': 'rel.stddev_pop()', 'result': ''},
    # 'stddev_samp': {'example': 'rel.stddev_samp()', 'result': ''},
    # 'string_agg': {'example': 'rel.string_agg()', 'result': ''},
    # 'sum': {'example': 'rel.sum()', 'result': ''},
    # 'unique': {'example': 'rel.unique()', 'result': ''},
    # 'value_counts': {'example': 'rel.value_counts()', 'result': ''},
    # 'var': {'example': 'rel.var()', 'result': ''},
    # 'var_pop': {'example': 'rel.var_pop()', 'result': ''},
    # 'var_samp': {'example': 'rel.var_samp()', 'result': ''},
    # 'variance': {'example': 'rel.variance()', 'result': ''},
}

OUTPUT_MEMBER_CODE_EXAMPLE_MAP = {
    'arrow': {
        'example': 'pa_table = rel.arrow()\n\npa_table',
        'result': """
pyarrow.Table
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: [["3ac9e0ba-8390-4a02-ad72-33b1caea6354","8b844392-1404-4bbc-b731-120f42c8ca27","ca5584ca-8e97-4fca-a295-ae3c16c32f5b","926d071e-5f64-488f-ae02-d19e315f9f5c","aabeedf0-5783-4eff-9963-b3967a6ea5d8","1f20db9a-bee8-4b65-b7e8-e7c36b5b8fee","795c678e-3524-4b52-96ec-7b48c24eeab1","9ffbd403-169f-4fe4-bc41-09751066f1f1","8fdb0a60-29f0-4f5b-afcc-c736a03cd083"]]
description: [["value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven"]]
value: [[1,2,3,4,5,6,7,8,9]]
created_timestamp: [[2025-04-10 09:07:12.614000Z,2025-04-10 09:08:12.614000Z,2025-04-10 09:09:12.614000Z,2025-04-10 09:10:12.614000Z,2025-04-10 09:11:12.614000Z,2025-04-10 09:12:12.614000Z,2025-04-10 09:13:12.614000Z,2025-04-10 09:14:12.614000Z,2025-04-10 09:15:12.614000Z]]
""",
        'default': True,
    },
    # 'close': {'example': '', 'result': '', 'default': False},
    'create': {
        'example': 'rel.create("table_code_example")\n\nduckdb_conn.table("table_code_example").limit(1)',
        'result': """
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 3ac9e0ba-8390-4a02-ad72-33b1caea6354 │ value is uneven │     1 │ 2025-04-10 11:07:12.614+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        'default': True,
    },
    'create_view': {
        'example': 'rel.create_view("view_code_example", replace=True)\n\nduckdb_conn.table("view_code_example").limit(1)',
        'result': """
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 3ac9e0ba-8390-4a02-ad72-33b1caea6354 │ value is uneven │     1 │ 2025-04-10 11:07:12.614+02 │
└──────────────────────────────────────┴─────────────────┴───────┴────────────────────────────┘
""",
        'default': True,
    },
    'df': {
        'example': 'rel.df()',
        'result': """
                                     id      description  value                created_timestamp
0  3ac9e0ba-8390-4a02-ad72-33b1caea6354  value is uneven      1 2025-04-10 11:07:12.614000+02:00
1  8b844392-1404-4bbc-b731-120f42c8ca27    value is even      2 2025-04-10 11:08:12.614000+02:00
2  ca5584ca-8e97-4fca-a295-ae3c16c32f5b  value is uneven      3 2025-04-10 11:09:12.614000+02:00
...
""",
        'default': True,
    },
    'execute': {
        'example': 'rel.execute()',
        'result': """
┌──────────────────────────────────────┬─────────────────┬───────┬────────────────────────────┐
│                  id                  │   description   │ value │     created_timestamp      │
│                 uuid                 │     varchar     │ int64 │  timestamp with time zone  │
├──────────────────────────────────────┼─────────────────┼───────┼────────────────────────────┤
│ 3ac9e0ba-8390-4a02-ad72-33b1caea6354 │ value is uneven │     1 │ 2025-04-10 11:07:12.614+02 │
│ 8b844392-1404-4bbc-b731-120f42c8ca27 │ value is even   │     2 │ 2025-04-10 11:08:12.614+02 │
│ ca5584ca-8e97-4fca-a295-ae3c16c32f5b │ value is uneven │     3 │ 2025-04-10 11:09:12.614+02 │
""",
        'default': True,
    },
    'fetch_arrow_reader': {
        'example': 'pa_reader = rel.fetch_arrow_reader(batch_size=1)\n\npa_reader.read_next_batch()',
        'result': """
pyarrow.RecordBatch
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: ["e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd"]
description: ["value is even"]
value: [2]
created_timestamp: [2025-04-10 09:25:51.259000Z]
""",
        'default': True,
    },
    'fetch_arrow_table': {
        'example': 'rel.fetch_arrow_table()',
        'result': """
pyarrow.Table
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: [["1587b4b0-3023-49fe-82cf-06303ca136ac","e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd","3f8ad67a-290f-4a22-b41b-0173b8e45afa","9a4e37ef-d8bd-46dd-ab01-51cf4973549f","12baa624-ebc9-45ae-b73e-6f4029e31d2d","56d41292-53cc-48be-a1b8-e1f5d6ca5581","1accca18-c950-47c1-9108-aef8afbd5249","56d8db75-72c4-4d40-90d2-a3c840579c37","e19f6201-8646-401c-b019-e37c42c39632"]]
description: [["value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven"]]
value: [[1,2,3,4,5,6,7,8,9]]
created_timestamp: [[2025-04-10 09:24:51.259000Z,2025-04-10 09:25:51.259000Z,2025-04-10 09:26:51.259000Z,2025-04-10 09:27:51.259000Z,2025-04-10 09:28:51.259000Z,2025-04-10 09:29:51.259000Z,2025-04-10 09:30:51.259000Z,2025-04-10 09:31:51.259000Z,2025-04-10 09:32:51.259000Z]]
""",
        'default': True,
    },
    'fetch_df_chunk': {
        'example': 'rel.fetch_df_chunk()',
        'result': """
                                     id      description  value                created_timestamp
0  1587b4b0-3023-49fe-82cf-06303ca136ac  value is uneven      1 2025-04-10 11:24:51.259000+02:00
1  e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd    value is even      2 2025-04-10 11:25:51.259000+02:00
2  3f8ad67a-290f-4a22-b41b-0173b8e45afa  value is uneven      3 2025-04-10 11:26:51.259000+02:00
...
""",
        'default': True,
    },
    'fetchall': {
        'example': 'rel.limit(1).fetchall()',
        'result': """
[(UUID('1587b4b0-3023-49fe-82cf-06303ca136ac'),
  'value is uneven',
  1,
  datetime.datetime(2025, 4, 10, 11, 24, 51, 259000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
""",
        'default': True,
    },
    'fetchdf': {
        'example': 'rel.fetchdf()',
        'result': """
                                     id      description  value                created_timestamp
0  1587b4b0-3023-49fe-82cf-06303ca136ac  value is uneven      1 2025-04-10 11:24:51.259000+02:00
1  e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd    value is even      2 2025-04-10 11:25:51.259000+02:00
2  3f8ad67a-290f-4a22-b41b-0173b8e45afa  value is uneven      3 2025-04-10 11:26:51.259000+02:00
...
""",
        'default': True,
    },
    'fetchmany': {
        'example': 'rel.fetchmany(size=1)',
        'result': """
[(UUID('1587b4b0-3023-49fe-82cf-06303ca136ac'),
  'value is uneven',
  1,
  datetime.datetime(2025, 4, 10, 11, 24, 51, 259000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))]
""",
        'default': True,
    },
    'fetchnumpy': {
        'example': 'rel.fetchnumpy()',
        'result': """
{'id': array([UUID('1587b4b0-3023-49fe-82cf-06303ca136ac'),
        UUID('e4ab8cb4-4609-40cb-ad7e-4304ed5ed4bd'),
        UUID('3f8ad67a-290f-4a22-b41b-0173b8e45afa'),
        UUID('9a4e37ef-d8bd-46dd-ab01-51cf4973549f'),
        UUID('12baa624-ebc9-45ae-b73e-6f4029e31d2d'),
        UUID('56d41292-53cc-48be-a1b8-e1f5d6ca5581'),
        UUID('1accca18-c950-47c1-9108-aef8afbd5249'),
        UUID('56d8db75-72c4-4d40-90d2-a3c840579c37'),
        UUID('e19f6201-8646-401c-b019-e37c42c39632')], dtype=object),
 'description': array(['value is uneven', 'value is even', 'value is uneven',
        'value is even', 'value is uneven', 'value is even',
        'value is uneven', 'value is even', 'value is uneven'],
       dtype=object),
 'value': array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
 'created_timestamp': array(['2025-04-10T09:24:51.259000', '2025-04-10T09:25:51.259000',
        '2025-04-10T09:26:51.259000', '2025-04-10T09:27:51.259000',
        '2025-04-10T09:28:51.259000', '2025-04-10T09:29:51.259000',
        '2025-04-10T09:30:51.259000', '2025-04-10T09:31:51.259000',
        '2025-04-10T09:32:51.259000'], dtype='datetime64[us]')}
""",
        'default': True,
    },
    'fetchone': {
        'example': 'rel.fetchone()',
        'result': """
(UUID('1587b4b0-3023-49fe-82cf-06303ca136ac'),
 'value is uneven',
 1,
 datetime.datetime(2025, 4, 10, 11, 24, 51, 259000, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>))
""",
        'default': True,
    },
    'pl': {
        'example': 'rel.pl(batch_size=1)',
        'result': """
shape: (9, 4)
┌─────────────────────────────────┬─────────────────┬───────┬────────────────────────────────┐
│ id                              ┆ description     ┆ value ┆ created_timestamp              │
│ ---                             ┆ ---             ┆ ---   ┆ ---                            │
│ str                             ┆ str             ┆ i64   ┆ datetime[μs, Europe/Amsterdam] │
╞═════════════════════════════════╪═════════════════╪═══════╪════════════════════════════════╡
│ b2f92c3c-9372-49f3-897f-2c86fc… ┆ value is uneven ┆ 1     ┆ 2025-04-10 11:49:51.886 CEST   │
""",
        'default': True,
    },
    'record_batch': {
        'example': 'pa_batch = rel.record_batch(batch_size=1)\n\npa_batch.read_next_batch()',
        'result': """
pyarrow.RecordBatch
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: ["908cf67c-a086-4b94-9017-2089a83e4a6c"]
description: ["value is uneven"]
value: [1]
created_timestamp: [2025-04-10 09:52:55.249000Z]
""",
        'default': True,
    },
    # 'tf': {'example': '', 'result': '', 'default': False},
    'to_arrow_table': {
        'example': 'rel.to_arrow_table()',
        'result': """
pyarrow.Table
id: string
description: string
value: int64
created_timestamp: timestamp[us, tz=Europe/Amsterdam]
----
id: [["86b2011d-3818-426f-a41e-7cd5c7321f79","07fa4f89-0bba-4049-9acd-c933332a66d5","f2f1479e-f582-4fe4-b82f-9b753b69634c","529d3c63-5961-4adb-b0a8-8249188fc82a","aa9eea7d-7fac-4dcf-8f32-4a0b5d64f864","4852aa32-03f2-40d3-8006-b8213904775a","c0127203-f2e3-4925-9810-655bc02a3c19","2a1356ba-5707-44d6-a492-abd0a67e5efb","800a1c24-231c-4dae-bd68-627654c8a110"]]
description: [["value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven","value is even","value is uneven"]]
value: [[1,2,3,4,5,6,7,8,9]]
created_timestamp: [[2025-04-10 09:54:24.015000Z,2025-04-10 09:55:24.015000Z,2025-04-10 09:56:24.015000Z,2025-04-10 09:57:24.015000Z,2025-04-10 09:58:24.015000Z,2025-04-10 09:59:24.015000Z,2025-04-10 10:00:24.015000Z,2025-04-10 10:01:24.015000Z,2025-04-10 10:02:24.015000Z]]
""",
        'default': True,
    },
    'to_csv': {
        'example': 'rel.to_csv("code_example.csv")',
        'result': 'The data is exported to a CSV file, named code_example.csv',
        'default': True,
    },
    'to_df': {
        'example': 'rel.to_df()',
        'result': """
                                     id      description  value                created_timestamp
0  e1f79925-60fd-4ee2-ae67-5eff6b0543d1  value is uneven      1 2025-04-10 11:56:04.452000+02:00
1  caa619d4-d79c-4c00-b82e-9319b086b6f8    value is even      2 2025-04-10 11:57:04.452000+02:00
2  64c68032-99b9-4e8f-b4a3-6c522d5419b3  value is uneven      3 2025-04-10 11:58:04.452000+02:00
...
""",
        'default': True,
    },
    'to_parquet': {
        'example': 'rel.to_parquet("code_example.parquet")',
        'result': 'The data is exported to a Parquet file, named code_example.parquet',
        'default': True,
    },
    'to_table': {
        'example': 'rel.to_table("table_code_example")',
        'result': 'A table, named table_code_example, is created with the data of the relation',
        'default': True,
    },
    'to_view': {
        'example': 'rel.to_view("view_code_example", replace=True)',
        'result': 'A view, named view_code_example, is created with the query definition of the relation',
        'default': True,
    },
    # 'torch': {'example': '', 'result': '', 'default': True},
    'write_csv': {
        'example': 'rel.write_csv("code_example.csv")',
        'result': 'The data is exported to a CSV file, named code_example.csv',
        'default': True,
    },
    'write_parquet': {
        'example': 'rel.write_parquet("code_example.parquet")',
        'result': 'The data is exported to a Parquet file, named code_example.parquet',
        'default': True,
    },
}

CODE_EXAMPLE_MAP = {
    **CREATION_MEMBER_CODE_EXAMPLE_MAP,
    **DEFINITION_MEMBER_CODE_EXAMPLE_MAP,
    **TRANSFORMATION_MEMBER_CODE_EXAMPLE_MAP,
    **FUNCTION_MEMBER_CODE_EXAMPLE_MAP,
    **OUTPUT_MEMBER_CODE_EXAMPLE_MAP,
}
