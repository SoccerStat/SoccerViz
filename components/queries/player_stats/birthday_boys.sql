select distinct
    p.id as "Id",
    p.name as "Player",
    p.birth_country as "Birth country",
    EXTRACT(YEAR FROM AGE(current_date, p.birth_date)) as "Age",
    '{{ season }}' as "Season",
    c.name as "Club"
from season_{{ season }}.team_player tp
left join upper.player p
on tp.player = p.id
left join season_{{ season }}.team t
on tp.team = t.id
left join upper.club c
on t.club = c.id
where to_char(p.birth_date, 'MM-DD') = to_char(DATE '{{ date }}', 'MM-DD');