WITH spp AS (
    SELECT id_player,
        SUM(home_win + away_win) AS "W",
         SUM(home_draw + away_draw) AS "D",
          SUM(home_lose + away_lose) AS "L"
    FROM analytics.staging_players_performance
    WHERE
    {% if name_comp != "All Competitions" %}
    competition = '{{ name_comp }}' AND
    {% endif %}
    season IN ({{ seasons_ids | join(', ') }})
    GROUP BY id_player
)
SELECT p.name, "W", "D", "L"
FROM spp
LEFT JOIN upper.player p
ON spp.id_player = p.id
ORDER BY "W" DESC, "D" DESC, "L" DESC, p.name;