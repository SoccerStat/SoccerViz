select p.name, sum(n_r_cards) as "R", sum(n_y_cards) as "Y"
from (
    SELECT
        id_player,
        home_y_cards + away_y_cards as n_y_cards,
        home_yr_cards + away_yr_cards as n_yr_cards,
        home_r_cards + away_r_cards as n_r_cards
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
order by "R" desc, "Y" desc, p.name;