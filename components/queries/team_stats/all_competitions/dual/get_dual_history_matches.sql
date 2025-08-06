with team_a as (
    SELECT
        competition as "Competition",
        season as "Season",
        week as "Week",
        round as "Round",
        date as "Date",
        club.name AS "Home Team",
        case
            when extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            then home_score || '-' || away_score || ' (ET)'
            when not extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            then home_score || '-' || away_score
            when home_penalty_shootout_scored is not null and away_penalty_shootout_scored is not null
            then home_score || '-' || away_score || ' (' || home_penalty_shootout_scored || '-' || away_penalty_shootout_scored || ')'
        end AS "Score",
        opponent.name AS "Away Team",
        CASE
            WHEN home_penalty_shootout_scored is null
                and away_penalty_shootout_scored is null
                and home_score > away_score THEN '🟢'
            WHEN home_penalty_shootout_scored is not null
                and away_penalty_shootout_scored is not null
                and home_penalty_shootout_scored > away_penalty_shootout_scored THEN '🟢'
            WHEN home_score = away_score
                and home_penalty_shootout_scored is null
                and away_penalty_shootout_scored is null THEN '⚫️'
            ELSE '🔴'
        END AS "Outcome for {{ teamA }}"
    FROM analytics.staging_teams_performance stp
    JOIN upper.club club
    ON stp.id_team = stp.id_comp || '_' || club.id AND club.name = '{{ teamA }}'
    JOIN upper.club opponent
    ON stp.id_opponent = stp.id_comp || '_' || opponent.id AND opponent.name = '{{ teamB }}'
    WHERE played_home and (round is null or round != 'Final') and date >= '2000-01-01'
),
team_b as (
    SELECT
        competition as "Competition",
        season as "Season",
        week as "Week",
        round as "Round",
        date as "Date",
        club.name AS "Home Team",
        case
            when extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            then home_score || '-' || away_score || '( ET)'
            when not extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            then home_score || '-' || away_score
            when home_penalty_shootout_scored is not null and away_penalty_shootout_scored is not null
            then home_score || '-' || away_score || ' (' || home_penalty_shootout_scored || '-' || away_penalty_shootout_scored || ')'
        end AS "Score",
        opponent.name AS "Away Team",
        CASE
            WHEN home_score < away_score THEN '🟢'
            WHEN home_penalty_shootout_scored is not null
                and away_penalty_shootout_scored is not null
                and home_penalty_shootout_scored < away_penalty_shootout_scored THEN '🟢'
            WHEN home_score = away_score
                and home_penalty_shootout_scored is null
                and away_penalty_shootout_scored is null THEN '⚫️'
            ELSE '🔴'
        END AS "Outcome for {{ teamA }}"
    FROM analytics.staging_teams_performance stp
    JOIN upper.club club
    ON stp.id_team = stp.id_comp || '_' || club.id AND club.name = '{{ teamB }}'
    JOIN upper.club opponent
    ON stp.id_opponent = stp.id_comp || '_' || opponent.id AND opponent.name = '{{ teamA }}'
    WHERE played_home and (round is null or round != 'Final') and date >= '2000-01-01'
),
neutral as (
    SELECT
        competition as "Competition",
        season as "Season",
        week as "Week",
        round as "Round",
        date as "Date",
        case
            when played_home
            then club.name
            else opponent.name
        end AS "Home Team",
        case
            when extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            then home_score || '-' || away_score || ' (ET)'
            when not extra_time and home_penalty_shootout_scored is null and away_penalty_shootout_scored is null
            then home_score || '-' || away_score
            when home_penalty_shootout_scored is not null and away_penalty_shootout_scored is not null
            then home_score || '-' || away_score || ' (' || home_penalty_shootout_scored || '-' || away_penalty_shootout_scored || ')'
        end AS "Score",
        case
            when played_home
            then opponent.name
            else club.name
        end AS "Away Team",
        CASE
            WHEN home_score = away_score
                and home_penalty_shootout_scored is null
                and away_penalty_shootout_scored is null
            THEN '⚫️'
            ELSE CASE
                WHEN played_home
                THEN CASE
                    WHEN home_penalty_shootout_scored is null
                        and away_penalty_shootout_scored is null
                        and home_score > away_score THEN '🟢'
                    WHEN home_penalty_shootout_scored is not null
                        and away_penalty_shootout_scored is not null
                        and home_penalty_shootout_scored > away_penalty_shootout_scored THEN '🟢'
                    ELSE '🔴'
                END
                ELSE CASE
                    WHEN home_penalty_shootout_scored is null
                        and away_penalty_shootout_scored is null
                        and home_score < away_score THEN '🟢'
                    WHEN home_penalty_shootout_scored is not null
                        and away_penalty_shootout_scored is not null
                        and home_penalty_shootout_scored < away_penalty_shootout_scored THEN '🟢'
                    ELSE '🔴'
                END
            END
        END AS "Outcome for {{ teamA }}"
    FROM analytics.staging_teams_performance stp
    JOIN upper.club club
    ON stp.id_team = stp.id_comp || '_' || club.id AND club.name = '{{ teamA }}'
    JOIN upper.club opponent
    ON stp.id_opponent = stp.id_comp || '_' || opponent.id AND opponent.name = '{{ teamB }}'
    WHERE round = 'Final' and date >= '2000-01-01'
),
selected_matches as (
    {% if teamA in side %}
    select *
    from team_a
    {% elif teamB in side %}
    select *
    from team_b
    {% elif side == 'Neutral' %}
    select *
    from neutral
    {% elif side == 'Both' %}
    select *
    from team_a
    union all
    select *
    from team_b
    {% else %}
    select *
    from team_a
    union all
    select *
    from team_b
    union all
    select *
    from neutral
    {% endif %}
)
select *
from selected_matches
order by "Date";