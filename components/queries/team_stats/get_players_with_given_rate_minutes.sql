with total_minutes_of_team as (
    select "Minutes"
    from analytics.all_teams_rankings(
        in_comp := '{{ chosen_comp }}',
        in_seasons := array['{{ chosen_season }}'],
        side := '{{ in_side }}'
    )
    where "Club" = '{{ name_team }}'
),
club as (
    select id
    from upper.club
    where name = '{{ name_team }}'
),
player_stats as (
    select
        p.name,
        analytics.set_bigint_stat(sum(home_minutes), sum(away_minutes), '{{ in_side }}') as "Minutes",
        analytics.set_bigint_stat(sum(home_match), sum(home_match), '{{ in_side }}') as "Matches"
    from analytics.staging_players_performance pp
    join upper.player p
    on pp.id_player = p.id
    join club c
    on pp.id_team = pp.id_comp || '_' || c.id
    where competition = '{{ chosen_comp }}'
    and season = '{{ chosen_season }}'
    group by p.name
),
total_players as (
    select count(*) as "Total number of players used"
    from player_stats
)
select
    ps.name as "Player",
    ps."Minutes",
    "Matches",
    round(ps."Minutes"::numeric/tmot."Minutes"::numeric, 3) as "% of minutes played",
    tp."Total number of players used"
from player_stats ps
join total_minutes_of_team tmot
on true
join total_players tp
on true
where ps."Minutes" >= (tmot."Minutes"::numeric * {{ rate }}/100)
order by "Minutes" desc, "Matches" desc;