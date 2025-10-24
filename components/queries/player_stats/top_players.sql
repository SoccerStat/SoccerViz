select p.name, analytics.set_bigint_stat(sum(home_goals), sum(away_goals), 'both') as "Goals"
from analytics.staging_players_performance spp
join upper.player p
on spp.id_player = p.id || '_' || spp.id_comp
where competition = 'Ligue 1'
and season = '2025_2026'
group by p.name
order by "Goals";