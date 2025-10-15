with global_teams_ranking as (
    SELECT
        "Club",
        "Ranking"
    FROM analytics.one_teams_ranking(
        in_ranking := 'Points',
        in_comp := '{{ name_comp }}',
        in_seasons := ARRAY['{{ season }}']
    )
)
select "Club"
from global_teams_ranking
where cast("Ranking" as int) > (select count(distinct "Club") from global_teams_ranking)-3