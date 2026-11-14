 create a new page following the style and design assets of quack/index.html.

there are multiple things to design, so please fan out subagents so make this faster.

for every box, link the relevant documentation pages (from docs/2.0) and the relevant blog post

box 1: DuckDB in-process database

DuckDB is a full-fledged SQL database that runs as a library

it has clients: standalone command-line client, Python, Java, etc.

for illustration, draw a rectangle that says 'host process' and inside it should run duckdb with the duckdb logo. the duckdb should have a back-and-forth arrow a file that sits right from the box. the file should be called dbfile.duckdb

box 2: DuckDB as a server

DuckDB can work as a server using the Quack (quack://) remote protocol.

the client and the server are both duckdb instances.

the quack page already has illustration for this.

quack unlock multiple writers for DuckDB.

box 3: DuckDB as a lakehouse engine

DuckDB can read-write lakehouse formats (e.g., Iceberg + Amazon S3 Tables or DuckLake). these allow multiple DuckDB instances to 

box 4: agent mode

Since DuckDB 2.0, the DuckDB CLI supports agent mode, which frontloads important information and removes whitespace from output tables to save tokens.

in this case, duckdb is executed by the agent (use the agent.svg file to represent the agent)

Explain (in text) that when using agent mode, things that are prototyped locally can also run on a server without any changes to the SQL syntax.
