CREATE OR REPLACE TABLE results AS FROM 'row-group-size-comparison.csv';

.mode markdown

SELECT
    row_group_size AS "Row Group Size",
    any_value(num_row_groups) AS "Number of Row Groups",
    median(time) || ' s' AS "Execution Time"
FROM results
GROUP BY row_group_size
ORDER BY row_group_size ASC;
