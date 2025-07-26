SELECT
    "Club",
    {{ week }} as "Week",
    "Ranking",
    "Stat" as "{{ ranking }}",
    round("Stat"::numeric / {{ week }}::numeric, 2) as "{{ ranking }}/Match"
FROM analytics.one_teams_ranking(
    in_ranking := '{{ ranking }}',
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := 1,
    last_week  := {{ week }})
ORDER BY "{{ ranking }}" DESC;