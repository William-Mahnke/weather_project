-- windiest week for each city in each year (by average max wind speed)
WITH weekly_wind AS (
    SELECT
        s.city_id,
        EXTRACT(YEAR FROM s.date) AS year,
        EXTRACT(WEEK FROM s.date) AS week,
        AVG(s.max_wind_speed_mph) AS avg_wind_mph,
        MAX(s.max_wind_speed_mph) AS peak_wind_mph
    FROM weather.statistics s
    WHERE s.max_wind_speed_mph IS NOT NULL
    GROUP BY s.city_id, EXTRACT(YEAR FROM s.date), EXTRACT(WEEK FROM s.date)
),
ranked AS (
    SELECT
        city_id,
        year,
        week,
        avg_wind_mph,
        peak_wind_mph,
        RANK() OVER (
            PARTITION BY city_id, year
            ORDER BY avg_wind_mph DESC
        ) AS wind_rank
    FROM weekly_wind
)
SELECT
    c.city_name,
    r.year,
    r.week,
    ROUND(r.avg_wind_mph, 2) AS avg_wind_mph,
    ROUND(r.peak_wind_mph, 2) AS peak_wind_mph
FROM ranked r
JOIN weather.city c ON c.city_id = r.city_id
WHERE r.wind_rank = 1
ORDER BY c.city_name, r.year;