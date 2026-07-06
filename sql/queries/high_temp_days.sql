-- number of high temperature days for each city 
-- high temperatures are above 95% quartile for temps in that city 
WITH city_thresholds AS (
    SELECT city_id,
    PERCENTILE_COUNT(0.95) WITHIN GROUP (ORDER BY max_temp_f) AS p95_threshold
    FROM weather.statistics 
    WHERE max_temp_f IS NOT NULL
    GROUP BY city_id
)

SELECT c.city_name, COUNT(*) AS high_temp_days
FROM weather.city c
JOIN weather.statistics s ON c.city_id = s.city_id
JOIN city_thresholds t ON s.city_id = t.city_id
WHERE s.max_temp_f >= t.p95_threshold
GROUP BY c.city_id, c.city_name;