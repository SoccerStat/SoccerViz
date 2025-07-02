WITH spp AS (
    SELECT id_player,
     SUM(home_goals + away_goals) AS "Goals"
    FROM analytics.staging_players_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' AND
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
    GROUP BY id_player
)
SELECT p.name, "Goals"
FROM spp
LEFT JOIN upper.player p
ON spp.id_player = p.id
ORDER BY "Goals" DESC, p.name;