with stats as (
    SELECT
        "Club",
        {{ week }} as "Week",
        "Ranking" as "Global Ranking",
        "Stat" as "{{ ranking }}",
        round("Stat"::numeric / {{ week }}::numeric, 2) as "{{ ranking }}/Match"
    FROM analytics.one_teams_ranking(
        in_ranking := '{{ ranking }}',
        in_comp    := '{{ name_comp }}',
        in_seasons := ARRAY['{{ season }}'],
        first_week := 1,
        last_week  := {{ week }})
)
SELECT *,
    dense_rank() over(
        order by cast("{{ ranking }}" as int) desc
    )::text as "{{ ranking }} Ranking"
FROM stats
    ORDER BY "{{ ranking }}" DESC;