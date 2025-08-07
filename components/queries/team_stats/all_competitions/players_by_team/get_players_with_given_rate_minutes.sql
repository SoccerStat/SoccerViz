with total_matches_of_team as (
    select sum("Matches") as "Matches"
    from analytics.all_teams_rankings(
        in_comp := 'all',
        in_seasons := array['{{ chosen_season }}'],
        side := 'all'
    )
    where "Club" = '{{ name_team }}'
),
players_performance as (
    select id_comp, id_team, id_player, home_match, away_match
    from analytics.staging_players_performance
    where season = '{{ chosen_season }}'
),
club as (
    select id
    from upper.club
    where name = '{{ name_team }}'
),
player_stats as (
    select
        p.name,
        COALESCE(
            EXTRACT(
                EPOCH FROM AGE(
                    CASE
                        WHEN '{{ chosen_season }}' = (
                          CASE
                            WHEN current_date < TO_DATE(EXTRACT(YEAR FROM current_date)::text || '-07-01', 'YYYY-MM-DD')
                            THEN (EXTRACT(YEAR FROM current_date) - 1)::text || '_' || EXTRACT(YEAR FROM current_date)::text
                            ELSE EXTRACT(YEAR FROM current_date)::text || '_' || (EXTRACT(YEAR FROM current_date) + 1)::text
                          END
                        )
                        THEN current_date
                        ELSE TO_DATE(split_part('{{ chosen_season }}', '_', 2) || '-06-30', 'YYYY-MM-DD')
                    END,
                    p.birth_date
                )
            ) / (365.25 * 24 * 60 * 60),
            0.0
        ) as "Age",
        sum(home_match) + sum(away_match) as "Matches"
    from players_performance pp
    join upper.player p
    on pp.id_player = p.id
    join club c
    on pp.id_team = pp.id_comp || '_' || c.id
    group by p.name, p.birth_date
),
total_players as (
    select count(*) as "Total number of players used"
    from player_stats
)
select
    ps.name as "Player",
    ps."Age",
    ps."Matches",
    tmot."Matches" as "Total number of matches",
    tp."Total number of players used"
from player_stats ps
join total_matches_of_team tmot
on true
join total_players tp
on true
order by "Matches" desc;