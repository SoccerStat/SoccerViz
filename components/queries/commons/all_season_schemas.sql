SELECT "Schema"
FROM analytics.get_season_schemas()
WHERE "Schema" >= 'season_2000_2001'
ORDER BY "Schema" desc