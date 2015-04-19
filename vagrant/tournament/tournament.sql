-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

/*
dependency tree:

tbl_tournaments
	vw_current_tournament
	tbl_players
	tbl_matches
		vw_opponents
		vw_wincount
			vw_rankings
		vw_opponents
		

*/
\c tournament;
drop view if exists vw_rankings;
drop view if exists vw_opponents;
drop view if exists vw_wincount;
drop view if exists vw_current_tournament;
drop table if exists tbl_matches;
drop table if exists tbl_players;
drop table if exists tbl_tournaments;
\c template1
drop database if exists tournament;

create database tournament;
\c tournament;

--tbl_players table
create table tbl_players (
	id serial primary key,
	name varchar(255) not null
);
	
--tbl_matches table
CREATE TABLE tbl_matches (
    id serial primary key,
    winner_id integer NOT NULL,
    loser_id integer NOT NULL,
    result boolean NOT NULL
);

--if true: player 1 wins
--if false: tie
			
--to record a 'bye': mark the skipped player as winner against loser_id = 0
--to select who gets the 'bye': select the player with the least wins who
--has not yet had a 'bye' match
--	select top 1 id
--	from players left outer join matches on players.id = matches.loser_id
--	order by count(matches.loser_id) desc
		
--vw_wincount view:
create view vw_wincount as
	select tbl_players.id as winner_id, coalesce(count(matches.winner_id), 0) as wins 
	from tbl_players left outer join (
		select winner_id, loser_id, result
		from tbl_matches
		where result = true
	) as matches on tbl_players.id = matches.winner_id
	group by tbl_players.id 
	order by wins desc;

--vw_opponents
create view vw_opponents as
	select distinct a, b 
	from (
		select winner_id as a, loser_id as b 
		from tbl_matches
		union 
		select loser_id as a, winner_id as b 
		from tbl_matches
	) 
	as opponents 
	order by a, b;


--vw_rankings
create view vw_rankings as
select wins.winner_id, tbl_players.name, wins.wins, sum(omw.wins) as omw, (coalesce(won_matches.wincount,0) + coalesce(losses.losscount,0)) as matchcount
from vw_wincount as wins inner join vw_opponents on wins.winner_id = vw_opponents.a
inner join vw_wincount as omw on vw_opponents.b = omw.winner_id
inner join tbl_players on wins.winner_id = tbl_players.id
left outer join (
	select tbl_matches.winner_id, count(tbl_matches.winner_id) as wincount 
	from tbl_matches
	where loser_id > 0
	group by tbl_matches.winner_id
) as won_matches on wins.winner_id = won_matches.winner_id 
left outer join (
	select tbl_matches.loser_id, count(tbl_matches.loser_id) as losscount 
	from tbl_matches
	group by tbl_matches.loser_id
) as losses on wins.winner_id = losses.loser_id
group by wins.winner_id, tbl_players.id, wins.wins, matchcount 
order by wins.wins desc, omw desc;

/*

select tbl_players.id, tbl_players.name, (coalesce(wins.wincount,0) + coalesce(losses.losscount,0)) as matchcount
from tbl_players left outer join (
	select tbl_matches.winner_id, count(tbl_matches.winner_id) as wincount 
	from tbl_matches 
	where loser_id > 0
	group by tbl_matches.winner_id
) as wins on tbl_players.id = wins.winner_id 
left outer join (
	select tbl_matches.loser_id, count(tbl_matches.loser_id) as losscount 
	from tbl_matches 
	group by tbl_matches.loser_id
) as losses on tbl_players.id = losses.loser_id;

*/