select
    "Coach",
    "Matches",
    "Points",
    "Points/Match",
    "Wins",
    "Draws",
    "Loses"
    "% Wins",
    "% Loses",
    "Goals For",
    "Goals Against",
    "Goals Diff",
    "Clean Sheets"
from analytics.all_coaches_rankings(
    in_comps := array['{{ comp }}'],
    in_seasons := array['{{ season }}'],
    group_clubs := {{ group_clubs }},
    group_competitions := {{ group_competitions }},
);