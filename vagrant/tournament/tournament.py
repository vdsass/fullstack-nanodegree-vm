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

    #except Exception as instance:
    #    print "Exception error connecting to the database"
    #    print 'type(instance) =', type(instance)# the exception instance
    #    print 'instance.args =', instance.args  # arguments stored in .args
    #    print 'instance =', instance            # __str__ allows args to be...
    #    sys.exit()                              #  ...printed directly

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

    #except Exception as x:
    #    print 'Error closing connection. exception =', x
    #    sys.exit()

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

    #except Exception as instance:
    #    print "Exception error connecting to the database"
    #    print 'type(instance) =', type(instance)# the exception instance
    #    print 'instance.args =', instance.args  # arguments stored in
    #    print 'instance =', instance            #   .args__str__ allows args...
    #    sys.exit()                              #   ...to be printed directly

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

    #except Exception as instance:
    #    print "Exception error connecting to the database"
    #    print 'type(instance) =', type(instance)# the exception instance
    #    print 'instance.args =', instance.args  # arguments stored in
    #    print 'instance =', instance            #   .args__str__ allows args...
    #    sys.exit()                              #   ...to be printed directly

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

    #except Exception as instance:
    #    print "Exception error connecting to the database"
    #    print 'type(instance) =', type(instance)# the exception instance
    #    print 'instance.args =', instance.args  # arguments stored in
    #    print 'instance =', instance            #   .args__str__ allows args...
    #    sys.exit()                              #   ...to be printed directly

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
        cursor.execute("INSERT INTO players (name) VALUES('" + pname + "');")
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    #except Exception as instance:
    #    print "Exception error connecting to the database"
    #    print 'type(instance) =', type(instance)# the exception instance
    #    print 'instance.args =', instance.args  # arguments stored in
    #    print 'instance =', instance            #   .args__str__ allows args...
    #    sys.exit()                              #   ...to be printed directly

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
            DROP VIEW IF EXISTS pid_1_view;
            DROP VIEW IF EXISTS pid_2_view;
            '''

    WINS = '''
            SELECT p.pid, p.name, count(m.win_id) as wins
            FROM players p
            LEFT OUTER JOIN matches m
            ON p.pid=m.win_id
            GROUP BY p.pid
            ORDER BY wins;
            '''
    PID_1_V = '''
                CREATE VIEW pid_1_view AS
                SELECT p.pid, p.name, count(m.pid_1) as primary
                FROM players as p
                LEFT OUTER JOIN matches as m
                ON(p.pid = m.pid_1)
                GROUP by p.pid, p.name
                ORDER by p.pid;
             '''
    PID_2_V = '''
                CREATE VIEW pid_2_view AS
                SELECT p.pid, p.name, count(m.pid_2) as secondary
                FROM players as p
                LEFT OUTER JOIN matches as m
                ON(p.pid = m.pid_2)
                GROUP BY p.pid, p.name
                ORDER BY p.pid;
              '''

    MATCHES = '''
                SELECT x.pid, x.name, (x.primary + y.secondary) as matches
                FROM pid_1_view x
                LEFT OUTER JOIN pid_2_view y
                ON(x.pid = y.pid)
                ORDER BY x.pid;
              '''

    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        cursor.execute(CLEAN)
        cursor.execute(WINS)

        wins = cursor.fetchall()

        cursor.execute(PID_1_V)
        cursor.execute(PID_2_V)
        cursor.execute(MATCHES)

        matches = cursor.fetchall()

        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print "psycopg2.Error Can't connect to the database. e =", e
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    # See https://docs.python.org/2/howto/sorting.html#sortinghowto for 'key' argument explanation
    # Example: http://pythoncentral.io/how-to-sort-a-list-tuple-or-object-with-sorted-in-python/
    #          http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    # sorted_rows: sorted on wins; reverse => most to fewest wins

    # define the item within the list for sorted() to match against
    def getItem2(item):
        return item[2]

    sorted_wins = sorted(wins, key=getItem2, reverse=True)

    #print 'sorted_wins =', sorted_wins
    #print
    #print 'matches =', matches
    #for row in matches:
    #    print row

    # match[2] is the sum of matches for pid
    comprehension_result = [add_item_to_tuple(win, match[2])
                                for win in sorted_wins
                                    for match in matches
                                        if win[0] == match[0]]

    #print 'comprehension_result =', comprehension_result
    #for cr_tuple in comprehension_result:
    #    print 'cr_tuple =', cr_tuple
    # returns: A list of tuples, each of which contains (id, name, wins, matches)
    return comprehension_result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pass
 
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
    pass

def add_item_to_tuple(input_tuple, item):
    '''add_item_to_tuple(): append item to result_tuple
       args: input_tuple - tuple that you want to append data to
             item - data to be appended
       return: result tuple
    '''
    result_tuple = input_tuple
    result_tuple = result_tuple + (item,)
    #print 'add_item_to_tuple(): result_tuple =', result_tuple
    return (result_tuple)

if __name__ == '__main__':
    print('Starting tournament.py. Connecting to database...')
    dB_connection = connect()
    print 'Successful dB connection.  connect_status =', dB_connection
    close_connection(dB_connection)

