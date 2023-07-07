---

layout: post
title:  "From Waddle to Flying: Quickly expanding DuckDB's functionality with Scalar Python UDFs."
author: Pedro Holanda, Thijs Bruineman and Phillip Cloud
excerpt_separator: <!--more-->

---

<img src="/images/blog/bird-dance.gif"
     alt="DuckDB-Waddle-fly"
     width=100
     />

*TLDR: DuckDB now supports vectorized Scalar Python User Defined Functions (UDFs). By implementing Python UDFs, users can easily expand the functionality of DuckDB while taking advantage of DuckDB's fast execution model, SQL and data safety.*

User Defined Functions (UDFs) enable users to extend the functionality of a Database Management System (DBMS) to perform domain-specific tasks that are not implemented as built-in functions. For instance, users who frequently need to export private data can benefit from an anonymization function that masks the local part of an email while preserving the domain. Ideally, this function would be executed directly in the DBMS. This approach offers several advantages:

1) **Performance.** The function could be executed using the same execution model (e.g., streaming results, beyond-memory/out-of-core execution) of the DBMS, and without any unnecessary transformations.

2) **Easy Use.** UDFs can be seamlessly integrated into SQL queries, allowing users to leverage the power of SQL to call the functions. This eliminates the need for passing data through a separate database connector and executing external code. The functions can be utilized in various SQL contexts (e.g., subqueries, join conditions).

3) **Safety.** The sensitive data never leaves the DBMS process. 

There are two main reasons users often refrain from implementing UDFs. 1) There are security concerns associated with UDFs. Since UDFs are custom code created by users and executed within the DBMS process, there is a potential risk of crashing the server. However, when it comes to DuckDB, an embedded database, this concern is mitigated as each analyst runs their own DuckDB process separately. Therefore, the impact on server stability is not a significant worry. 2) The difficulty of implementation is a common deterrent for users. High-Performance UDFs are typically only supported in low-level languages. UDFs in higher-level languages like Python incur significant performance costs. Consequently many users cannot quickly implement their UDFs without investing a significant amount of time in learning a low-level language and understanding the internal details of the DBMS.

DuckDB followed a similar approach. As a DBMS tailored for analytical tasks, performance is a key consideration, leading to the implementation of its core in C++. Consequently, the initial focus of extensibility efforts [was centered around C++](https://www.youtube.com/watch?v=UKo_LQyLTko&ab_channel=DuckDBLabs). However, this  duck is not limited to just waddling; it can also fly. So we are delighted to announce the [recent addition](https://github.com/duckdb/duckdb/pull/7171) of Scalar Python UDFs to DuckDB.

DuckDB provides support for two distinct types of Python UDFs, differing in the Python object used for communication between [DuckDB's native data types](https://duckdb.org/docs/sql/data_types/overview) and the Python process. These communication layers include support for [Python built-in types](https://duckdb.org/docs/sql/data_types/overview) and [PyArrow Tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).

The two approaches exhibit two key differences:

1) **Zero-Copy.** PyArrow Tables leverage our [zero-copy integration with Arrow](https://duckdb.org/2021/12/03/duck-arrow.html), enabling efficient translation of data types to Python-Land with zero-copy cost.

2) **Vectorization.** PyArrow Table functions operate on a chunk level, processing chunks of data containing up to 2048 rows. This approach maximizes cache locality and leverages vectorization. On the other hand, the built-in types UDF implementation operates on a per-row basis.

This blog post aims to demonstrate how you can extend DuckDB using Python UDFs, with a particular emphasis on PyArrow-powered UDFs. In our quick-tour section, we will provide examples using the PyArrow UDF types. For those interested in benchmarks, you can jump ahead to the [benchmark section below](#BenchmarkComparison). If you want to see a detailed description of the Python UDF API, please refer to our [documentation](https://duckdb.org/docs/api/python/function).

## Python UDFs
This section depicts several practical examples of using Python UDFs. Each example uses a different type of Python UDF.

### Quick-Tour
To demonstrate the usage of Python UDFs in DuckDB, let's consider the following example. We have a dictionary called `world_cup_titles` that maps countries to the number of World Cups they have won. We want to create a Python UDF that takes a country name as input, searches for the corresponding value in the dictionary, and returns the number of World Cups won by that country. If the country is not found in the dictionary, the UDF will return `NULL`.

Here's an example implementation:

```python
import duckdb
from duckdb.typing import *

con = duckdb.connect()

# Dictionary that maps countries and world cups they won
world_cup_titles = {
    "Brazil": 5,
    "Germany": 4,
    "Italy": 4,
    "Argentina": 2,
    "Uruguay": 2,
    "France": 2,
    "England": 1,
    "Spain": 1
}

# Function that will be registered as an UDF, simply does a lookup in the python dictionary
def world_cups(x):
     return world_cup_titles.get(x)

# We register the function
con.create_function("wc_titles", world_cups, [VARCHAR], INTEGER)
```

That's it, the function is then registered and ready to be called through SQL.
```python
# Let's create an example countries table with the countries we are interested in using
con.execute("CREATE TABLE countries(country VARCHAR)")
con.execute("INSERT INTO countries VALUES ('Brazil'), ('Germany'), ('Italy'), ('Argentina'), ('Uruguay'), ('France'), ('England'), ('Spain'), ('Netherlands')")
# We can simply call the function through SQL, and even use the function return to eliminate the countries that never won a world cup
con.sql("SELECT country, wc_titles(country) as world_cups from countries").fetchall()
# [('Brazil', 5), ('Germany', 4), ('Italy', 4), ('Argentina', 2), ('Uruguay', 2), ('France', 2), ('England', 1), ('Spain', 1), ('Netherlands', None)]

```

### Generating Fake Data with Faker (Built-In Type UDF)
Here is an example that demonstrates the usage of the [Faker library](https://faker.readthedocs.io/en/master/)  to generate a scalar function in DuckDB, which returns randomly generated dates. The function, named `random_date`, does not require any inputs and outputs a `DATE` column. Since Faker utilizes built-in Python types, the function directly returns them.
One important thing to notice is that a function that is not deterministic based on its input must be marked as having `side_effects`.

```python
import duckdb

# By importing duckdb.typing we can specify DuckDB Types directly without using strings
from duckdb.typing import *

from faker import Faker

# Our Python UDF generates a random date every time it's called
def random_date():
     fake = Faker()
     return fake.date_between()
```

We then have to register the Python function in DuckDB using `create_function`. Since our function doesn't require any inputs, we can pass an empty list as the `argument_type_list`. As the function returns a date, we specify `DATE` from `duckdb.typing` as the `return_type`. Note that since our `random_date()` function returns a built-in Python type (`datetime.date`), we don't need to specify the UDF type.

```py
# To exemplify the effect of side-effect, let's first run the function without marking it.
duckdb.create_function('random_date', random_date, [], DATE)

# After registration, we can use the function directly via SQL
# Notice that without side_effect=True, it's not guaranteed that the function will be re-evaluated.
res = duckdb.sql('select random_date() from range (3)').fetchall()
# [(datetime.date(2003, 8, 3),), (datetime.date(2003, 8, 3),), (datetime.date(2003, 8, 3),)]

# Now let's re-add the function with side-effects marked as true.
duckdb.remove_function('random_date')
duckdb.create_function('random_date', random_date, [], DATE, side_effects=True)
res = duckdb.sql('select random_date() from range (3)').fetchall()
# [(datetime.date(2020, 11, 29),), (datetime.date(2009, 5, 18),), (datetime.date(2018, 5, 24),)]
```

### Swap String Case (PyArrow Type UDF)
One issue with using built-in types is that you don't benefit from zero-copy, vectorization and cache locality. Using PyArrow as a UDF type should be favored to leverage these optimizations.

To demonstrate a PyArrow function, let's consider a simple example where we want to transform lowercase characters to uppercase and uppercase characters to lowercase. Fortunately, PyArrow already has a function for this in the compute engine, and it's as simple as calling `pc.utf8_swapcase(x)`.

```python
import duckdb

# By importing duckdb.typing we can specify DuckDB Types directly without using strings
from duckdb.typing import *

import pyarrow as pa
import pyarrow.compute as pc

def swap_case(x):
     # Swap the case of the 'column' using utf8_swapcase and return the result
     return pc.utf8_swapcase(x)

con = duckdb.connect()
# To register the function, we must define it's type to be 'arrow'
con.create_function('swap_case', swap_case, [VARCHAR], VARCHAR, type='arrow')

res = con.sql("select swap_case('PEDRO HOLANDA')").fetchall()
# [('pedro holanda',)]
```


### Predicting Taxi Fare costs (Ibis + PyArrow UDF)

Python UDFs offer significant power as they enable users to leverage the extensive Python ecosystem and tools, including libraries like [PyTorch](https://pytorch.org/) and [Tensorflow](https://www.tensorflow.org/) that efficiently implement machine learning operations.

Additionally the [Ibis project](https://ibis-project.org/) offers a DataFrame API with great DuckDB integration and supports both of DuckDB's native Python and PyArrow UDFs.

In this example, we demonstrate the usage of a pre-built PyTorch model to estimate taxi fare costs based on the traveled distance. You can find a complete example [in this blog post by the Ibis team](https://ibis-project.org/blog/rendered/torch/).

```python
import torch
import pyarrow as pa
import ibis
import ibis.expr.datatypes as dt

from ibis.expr.operations import udf


# The code to generate the model is not specified in this snippet, please refer to the provided link for more information
model = ...

# Function that uses the model and a traveled distance input tensor to predict values, please refer to the provided link for more information
def predict_linear_regression(model, tensor: torch.Tensor) -> torch.Tensor:
    ...


# Indicate to ibis that this is a scalar user-defined function whose input format is pyarrow
@udf.scalar.pyarrow
def predict_fare(x: dt.float64) -> dt.float32:
    # `x` is a pyarrow.ChunkedArray; the `dt.float64` annotation indicate the element type of the ChunkedArray.

    # Transform the data from PyArrow to the required torch tensor format and dimension.
    tensor = torch.from_numpy(x.to_numpy()[:, None]).float()

    # Call the actual prediction function, which also returns a torch tensor.
    predicted = predict_linear_regression(model, tensor).ravel()
    return pa.array(predicted.numpy())


# Execute a query on the NYC Taxi parquet file to showcase our model's predictions, the actual fare amount, and the distance.
expr = (
    ibis.read_parquet('yellow_tripdata_2016-02.parquet')
    .mutate(
        "fare_amount",
        "trip_distance",
        predicted_fare=lambda t: predict_fare(t.trip_distance),
    )
)
df = expr.execute()
```

By utilizing Python UDFs in DuckDB with Ibis, you can seamlessly incorporate machine learning models and perform predictions directly within your Ibis code and SQL queries. The example demonstrates how to predict taxi fare costs based on distance using a PyTorch model, showcasing the integration of machine learning capabilities within DuckDB's SQL environment driven by Ibis.

## Benchmarks
In this section, we will perform simple benchmark comparisons to demonstrate the performance differences between two different types of Python UDFs. The benchmark will measure the execution time, and peak memory consumption. The benchmarks are executed 5 times, and the median value is considered. The benchmark is conducted on a Mac Apple M1 with 16GB of RAM.


### Built-In Python Vs PyArrow
To benchmark these UDF types, we create UDFs that take an integral column as input, add one to each value, and return the result. The code used for this benchmark section can be found [here](https://gist.github.com/pdet/ebd201475581756c29e4533a8fa4106e). 

```python
import pyarrow.compute as pc
import duckdb
import pyarrow as pa

# Built-In UDF
def add_built_in_type(x):
     return x + 1

#Arrow UDF
def add_arrow_type(x):
     return pc.add(x,1)

con = duckdb.connect()

# Registration
con.create_function('built_in_types', add_built_in_type, ['BIGINT'], 'BIGINT', type='native')
con.create_function('add_arrow_type', add_arrow_type, ['BIGINT'], 'BIGINT', type='arrow')

# Integer View with 10,000,000 elements.
con.sql("""
     select
          i
          from range(10000000) tbl(i);
""").to_view("numbers")

# Calls for both UDFs
native_res = con.sql("select sum(add_built_in_type(i)) from numbers").fetchall()
arrow_res = con.sql("select sum(add_arrow_type(i)) from numbers").fetchall()

```

|    Name     | Time (s) |
|-------------|----------|
| Built-In    | 5.37     |
| PyArrow     | 0.35     |

We can observe a performance difference of more than one order of magnitude between the two UDFs. The difference in performance is primarily due to three factors:

1) In Python, object construction and general use is rather slow. This is due to to several reasons, including automatic memory management, interpretation, and dynamic typing.
2) The PyArrow UDF does not require any data copying.
3) The PyArrow UDF is executed in a vectorized fashion, processing chunks of data instead of individual rows.


### Python UDFs Vs External Functions
Here we compare the usage of a Python UDF with an external function. In this case, we have a function that calculates the sum of the lengths of all strings in a column. You can find the code used for this benchmark section [here](https://gist.github.com/pdet/2907290725539d390df7981e799ed593).

```python
import duckdb
import pyarrow as pa

# Function used in UDF
def string_length_arrow(x):
     tuples = len(x)
     values = [len(i.as_py()) if i.as_py() != None else 0 for i in x]
     array = pa.array(values, type=pa.int32(), size=tuples)
     return array


# Same Function but external to the database
def exec_external(con):
     arrow_table = con.sql("select i from strings tbl(i)").arrow()
     arrow_column = arrow_table['i']
     tuples = len(arrow_column)
     values = [len(i.as_py()) if i.as_py() != None else 0 for i in arrow_column]
     array = pa.array(values, type=pa.int32(), size=tuples)
     arrow_tbl = pa.Table.from_arrays([array], names=['i'])
     return con.sql("select sum(i) from arrow_tbl").fetchall()


con = duckdb.connect()
con.create_function('strlen_arrow', string_length_arrow, ['VARCHAR'], int, type='arrow')

con.sql("""
     select
          case when i != 0 and i % 42 = 0
          then
               NULL
          else
               repeat(chr((65 + (i % 26))::INTEGER), (4 + (i % 12))) end
          from range(10000000) tbl(i);
""").to_view("strings")

con.sql("select sum(strlen_arrow(i)) from strings tbl(i)").fetchall()

exec_external(con)

```


|    Name     | Time (s) | Peak Memory Consumption (MB) |
|-------------|----------|------------------------------|
| External    | 5.65     | 584.032                      |
| UDF         | 5.63     | 112.848                      |


Here we can see that there is no significant regression in performance when utilizing UDFs. However, you still have the benefits of safer execution and the utilization of SQL. In our example, we can also notice that the external function materializes the entire query, resulting in a 5x higher peak memory consumption compared to the UDF approach.

## Conclusions and Further Development
Scalar Python UDFs are now supported in DuckDB, marking a significant milestone in extending the functionality of the database. This enhancement empowers users to perform complex computations using a high-level language. Additionally, Python UDFs can leverage DuckDB's zero-copy integration with Arrow, eliminating data transfer costs and ensuring efficient query execution.

While the introduction of Python UDFs is a major step forward, our work in this area is ongoing. Our roadmap includes the following focus areas:

1. **Aggregate/Table-Producing UDFs**: Currently, users can create Scalar UDFs, but we are actively working on supporting Aggregation Functions (which perform calculations on a set of values and return a single result) and Table-Producing Functions (which return tables without limitations on the number of columns and rows).

2. **Types**: Scalar Python UDFs currently support most DuckDB types, with the exception of ENUM types and BIT types. We are working towards expanding the type support to ensure comprehensive functionality.

As always, we are happy to hear your thoughts! Feel free to drop us an [email](mailto:pedro@duckdblabs.com;thijs@duckdblabs.com) if you have any suggestions, comments or questions.

Last but not least, if you encounter any problems using our Python UDFs, please open an issue in [DuckDB's issue tracker](https://github.com/duckdb/duckdb/issues).
