import duckdb
import time

print("Benchmark to join on VARCHAR field encoding a UUID")
print(f"DuckDB version: {duckdb.__version__}")
con = duckdb.connect(database = "ldbc.duckdb")
con.sql("""
        CREATE TABLE Comment (
            creationDate TIMESTAMP WITH TIME ZONE NOT NULL,
            id BIGINT NOT NULL,
            locationIP TEXT NOT NULL,
            browserUsed TEXT NOT NULL,
            content TEXT NOT NULL,
            length INT NOT NULL,
            CreatorPersonId BIGINT NOT NULL,
            LocationCountryId BIGINT NOT NULL,
            ParentPostId BIGINT,
            ParentCommentId BIGINT,
        );
        """)

print("Loading database")
con.sql("""
        INSERT INTO Comment
            FROM read_csv('ldbc-sf100-comments/*.csv.gz', auto_detect=true, delim='|', header=true);
        """)

print("Adding UUIDs to the schema")
con.sql("ALTER TABLE Comment ADD COLUMN id_uuid VARCHAR;")
con.sql("ALTER TABLE Comment ADD COLUMN ParentCommentId_uuid VARCHAR;")

print("Assigning UUIDs to id_uuid")
con.sql("""
        UPDATE Comment
        SET id_uuid = uuid();
        """)
print("Assigning UUIDs to ParentCommentId_uuid")
con.sql("""
        UPDATE Comment
        SET ParentCommentId_uuid = ParentComment.id_uuid
        FROM Comment ParentComment
        WHERE ParentComment.id = Comment.ParentCommentId;
        """)

print("Running the join 5 times")
with open("results.csv", "a") as f:
        for i in range(0, 5):
                start = time.time()
                con.sql("""
                        SELECT count(*) AS count
                        FROM Comment c1
                        JOIN Comment c2 ON c1.ParentCommentId_uuid = c2.id_uuid;
                        """).show()
                end = time.time()
                duration = end - start
                f.write(f"UUID as VARCHAR,{i},{duration}\n")
