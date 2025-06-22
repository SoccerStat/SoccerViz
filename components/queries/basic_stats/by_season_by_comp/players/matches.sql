select p.name, count(*)
from (SELECT DISTINCT *
      FROM analytics.staging_players_performance
) as spp
left join upper.player p
on spp.id_player = p.id
where competition = '{{ name_comp }}'
and season IN ({{ seasons_ids | join(', ') }})
group by p.name
order by count(*) desc, p.name;