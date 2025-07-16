SELECT
    name as "Player",
    birth_date as "Birthday",
    birth_country as "Birth country",
    nationalities as "Nationalities",
    EXTRACT(YEAR FROM AGE(current_date, birth_date)) as "Age"
FROM upper.player p
left join (select player, array_agg(country) as nationalities from upper.player_nationality group by player) pn
on p.id = pn.player
WHERE extract(month from birth_date) = extract(month from current_date)
and extract(day from birth_date) = extract(day from current_date)
order by birth_date desc;