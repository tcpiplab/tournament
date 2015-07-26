#!/usr/bin/env python
# 
# Luke Sheppard
# lshep.usc[(at)]gmail.com
# Project 2 of the Fullstack Nanodegree at Udacity.
# July 25, 2015
#
# tournament.py -- implementation of a Swiss-system tournament
#
# This script will store the win/lose outcomes of game matches between pairs of players and generate pairings for Swiss-System tournaments. See README.txt for prerequisites, build, and run instructions


import sys
import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM matches")
    DB.commit()
    cursor.close()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM playernames")
    DB.commit()
    cursor.close()
    DB.close()


def showPlayers():
    """Returns a list of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT id, name FROM playernames")
    player_list = cursor.fetchall()
    cursor.close()
    DB.close()
    print('ID  Name') 
    print('--  ------------------')
    for row in player_list:
        for item in row:
            if str(item).isdigit():
                sys.stdout.write(str(item) + '  ')
            else:
                print(item)


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT COUNT(id) FROM playernames")
    thecount = cursor.fetchall()
    count =    thecount[0][0]
    cursor.close()
    DB.close()
    return count


def registerPlayer(newname):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

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

    DB = connect()
    cursor = DB.cursor()
    query = """ SELECT    playernames.id, name, 
                COUNT(CASE playernames.id WHEN winner THEN 1 ELSE NULL END) AS wins, 
                COUNT(match_id) AS matches
                FROM      playernames 
                          LEFT JOIN matches ON playernames.id IN (winner, loser)
                GROUP BY  playernames.id, name
                ORDER BY wins DESC"""
    cursor.execute(query)
    id_name_wins_matches = cursor.fetchall()
    count =    id_name_wins_matches[0][0]
    # [(38, 'Melpomene Murray', 3L, 4L), (40, 'Clark Kent', 1L, 1L), (39, 'Randy Schwartz', 1L, 5L), (41, 'Jimmy Carter', 0L, 0L)]
    cursor.close()
    DB.close()
    return id_name_wins_matches


def showPlayerStandings():
    """Prints a list of players standings."""
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
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser) )
    DB.commit()
    cursor.close()
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

    swiss_pairings = []
    this_pair = ()
    thestandings = playerStandings()
    col = 0
    players = 0
    for row in thestandings:
        for item in row:
            if col == 0:
                the_id = str(item)
                col += 1
            elif col == 1:
                the_name = item
                col += 1
                pass
            elif col == 2:
                col += 1
                pass
            else:
                col = 0
                players += 1
                if players == 1:
                    this_pair = this_pair + (int(the_id), the_name)
                    #swiss_pairings.append(this_pair)
                elif players == 2:
                    this_pair = this_pair + (int(the_id), the_name)
                    swiss_pairings.append(this_pair)
                    this_pair = ()
                    players = 0
    return swiss_pairings


def showSwissPairings():
    """ Generate and print out the next round of Swiss pairings """
    pairings = swissPairings()
    print('\n')
    for row in pairings:
        print(row)
    

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
