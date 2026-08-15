SELECT
    player,
    SUM(home_y_cards + away_y_cards) AS "Y",
    SUM(home_yr_cards + away_yr_cards) AS "YR",
    SUM(home_r_cards + away_r_cards) AS "R"
FROM analytics.staging_players_performance
WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND
    {%- endif -%}
    {{- " " }} season IN ({{ seasons_ids | join(', ') }})
GROUP BY player
ORDER BY "R" DESC, "Y" DESC, player
LIMIT 100;