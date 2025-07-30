SELECT
    "Club",
    "Ranking"
    {% if combined_ranking == 'xg' %}
    ,
    "xG For (soccerstat)",
    "xG Against (soccerstat)",
    "xG For",
    "xG Against",
    "Goals For",
    "Goals Against"
    {% endif %}
FROM analytics.all_teams_rankings_enriched(
    in_comp    := '{{ name_comp }}',
    in_seasons := ARRAY['{{ season }}'],
    first_week := {{ first_week }},
    last_week  := {{ last_week }},
    first_date := '{{ first_date }}',
    last_date  := '{{ last_date }}',
    side       := '{{ in_side }}',
    r          := 2
);