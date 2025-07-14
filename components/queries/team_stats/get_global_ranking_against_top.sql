with global_teams_ranking as (
    SELECT
        "Club",
        "Ranking",
        "Stat" as "{{ ranking }}"
    FROM analytics.one_teams_ranking(
        in_ranking := '{{ ranking }}',
        in_comp := '{{ name_comp }}',
        in_seasons := ARRAY['2024_2025'])
    WHERE cast("Ranking" as int) <= 5
),
teams_performance as (
	SELECT *
	FROM analytics.staging_teams_performance stp
	WHERE season = '2024_2025'
	AND competition = '{{ name_comp }}'
)
select c1.name as "Team", c2.name as "Opponent", tp.week, tp.*
from teams_performance tp
LEFT JOIN upper.club c1
ON tp.id_team = tp.id_comp || '_' || c1.id
LEFT JOIN upper.club c2
ON tp.id_opponent = tp.id_comp || '_' || c2.id
JOIN global_teams_ranking tr
ON tr."Club" = c2.name
order by c1.name, cast(week as int)





-- select * from analytics.all_teams_rankings(in_comp := 'Premier League', in_seasons := array['2024_2025']) limit 5;
--
-- select * from analytics.teams_oppositions(array['2024_2025'], 'Premier League', 'Arsenal FC', 'both');
--
--
-- with global_teams_ranking as (
--     SELECT
--         "Club",
--         "Ranking"
--     FROM analytics.one_teams_ranking(
--         in_ranking := 'Points',
--         in_comp := 'Premier League',
--         in_seasons := ARRAY['2024_2025'])
--     WHERE cast("Ranking" as int) <= 5
-- )
-- SELECT t.team, f.*
-- FROM teams t,
-- LATERAL my_func(t.team) f;