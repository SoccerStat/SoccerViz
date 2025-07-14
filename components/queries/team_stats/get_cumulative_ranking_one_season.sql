SELECT
    "Club",
    {{ week }} as "Week",
    "Ranking",
    "Stat" as "{{ ranking }}"
FROM analytics.one_teams_ranking(
    in_ranking := '{{ ranking }}',
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := 1,
    last_week  := {{ week }})
ORDER BY "{{ ranking }}" DESC;