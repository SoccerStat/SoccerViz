SELECT
    "Club",
    '{{ season }}' as "Season",
    "Ranking"
FROM analytics.overall_teams_ranking(
    in_comp := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}']
)