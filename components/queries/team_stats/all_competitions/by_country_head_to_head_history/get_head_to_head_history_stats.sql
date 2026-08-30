with home AS (
    select
        "Competition",
        "Opponent",
        "Matches",
        "Wins" AS "Wins {{ team }}",
        "Draws",
        "Loses" AS "Wins Opponent",
        "Goals For" AS "Goals {{ team }}",
        "Goals Against" AS "Goals Opponent"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        ARRAY[{{ comps }}],
        '{{ team }}',
        'home'
    )
    WHERE "Opponent Country" = '{{ country }}' AND "Competition" != 'All'
),
away AS (
    select
        "Competition",
        "Opponent",
        "Matches",
        "Wins" AS "Wins {{ team }}",
        "Draws",
        "Loses" AS "Wins Opponent",
        "Goals For" AS "Goals {{ team }}",
        "Goals Against" AS "Goals Opponent"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        ARRAY[{{ comps }}],
        '{{ team }}',
        'away'
    )
    WHERE "Opponent Country" = '{{ country }}' AND "Competition" != 'All'
),
neutral AS (
    select
        "Competition",
        "Opponent",
        "Matches",
        "Wins" AS "Wins {{ team }}",
        "Draws",
        "Loses" AS "Wins Opponent",
        "Goals For" AS "Goals {{ team }}",
        "Goals Against" AS "Goals Opponent"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ team }}',
        'neutral'
    )
    WHERE "Opponent Country" = '{{ country }}' AND "Competition" != 'All'
),
both_sides AS (
    select
        h."Competition",
        h."Opponent",
        h."Matches"          + a."Matches"          AS "Matches",
        h."Wins {{ team }}"  + a."Wins {{ team }}"  AS "Wins {{ team }}",
        h."Draws"            + a."Draws"            AS "Draws",
        h."Wins Opponent"    + a."Wins Opponent"    AS "Wins Opponent",
        h."Goals {{ team }}" + a."Goals {{ team }}" AS "Goals {{ team }}",
        h."Goals Opponent"   + a."Goals Opponent"   AS "Goals Opponent"
    FROM home h
    JOIN away a
    ON h."Opponent" = a."Opponent"
    AND h."Competition" = a."Competition"
),
all_matches AS (
    select
        "Competition",
        "Opponent",
        "Matches",
        "Wins" AS "Wins {{ team }}",
        "Draws",
        "Loses" AS "Wins Opponent",
        "Goals For" AS "Goals {{ team }}",
        "Goals Against" AS "Goals Opponent"
    FROM analytics.teams_oppositions(
        ARRAY[{{ seasons }}],
        array[{{ comps }}],
        '{{ team }}',
        'all'
    )
    WHERE "Opponent Country" = '{{ country }}' AND "Competition" != 'All'
),
selected_matches AS (
    SELECT
        "Opponent",
        "Competition",
        "Matches",
        "Wins {{ team }}",
        "Draws",
        "Wins Opponent",
        "Goals {{ team }}",
        "Goals Opponent"
    {%- if 'home' in side %}
    FROM home
    {%- elif 'away' in side %}
    FROM away
    {%- elif side == 'Neutral' %}
    FROM neutral
    {%- elif side == 'Both' %}
    FROM both_sides
    {%- else %}
    FROM all_matches
    {%- endif %}
)
SELECT
    CASE WHEN GROUPING("Opponent") = 1 THEN 'ALL' ELSE "Opponent" END AS "Opponent",
    CASE WHEN GROUPING("Competition") = 1 THEN 'ALL' ELSE "Competition" END AS "Competition",
    SUM("Matches") AS "Matches",
    SUM("Wins {{ team }}") AS "Wins {{ team }}",
    SUM("Draws") AS "Draws",
    SUM("Wins Opponent") AS "Wins Opponent",
    SUM("Goals {{ team }}") AS "Goals {{ team }}",
    SUM("Goals Opponent") AS "Goals Opponent"
FROM selected_matches
GROUP BY GROUPING SETS (("Opponent", "Competition"), ("Competition"), ())
ORDER BY "Opponent", "Competition";