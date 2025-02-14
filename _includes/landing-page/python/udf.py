# Create custom user-defined function
import duckdb

def plus_one(x):
    return x + 1

con = duckdb.connect()
con.create_function('plus_one', plus_one,
    ['BIGINT'], 'BIGINT', type='native')

con.sql("""
    SELECT sum(plus_one(i)) FROM range(10) tbl(i);
    """)
