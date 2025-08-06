with stats as (
    SELECT
        "Club",
        "Ranking" as "Global Ranking",
        "Stat" as "{{ ranking }}"
    FROM analytics.one_teams_ranking(
        in_ranking := '{{ ranking }}',
        in_comp    := '{{ name_comp }}',
        in_seasons := ARRAY['{{ season }}'],
        first_week := {{ first_week }},
        last_week  := {{ last_week }},
        first_date := '{{ first_date }}',
        last_date  := '{{ last_date }}',
        side       := '{{ in_side }}'
    )
)
SELECT *,
    dense_rank() over(
        order by cast("{{ ranking }}" as int) desc
    ) as "{{ ranking }} Ranking"
FROM stats
ORDER BY "{{ ranking }}" DESC;