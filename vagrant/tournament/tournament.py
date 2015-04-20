#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# global connection object?

def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("TRUNCATE TABLE tbl_matches")
		conn.commit()
		cur.close()
		conn.close()


def deletePlayers():
	"""Remove all the player records from the database."""
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("TRUNCATE TABLE tbl_players")
		conn.commit()
		cur.close()
		conn.close()

def countPlayers():
	"""Returns the number of players currently registered."""
	playerCount = 0
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("SELECT COUNT(*) FROM tbl_players")
		playerCount = cur.fetchone()[0]
		cur.close()
		conn.close()
		""" print "Count of Players is " + str(playerCount) """
	
	return playerCount


def registerPlayer(name):
	"""Adds a player to the tournament database.
  
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
  
	Args:
	  name: the player's full name (need not be unique).
	"""
	conn = connect()
	if conn != None:
		""" print "Now registering player """
		cur = conn.cursor()
		cur.execute("INSERT INTO tbl_players (name) values (%(theName)s);", {'theName': name})
		conn.commit()
		cur.close()
		conn.close()
	

def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	  A list of tuples, each of which contains (id, name, wins, matches):
		id: the player's unique id (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played
	"""
	results = []
	
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("SELECT winner_id, name, wins, matchcount FROM vw_rankings")
		
		if cur.rowcount == 0:
			cur.execute("SELECT id as winner_id, name, 0 as wins, 0 as matchcount FROM tbl_players")
			""" print cur """
		
		for record in cur:
			""" print record """
			""" results.append(("id": record[0], "name": record[1], "wins": record[2], "matches": record[3])) """
			results.append((record[0],record[1],record[2],record[3]))
		
		cur.close()
		conn.close()
	
	""" 
	print "playerStandings()"
	print results
	"""
	return results

def reportMatch(winner, loser, result = None):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	if result is None:
		result = True
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("INSERT INTO tbl_Matches (winner_id, loser_id, result) values (%s, %s, %s);", (winner, loser, result))
		conn.commit()
		cur.close()
		conn.close()
 
 
def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.
  
	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.
  
	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
		id1: the first player's unique id
		name1: the first player's name
		id2: the second player's unique id
		name2: the second player's name
	"""
	
	thePairings = []
	rankings = playerStandings()
	
	x = 0
	while x < len(rankings) :
		thePairings.append((rankings[x][0], rankings[x][1], rankings[x + 1][0], rankings[x + 1][1]))
		
		x = x + 2
		
	""" print thePairings """
	return thePairings
