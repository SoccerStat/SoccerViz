SELECT "Player", "Matches", "Stat" as "{{ ranking }}"
FROM analytics.one_players_ranking('{{ ranking }}', array['{{ comp }}'], array['{{ season }}'])
WHERE case
	when 'ALL' = ANY(ARRAY['{{ comp }}'])
	then "Competition" = 'ALL'
	else "Competition" != 'ALL'
end
AND "Club" = 'ALL'
ORDER BY "Stat" DESC;