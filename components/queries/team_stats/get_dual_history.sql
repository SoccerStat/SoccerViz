with team_a as (
    SELECT
        "Competition",
        "Team" as "Club",
        "Opponent",
        "Matches",
        "Wins",
        "Draws",
        "Loses",
        "Goals For",
        "Goals Against"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ teamA }}',
        'home'
    )
    WHERE "Opponent" = '{{ teamB }}'
),
team_b as (
    SELECT
        "Competition",
        "Team" as "Club",
        "Opponent",
        "Matches",
        "Wins",
        "Draws",
        "Loses",
        "Goals For",
        "Goals Against"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ teamB }}',
        'home'
    )
    WHERE "Opponent" = '{{ teamA }}'
),
neutral as (
    SELECT
        "Competition",
        "Team" || ' - ' || "Opponent" as "Face-to-Face",
        "Matches",
        "Wins" as "Wins_A",
        "Draws",
        "Loses" as "Wins_B",
        "Goals For" as "Goals_A",
        "Goals Against" as "Goals_B"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ teamA }}',
        'neutral'
    )
    WHERE "Opponent" = '{{ teamB }}'
),
both_sides as (
    select
        a."Competition",
        a."Club" || ' - ' || b."Club"         as "Face-to-Face",
        a."Matches"       + b."Matches"       as "Matches",
        a."Wins"          + b."Loses"         as "Wins_A",
        a."Draws"         + b."Draws"         as "Draws",
        a."Loses"         + b."Wins"          as "Wins_B",
        a."Goals For"     + b."Goals Against" as "Goals_A",
        a."Goals Against" + b."Goals For"     as "Goals_B"
    from team_a a
    join team_b b
    on a."Club" = b."Opponent"
    and a."Opponent" = b."Club"
    and a."Competition" = b."Competition"
),
all_matches as (
    SELECT
        "Competition",
        "Team" || ' - ' || "Opponent" as "Face-to-Face",
        "Matches",
        "Wins" as "Wins_A",
        "Draws",
        "Loses" as "Wins_B",
        "Goals For" as "Goals_A",
        "Goals Against" as "Goals_B"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ teamA }}',
        'all'
    )
    WHERE "Opponent" = '{{ teamB }}'
)
,
selected_matches as (
    {% if teamA in side %}
    select *
    from team_a
    {% elif teamB in side %}
    select *
    from team_b
    {% elif side == 'Neutral' %}
    select *
    from neutral
    {% elif side == 'Both' %}
    select *
    from both_sides
    {% else %}
    select *
    from all_matches
    {% endif %}
)
select *
from selected_matches;