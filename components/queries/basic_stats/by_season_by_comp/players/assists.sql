WITH spp AS (
    SELECT id_player,
     SUM(home_assists + away_assists) AS "Assists"
    FROM analytics.staging_players_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' AND
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
    GROUP BY id_player
)
SELECT p.name, "Assists"
FROM spp
LEFT JOIN upper.player p
ON spp.id_player = p.id
ORDER BY "Assists" DESC, p.name;