# Create custom user-defined function
import duckdb

def add_plus_one(x):
    return x + 1

con = duckdb.connect()
con.create_function('add_plus_one', add_plus_one,
    ['BIGINT'], 'BIGINT', type='native')

con.sql("""
    SELECT sum(add_plus_one(i)) FROM range(10) tbl(i);
    """)
