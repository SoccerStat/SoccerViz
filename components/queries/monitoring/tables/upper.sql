SELECT id, name, {{ date_column }}
FROM upper.{{ in_tab }}
WHERE date_trunc('day', {{ date_column }}) BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
ORDER BY {{ date_column }} DESC;