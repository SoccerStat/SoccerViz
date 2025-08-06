SELECT distinct c.name as "Club"
FROM analytics.staging_teams_performance stp
left join upper.club c
on stp.id_team = stp.id_comp || '_' || c.id
where season = any(ARRAY[{{ seasons }}])
{% if name_comp != 'all' %}
AND competition = '{{ name_comp }}'
{% endif %}