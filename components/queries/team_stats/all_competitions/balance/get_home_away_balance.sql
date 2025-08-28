with sums as (
    select
        case when grouping(season) = 1 then 'All' else season end as "Season",
        competition as "Competition",

        sum(home_win) as "Home Wins",
        sum(home_draw) as "Draws",
        sum(away_win) as "Away Wins",

        sum(case when played_home then home_score end) as "Home Goals",
        sum(case when not played_home then away_score end) as "Away Goals",

        sum(case when played_home then home_y_cards end) as "Home Yellow Cards",
        sum(case when not played_home then away_y_cards end) as "Away Yellow Cards",

        sum(case when played_home then home_yr_cards end) as "Home 2nd Yellow Cards",
        sum(case when not played_home then away_yr_cards end) as "Away 2nd Yellow Cards",

        sum(case when played_home then home_r_cards end) as "Home Red Cards",
        sum(case when not played_home then away_r_cards end) as "Away Red Cards",

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
    "Away Goals",
    case
        when "Home Goals" + "Away Goals" = 0
        then 0
        else "Home Goals" / ("Home Goals" + "Away Goals")::numeric
    end as "% Home Goals",
    "Home Goals" + "Away Goals" as "Total Goals",
    case
        when "Home Goals" + "Away Goals" = 0
        then 0
        else "Away Goals" / ("Home Goals" + "Away Goals")::numeric
    end as "% Away Goals",

    "Home Yellow Cards",
    "Away Yellow Cards",
    case
        when "Home Yellow Cards" + "Away Yellow Cards" = 0
        then 0
        else "Home Yellow Cards" / ("Home Yellow Cards" + "Away Yellow Cards")::numeric
    end "% Home Yellow Cards",
    case
        when "Home Yellow Cards" + "Away Yellow Cards" = 0
        then 0
        else "Away Yellow Cards" / ("Home Yellow Cards" + "Away Yellow Cards")::numeric
    end "% Away Yellow Cards",
    "Home Yellow Cards" + "Away Yellow Cards" as "Total Yellow Cards",

    "Home 2nd Yellow Cards",
    "Away 2nd Yellow Cards",
    case
        when "Home 2nd Yellow Cards" + "Away 2nd Yellow Cards" = 0
        then 0
        else "Home 2nd Yellow Cards" / ("Home 2nd Yellow Cards" + "Away 2nd Yellow Cards")::numeric
    end as "% Home 2nd Yellow Cards",
    case
        when "Home 2nd Yellow Cards" + "Away 2nd Yellow Cards" = 0
        then 0
        else "Away 2nd Yellow Cards" / ("Home 2nd Yellow Cards" + "Away 2nd Yellow Cards")::numeric
    end as "% Away 2nd Yellow Cards",
    "Home 2nd Yellow Cards" + "Away 2nd Yellow Cards" as "Total 2nd Yellow Cards",

    "Home Red Cards",
    "Away Red Cards",
    case
        when "Home Red Cards" + "Away Red Cards" = 0
        then 0
        else "Home Red Cards" / ("Home Red Cards" + "Away Red Cards")::numeric
    end as "% Home Red Cards",
    case
        when "Home Red Cards" + "Away Red Cards" = 0
        then 0
        else "Away Red Cards" / ("Home Red Cards" + "Away Red Cards")::numeric
    end as "% Away Red Cards",
    "Home Red Cards" + "Away Red Cards" as "Total Red Cards",

    "Matches"
from sums
;