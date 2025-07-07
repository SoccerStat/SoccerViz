SELECT date_trunc('day', {{ date_column }}) AS {{ date_column }}, count(*) AS "{{ in_tab }}_count"
FROM {{ in_season }}.{{ in_tab }}
GROUP BY date_trunc('day', {{ date_column }});