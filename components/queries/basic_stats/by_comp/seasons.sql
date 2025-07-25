SELECT DISTINCT season
FROM analytics.staging_teams_performance
WHERE season >= '2000_2001'
{% if name_comp not in ("All Competitions", None) %}
AND competition = '{{ name_comp }}'
{% endif %}
GROUP BY season
ORDER BY season DESC;