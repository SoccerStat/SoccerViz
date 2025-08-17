with stats as (
    SELECT
        "Club",
        '{{ season }}' as "Season",
        "Ranking" as "Global Ranking",
        "Stat" as "{{ ranking }}"
    FROM analytics.one_teams_ranking(
        in_ranking := '{{ ranking }}',
        in_comp    := '{{ name_comp }}',
        in_seasons := ARRAY['{{ season }}']
    )
)
select
    *,
    dense_rank() over(
        order by cast("{{ ranking }}" as int) desc
    )::text as "{{ ranking }} Ranking"
from stats
ORDER BY "Season", "{{ ranking }}" desc;