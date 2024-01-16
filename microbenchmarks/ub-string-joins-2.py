import duckdb
import time

print("Benchmark to join on VARCHAR field")
print(f"DuckDB version: {duckdb.__version__}")
con = duckdb.connect(database = "ldbc.duckdb")

print("Loading database")
con.sql("""
        CREATE TABLE Comment AS FROM read_csv('ldbc-sf300-comments/*.csv.gz', auto_detect=true, all_varchar=true, delim='|', header=true);
        """)

print("Running the join 5 times")
for i in range(0, 5):
        start = time.time()
        con.sql("""
                SELECT count(*) AS count
                FROM Comment c1
                JOIN Comment c2 ON c1.ParentCommentId = c2.id
                """).show()
        end = time.time()
        duration = end - start
        print(f"{duration}")
