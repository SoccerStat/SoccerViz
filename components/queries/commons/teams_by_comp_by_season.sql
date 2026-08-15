SELECT distinct c.name as "Club"
FROM analytics.staging_teams_performance stp
LEFT JOIN upper.club c
ON stp.id_team = stp.id_comp || '_' || c.id
WHERE season = any(
    ARRAY[
        {%- for season in seasons -%}
        '{{ season }}'{% if not loop.last %}, {% endif %}
    {%- endfor -%}
    ]
)
{%- if name_comp.lower() != 'all' -%}
    {{ " " -}} AND competition = '{{ name_comp }}'
{% endif %}