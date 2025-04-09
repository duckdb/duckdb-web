---
layout: docu
title: SQL to/from JSON
---

DuckDB provides functions to serialize and deserialize `SELECT` statements between SQL and JSON, as well as executing JSON serialized statements.

| Function | Type | Description |
|:------|:-|:---------|
| `json_deserialize_sql(json)` | Scalar  | Deserialize one or many `json` serialized statements back to an equivalent SQL string. |
| `json_execute_serialized_sql(varchar)` | Table | Execute `json` serialized statements and return the resulting rows. Only one statement at a time is supported for now. |
| `json_serialize_sql(varchar, skip_default := boolean, skip_empty := boolean, skip_null := boolean, format := boolean)` | Scalar | Serialize a set of semicolon-separated (`;`) select statements to an equivalent list of `json` serialized statements. |
| `PRAGMA json_execute_serialized_sql(varchar)` | Pragma | Pragma version of the `json_execute_serialized_sql` function. |

The `json_serialize_sql(varchar)` function takes three optional parameters, `skip_empty`, `skip_null`, and `format` that can be used to control the output of the serialized statements.

If you run the `json_execute_serialized_sql(varchar)` table function inside of a transaction the serialized statements will not be able to see any transaction local changes. This is because the statements are executed in a separate query context. You can use the `PRAGMA json_execute_serialized_sql(varchar)` pragma version to execute the statements in the same query context as the pragma, although with the limitation that the serialized JSON must be provided as a constant string, i.e., you cannot do `PRAGMA json_execute_serialized_sql(json_serialize_sql(...))`.

Note that these functions do not preserve syntactic sugar such as `FROM * SELECT ...`, so a statement round-tripped through `json_deserialize_sql(json_serialize_sql(...))` may not be identical to the original statement, but should always be semantically equivalent and produce the same output.

### Examples

Simple example:

```sql
SELECT json_serialize_sql('SELECT 2');
```

```text
{"error":false,"statements":[{"node":{"type":"SELECT_NODE","modifiers":[],"cte_map":{"map":[]},"select_list":[{"class":"CONSTANT","type":"VALUE_CONSTANT","alias":"","query_location":7,"value":{"type":{"id":"INTEGER","type_info":null},"is_null":false,"value":2}}],"from_table":{"type":"EMPTY","alias":"","sample":null,"query_location":18446744073709551615},"where_clause":null,"group_expressions":[],"group_sets":[],"aggregate_handling":"STANDARD_HANDLING","having":null,"sample":null,"qualify":null},"named_param_map":[]}]}
```

Example with multiple statements and skip options:

```sql
SELECT json_serialize_sql('SELECT 1 + 2; SELECT a + b FROM tbl1', skip_empty := true, skip_null := true);
```

```text
{"error":false,"statements":[{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":9,"function_name":"+","children":[{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":7,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":1}},{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":11,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":2}}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"EMPTY","query_location":18446744073709551615},"aggregate_handling":"STANDARD_HANDLING"}},{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":23,"function_name":"+","children":[{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":21,"column_names":["a"]},{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":25,"column_names":["b"]}],"order_bys":{"type":"ORDER_MODIFIER"},"distinct":false,"is_operator":true,"export_state":false}],"from_table":{"type":"BASE_TABLE","query_location":32,"table_name":"tbl1"},"aggregate_handling":"STANDARD_HANDLING"}}]}
```

Skip the default values in the AST (e.g., `"distinct":false`):

```sql
SELECT json_serialize_sql('SELECT 1 + 2; SELECT a + b FROM tbl1', skip_default := true, skip_empty := true, skip_null := true);
```

```text
{"error":false,"statements":[{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":9,"function_name":"+","children":[{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":7,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":1}},{"class":"CONSTANT","type":"VALUE_CONSTANT","query_location":11,"value":{"type":{"id":"INTEGER"},"is_null":false,"value":2}}],"order_bys":{"type":"ORDER_MODIFIER"},"is_operator":true}],"from_table":{"type":"EMPTY"},"aggregate_handling":"STANDARD_HANDLING"}},{"node":{"type":"SELECT_NODE","select_list":[{"class":"FUNCTION","type":"FUNCTION","query_location":23,"function_name":"+","children":[{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":21,"column_names":["a"]},{"class":"COLUMN_REF","type":"COLUMN_REF","query_location":25,"column_names":["b"]}],"order_bys":{"type":"ORDER_MODIFIER"},"is_operator":true}],"from_table":{"type":"BASE_TABLE","query_location":32,"table_name":"tbl1"},"aggregate_handling":"STANDARD_HANDLING"}}]}
```
Example with a syntax error:

```sql
SELECT json_serialize_sql('TOTALLY NOT VALID SQL');
```

```text
{"error":true,"error_type":"parser","error_message":"syntax error at or near \"TOTALLY\"","error_subtype":"SYNTAX_ERROR","position":"0"}
```

Example with deserialize:

```sql
SELECT json_deserialize_sql(json_serialize_sql('SELECT 1 + 2'));
```

```text
SELECT (1 + 2)
```

Example with deserialize and syntax sugar, which is lost during the transformation:

```sql
SELECT json_deserialize_sql(json_serialize_sql('FROM x SELECT 1 + 2'));
```

```text
SELECT (1 + 2) FROM x
```

Example with execute:

```sql
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('SELECT 1 + 2'));
```

```text
3
```

Example with error:

```sql
SELECT * FROM json_execute_serialized_sql(json_serialize_sql('TOTALLY NOT VALID SQL'));
```

```console
Parser Error:
Error parsing json: parser: syntax error at or near "TOTALLY"
```