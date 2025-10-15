SELECT distinct c.name as "Club"
FROM analytics.staging_teams_performance stp
LEFT JOIN upper.club c
ON stp.id_team = stp.id_comp || '_' || c.id
WHERE season = any(ARRAY[{{ seasons }}])
{%- if name_comp != 'all' -%}
    {{ " " -}} AND competition = '{{ name_comp }}'
{% endif %}