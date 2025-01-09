-- Find the top-3 longest domestic train routes
SELECT s1.name_short, s2.name_short, distances.distance
FROM distances
JOIN stations s1 ON distances.station1 = s1.code
JOIN stations s2 ON distances.station2 = s2.code
WHERE s1.country = s2.country
  AND s1.code < s2.code
ORDER BY distance DESC
LIMIT 3;
