select c.name, count(*)
from analytics.staging_teams_performance stp
left join upper.club c
on stp.id_team = stp.id_comp || '_' || c.id
where competition = '{{ name_comp }}'
and season IN ({{ seasons_ids | join(', ') }})
group by c.name
ORDER BY count(*) desc, c.name;