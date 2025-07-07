SELECT DISTINCT season
FROM analytics.staging_teams_performance
{% if name_comp not in ("All Competitions", None) %}
WHERE competition = '{{ name_comp }}'
{% endif %}
GROUP BY season
ORDER BY season DESC;