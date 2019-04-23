# Contributing

## General Guidelines
* Do not commit/push directly to the master branch. Instead, create a feature branch/fork and file a merge request.

## Testing
* `make unit` runs the **fast** unit tests (~one minute), `make allunit` runs **all** unit tests (~one hour).
* Write many tests
* Test with different types, especially numerics and strings
* Try to test unexpected/incorrect usage as well, instead of only the happy path
* Slower tests should be added to the **all** unit tests. You can do this by adding `[.]` after the test group, e.g. `TEST_CASE("Test TPC-H SF0.1", "[tpch][.]")`.

## Formatting
* Tabs for indentation, spaces for alignment
* 120 columns
* `clang_format` enforces these rules automatically, use `make format` to run the formatter.

## C++ Guidelines
* Do not use `malloc`, prefer the use of smart pointers
* Strongly prefer the use of `unique_ptr` over `shared_ptr`, only use `shared_ptr` if you **absolutely** have to
* Do **not** import namespaces in headers (e.g. `using std`), only in source files
* When overriding a virtual method, avoid repeating virtual and always use override or final
* Use [u]int(8|16|32|64)_t instead of int, long, uint etc.
* Prefer using references over pointers
* Use C++11 for loops when possible: for (const auto& item : items) {...}

## Error Handling
* Use exceptions **only** when an error is encountered that terminates a query (e.g. parser error, table not found). Exceptions should only be used for **exceptional** situations. For regular errors that does not break the execution flow (e.g. errors you **expect** might occur) use a return value instead.
* Try to add test cases that trigger exceptions. If an exception cannot be easily triggered using a test case then it should probably be an assertion. This is not always true (e.g. out of memory errors are exceptions).
* Use **assert** only when failing the assert means a programmer error. Assert should never be triggered by a user input.
* Assert liberally, but make it clear with comments next to the assert what went wrong when the assert is triggered. Avoid code like `assert(a > b + 3);` without comments or context.

## Naming Conventions
* Files: lowercase separated by underscores, e.g., abstract_operator.cpp
* Types (classes, structs, enums, typedefs, using): CamelCase starting with uppercase letter, e.g., BaseColumn
* Variables: lowercase separated by underscores, e.g., chunk_size
* Functions: CamelCase starting with uppercase letter, e.g., GetChunk
* Choose descriptive names.
* Avoid i, j, etc. in **nested** loops. Prefer to use e.g. **column_idx**, **check_idx**. In a **non-nested** loop it is permissible to use **i** as iterator index.
