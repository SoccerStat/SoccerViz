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
    select
        id_comp,
        id_team,
        id_player,
        array_cat(home_positions, away_positions) as positions,
        home_match,
        away_match
    from analytics.staging_players_performance
    where season = '{{ chosen_season }}'
),
players_positions as (
	select id_comp, id_team, split_part(id_team, '_', -1) as id_club, id_player, unnest(positions) as position
	from players_performance
),
positions_freq as (
	select id_club, id_player, position, count(*) as freq
	from players_positions
	group by id_club, id_player, position
	order by id_player, freq desc
),
most_played_positions as (
	select id_club, id_player, position
	from (
		select
			id_club,
			id_player,
			position,
			freq,
			ROW_NUMBER() OVER (PARTITION BY id_club, id_player ORDER BY freq DESC) AS rnk
		from positions_freq
	) ppe
	where rnk <= 2
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
        sum(home_match) + sum(away_match) as matches
    from players_performance pp
    join upper.player p
    on pp.id_player = p.id
    join club c
    on pp.id_team = pp.id_comp || '_' || c.id
    group by pp.id_player, p.name, p.birth_date
),
total_players as (
    select count(*) as "Total number of players used"
    from player_stats
)
select
    ps.name as "Player",
    array_agg(distinct mpp.position) as "Positions",
    ps.age as "Age",
    ps.matches as "Matches",
    tmot."Matches" as "Total number of matches",
    tp."Total number of players used"
from player_stats ps
join most_played_positions mpp
on ps.id_player = mpp.id_player
join total_matches_of_team tmot
on true
join total_players tp
on true
group by ps.name, ps.age, ps.matches, tmot."Matches", tp."Total number of players used"
order by "Matches" desc;