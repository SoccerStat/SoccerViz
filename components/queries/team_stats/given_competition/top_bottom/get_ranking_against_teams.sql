select
    "Team" as "Club",
    "Opponent",
    "Matches",
    "Wins",
    "Draws",
    "Loses",
    "Goals For",
    "Goals Against"
from analytics.teams_oppositions(
    ARRAY['{{ season }}'],
    array['{{ name_comp }}'],
    '{{ name_team }}',
    '{{ side }}'
)
where "Opponent" = any(array[{{ opponents }}]);