SELECT DISTINCT extract(isodow from date), time, trim(to_char(date, 'Day')) || ' ' || LEFT(time::text, 5) as "Slot"
FROM analytics.staging_teams_performance stp
WHERE season = '{{ season }}'
AND CASE
    WHEN lower('{{ name_comp }}') = 'all'
    THEN TRUE
    ELSE competition = '{{ name_comp }}'
END
ORDER BY EXTRACT(ISODOW FROM date), time;