SELECT "Player", "Matches" as "M", "Involved Matches" as "Inv. M", coalesce("Stat", 0) as "{{ ranking }}"
FROM analytics.one_players_ranking(
    in_ranking := '{{ ranking }}',
    in_comps := array['{{ comp }}'],
    in_seasons := array['{{ season }}'],
    group_competitions := 'ALL' = ANY(ARRAY[upper('{{ comp }}')])
)
ORDER BY "Stat" DESC, "Matches" ASC;