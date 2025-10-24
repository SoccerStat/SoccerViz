WITH chps AS (
    SELECT name as "Competition"
    from upper.championship c
)
SELECT chps."Competition", rk.*
FROM chps
CROSS JOIN LATERAL (
	SELECT
		"Club",
		"Matches",
		"Wins",
		"Draws",
		"Loses",
		"Goals For",
		"Goals Against",
		"Goals Diff",
		"Points"
	FROM analytics.overall_teams_ranking(chps."Competition", ARRAY['{{ season }}'])
	LIMIT 1
) rk
ORDER BY chps."Competition", rk."Points" DESC;