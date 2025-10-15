SELECT DISTINCT extract(isodow from date), time, trim(to_char(date, 'Day')) || ' ' || LEFT(time::text, 5) as "Slot"
FROM analytics.staging_teams_performance stp
WHERE season = '{{ season }}'
AND competition = '{{ name_comp }}'
ORDER BY EXTRACT(ISODOW FROM date), time;