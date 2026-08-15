SELECT player,
    SUM(home_win + away_win) AS "W",
     SUM(home_draw + away_draw) AS "D",
     SUM(home_lose + away_lose) AS "L"
FROM analytics.staging_players_performance
WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND
    {%- endif -%}
    {{- " " }} season IN ({{ seasons_ids | join(', ') }})
GROUP BY player
ORDER BY "W" DESC, "D" DESC, "L" DESC, player
LIMIT 100;