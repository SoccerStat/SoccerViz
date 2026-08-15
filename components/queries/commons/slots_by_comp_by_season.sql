SELECT DISTINCT extract(isodow from date), time, trim(to_char(date, 'Day')) || ' ' || LEFT(time::text, 5) as "Slot"
FROM analytics.staging_teams_performance stp
WHERE season = any(
    ARRAY[
        {%- for season in seasons -%}
        '{{ season }}'{% if not loop.last %}, {% endif %}
    {%- endfor -%}
    ]
)
{% if name_comp.lower() not in ['all', 'all competitions'] %}
AND competition = '{{ name_comp }}'
{% endif %}
ORDER BY EXTRACT(ISODOW FROM date), time;