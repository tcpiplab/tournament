#!/usr/bin/env python
# 
# Luke Sheppard
# lshep.usc[(at)]gmail.com
# Project 2 of the Fullstack Nanodegree at Udacity.
# July 31, 2015
#
# tournament.py -- implementation of a Swiss-system tournament
#
# This script will store the win/lose outcomes of game matches between pairs of 
# players and generate pairings for Swiss-System tournaments. See the 
# accompanying README.txt file for prerequisites, build, and run instructions.

import sys
import psycopg2

class DB:
    def __init__(self, db_con_str="dbname=tournament"):
        """
        Creates a database connection with the connection string provided
        :param str db_con_str: Contains the database connection string, with a default value when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor();

    def execute(self, sql_query_string, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: Contain the query string to be executed
        :param bool and_close: If true, closes the database connection after executing and commiting the SQL Query
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string)
        if and_close:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # Call the connect() function from the psycopg2 module
    # Return a new connection object.
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Delete every row from the 'matches' database table.
    # But don't delete the table itself.
    DB().execute("DELETE FROM matches", True)



def deletePlayers():
    """Remove all the player records from the database."""
    # Delete every row from the 'playernames' database table.
    # But don't delete the table itself.
    DB().execute("DELETE FROM playernames", True)


def showPlayers():
    """Returns a list of players currently registered."""
    # Execute a SELECT query for the 'id' and 'name' columns
    # of the 'playernames' database table.
    # Print the results to stdout with a header.
    conn = DB().execute("SELECT id, name FROM playernames")
    cursor = conn["cursor"].fetchall()
    conn['conn'].close()
    print('ID  Name') 
    print('--  ------------------')
    for row in cursor:
        for item in row:
            if str(item).isdigit():
                sys.stdout.write(str(item) + '  ')
            else:
                print(item)


def countPlayers():
    """Returns the number of players currently registered."""
    # Execute a SELECT query for the 'id' column and count the rows.
    # Return the count as an integer.
    conn = DB().execute("SELECT COUNT(id) FROM playernames")
    cursor = conn["cursor"].fetchall()
    conn['conn'].close()
    return cursor[0][0]


def registerPlayer(newname):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Execute an INSERT query against the 'playernames' database table.
    # The required argument is a string.
    # The argument is formatted as a one-item list to prevent SQLi attacks.
    #
    # The DB() class defined above does not allow me to parameterize the values,
    # so I'm connecting manually.
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO playernames (name) VALUES (%s)", (newname,) )
    DB.commit()
    cursor.close()
    DB.close()


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
    # Execute a SELECT query against the 'id' and 'name' tables,
    # LEFT JOINed with the 'matches' table, counting id if the id 
    # appears in the 'winner' column of the 'matches' table.
    # Populate a tuple with lists of the form (id, name, wins, matches).
    # Return that tuple to the calling function.
    query = """ SELECT    playernames.id, name, 
                COUNT(CASE playernames.id WHEN winner THEN 1 ELSE NULL END) AS wins, 
                COUNT(match_id) AS matches
                FROM      playernames 
                          LEFT JOIN matches ON playernames.id IN (winner, loser)
                GROUP BY  playernames.id, name
                ORDER BY wins DESC"""
    conn = DB().execute(query)
    # populate a tuple of lists
    cursor = conn["cursor"].fetchall()
    # Example of the tuple of lists:
    # [(38, 'Melpomene Murray', 3L, 4L), (40, 'Clark Kent', 1L, 1L), (39, 'Randy Schwartz', 1L, 5L), (41, 'Jimmy Carter', 0L, 0L)]
    conn['conn'].close()
    return cursor


def showPlayerStandings():
    """Prints a list of players standings."""
    # Print a four-column header to stdout: id, name, wins, matches.
    # Iterate through the tuple returned by calling playerStandings(),
    # printing each list of the tuple as a row to stdout. 
    standings = playerStandings()    
    print('ID |        NAME        | WINS | MATCHES')
    print('--  --------------------  ----   -------')
    col = 0
    for row in standings:
        for item in row:
            if col == 0:
                sys.stdout.write(str(item) + '  ')
                col += 1
            elif col == 1:
                sys.stdout.write(item.ljust(22))
                col += 1
            elif col == 2:
                sys.stdout.write(str(item).rjust(1))
                col += 1
            else:
                print('      ' + str(item))
                col = 0

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Execute an INSERT query against the 'winner' and 'loser' columns
    # of the 'matches' database table.
    # The required arguments are strings of the numeric ids of the respective
    # winner and loser of the match.
    # The arguments are formatted as a two-item list of strings to prevent 
    # SQLi attacks. 
    #
    # The DB() class defined above does not allow me to parameterize the values,
    # so I'm connecting manually.
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser) )
    DB.commit()
    cursor.close()
    DB.close()
 
 
def showSwissPairings():
    """ Generate and print out the next round of Swiss pairings """
    # Call swissPairings() and print the tuple it returns.
    pairings = swissPairings()
    print('\n')
    for row in pairings:
        print(row)
   

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
    # Use the custom VIEW called "player_wins" to SELECT players' id and name, 
    # which have an equal number of wins, just once, to avoid repetition.
    # Self JOIN the view, SELECTing all the players and their wins, 
    # where the wins are equal ON a.wins = b.wins, with a progression of the 
    # player's id, to avoid repetition.
    # Return a tuple of lists:
    # [(id1, name1, id2, name2), (id3, name3, id4, name4)]

    query = """SELECT a.id, a.name, b.id, b.name 
                 FROM player_wins as a JOIN player_wins as b 
                 ON a.wins = b.wins WHERE a.id > b.id"""
    conn = DB().execute(query)
    # populate a tuple of lists
    cursor = conn["cursor"].fetchall()
    conn['conn'].close()
    return cursor


# only show the menu if invoked as a command line tool
if __name__ == '__main__':
  while 1:
    print("""

    1) Delete all matches.

    2) Delete all players.

    3) Show all Players.

    4) Add a player.

    5) Show player standings.

    6) Record the outcome of a match.

    7) Generate the next Swiss Pairings.

    8) Exit.

    """)
    selection = int(input('Select a menu item: '))
    if selection == 1:
        deleteMatches()
    elif selection == 2:
        deletePlayers()
    elif selection == 3:
        showPlayers()
    elif selection == 4:
        newname = raw_input('New name: ')
        registerPlayer(newname)
    elif selection == 5:
        showPlayerStandings()
    elif selection == 6:
        showPlayers()
        print('\n')
        winner = raw_input('ID of the winner: ')
        loser = raw_input('ID of the loser: ')
        reportMatch(winner, loser)
    elif selection == 7:
        showSwissPairings()
    elif selection == 8:
        exit()
