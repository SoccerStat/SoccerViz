SELECT
    "Club",
    "Ranking"
    {% if combined_ranking == 'shots' %}
    ,
    "Goals For",
    "Goals Against",
    "Shots For",
    "Shots Against",
    "Shots on Target For",
    "Shots on Target Against"
    {% endif %}
FROM analytics.all_teams_rankings(
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := {{ first_week }},
    last_week  := {{ last_week }},
    first_date := '{{ first_date }}',
    last_date  := '{{ last_date }}',
    side       := '{{ in_side }}'
);