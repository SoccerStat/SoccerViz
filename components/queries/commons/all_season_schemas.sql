SELECT "Schema"
FROM analytics.get_season_schemas()
WHERE "Schema" >= 'season_{{ threshold_season }}'
ORDER BY "Schema" desc