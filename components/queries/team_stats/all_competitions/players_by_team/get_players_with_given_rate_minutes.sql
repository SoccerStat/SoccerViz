with total_matches_of_team as (
    select sum("Matches") as "Matches"
    from analytics.all_teams_rankings(
        in_comp := 'all',
        in_seasons := array['{{ chosen_season }}'],
        side := 'all'
    )
    where "Club" = '{{ name_team }}'
),
team_players as (
    select
        split_part(team, '_', -1) as id_club,
        player,
        array_agg(distinct pos) as positions,
        array_agg(distinct grp) as position_groups
    from season_{{ chosen_season }}.team_player tp
    CROSS JOIN LATERAL unnest(positions) AS pos
    CROSS JOIN LATERAL unnest(position_groups) AS grp
    group by id_club, player
),
players_performance as (
    select
        id_comp,
        id_team,
        id_player,
        --array_cat(home_positions, away_positions) as positions,
        array(
            select distinct number
            from unnest(ARRAY[home_number, away_number]) as number
            where number IS NOT NULL
        ) as numbers,
        home_match,
        away_match
    from analytics.staging_players_performance
    where season = '{{ chosen_season }}'
),
club as (
    select id
    from upper.club
    where name = '{{ name_team }}'
),
player_stats_and_positions as (
    select
        pp.id_player,
        p.name,
        array(
            select distinct unnest(array_agg(pp.numbers))
        ) as "Numbers",
        array(
            select distinct unnest(array_agg(tps.positions))
        ) as "Positions",
        array(
            select distinct unnest(array_agg(tps.position_groups))
        ) as "Position Groups",
        analytics.get_player_age('{{ chosen_season }}', p.birth_date) as age,
        sum(home_match) + sum(away_match) as matches
    from players_performance pp
    join upper.player p
    on pp.id_player = p.id
    join club c
    on pp.id_team = pp.id_comp || '_' || c.id
    left join team_players tps
    on pp.id_player = tps.player and pp.id_team = pp.id_comp || '_' || tps.id_club
    group by pp.id_player, p.name, p.birth_date
),
total_players as (
    select count(*) as "Total number of players used"
    from player_stats_and_positions
)
select
    ps.name as "Player",
    ps."Numbers",
    ps."Positions",
    ps."Position Groups",
    ps.age as "Age",
    ps.matches as "Matches",
    tmot."Matches" as "Total number of matches",
    tp."Total number of players used"
from player_stats_and_positions ps
join total_matches_of_team tmot
on true
join total_players tp
on true
order by "Matches" desc;