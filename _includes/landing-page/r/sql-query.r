# Find the largest sepals/petals in the Iris data set
library(duckdb)

con <- dbConnect(duckdb())
duckdb_register(con, "iris", iris)

query <- paste(
    'SELECT count(*) AS num_observations, ',
    'max("Sepal.Width") AS max_width, ',
    'max("Petal.Length") AS max_petal_length ',
    'FROM iris ',
    'WHERE "Sepal.Length" > 5 ',
    'GROUP BY ALL')
dbGetQuery(con, query)
