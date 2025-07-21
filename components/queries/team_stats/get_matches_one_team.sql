SELECT
    round as "Round",
    week as "Week",
    date as "Date",
    CASE
        WHEN played_home THEN opponent.name
        ELSE club.name
    END AS "Home Team",
    home_score || '-' || away_score AS "Score",
    CASE
        WHEN not played_home THEN club.name
        ELSE opponent.name
    END AS "Away Team",
    CASE
        WHEN played_home THEN
            CASE
                WHEN home_score > away_score THEN 'W'
                WHEN home_score = away_score THEN 'D'
                ELSE 'L'
            END
        ELSE
            CASE
                WHEN home_score < away_score THEN 'L'
                WHEN home_score = away_score THEN 'D'
                ELSE 'W'
            END
    END AS "Outcome"
FROM analytics.staging_teams_performance stp
JOIN upper.club club
ON stp.id_team = stp.id_comp || '_' || club.id AND club.name = '{{ name_team }}'
JOIN upper.club opponent
ON stp.id_opponent = stp.id_comp || '_' || opponent.id
WHERE competition = '{{ name_comp }}'
AND season = '{{ season }}'
AND (
    {% if kind_comp == 'C_CUP' %}
    week is null
    or
    {% endif %}
    cast(week as int) between {{ first_week }} and {{ last_week }}
)
AND date between '{{ first_date }}' and '{{ last_date }}'
AND CASE
    WHEN '{{ in_side }}' = 'home' THEN played_home and (round is null or round != 'Final')
    WHEN '{{ in_side }}' = 'away' THEN not played_home and (round is null or round != 'Final')
    WHEN '{{ in_side }}' = 'both' THEN (round is null or round != 'Final')
    WHEN '{{ in_side }}' = 'neutral' THEN round = 'Final'
    ELSE TRUE
END
ORDER BY date;