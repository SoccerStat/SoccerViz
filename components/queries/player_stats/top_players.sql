SELECT "Player",
    "Club",
    "Competition",
    --"Season",
    "Matches" as "M",
    "Involved Matches" as "Inv. M",
    coalesce("Stat", 0) as "{{ ranking }}"
FROM analytics.one_players_ranking(
    in_ranking := '{{ ranking }}',
    in_comps := array['{{ comp }}'],
    in_seasons := array['{{ season }}'],
    group_by_club := {{ group_by_club }},
    group_by_competition := {{ group_by_competition }},
    group_by_season := {{ group_by_season }}
)
ORDER BY "Stat" DESC, "Matches" ASC;