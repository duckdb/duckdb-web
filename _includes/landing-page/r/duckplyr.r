# Find the largest sepals/petals in the Iris data set
# using duckplyr
library("duckplyr")

iris |>
    filter(Sepal.Length > 5) |>
    group_by(Species) |>
    summarize(
        num_observations = n(),
        max_width = max(Sepal.Width),
        max_petal_length = max(Petal.Length),
        na.rm = TRUE) |>
    collect()
