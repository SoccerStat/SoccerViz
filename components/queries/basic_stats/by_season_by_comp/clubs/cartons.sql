select
    c.name as "Club",
    sum(n_r_cards) as "R",
    sum(n_y_cards) as "Y"
from (
    select
        id_comp,
        id_team,
        home_y_cards + away_y_cards as n_y_cards,
        home_yr_cards + away_yr_cards as n_yr_cards,
        home_r_cards + away_r_cards as n_r_cards
    from analytics.staging_teams_performance
    WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND {{- " " }}
    {%- endif -%}
    season IN ({{ seasons_ids | join(', ') }})
) as stp
left join upper.club c
on stp.id_team = stp.id_comp || '_' || c.id
group by c.name
ORDER BY "R" desc, "Y" desc, c.name;