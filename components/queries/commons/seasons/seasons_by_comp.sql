SELECT DISTINCT season as "Season"
FROM analytics.staging_teams_performance
WHERE season >= '{{ threshold_season }}'
{%- if name_comp.lower() not in ("all", "all competitions", None) -%}
    {{ " " -}} AND competition = '{{ name_comp }}'
{% endif -%}
GROUP BY season
ORDER BY season DESC;