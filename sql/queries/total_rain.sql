-- total rainfall by month & year for each city
WITH rain_sums AS (
    SELECT
        city_id,
        EXTRACT(YEAR FROM date)  AS year,
        EXTRACT(MONTH FROM date) AS month,
        SUM(total_rain_in)       AS rain_sum
    FROM weather.statistics
    GROUP BY city_id, EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
)

SELECT 
    w.city_name,
    r.year,
    r.month,
    r.rain_sum total_rain
FROM weather.city w
JOIN rain_sums r ON w.city_id = r.city_id
ORDER BY 
    w.city_name,
    r.year,
    r.month;

