with total_minutes_of_team as (
    select "Minutes"
    from analytics.all_teams_rankings(
        in_comp := '{{ chosen_comp }}',
        in_seasons := array['{{ chosen_season }}'],
        side := '{{ in_side }}'
    )
    where "Club" = '{{ name_team }}'
),
players_performance as (
    select id_comp, id_team, id_player, home_match, away_match, home_minutes, away_minutes, round
    from analytics.staging_players_performance
    where competition = '{{ chosen_comp }}'
    and season = '{{ chosen_season }}'
),
club as (
    select id
    from upper.club
    where name = '{{ name_team }}'
),
player_stats as (
    select
        p.name,
        analytics.set_bigint_stat(sum(home_match), sum(away_match), '{{ in_side }}') as "Matches",
        analytics.set_bigint_stat(sum(home_minutes), sum(away_minutes), '{{ in_side }}') as "Minutes"
    from players_performance pp
    join upper.player p
    on pp.id_player = p.id
    join club c
    on pp.id_team = pp.id_comp || '_' || c.id
    where case
        when '{{ in_side }}' = 'neutral' then (round = 'Final')
        when '{{ in_side }}' in ('home', 'away', 'both') then (round is null or round != 'Final')
        else true
    end
    group by p.name
),
total_players as (
    select count(*) as "Total number of players used"
    from player_stats
)
select
    ps.name as "Player",
    ps."Matches",
    ps."Minutes",
    round(ps."Minutes"::numeric / 90.0, {{ r }}) as "90s",
    round(ps."Minutes"::numeric / tmot."Minutes"::numeric, {{ r }}) as "% of minutes played",
    tp."Total number of players used"
from player_stats ps
join total_minutes_of_team tmot
on true
join total_players tp
on true
where ps."Minutes" >= (tmot."Minutes"::numeric * {{ rate }}/100)
order by "Minutes" desc, "Matches" desc;