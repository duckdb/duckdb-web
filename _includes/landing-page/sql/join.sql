-- Find the top-5 most expensive train routes in the Netherlands
SELECT s1.name, s2.name, tariffs.price
FROM tariffs
JOIN station s1
  ON s1.country = 'NL'
 AND tariffs.station1 = s1.code
JOIN station s2
  ON s2.country = 'NL'
 AND tariffs.station2 = s2.code
WHERE station1 < station2
ORDER BY Price DESC
LIMIT 5;
