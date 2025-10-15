WITH spp AS (
    SELECT id_player,
        SUM(home_minutes + away_minutes) AS "Minutes",
        SUM(home_match + away_match) AS "Matches"
    FROM analytics.staging_players_performance
    WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND {{- " " }}
    {%- endif -%}
    season IN ({{ seasons_ids | join(', ') }})
    GROUP BY id_player
)
SELECT p.name, "Matches", "Minutes"/90 as "Min/90"
FROM spp
LEFT JOIN upper.player p
ON spp.id_player = p.id
ORDER BY "Matches" DESC, "Min/90" DESC, p.name;