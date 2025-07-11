select
    c.name as "Club",
    COUNT(*) AS "Matches",
    SUM(points) AS "Points"
FROM (
    SELECT id_comp, id_team, home_points + away_points AS points
    FROM analytics.staging_teams_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' AND
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
) AS stp
LEFT JOIN upper.club c
ON stp.id_team = stp.id_comp || '_' || c.id
GROUP BY c.name
ORDER BY "Matches" DESC, "Points" DESC, c.name;