SELECT
    "Club",
    "Matches" as "M",
    "Points" as "P",
    "Wins" as "W",
    "Draws" as "D",
    "Loses" as "L",
    "Goals For" as "GF",
    "Goals Against" as "GA",
    "Goals Diff" as "GD",
    "Succ Passes Rate" as "% Succ Passes",
    "Points/Match",
    "Shots/onTarget Conversion Rate For" as "Shots/onTarget For CR",
 	"Shots/onTarget Conversion Rate Against" as "Shots/onTarget Against CR",
 	"Shots/Goals Conversion Rate For" as "Shots/Goals For CR",
 	"Shots/Goals Conversion Rate Against" as "Shots/Goals Against CR",
 	"onTarget/Goals Conversion Rate For" as "onTarget/Goals For CR",
 	"onTarget/Goals Conversion Rate Against" as "onTarget/Goals Against CR"
FROM analytics.all_teams_rankings(
    in_comp := '{{ name_comp }}',
    in_seasons := array['{{ season }}'],
    first_week := {{ first_week }},
    last_week := {{ last_week }},
    first_date := '{{ first_date }}',
    last_date := '{{ last_date }}',
    day_slots  := ARRAY[{{ day_slots }}]::varchar[],
    time_slots := ARRAY[{{ time_slots }}]::varchar[],
    side := '{{ in_side }}'
)
WHERE "Club" = '{{ name_team }}';