---
layout: docu
title: Multiple Python Threads
selected: Multiple Python Threads
---

# Multiple Reader and Writer Threads Example
This demonstrates how to simultaneously insert into and read from a DuckDB database across multiple Python threads. 
This could be useful in scenarios where new data is flowing in and an analysis should be periodically re-run. 
Note that this is all within a single Python process (see the [FAQ](/faq) for details on DuckDB concurrency).
Feel free to follow along in this [Google Collaboratory Notebook](https://colab.research.google.com/drive/190NB2m-LIfDcMamCY5lIzaD2OTMnYclB?usp=sharing).

## Setup
First, import duckdb and several modules from the Python standard library. 
Then connect to a file-backed DuckDB database and create an example table to store inserted data. 
This table will track the name of the thread that completed the insert and automatically insert the timestamp when that insert occured using the [`DEFAULT` expression](/docs/sql/statements/create_table#syntax).
```python
import duckdb
from threading import Thread, current_thread
import random

duckdb_con = duckdb.connect('my_peristent_db.duckdb') 
# duckdb_con = duckdb.connect() # Pass in no parameters for an in memory database
duckdb_con.execute("""
    CREATE OR REPLACE TABLE my_inserts (
        thread_name varchar, 
        insert_time timestamp DEFAULT current_timestamp
    )
""")
```

## Reader and Writer Functions
Next, define functions to be executed by the writer and reader threads. 
Each thread must use the `.cursor()` method to create a thread-local connection to the same DuckDB file based on the original connection. 
This approach also works with in-memory DuckDB databases.

```python
def write_from_thread(duckdb_con):
    # Create a DuckDB connection specifically for this thread
    local_con = duckdb_con.cursor()
    # Insert a row with the name of the thread. insert_time is auto-generated.
    thread_name = str(current_thread().name)
    result = local_con.execute("""
        INSERT INTO my_inserts (thread_name) 
        VALUES (?)
    """, (thread_name,)).fetchall()

def read_from_thread(duckdb_con):
    # Create a DuckDB connection specifically for this thread
    local_con = duckdb_con.cursor()
    # Query the current row count
    thread_name = str(current_thread().name)
    results = local_con.execute("""
        SELECT 
            ? as thread_name,
            count(*) as row_counter,
            current_timestamp 
        FROM my_inserts
    """, (thread_name,)).fetchall()
    print(results)
```

## Create Threads
We define how many writers and readers to use, and define a list to track all of the Threads that will be created.
Then, create first writer and then reader Threads. 
Next, shuffle them so that they will be kicked off in a random order to simulate simultaneous writers and readers.
Note that the Threads have not yet been executed, only defined.
```python
write_thread_count = 50
read_thread_count = 5
threads = []

# Create multiple writer and reader threads (in the same process) 
# Pass in the same connection as an argument
for i in range(write_thread_count):
    threads.append(Thread(target=write_from_thread,
                            args=(duckdb_con,),
                            name='write_thread_'+str(i)))

for j in range(read_thread_count):
    threads.append(Thread(target=read_from_thread,
                            args=(duckdb_con,),
                            name='read_thread_'+str(j)))

# Shuffle the threads to simulate a mix of readers and writers
random.seed(6) # Set the seed to ensure consistent results when testing
random.shuffle(threads)
```

## Run Threads and Show Results
Now, kick off all threads to run in parallel, then wait for all of them to finish before printing out the results. 
Note that the timestamps of readers and writers are interspersed as expected due to the randomization.
```python
# Kick off all threads in parallel
for thread in threads:
    thread.start()

# Ensure all threads complete before printing final results
for thread in threads:
    thread.join()

print(duckdb_con.execute("""
    SELECT 
        * 
    FROM my_inserts 
    ORDER BY 
        insert_time
""").df())

```