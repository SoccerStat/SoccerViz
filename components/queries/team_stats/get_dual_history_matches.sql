with teamA as (
    SELECT
        competition as "Competition",
        season as "Season",
        week as "Week",
        round as "Round",
        date || ' ' || time as "Date",
        club.name AS "Home Team",
        home_score || '-' || away_score AS "Score",
        opponent.name AS "Away Team",
        CASE
            WHEN home_score > away_score THEN 'W'
            WHEN home_score = away_score THEN 'D'
            ELSE 'L'
        END AS "Outcome"
    FROM analytics.staging_teams_performance stp
    JOIN upper.club club
    ON stp.id_team = stp.id_comp || '_' || club.id AND club.name = '{{ teamA }}'
    JOIN upper.club opponent
    ON stp.id_opponent = stp.id_comp || '_' || opponent.id AND opponent.name = '{{ teamB }}'
    WHERE played_home
),
teamB as (
    SELECT
        competition as "Competition",
        season as "Season",
        week as "Week",
        round as "Round",
        date || ' ' || time as "Date",
        club.name AS "Home Team",
        home_score || '-' || away_score AS "Score",
        opponent.name AS "Away Team",
        CASE
            WHEN home_score > away_score THEN 'W'
            WHEN home_score = away_score THEN 'D'
            ELSE 'L'
        END AS "Outcome"
    FROM analytics.staging_teams_performance stp
    JOIN upper.club club
    ON stp.id_team = stp.id_comp || '_' || club.id AND club.name = '{{ teamB }}'
    JOIN upper.club opponent
    ON stp.id_opponent = stp.id_comp || '_' || opponent.id AND opponent.name = '{{ teamA }}'
    WHERE played_home
),
all_selected_matches as (
    {% if teamA in side %}
    select *
    from teamA
    {% elif teamB in side %}
    select *
    from teamB
    {% else %}
    select *
    from teamA
    union all
    select *
    from teamB
    {% endif %}
)
select *
from all_selected_matches
order by "Date";