with teamA as (
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
teamB as (
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
all_selected_matches as (
    {% if teamA in side %}
    select *
    from teamA
    {% elif teamB in side %}
    select *
    from teamB
    {% else %}
    select
        a."Competition",
        a."Club" || ' - ' || b."Club"         as "Face-to-Face",
        a."Matches"       + b."Matches"       as "Matches",
        a."Wins"          + b."Loses"         as "Wins_A",
        a."Draws"         + b."Draws"         as "Draws",
        a."Loses"         + b."Wins"          as "Wins_B",
        a."Goals For"     + b."Goals Against" as "Goals_A",
        a."Goals Against" + b."Goals For"     as "Goals_B"
    from teamA a
    join teamB b
    on a."Club" = b."Opponent"
    and a."Opponent" = b."Club"
    and a."Competition" = b."Competition"
    {% endif %}
)
select *
from all_selected_matches