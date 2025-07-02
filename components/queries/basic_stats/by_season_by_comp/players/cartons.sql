WITH spp AS (
    SELECT id_player,
     SUM(home_y_cards + away_y_cards) AS "Y",
      SUM(home_r_cards + away_r_cards) AS "R"
    FROM analytics.staging_players_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' AND
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
    GROUP BY id_player
)
SELECT p.name, "R", "Y"
FROM spp
LEFT JOIN upper.player p
ON spp.id_player = p.id
ORDER BY "R" DESC, "Y" DESC, p.name;