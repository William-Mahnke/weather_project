-- days where max temp reached 90°F or above, per month by city
SELECT
    c.city_name,
    EXTRACT(YEAR FROM s.date) AS year,
    EXTRACT(MONTH FROM s.date) AS month,
    COUNT(*) AS days_above_90f
FROM weather.statistics s
JOIN weather.city c ON s.city_id = c.city_id
WHERE s.max_temp_f >= 90
GROUP BY c.city_id, c.city_name, EXTRACT(YEAR FROM s.date), EXTRACT(MONTH FROM s.date)
ORDER BY c.city_name, month, year;