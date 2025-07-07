SELECT schema_name
FROM information_schema.schemata
WHERE schema_name LIKE 'season_%%'
AND EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = schema_name
      AND table_name = 'match'
)
ORDER BY schema_name desc