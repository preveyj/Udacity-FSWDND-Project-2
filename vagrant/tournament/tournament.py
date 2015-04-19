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
    	cur.execute("DELETE FROM tbl_matches")
    	cur.close()
    	conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("DELETE FROM tbl_players")
		cur.close()
		conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    if conn != None:
    	cur = conn.cursor()
    	cur.execute("SELECT COUNT(*) FROM tbl_players")
    	return cur.fetchone()[0]
    	cur.close()
    	conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
	conn = connect()
	if conn != None:
		cur = conn.cursor()
		cur.execute("INSERT INTO tbl_players (name) values (%(theName)s);", {"theName", name})
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
		for record in cur:
			results.append({record.winner_id, record.name, record.wins, record.matchcount})
		
		cur.close()
		conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    conn = connect()
    if conn != None:
    	cur = conn.cursor()
    	cur.execute("INSERT INTO tbl_Matches (winner_id, loser_id, result) values (%s, %s, true);", {winner, loser})
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


