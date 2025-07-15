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
    seasons := ARRAY['{{ season }}'],
    comps := array['{{ name_comp }}'],
    team := '{{ name_team }}'
)
where "Opponent" = any(array[{{ opponents }}]);