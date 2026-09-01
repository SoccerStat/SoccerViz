SELECT
    "Club",
    '{{ season }}' as "Season",
    "Ranking" as "Overall Ranking",
    "Ranking (excl. p.d.)" as "Overall Ranking (excl. p.d.)"
FROM analytics.overall_teams_ranking(
    in_comp := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}']
)