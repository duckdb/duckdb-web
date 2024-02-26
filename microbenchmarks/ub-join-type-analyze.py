import duckdb

print("Analyze the join type results")
con = duckdb.connect()
con.sql("""CREATE TABLE results AS FROM 'results.csv';""")
con.sql("""
        SELECT type, median(duration) AS median_duration
        FROM results
        GROUP BY ALL
        ORDER BY type
        """).show()
