SELECT
    {% if in_tab == 'team_player' %}
    team, player
    {% elif in_tab == 'team' %}
    id, competition
    {% elif in_tab == 'match' %}
    id, competition, round, week
    {% endif %},
    {{ date_column }}
FROM {{ in_season }}.{{ in_tab }}
WHERE
    date_trunc('day', {{ date_column }})
    BETWEEN CURRENT_DATE - INTERVAL
    {% if frequency == 'hours' %}
    '48 hours'
    {% elif frequency == 'days' %}
    '7 days'
    {% elif frequency == 'weeks' %}
    '4 weeks'
    {% elif frequency == 'months' %}
    '3 months'
    {% endif %}
     AND CURRENT_DATE
ORDER BY {{ date_column }} DESC;