select
    c.name as "Club",
    sum(n_goals_for) as "For",
    sum(n_goals_against) as "Against",
    sum(n_goals_for) - sum(n_goals_against) as "Diff"
from (
    select
        id_comp,
        id_team,
        home_goals_for + away_goals_for as n_goals_for,
        home_goals_against + away_goals_against as n_goals_against
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
ORDER BY "For" desc, "Against" desc, c.name;