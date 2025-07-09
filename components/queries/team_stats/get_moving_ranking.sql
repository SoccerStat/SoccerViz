SELECT
    "Club",
    {{ week }} as "Week",
    "Stat" as "{{ ranking }}"
FROM analytics.one_teams_ranking(
    in_ranking := '{{ ranking }}',
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := {{ week }},
    last_week  := {{ week }})
ORDER BY "{{ ranking }}" DESC;