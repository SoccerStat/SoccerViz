with upper_data as (
    select
        {% if frequency == 'hourly' %}
        date_trunc('hour', {{ date_column }})
        {% elif frequency == 'daily' %}
        date_trunc('day', {{ date_column }})
        {% elif frequency == 'weekly' %}
        date_trunc('week', {{ date_column }})
        {% elif frequency == 'monthly' %}
        date_trunc('month', {{ date_column }})
        {% endif %}
        AS "{{ date_column }}"
    FROM upper.{{ in_tab }}
)
SELECT
    "{{ date_column }}",
    count(*) AS "{{ in_tab }}_count"
FROM upper_data
GROUP BY "{{ date_column }}";