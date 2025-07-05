SELECT
    "Player",
    "Matches",
    "Minutes",
    "Wins" AS "W",
    "Draws" AS "D",
    "Loses" AS "L",
    "Goals",
    "Assists",
    "Red Cards" AS "R",
    "Yellow Cards" AS "Y"
FROM analytics.players_rankings('{{ name_comp }}', ARRAY[{{ seasons_ids | join(', ')}}]);