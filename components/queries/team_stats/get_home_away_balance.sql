select
    competition as "Competition",
    sum(home_win) as "Home Wins",
    sum(home_draw) as "Draws",
    sum(away_win) as "Away Wins",
    sum(case when played_home then home_score end) as "Home Goals",
    0 as "Draws Goals",
    sum(case when not played_home then away_score end) as "Away Goals",
    sum(home_match) as "Matches"
from analytics.staging_teams_performance stp
where date >= '2000-01-01'
group by "Competition";