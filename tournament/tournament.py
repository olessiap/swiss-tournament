#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    #DB = psycopg2.connect("dbname=tournament")
    #cursor = DB.cursor()
    return psycopg2.connect("dbname=tournament")

def deleteMatches(): #1
    """Remove all the match records from the database."""
    #connect to DB
    DB = connect()
    #wipe matches table
    cursor = DB.cursor()
    cursor.execute("TRUNCATE TABLE matches;")
    #commit changes and close DB connection
    DB.commit()
    DB.close()

def deletePlayers(): #2
    """Remove all the player records from the database."""
    DB = connect()
    #delete players
    cursor = DB.cursor()
    cursor.execute ("TRUNCATE TABLE players CASCADE;")
    DB.commit()
    DB.close()

def countPlayers(): #3
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("select count(*) from players;")
    #fetch results
    results = cursor.fetchone()
    DB.close()
    #force return 0 value
    if not results:
        return 0
    else:
        return int(results[0])

def registerPlayer(name): #4
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (bleach.clean(name),)) #for protection ;)
    DB.commit()
    DB.close()


def playerStandings(): #5 left join to show empty rows too
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns: #4 columns
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT * from standings;")
    standings = cursor.fetchall()
    DB.commit()
    DB.close()
    return standings

def reportMatch(winner, loser): #6
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);", (winner, loser))
    DB.commit()
    DB.close()


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
    DB = connect()
    #get current list of players from standings view
    standings = playerStandings()
    #print standings
    cursor = DB.cursor()
    cursor.execute("SELECT COUNT(*) FROM standings;")
    #return a players list of tuples
    results = cursor.fetchall()
    # select only player info from standings view
    player = [item[0:2] for item in standings]
    index = 0
    pairings = []
    # loop through each row and pair players
    for row in results:
        while (index < row[0]):
            pair = player[index] + player[index+1]
            pairings.append(pair) # add pair to tuple list
            #print pairings
            index = index + 2
    DB.close()
    return pairings
