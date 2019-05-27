
## String Functions
This section describes functions and operators for examining and manipulating string values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| *string* \|\| *string* | String concatenation | 'Duck' \|\| 'DB' | DuckDB |
| length(*string*) | Number of characters in string | length('Hello') | 5 |
| lower(*string*) | Convert string to lower case | lower('Hello') | hello |
| upper(*string*) | Convert string to upper case | upper('Hello') | HELLO |
| substring(*string*, *start*, *length*) | Extract substring of *length* characters starting from character *start*. Note that a *start* value of `1` refers to the *first* character of the string. | substring('Hello', 2, 2) | el |
