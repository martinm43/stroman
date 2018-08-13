-- retrieves most current team ratings in database
select t.id,t.mlbgames_name,t.abbreviation,t.league,t.division,s.rating from teams as t
inner join SRS_Ratings as s
on s.team_id=t.id
where s.rating <> 0
and s.rating_date = (select rating_date from SRS_ratings order by rating_date desc limit 1)
