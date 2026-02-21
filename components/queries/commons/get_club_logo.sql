SELECT logo, similarity(unaccent(name), unaccent('{{ club_name }}')) + similarity(unaccent(city), unaccent('{{ club_name }}')) as similarity
FROM upper.club_logo
where similarity(unaccent(name), unaccent('{{ club_name }}')) > 0.1 or similarity(unaccent(city), unaccent('{{ club_name }}')) > 0.1
order by 1 desc
limit 1;