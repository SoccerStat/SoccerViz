select distinct
    p.name as "Player",
    p.birth_country as "Birth country",
    c.name as "Club",
    EXTRACT(YEAR FROM AGE(current_date, p.birth_date)) as "Age"
from {{ season_schema }}.team_player tp
left join upper.player p
on tp.player = p.id
left join {{ season_schema }}.team t
on tp.team = t.id
left join upper.club c
on t.club = c.id
where extract(month from birth_date) = extract(month from current_date)
and extract(day from birth_date) = extract(day from current_date)
order by "Age";