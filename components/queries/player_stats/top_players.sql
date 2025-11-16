SELECT "Player", "Club", "Matches" as "M", "Involved Matches" as "Inv. M", coalesce("Stat", 0) as "{{ ranking }}"
FROM analytics.one_players_ranking(
    in_ranking := '{{ ranking }}',
    in_comps := array['{{ comp }}'],
    in_seasons := array['{{ season }}'],
    group_clubs := {{ group_clubs }},
    group_competitions := {{ group_competitions }},
)
ORDER BY "Stat" DESC, "Matches" ASC;