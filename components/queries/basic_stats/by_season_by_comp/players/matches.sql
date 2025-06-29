select p.name, count(*) as "Matches"
from (
    SELECT id_player
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
order by "Matches" desc, p.name;