SELECT
    "Club",
    "Matches",
    "Wins",
    "Draws",
    "Loses",
    "Goals For",
    "Goals Against"
FROM analytics.all_teams_rankings(
    in_comp := '{{ name_comp }}',
    in_seasons := array['{{ season }}'],
    first_week := {{ first_week }},
    last_week := {{ last_week }},
    first_date := '{{ first_date }}',
    last_date := '{{ last_date }}',
    side := '{{ in_side }}'
)
WHERE "Club" = '{{ name_team }}';