SELECT
    "Club",
    "Ranking"
    {%- if combined_ranking == 'shots' %},
    "Goals For",
    "Goals Against",
    "Shots For",
    "Shots Against",
    "Shots on Target For",
    "Shots on Target Against"
    {%- elif combined_ranking == 'outcomes' %},
    "Wins",
    "Draws",
    "Loses"
    {%- elif combined_ranking == 'passes' %},
    "Succ Passes",
    "Att Passes",
    "Succ Passes" + "Att Passes" as "Total Passes",
    "Succ Passes Rate"
    {%- endif %}
FROM analytics.all_teams_rankings(
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := {{ first_week }},
    last_week  := {{ last_week }},
    first_date := '{{ first_date }}',
    last_date  := '{{ last_date }}',
    side       := '{{ in_side }}',
    day_slots  := ARRAY[{{ day_slots }}]::varchar[],
    time_slots := ARRAY[{{ time_slots }}]::varchar[],
    r          := 2
);