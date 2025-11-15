with goals as (
	select stp.id_match, stp."date", case when stp.id_team = e.team then 'Team' else 'Opponent' end as team_scorer, e.timestamp, e.notes
	from analytics.staging_teams_performance stp
	join season_2025_2026."event" e
	on stp.id_match = e.match and (e.team = stp.id_team or e.team = stp.id_opponent)
	where season >= '2023-2024'
	and competition = 'Ligue 1'
	and id_team like '%b3072e00%'
	and e.outcome = 'goal'
	order by stp.date, e."timestamp"
),
team as (
	select *, case
		when timestamp like '45+%' then '1st half - ET'
		when timestamp like '90+%' then '2nd half - ET'
		when cast(timestamp as int) <= 15 then '<= 15'
		when cast(timestamp as int) <= 30 then '[16; 30]'
		when cast(timestamp as int) <= 45 then '[31; 45]'
		when cast(timestamp as int) <= 60 then '[46; 60]'
		when cast(timestamp as int) <= 75 then '[61; 75]'
		when cast(timestamp as int) <= 90 then '[76; 90]'
		else timestamp
	end as period
	from goals
	where team_scorer = 'Team'
),
opponent as (
	select *, case
		when timestamp like '45+%' then '1st half - ET'
		when timestamp like '90+%' then '2nd half - ET'
		when cast(timestamp as int) <= 15 then '<= 15'
		when cast(timestamp as int) <= 30 then '[16; 30]'
		when cast(timestamp as int) <= 45 then '[31; 45]'
		when cast(timestamp as int) <= 60 then '[46; 60]'
		when cast(timestamp as int) <= 75 then '[61; 75]'
		when cast(timestamp as int) <= 90 then '[76; 90]'
		else timestamp
	end as period
	from goals
	where team_scorer = 'Opponent'
)
select 'Team' as "Scorer", period, count(*)
from team
group by period
union all
select 'Opponent' as "Scorer", period, count(*)
from opponent
group by period
order by period, "Scorer" desc