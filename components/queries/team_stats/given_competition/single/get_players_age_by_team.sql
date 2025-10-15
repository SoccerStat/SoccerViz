with total_matches_minutes_by_team as (
    select mi."Club", ma."Stat" as "Matches", mi."Stat" as "Minutes"
    from analytics.one_teams_ranking(
        in_ranking := 'Minutes',
        in_comp := '{{ name_comp }}',
        in_seasons := array['{{ season }}'],
        side := 'all'
    ) mi
    join analytics.one_teams_ranking(
        in_ranking := 'Matches',
        in_comp := '{{ name_comp }}',
        in_seasons := array['{{ season }}'],
        side := 'all'
    ) ma
    on mi."Club" = ma."Club"
),
players_performance as (
    select
        id_team,
        split_part(id_team, '_', -1) as id_club,
        id_player,
        home_match,
        away_match,
        home_minutes,
        away_minutes
    from analytics.staging_players_performance
    where competition = '{{ name_comp }}'
    and season = '{{ season }}'
),
club as (
    select id, name
    from upper.club
    where name in (select "Club" from total_matches_minutes_by_team)
),
player_stats as (
    select
        c.name as "Club",
        pp.id_player,
        p.name,
        analytics.get_player_age('{{ season }}', p.birth_date) as age,
        sum(home_match) + sum(away_match) as matches,
        sum(home_minutes) + sum(away_minutes) as minutes
    from players_performance pp
    join upper.player p
    on pp.id_player = p.id || '_' || pp.id_team
    join club c
    on pp.id_club = c.id
    group by c.name, pp.id_player, p.name, p.birth_date
),
total_players_by_team as (
    select "Club", count(*) as "Total number of players used"
    from player_stats
    group by "Club"
)
select
    ps."Club",
    ps.name as "Player",
    ps.age as "Age",
    ps.matches as "Matches",
    ps.minutes as "Minutes",
    round(ps.minutes::numeric / tmot."Minutes"::numeric, {{ r }}) as "% of minutes played",
    round(ps.matches::numeric / tmot."Matches"::numeric, {{ r }}) as "% of matches played",
    tmot."Minutes" as "Total Minutes played by the whole team",
    tp."Total number of players used"
from player_stats ps
join total_matches_minutes_by_team tmot
on ps."Club" = tmot."Club"
join total_players_by_team tp
on ps."Club" = tp."Club";