SELECT "Player", "Matches", coalesce("Stat", 0) as "{{ ranking }}"
FROM analytics.one_players_ranking('{{ ranking }}', array['{{ comp }}'], array['{{ season }}'])
WHERE case
	when 'ALL' = ANY(ARRAY[upper('{{ comp }}')])
	then "Competition" = 'ALL'
	else "Competition" != 'ALL'
end
AND "Club" = 'ALL'
ORDER BY "Stat" DESC;