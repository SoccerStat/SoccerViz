SELECT date_trunc('day', {{ date_column }}) AS "{{ date_column }}", count(*) AS "{{ in_tab }}_count"
FROM upper.{{ in_tab }}
GROUP BY date_trunc('day', {{ date_column }});