SELECT
    "Club",
    "Matches" as "M",
    "Wins" as "W",
    "Draws" as "D",
    "Loses" as "L",
    "Goals For" as "GF",
    "Goals Against" as "GA",
    "Goals Diff" as "GD",
    "Shots Conversion Rate For" as "Shots For CR",
    "Shots Conversion Rate Against" as "Shots Against CR",
    "Shots on Target Conversion Rate For" as "On Target For CR",
    "Shots on Target Conversion Rate Against" as "On Target Against CR"
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