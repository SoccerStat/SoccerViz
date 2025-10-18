WITH matches AS (
    SELECT
        club.name as "Club",
        id_match as "Match",
        round as "Round",
        week as "Week",
        date as "Date",
        TO_CHAR(time::time, 'HH24:MI') as "Time",
        TRIM(
            CASE
                WHEN played_home THEN club.name || ' ' || repeat('🟥', MAX(stp.home_r_cards) OVER(PARTITION BY id_match))
                ELSE opponent.name || ' ' || repeat('🟥', MAX(stp.home_r_cards) OVER(PARTITION BY id_match))
            END
        ) AS "Home Team",
        CASE
            WHEN extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            THEN home_score || '-' || away_score || ' (ET)'
            WHEN not extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            THEN home_score || '-' || away_score
            WHEN home_penalty_shootout_scored is not null and away_penalty_shootout_scored is not null
            THEN home_score || '-' || away_score || ' (' || home_penalty_shootout_scored || '-' || away_penalty_shootout_scored || ')'
        END AS "Score",
        TRIM(
            CASE
                WHEN played_home THEN opponent.name || ' ' || repeat('🟥', MAX(stp.away_r_cards) OVER(PARTITION BY id_match))
                ELSE club.name || ' ' || repeat('🟥', MAX(stp.away_r_cards) OVER(PARTITION BY id_match))
            END
        ) AS "Away Team",
        CASE
            WHEN played_home
            THEN home_manager
            ELSE away_manager
        END AS "Manager",
        CASE
            WHEN home_penalty_shootout_scored is null
                and away_penalty_shootout_scored is null
                and home_score = away_score THEN '⚫️'
            WHEN played_home THEN
                CASE
                    WHEN home_penalty_shootout_scored is null
                        and away_penalty_shootout_scored is null
                        and home_score > away_score THEN '🟢'
                    WHEN home_penalty_shootout_scored is not null
                        and away_penalty_shootout_scored is not null
                        and home_penalty_shootout_scored > away_penalty_shootout_scored THEN '🟢'
                    ELSE '🔴'
                END
            WHEN not played_home THEN
                CASE
                    WHEN home_penalty_shootout_scored is null
                        and away_penalty_shootout_scored is null
                        and home_score > away_score THEN '🔴'
                    WHEN home_penalty_shootout_scored is not null
                        and away_penalty_shootout_scored is not null
                        and home_penalty_shootout_scored > away_penalty_shootout_scored THEN '🔴'
                    ELSE '🟢'
                END
        END AS "Outcome"
    FROM analytics.staging_teams_performance stp
    JOIN upper.club club
    ON stp.id_team = stp.id_comp || '_' || club.id
    JOIN upper.club opponent
    ON stp.id_opponent = stp.id_comp || '_' || opponent.id
    WHERE competition = '{{ name_comp }}'
    AND season = '{{ season }}'
    AND (
        {%- if kind_comp == 'C_CUP' -%}
        week is null or {{- " " }}
        {%- endif -%}
        cast(week as int) between {{ first_week }} and {{ last_week -}}
    )
    AND date between '{{ first_date }}' and '{{ last_date }}'
    AND (
        cardinality(ARRAY[{{ day_slots }}]::text[]) = 0
        OR TRIM(TO_CHAR(date, 'Day')) = ANY(ARRAY[{{ day_slots }}]::text[])
    )
    AND (
        cardinality(ARRAY[{{ time_slots }}]::text[]) = 0
        OR LEFT(stp.time::text, 5) = ANY(ARRAY[{{ time_slots }}]::text[])
    )
    AND CASE
        WHEN '{{ in_side }}' = 'home' THEN played_home and (round is null or round != 'Final')
        WHEN '{{ in_side }}' = 'away' THEN not played_home and (round is null or round != 'Final')
        WHEN '{{ in_side }}' = 'both' THEN (round is null or round != 'Final')
        WHEN '{{ in_side }}' = 'neutral' THEN round = 'Final'
        ELSE TRUE
    END
)
SELECT
    "Match",
    "Round",
    "Week",
    "Date",
    "Time",
    "Home Team",
    "Score",
    "Away Team",
    "Manager",
    "Outcome"
FROM matches
WHERE "Club" = '{{ name_team }}'
ORDER BY "Date";