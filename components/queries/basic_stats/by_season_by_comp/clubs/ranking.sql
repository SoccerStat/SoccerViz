SELECT
    "Club",
    "Matches",
    "Points",
    "Goals For" AS "For",
    "Goals Against" AS "Against",
    "Red Cards" AS "R",
    "Yellow Cards" AS "Y",
    "Wins" AS "W",
    "Draws" AS "D",
    "Loses" AS "L"
FROM analytics.teams_rankings('{{ name_comp }}', ARRAY[{{ seasons_ids | join(', ')}}]);