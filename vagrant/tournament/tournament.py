#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys
import traceback

def connect(connect_string):
    """
    Connect to the PostgreSQL database

    Argument: connect_string - of the form "dbname=database_name"
    Return: a database connection object
    """
    connection = None
    try:
        connection = psycopg2.connect(connect_string)

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return connection


def close_connection(connection):
    """
    Close the database connection

    Argument: none
    Returns: True on success; exception otherwise
    """
    try:
        psycopg2.Close(connection)

    except psycopg2.Error as e:
        print 'psycopg2.Error closing connection. error =', e
        sys.exit()

    return True

def deleteMatches():
    """
    Remove all the match records from the database.

    Argument: none
    Returns: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        # delete all rows in matches table
        cursor.execute("delete from matches;")
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True

def deletePlayers():
    """
    Remove all the player records from the database.

    Argument: none
    Returns: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        # delete all rows in players table
        cursor.execute("delete from players;")
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True

def countPlayers():
    """
    Returns the number of players currently registered.

    Argument: none
    Return: numeric value of count on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        cursor.execute("select count(*) from players;")
        count = cursor.fetchone()
        if type(count) is tuple:
            count = count[0]
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return count

def registerPlayer(pname):
    """
    Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Argument:
      name: the player's full name (need not be unique)
    Return: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        INSERT = cursor.mogrify('''INSERT INTO players (name) VALUES(%s);''', (pname,))
        cursor.execute(INSERT)

        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True


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
    CLEAN = '''
            DROP VIEW IF EXISTS winners;
            DROP VIEW IF EXISTS losers;
            '''

    WINNERS = '''
                CREATE VIEW winners AS
                    SELECT p.pid, p.name, count(m.winner) as wins
                    FROM players as p
                    LEFT OUTER JOIN matches as m
                    ON(p.pid = m.winner)
                    GROUP by p.pid, p.name
                    ORDER by p.pid;
             '''

    LOSERS = '''
                CREATE VIEW losers AS
                    SELECT p.pid, p.name, count(m.loser) as losses
                    FROM players as p
                    LEFT OUTER JOIN matches as m
                    ON(p.pid = m.loser)
                    GROUP BY p.pid, p.name
                    ORDER BY p.pid;
              '''

    WINS = '''
            SELECT * FROM winners ORDER BY wins DESC;
            '''

    LOSSES = '''
            SELECT * FROM losers ORDER BY losses DESC;
            '''

    MATCHES = '''
                SELECT w.pid, w.name, (w.wins + l.losses) as matches
                FROM winners w
                LEFT OUTER JOIN losers l
                ON(w.pid = l.pid)
                ORDER BY w.pid;
              '''

    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        # remove views
        cursor.execute(CLEAN)

        # create views
        cursor.execute(WINNERS)
        cursor.execute(LOSERS)

        # use view to acquire wins
        cursor.execute(WINS)
        wins = cursor.fetchall()

        #print 'playerStandings(): wins    =', wins

        # use view to acquire losses
        cursor.execute(LOSSES)
        losses = cursor.fetchall()
        #print 'playerStandings(): losses  =', losses

        # use view to calculate matches
        cursor.execute(MATCHES)
        matches = cursor.fetchall()
        #print 'playerStandings(): matches =', matches

        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    # match[2] is the match count for pid
    standings = [add_item_to_tuple(win, match[2])
                    for win in wins
                        for match in matches
                            # win[0] and match[0] are the pid
                            if win[0] == match[0]]

    # Return list of tuples, each of which contains (id, name, wins, matches)
    # print 'playerStandings(): standings =', standings
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        INSERT = cursor.mogrify('''INSERT INTO matches VALUES(%s,%s);''', (winner, loser))

        cursor.execute(INSERT)
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()
 
    return

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
    standings = playerStandings()
    print 'swissPairings(): standings =', standings

    # input to this algorithm is player info: (pid, name, wins, matches)
    pairing = []
    pair = ()
    # enumerate standings to get an index into players
    for (number, player) in enumerate(standings):
        print "number =", number, " player =", player
        # extract pid, name from player
        for index in range(0,1,1):
            identifier = player[index], player[index + 1]
            print "identifier =", identifier
        # create a pair of adjacent players
        pair += identifier
        print 'pair = ', pair

        # capture a single pair then reset pair on odd nubered players
        if number % 2 != 0:
            pairing.append(pair)
            pair = ()

    print 'pairing =', pairing
    return pairing


def add_item_to_tuple(input_tuple, item):
    '''add_item_to_tuple(): append item to input_tuple
       args: input_tuple - tuple that you want to append data to
             item - data to be appended
       return: input_tuple + (item,)
    '''
    return input_tuple + (item,)

def DumpTables():
    ''' DumpTables(): print contents of database tables
        Args: None
    '''
    PLAYERS = '''
                SELECT p.pid, p.name
                FROM players p
                ORDER BY p.pid;
              '''

    MATCHES = '''
                SELECT m.winner W, m.loser L
                FROM players p
                LEFT OUTER JOIN matches m
                ON(p.pid = m.winner);
              '''
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        cursor.execute(MATCHES)
        dump_matches = cursor.fetchall()

        cursor.execute(PLAYERS)
        dump_players = cursor.fetchall()

        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    print 'DumpTables(): dump_players =', dump_players
    print 'DumpTables(): dump_matches =', dump_matches

    return


if __name__ == '__main__':

    #registerPlayer("Twilight Sparkle")
    #registerPlayer("Fluttershy")
    #registerPlayer("Applejack")
    #registerPlayer("Pinkie Pie")

    standings = playerStandings()
    print 'script(): standings =', standings

    #winner, loser = 0, 0
    #
    #for (index, row) in enumerate(standings):
    #    print 'index, row =', index, ' ', row
    #    if index == 3:
    #        winner = row[0]
    #    if index == 4:
    #        loser = row[0]
    #
    #print 'winner =', winner
    #print 'loser  =', loser

    DumpTables()
    #reportMatch(winner, loser)
    #DumpTables()

