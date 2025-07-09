SELECT
    "Club",
    "Ranking",
    "Stat" as "{{ ranking }}"
FROM analytics.one_teams_ranking('{{ ranking }}', '{{ name_comp }}', ARRAY['{{ season }}'])
ORDER BY "{{ ranking }}" DESC;