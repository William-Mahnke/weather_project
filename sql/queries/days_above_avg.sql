-- days where daily mean temp exceeds that city's monthly average
WITH monthly_avg AS (
    SELECT
        city_id,
        EXTRACT(MONTH FROM date) AS month,
        AVG(mean_temp_f) AS month_avg_temp
    FROM weather.statistics
    WHERE mean_temp_f IS NOT NULL
    GROUP BY city_id, EXTRACT(MONTH FROM date)
)

SELECT
    c.city_name,
    m.month,
    COUNT(*) AS days_above_monthly_avg
FROM weather.statistics s
JOIN weather.city c ON c.city_id = s.city_id
JOIN monthly_avg m
    ON s.city_id = m.city_id
   AND EXTRACT(MONTH FROM s.date) = m.month
WHERE s.mean_temp_f > m.month_avg_temp
GROUP BY c.city_id, c.city_name, m.month
ORDER BY c.city_name, m.month;