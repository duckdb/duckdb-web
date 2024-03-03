CREATE OR REPLACE TABLE results AS FROM 'pk.csv';

.mode markdown

SELECT operation AS "Operation", median(time) || 's' AS "Execution Time"
FROM results
GROUP BY operation
ORDER BY operation ASC;
