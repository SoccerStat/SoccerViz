select p.name, sum(n_goals_for) as "For"
from (
    SELECT
        id_player,
        home_goals + away_goals as n_goals_for
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
order by "For" desc, p.name;