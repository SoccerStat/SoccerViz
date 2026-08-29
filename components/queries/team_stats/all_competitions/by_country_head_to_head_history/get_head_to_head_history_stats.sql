with home AS (
    select
        "Competition",
        "Team" AS "Club",
        "Opponent",
        "Matches",
        "Wins",
        "Draws",
        "Loses",
        "Goals For",
        "Goals Against"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        ARRAY[{{ comps }}],
        '{{ team }}',
        'home'
    )
    WHERE "Opponent Country" = '{{ country }}'
),
away AS (
    select
        "Competition",
        "Team" AS "Club",
        "Opponent",
        "Matches",
        "Wins",
        "Draws",
        "Loses",
        "Goals For",
        "Goals Against"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        ARRAY[{{ comps }}],
        '{{ team }}',
        'away'
    )
    WHERE "Opponent Country" = '{{ country }}'
),
neutral AS (
    select
        "Competition",
        "Team" || ' - ' || "Opponent" AS "Face-to-Face",
        "Matches",
        "Wins" AS "Wins Team",
        "Draws",
        "Loses" AS "Wins Opponent",
        "Goals For" AS "Goals Team",
        "Goals Against" AS "Goals Opponent"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ team }}',
        'neutral'
    )
    WHERE "Opponent Country" = '{{ country }}'
),
both_sides AS (
    select
        h."Competition",
        h."Club" || ' - ' || a."Opponent"     AS "Face-to-Face",
        h."Matches"       + a."Matches"       AS "Matches",
        h."Wins"          + a."Loses"         AS "Wins Team",
        h."Draws"         + a."Draws"         AS "Draws",
        h."Loses"         + a."Wins"          AS "Wins Opponent",
        h."Goals For"     + a."Goals Against" AS "Goals Team",
        h."Goals Against" + a."Goals For"     AS "Goals Opponent"
    FROM home h
    JOIN away a
    ON h."Club" = a."Club"
    AND h."Opponent" = a."Opponent"
    AND h."Competition" = a."Competition"
),
all_matches AS (
    select
        "Competition",
        "Team" || ' - ' || "Opponent" AS "Face-to-Face",
        "Matches",
        "Wins" AS "Wins Team",
        "Draws",
        "Loses" AS "Wins Opponent",
        "Goals For" AS "Goals Team",
        "Goals Against" AS "Goals Opponent"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ team }}',
        'all'
    )
    WHERE "Opponent Country" = '{{ country }}'
),
selected_matches AS (
    {%- if 'home' in side %}
    SELECT *
    FROM home
    {%- elif 'away' in side %}
    SELECT *
    FROM away
    {%- elif side == 'Neutral' %}
    SELECT *
    FROM neutral
    {%- elif side == 'Both' %}
    SELECT *
    FROM both_sides
    {%- else %}
    SELECT *
    FROM all_matches
    {%- endif %}
)
SELECT *
FROM selected_matches;