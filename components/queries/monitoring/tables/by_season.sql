SELECT {% if in_tab != 'team_player' %}id, competition{% else %}team, player{% endif %}, {{ date_column }}
FROM {{ in_season }}.{{ in_tab }}
WHERE date_trunc('day', {{ date_column }}) BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
ORDER BY {{ date_column }} DESC;