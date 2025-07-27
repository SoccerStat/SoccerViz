select
    case when played_home then h.name else a.name end as "Club",
    {{ week }} as "Partition",
    se.id,
    se.match,
    e.outcome,
    e.timestamp,
    e.played_home,
    se.xg_shot
from season_{{ season }}.match m
join upper.championship chp
on m.competition = chp.id
join upper.club h
on m.home_team = m.competition || '_' || h.id
join upper.club a
on m.away_team = m.competition || '_' || a.id
join season_{{ season }}.event e
on m.id = e.match
join season_{{ season }}.shot_event se
on e.match = se.match and e.id = se.id
where chp.name = '{{ name_comp }}'
and cast(week as int) between 1 and {{ week }}
--and m.id = '15ee650c';
