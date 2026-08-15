SELECT player,
    SUM(home_goals + away_goals) AS "Goals"
FROM analytics.staging_players_performance
WHERE
    {%- if name_comp != "All Competitions" -%}
        {{ " " -}} competition = '{{ name_comp }}' AND
    {%- endif -%}
    {{- " " }} season IN ({{ seasons_ids | join(', ') }})
GROUP BY player
ORDER BY "Goals" DESC, player
LIMIT 100;