with total_minutes_of_team as (
    select "Minutes"
    from analytics.all_teams_rankings(
        in_comp := '{{ chosen_comp }}',
        in_seasons := array['{{ chosen_season }}'],
        side := '{{ in_side }}'
    )
    where "Club" = '{{ name_team }}'
),
team_players as (
    select
        team,
        player,
        array_agg(distinct pos) as positions,
        array_agg(distinct grp) as position_groups
    from season_{{ chosen_season }}.team_player tp
    CROSS JOIN LATERAL unnest(positions) AS pos
    CROSS JOIN LATERAL unnest(position_groups) AS grp
    group by team, player
),
players_performance as (
    select
        id_comp,
        id_team,
        id_player,
        array_cat(home_positions, away_positions) as positions,
        home_match,
        away_match,
        home_minutes,
        away_minutes,
        round
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
        pp.id_player,
        p.name,
        array(
            select distinct unnest(array_agg(tps.positions))
        ) as "Positions",
        array(
            select distinct unnest(array_agg(tps.position_groups))
        ) as "Position Groups",
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
        ) as age,
        analytics.set_bigint_stat(sum(home_match), sum(away_match), '{{ in_side }}') as matches,
        analytics.set_bigint_stat(sum(home_minutes), sum(away_minutes), '{{ in_side }}') as minutes
    from players_performance pp
    join upper.player p
    on pp.id_player = p.id
    join club c
    on pp.id_team = pp.id_comp || '_' || c.id
    left join team_players tps
    on pp.id_player = tps.player and pp.id_team = tps.team
    where case
        when '{{ in_side }}' = 'neutral' then (round = 'Final')
        when '{{ in_side }}' in ('home', 'away', 'both') then (round is null or round != 'Final')
        else true
    end
    group by pp.id_player, p.name, p.birth_date
),
total_players as (
    select count(*) as "Total number of players used"
    from player_stats
)
select
    ps.name as "Player",
    ps."Positions",
    ps."Position Groups",
    ps.age as "Age",
    ps.matches as "Matches",
    ps.minutes as "Minutes",
    round(ps.minutes::numeric / 90.0, {{ r }}) as "90s",
    round(ps.minutes::numeric / tmot."Minutes"::numeric, {{ r }}) as "% of minutes played",
    tp."Total number of players used"
from player_stats ps
join total_minutes_of_team tmot
on true
join total_players tp
on true
where ps.minutes >= (tmot."Minutes"::numeric * {{ rate }}/100)
--group by ps.name, ps.age, ps.matches, ps.minutes, tmot."Minutes", tp."Total number of players used", ps."Positions", ps."Position Groups"
order by "Minutes" desc, "Matches" desc;