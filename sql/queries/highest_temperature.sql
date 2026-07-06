-- highest temperature for each city (and date)
WITH ranked AS (
    SELECT c.city_name, s.max_temp_f, s.date,
    RANK() OVER (
        PARTITION BY s.city_id
        ORDER BY s.max_temp_f DESC
    ) AS temp_rank
    FROM weather.city c
    JOIN weather.statistics s ON c.city_id = s.city_id
)

SELECT city_name, max_temp_f highest_temp, date
FROM ranked
WHERE temp_rank = 1
ORDER BY city_name, date;
