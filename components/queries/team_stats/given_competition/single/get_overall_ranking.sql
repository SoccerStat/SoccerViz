SELECT *
FROM analytics.overall_teams_ranking(
    in_comp := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := {{ first_week }},
    last_week  := {{ last_week }},
    first_date := '{{ first_date }}',
    last_date  := '{{ last_date }}',
    day_slots  := ARRAY[{{ day_slots }}]::varchar[],
    time_slots := ARRAY[{{ time_slots }}]::varchar[],
    side       := '{{ in_side }}'
)