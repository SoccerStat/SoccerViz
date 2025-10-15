with matches as (
	select
	    c1.name as "Club",
	    c2.name as "Opponent",
	    played_home,
	    case
	        when played_home
	        then case
	            when home_win = 1
	            then 'Won'
	            when home_draw = 1
	            then 'Drew'
	            when home_lose = 1
	            then 'Lost'
	        end
	        else case
	            when away_win = 1
	            then 'Won'
	            when away_draw = 1
	            then 'Drew'
	            when away_lose = 1
	            then 'Lost'
	        end
	    end as "Result"
	from analytics.staging_teams_performance stp
	join upper.club c1
	on stp.id_team = stp.id_comp || '_' || c1.id
	join upper.club c2
	on stp.id_opponent = stp.id_comp || '_' || c2.id
	where competition = '{{ name_comp }}'
	and season = '{{ season }}'
	and week = '{{ week }}'
),
stats as (
    SELECT
        "Club",
        {{ week }} as "Week",
        "Ranking" as "Global Ranking",
        "Stat" as "{{ ranking }}",
        round("Stat"::numeric / {{ week }}::numeric, 2) as "{{ ranking }}/Match"
    FROM analytics.one_teams_ranking (
        in_ranking := '{{ ranking }}',
        in_comp    := '{{ name_comp }}',
        in_seasons := ARRAY['{{ season }}'],
        first_week := 1,
        last_week  := {{ week }}
    )
)
SELECT
    s.*,
    m."Opponent",
    case when m.played_home then 'Home' else 'Away' end as "Side",
    m."Result",
    dense_rank() over(
        order by cast("{{ ranking }}" as int) desc
    )::text as "{{ ranking }} Ranking"
FROM stats s
JOIN matches m
ON s."Club" = m."Club"
ORDER BY "{{ ranking }}" DESC;