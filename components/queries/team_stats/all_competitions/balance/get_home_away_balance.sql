with sums as (
    select
        case when grouping(season) = 1 then 'All' else season end as "Season",
        competition as "Competition",
        sum(home_win) as "Home Wins",
        sum(home_draw) as "Draws",
        sum(away_win) as "Away Wins",
        sum(case when played_home then home_score end) as "Home Goals",
        sum(case when not played_home then away_score end) as "Away Goals",
        sum(home_match) as "Matches"
    from analytics.staging_teams_performance stp
    where season >= '2000-2001' and (round is null or round != 'Final')
    group by grouping sets((season, competition), (competition))
)
select
    "Season",
    "Competition",
    "Home Wins",
    "Draws",
    "Away Wins",
    "Home Goals",
    "Home Goals" / ("Home Goals" + "Away Goals")::numeric as "% Home Goals",
    "Home Goals" + "Away Goals" as "Total Goals",
    "Away Goals" / ("Home Goals" + "Away Goals")::numeric as "% Away Goals",
    "Away Goals",
    "Matches"
from sums
;