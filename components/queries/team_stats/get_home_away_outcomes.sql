select
    competition as "Competition",
    sum(home_win) as "Home Wins",
    sum(home_draw) as "Draws",
    sum(away_win) as "Away Wins"
from analytics.staging_teams_performance stp
where date >= '2000-01-01'
group by "Competition";