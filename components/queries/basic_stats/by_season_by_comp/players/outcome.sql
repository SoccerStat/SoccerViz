select p.name, sum(n_wins) as "W", sum(n_draws) as "D", sum(n_loses) as "L"
from (
    SELECT
        id_player,
        home_win + away_win as n_wins,
        home_draw + away_draw as n_draws,
        home_lose + away_lose as n_loses
    FROM analytics.staging_players_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' and
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
) as spp
left join upper.player p
on spp.id_player = p.id
group by p.name
order by "W" desc, "D" desc, "L" asc, p.name;