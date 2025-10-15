select
    c.name as "Club",
    sum(n_wins) as "W",
    sum(n_draws) as "D",
    sum(n_loses) as "L"
from (
    select
        id_comp,
        id_team,
        home_win + away_win as n_wins,
        home_draw + away_draw as n_draws,
        home_lose + away_lose as n_loses
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
ORDER BY "W" desc, "D" desc, "L" asc, c.name;