SELECT
    player,
    SUM(home_assists + away_assists) AS "Assists"
FROM analytics.staging_players_performance
WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND
    {%- endif -%}
    {{- " " }} season IN ({{ seasons_ids | join(', ') }})
GROUP BY player
ORDER BY "Assists" DESC, player
LIMIT 100;