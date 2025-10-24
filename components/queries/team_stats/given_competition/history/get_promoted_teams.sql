with teams_current_season as (
	select chp.name as "Competition", cl.name as "Club"
	from season_{{ current_season }}.team t
	join upper.club cl
	on t.club = cl.id
	join upper.championship chp
	on t.competition = chp.id
),
teams_previous_season as (
	select chp.name as "Competition", cl.name as "Club"
	from season_{{ previous_season }}.team t
	join upper.club cl
	on t.club = cl.id
	join upper.championship chp
	on t.competition = chp.id
)
select "Competition", t."Club"
from teams_current_season t
where t."Club" not in (select "Club" from teams_previous_season)
order by "Competition", "Club";