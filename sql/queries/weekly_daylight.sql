-- get average daylight duration by week for each city
SELECT c.city_name, EXTRACT(WEEK FROM s.date) AS week, AVG(s.daylight_duration_s) AS avg_daylight
FROM weather.statistics s
JOIN weather.city c ON c.city_id = s.city_id
GROUP BY c.city_id, c.city_name, EXTRACT(WEEK FROM s.date)
ORDER BY c.city_name, week;