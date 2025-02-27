# Find the largest sepals/petals in the Iris data set
# using dplyr
library("duckdb")
library("dplyr")

con <- dbConnect(duckdb())
duckdb_register(con, "iris", iris)
tbl(con, "iris") |>
    filter(Sepal.Length > 5) |>
    group_by(Species) |>
    summarize(
        num_observations = count(),
        max_width = max(Sepal.Width),
        max_petal_length = max(Petal.Length),
        na.rm = TRUE) |>
    collect()
