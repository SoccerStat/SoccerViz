WITH spp AS (
    SELECT player,
        SUM(home_minutes + away_minutes) AS "Minutes",
        SUM(home_match + away_match) AS "Matches"
    FROM analytics.staging_players_performance
    WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND
    {%- endif -%}
    {{- " " }} season IN ({{ seasons_ids | join(', ') }})
    GROUP BY player
)
SELECT player, "Matches", "Minutes"/90 as "Min/90"
FROM spp
ORDER BY "Matches" DESC, "Min/90" DESC, player
LIMIT 100;