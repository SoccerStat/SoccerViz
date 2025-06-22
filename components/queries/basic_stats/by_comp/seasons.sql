SELECT DISTINCT season
FROM analytics.staging_teams_performance
{% if name_comp != "All Competitions" %}
WHERE competition = '{{ name_comp }}'
{% endif %}
GROUP BY season;