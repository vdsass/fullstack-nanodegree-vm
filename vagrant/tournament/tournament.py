#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys
import traceback

class TournamentHeader:
    '''
    TournamentHeader - uses class variables so any instantiation will
                       include updates to tid and title
    '''
    tid = 100
    title = 'Default Tournament'
    tournaments_dict = {}
    header = \
    '''
{:^37}

Current Tournament TID  : {:<9}
Current Tournament Title: {:<45}'''.\
        format('TOURNAMENT MANAGER', tid, title)

    def __init__(self):
        '''
        not creating instantiated objects
        '''
        pass

    def update_header(self):
        '''
        update_header(self) - [re-]generate the header string with current tid
                              and title
        '''
        self.header = \
    '''
{:^37}

Current Tournament PID  : {:<9}
Current Tournament Title: {:<45}'''.\
        format('TOURNAMENT MANAGER', self.tid, self.title)

def addTournament(title=None):
    """
    addTournament(): Add new tournament to dB

    Argument: title - string representing tournament name

    Return: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        # add tournament title
        INSERT = cursor.mogrify('''INSERT INTO tournaments (tname) VALUES(%s);''', (title,))
        cursor.execute(INSERT)
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True

def connect(connect_string):
    """
    Connect to the PostgreSQL database

    Argument: connect_string - of the form "dbname=<database_name>"
                                where 'database_name' is the name of your database
    Return: a database connection object
    """
    connection = None
    try:
        connection = psycopg2.connect(connect_string)

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return connection

def countPlayers(tid=100):
    """
    countPlayers(): returns the number of players currently registered.

    Argument: none

    Return: numeric value of count on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        cursor.execute('''SELECT count(*) FROM players
                          WHERE (tid = %s);''', (tid,))

        count = cursor.fetchone()
        if type(count) is tuple:
            count = count[0]
        else:
            print "countPlayers() ERROR: expected type(count)= 'tuple' but type(count)=",type(count)
            sys.exit()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return count

def deleteMatches():
    """
    Remove all the match records from the database.

    Argument: none
    Return: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        # delete all rows in matches table
        cursor.execute("delete from matches;")
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True

def deletePlayers():
    """
    Remove all the player records from the database.

    Argument: none

    Return: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        # delete all rows in players table
        cursor.execute("delete from players;")
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True

def getPlayers(tid):
    """
    getPlayers(tid): Returns a list of players in a Tournament, sorted by PID.

    Argument: tid - Tournament ID

    Return: list of players - [(tid1,pid1,name1), (tid2,pid2,name2) ...]

    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        PLAYERS = cursor.mogrify('''SELECT tid, pid, name
                                    FROM players
                                    WHERE (tid = %s)
                                    ORDER BY pid;''', (tid,))
        cursor.execute(PLAYERS)
        players = cursor.fetchall()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return players


def getTournaments():
    '''
    getTournaments(): return contents of tournaments table

    Argument: none

    Return: tournaments table
    '''
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        cursor.execute('''SELECT * FROM tournaments ORDER BY tid;''')
        tournaments = cursor.fetchall()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return tournaments


def playerStandings(tid=100):
    """
    playerStandings(): Returns a list of the players and their win records,
    sorted by wins.

    TODO: The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Argument: Tournament ID (tid, Default = 100)

    Return:
      standings: a list of tuples, each of which contains (id, name, wins, matches):
        where,
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()

        # remove views
        CLEAN = '''
                DROP VIEW IF EXISTS winners;
                DROP VIEW IF EXISTS losers;
                '''
        cursor.execute(CLEAN)

        # create views
        WINNERS = cursor.mogrify('''
                        CREATE VIEW winners AS
                            SELECT p.tid, p.pid, p.name, count(m.winner) as wins
                            FROM players as p
                            LEFT OUTER JOIN matches as m
                            ON ((p.tid = m.tid and p.pid = m.winner) and
                                (p.tid = %s and m.tid = %s))
                            GROUP by p.tid, p.pid, p.name
                            ORDER by p.pid;''', (tid,tid))

        #print 'playerStandings(): WINNERS =', WINNERS
        cursor.execute(WINNERS)

        LOSERS = cursor.mogrify('''
                    CREATE VIEW losers AS
                        SELECT p.tid, p.pid, p.name, count(m.loser) as losses
                        FROM players as p
                        LEFT OUTER JOIN matches as m
                        ON ((p.tid = m.tid and p.pid = m.loser) and
                            (p.tid = %s and m.tid = %s))
                        GROUP BY p.tid, p.pid, p.name
                        ORDER BY p.pid;''', (tid,tid))

        #print 'LOSERS =', LOSERS
        cursor.execute(LOSERS)

        # use view to acquire wins
        WINS = '''
               SELECT * FROM winners ORDER BY wins DESC, pid;
               '''
        cursor.execute(WINS)
        wins = cursor.fetchall()
        #print 'wins =', wins

        # use view to acquire losses
        LOSSES = '''
                 SELECT * FROM losers ORDER BY losses DESC;
                 '''
        cursor.execute(LOSSES)
        losses = cursor.fetchall()
        #print 'losses =', losses

        # use views to calculate matches
        MATCHES = cursor.mogrify('''SELECT w.tid, w.pid, w.name, (w.wins + l.losses) as matches
                FROM winners w
                LEFT OUTER JOIN losers l
                ON ((w.tid = l.tid and w.pid = l.pid) and
                    (w.tid = %s and l.tid = %s))
                ORDER BY w.pid;''', (tid,tid))

        cursor.execute(MATCHES)
        matches = cursor.fetchall()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    # format the data for display
    standings = []
    for win in wins:
        # some dB integer data is 'nL' (i.e., long int) and is converted to int
        win_tid,win_pid,win_name,win_wins = win[0],win[1],win[2],int(win[3])
        for match in matches:
            # convert match_sum None values to zero
            match_tid,match_pid,match_sum = (match[0],
                                             match[1],
                                             int(0 if match[3] is None else match[3]))

            # compare tournament id and player id; build the list
            if match_tid == tid:
                if win_tid == match_tid and win_pid == match_pid:
                    standings.append((win_pid, win_name, win_wins, match_sum))
    return standings

def registerPlayer(pname, tid=100):
    """
    registerPlayer(pname, tid): Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    is handled by the SQL database schema, not the Python code.)

    Argument:
        pname: the player's full name (need not be unique)
        tid: tournament id supports multiple tounaments. Default Tournament ID
        is 100 and increases by one for each added Tournament.

    Return: True on success; exception otherwise
    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        INSERT = cursor.mogrify('''INSERT INTO players (tid,name) VALUES(%s,%s);''', (tid,pname))
        cursor.execute(INSERT)
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()

    return True

def reportMatch(winner, loser, tid=100):
    """
    reportMatch(): Records the outcome of a single match between two players
    for the currently selected Tournament.

    Argument:
        winner: the Player ID of the winner
        loser: the Player ID of the loser
        tid: the Tournament ID

    Return: True on success; exception otherwise

    """
    try:
        dB_connection = connect("dbname=tournament")
        cursor = dB_connection.cursor()
        INSERT = cursor.mogrify('''INSERT INTO matches VALUES(%s,%s,%s);''',
                                (tid, winner, loser))
        cursor.execute(INSERT)
        dB_connection.commit()
        dB_connection.close()

    except psycopg2.Error as e:
        print 'e.pgcode =', e.pgcode
        print 'e.pgerror =', e.pgerror
        print 'traceback.format_exc() =', traceback.format_exc()
        sys.exit()
 
    return True

def swissPairings(tid=100):
    """
    swissPairings(): returns a list of player pairs for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Argument: tid - Tournament ID

    Return:
      A list of tuples, each of which contains (id1, name1, id2, name2), where
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

    Extra Credit: *TODO* Prevent rematches between players.

    """
    standings = playerStandings(tid)

    pairing = []
    pair = ()

    # enumerate to get an index
    for (number, player) in enumerate(standings):

        for index in range(0,1,1):
            adjacent_players = player[index], player[index + 1]
        # create a pair of *adjacent* players
        pair += adjacent_players

        # append chosen pair to list; reset pair on odd number
        if number % 2 != 0:
            pairing.append(pair)
            pair = ()

    return pairing
