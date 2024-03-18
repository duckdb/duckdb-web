| Function | Description | Example | Result |
|:--|:---|:---|:-|
| *`union`*`.`*`tag`* | Dot notation serves as an alias for `union_extract`.| `(union_value(k := 'hello')).k` | `string` |
| `union_extract(`*`union`*`, `*`'tag'`*`)` | Extract the value with the named tags from the union. `NULL` if the tag is not currently selected | `union_extract(s, 'k')` | `hello` |
| `union_value(`*`tag := any`*`)` | Create a single member `UNION` containing the argument value. The tag of the value will be the bound variable name. | `union_value(k := 'hello')` | `'hello'::UNION(k VARCHAR)`| 
| `union_tag(`*`union`*`)` | Retrieve the currently selected tag of the union as an [Enum](../../sql/data_types/enum). | `union_tag(union_value(k := 'foo'))`  | `'k'` |
