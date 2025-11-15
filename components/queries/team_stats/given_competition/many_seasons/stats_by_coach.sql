	select case when stp.played_home then home_manager else away_manager end as manager,
		case when stp.played_home then stp.home_win else stp.away_win end as win,
		case when stp.played_home then stp.home_draw else stp.away_draw end as draw,
		case when stp.played_home then stp.home_lose else stp.away_lose end as lose,
		case when stp.played_home then stp.home_goals_for else stp.away_goals_for end as goals_for,
		case when stp.played_home then stp.home_goals_against else stp.away_goals_against end as goals_against,
		case when stp.played_home then stp.home_xg_for else stp.away_xg_for end as xg_for,
		case when stp.played_home then stp.home_xg_against else stp.away_xg_against end as xg_against,
		case when stp.played_home then stp.home_passes_succ else stp.away_passes_succ end as passes_succ,
		case when stp.played_home then stp.home_passes_total else stp.away_passes_total end as passes_total,
		case when stp.played_home then stp.home_clean_sheet else stp.away_clean_sheet end as clean_sheets_for,
		case when stp.played_home then case when stp.home_goals_for = 0 then 1 else 0 end else case when stp.away_goals_for = 0 then 1 else 0 end end as clean_sheets_against
	from analytics.staging_teams_performance stp
	where season >= '2023-2024'
	and competition = 'Ligue 1'
	and id_team like '%b3072e00%'
)
select
	manager,
	count(*) as matches,
	sum(win) as wins,
	sum(draw) as draws,
	sum(lose) as loses,
	round((3*sum(win) + sum(draw))::numeric / count(*), 2) as pts_per_match,
	round(sum(win)::numeric / count(*), 2) as prct_wins,
	round(sum(lose)::numeric / count(*), 2) as prct_loses,
	sum(clean_sheets_for) as clean_sheets_for,
	sum(clean_sheets_against) as clean_sheets_against,
	sum(goals_for) as goals_for,
	round(sum(goals_for)::numeric /count(*), 2) as goals_per_match_for,
	sum(goals_against) as goals_against,
	round(sum(goals_against)::numeric / count(*), 2) as goals_per_match_against,
	sum(goals_for) - sum(goals_against) as goals_diff,
	round(100*sum(passes_succ)::numeric / sum(passes_total), 2) as succ_passes_rate,
	sum(xg_for) as xg_for,
	sum(xg_against) as xg_against,
	sum(goals_for)::numeric - sum(xg_for) as perf_for,
	sum(goals_against)::numeric - sum(xg_against) as perf_against
from stats
where manager in ('Julien Stéphan', 'Habib Beye', 'Jorge Sampaoli')
group by manager
order by count(*) desc