select g.id, g.away_team, ra.rating, g.home_team, rh.rating 
from games as g 
inner join srs_ratings as ra on ra.team_id=g.away_team 
inner join srs_ratings as rh on rh.team_id=g.home_team 
where g.scheduled_date >= datetime('now') 
and ra.rating_date = (select max(rating_date) from srs_ratings) 
and rh.rating_date = (select max(rating_date) from srs_ratings);
