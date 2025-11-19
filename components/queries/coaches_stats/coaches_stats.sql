select
    "Coach",
    "Club",
    "Competition",
    --"Season",
    "Matches",
    "Points",
    "Points/Match",
    "Wins",
    "Draws",
    "Loses",
    "% Wins",
    "% Loses",
    "Goals For",
    "Goals Against",
    "Goals Diff",
    "Clean Sheets"
from analytics.all_coaches_rankings(
    in_comps := array['{{ comp }}'],
    in_seasons := array['{{ season }}'],
    side := '{{ side }}',
    group_by_club := {{ group_by_club }},
    group_by_competition := {{ group_by_competition }},
    group_by_season := {{ group_by_season }}
)
order by "Points" desc, "Goals Diff" desc, "Goals For" desc;