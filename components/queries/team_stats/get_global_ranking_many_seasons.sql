SELECT
    "Club",
    '{{ season }}' as "Season",
    "Stat" as "{{ ranking }}"
FROM analytics.one_teams_ranking(
    in_ranking := '{{ ranking }}',
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}']
)
ORDER BY "Season", "{{ ranking }}" desc;