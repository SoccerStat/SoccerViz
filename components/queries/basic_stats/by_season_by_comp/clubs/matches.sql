select c.name, count(*) as "Matches"
from (
    select id_comp, id_team
    from analytics.staging_teams_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' and
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
) as stp
left join upper.club c
on stp.id_team = stp.id_comp || '_' || c.id
group by c.name
ORDER BY "Matches" desc, c.name;