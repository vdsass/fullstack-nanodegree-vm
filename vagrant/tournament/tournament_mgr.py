#!/usr/bin/env python
#
# tournament_app.py -- user application for Swiss tournaments
#
'''
TAKE NOTE:
http://stackoverflow.com/questions/3338283/python-sharing-global-variables-between-modules-and-classes-therein

'from whatever import *' is not a good idiom to use in your code -- it's intended for use, if ever, in an interactive session as a shortcut to save some typing. It basically "snapshots" all names from the module at that point in time -- if you ever rebind any of those names, the snapshot will have grown stale and all sort of problems will ensue. And that's only the beginning of the inextricable mess you're signing up for by using the wretched 'from ... import *' construct.

from tournament import *
'''
from math import ceil, log

import tournament as tour
#  'menu' provides formatted menu(s) on the command line
#  http://pypi.python.org/pypi/Menu/
import menu
import sys

# global
# titles and names should not contain these characters
NON_ALPHA_CHARACTERS = set(['0','1','2','3','4','5','6','7','8','9',
                            '!','@','#','$','%','^','&','*','(',')',
                            '_','+','=','{','[','}',']','|','\\',':',
                            ';','\"',"'",'<','>','/','?'])

def update_mainMenu(arg):
    '''
    update_mainMenu(arg) - called every time the main menu is displayed. This
                            function updates Tournament header data: the current
                            Tournament ID (TID) and Tournament title.

    Argument: arg - [type Menu] -   title
                                indicator
                                options[]
                                FUNCTION
                                NAME

    Return: None
    '''
    # update header information with current Tournament data
    #   'arg' is the main menu object
    header = tour.TournamentHeader()
    header.update_header()
    arg.title = header.header
    return

def update_Submenu_Function(arg):
    '''
        TODO
    '''

    print 'update_Submenu_Function(): entered'
    print 'update_Submenu_Function(): arg =', arg
    print 'update_Submenu_Function(): exited'
    return

def display_tournaments(pause=True):
    '''
    display_tournaments(): Display a list of Tournaments in the dB

    Argument: prompt - Boolean - controls pause at end of display

    Return: None
    '''
    tournaments = tour.getTournaments()

    # tournaments header
    print '         TOURNAMENTS\n'
    print '      {:^3}        {:^5}'.format('TID', 'TITLE')

    # tournaments is a list of tournament tuples: (ID, TITLE)
    # TournamentHeader.tournaments_dict lists tournaments by TID and is used
    #   as a lookup in other functions
    tournaments_dict = {}
    for tournament in tournaments:
        # display the Tournaments
        print '{0:9d}  {1:45}'.format(tournament[0], tournament[1])
        # update the dict
        tournaments_dict[tournament[0]] = tournament[1]

    # update the TournamentHeader class variable
    tour.TournamentHeader.tournaments_dict = tournaments_dict

    if pause:
        queryEnter()

    return

def new_tournament():
    '''
    new_tournament(): Define a new Tournament in the dB. The TID will be assigned by the dB. The Tournament Title is input by the user.

    Argument: None

    Return: None

    '''
    # display the current list of Tournaments (TID, Title)
    display_tournaments(pause=False)

    tournament_title = ''
    while tournament_title == '':

        tournament_title = raw_input("Type Tournament Title and press Enter to continue: ")

        # verify title contains valid characters
        if contains_any(tournament_title, NON_ALPHA_CHARACTERS):
            print ('''Type alphabetic, including hyphen, characters for Tournament title, please.''')
            tournament_title = ''
            continue
    tour.addTournament(title=tournament_title)

    # show the user the current list of tournaments (TID, Title)
    display_tournaments()

    return

def select_tournament():
    '''
    select_tournament(): Display the dB tournaments table; query for an ID.

    Argument: None

    Return: None

    Side effects: updates Tournament header class data Tournament ID and name.
    '''
    # give the user a reference list
    display_tournaments(pause=False)

    # get currently defined Tournament ID's for later verification
    header_dict = tour.TournamentHeader.tournaments_dict
    tid_list = []
    for key in header_dict.iterkeys():
        tid_list.append(key)

    # get Tournament number from user
    tid = 0
    while tid == 0:
        try:
            response = int(raw_input("\nType a valid ID and press Enter to continue: "))

        except (ValueError, KeyError):
            print 'Not a valid response. Please try again. Type Ctrl-C to exit.\n'
            tid = 0
            continue

        except KeyboardInterrupt:
            return             # exit to main menu

        else:
            # verify user input tid exists
            if response not in tid_list:
                print 'Please choose an ID from the list above.\n'
                continue

            else:
                tid = response
                tour.TournamentHeader.tid = tid
                tour.TournamentHeader.title = tour.TournamentHeader.tournaments_dict[tour.TournamentHeader.tid]
    return

def display_players():
    '''
    display_players(): Display players for the currently selected Tournament.

    Argument: None

    Return: None
    '''
    header = tour.TournamentHeader()
    tid = header.tid
    if tid < 100:
        # TODO fix the raise statement
        raise "TID_Error - tid must be set to 100 or greater"
    players = tour.getPlayers(tid)

    print '''{:^45}'''.format('PLAYERS')
    print '''{:^5} {:^5} {:^35}'''.format('TID','PID','NAME')
    print '-'*45
    for (tid,pid,name) in players:
        print '''{0:^5d} {1:^5d} {2:<35}'''.format(tid, pid, name)
    queryEnter()
    return

def contains_any(string, set):
    '''
    contains_any(string, set): Compare a string for characters in a comparison set.

    Argument: string - the string to verify
          set    - the set of characters to compare

    Return: True - string contains one of the characters in the set
            False - string does not contain any of the characters in the set

    Reference: http://code.activestate.com/recipes/65441-checking-whether-a-string-contains-a-set-of-chars/

     Author: Horst Hansen
    '''
    for character in set:
        if character in string:
            return True;
    return False;

def verify_name():
    '''
    verify_name(): Prompt for name, verify valid characters, return string.

    Argument: None

    Return: Name as string
    '''
    pname_ok = False
    pname = ''
    # prompt for name
    #  verify alpha characters only
    #  repeat query until valid name
    #  return name
    while not pname_ok:

        try:
            pname = raw_input("Type the player's full name: ")

        except KeyboardInterrupt:
            print ('''Incorrect input. Please try again.''')
            pname_ok = False
            continue

        else:
            # verify user input
            if contains_any(pname, NON_ALPHA_CHARACTERS):
                print ('''Type alphabetic, including hyphen, characters for player's name, please.''')
                pname_ok = False
                continue
            else:
                pname_ok = True

    return pname

def add_player(name=None):
    '''
    add_player(): Register a new Player for the current Tournament. The Player
    ID (PID) will be assigned by the dB. The Player's name is input by the user
    and verified to contain non-numeric characters.

    Argument: name - default = None

    Return: None - returns to main menu
    '''
    current_tid = getTid()

    if current_tid < 100:
        print 'Please "Select Tournament" from the main menu.'
        queryEnter()
        return

    print '''This Tournament only supports even numbers of players. This function will help you add two players at a time.'''.format()

    while True:
        # the name must be alphabetic characters only
        pname = verify_name()
        tour.registerPlayer(pname, current_tid)
        if tour.countPlayers() % 2 != 0:
            continue
        else:
            break

    # display registered tournament players after entry
    display_players()
    return

def getpidList(listOfPairs):
    '''
    getpidList(listOfPairs): get a list of player IDs

    Argument: listOfPairs - list of pairs (tuples) that are tournament match pid's

    Return: list of match pid pairs

    '''
    pidSet= set()
    for (winner, loser) in listOfPairs:
        pidSet.add(winner)
        pidSet.add(loser)
    pidList = list(pidSet)
    return pidList

def getRound(tid=100):
    '''
    getRound(): return the current round of the Tournament, if the last
    round is complete, and the next round

    Argument: tid

    Return: Tournament round, Boolean for last round complete, Tournament next round
    '''
    playerCount = tour.countPlayers()

    # number of rounds in Swiss Pairing is based on number of players
    # need calculatedRounds to know when Tournament is finished
    #   i.e., current round > calculatedRounds
    calculatedRounds = int(ceil(log(playerCount,2)))
    standings = tour.playerStandings(tid)
    sumMatches = 0
    for playerStatistics in standings:
        pid,name,wins,matches = playerStatistics
        sumMatches += matches

    matchesPlayed = sumMatches / 2
    sumMatches_div_playerCount = sumMatches / playerCount

    current_round = sumMatches_div_playerCount + 1
    next_round = current_round + 1

    round_complete = False
    if playerCount / 2 == matchesPlayed:
        #   is True only when all matches for last round are played
        #   is False during current_round
        round_complete = True

    return current_round, round_complete, next_round

def update_match():
    '''
    update_match(): log results of a match (i.e., winner, loser) to the dB.

    Argument: None

    Return: None - returns to main menu
    '''
    # get pairings for this Tournament
    tid = getTid()
    pairings = tour.swissPairings(tid)

    display_pairings(pause=False)

    for (pid1,name1,pid2,name2) in pairings:
        winner_pid = 0
        loser_pid  = 0
        # get and verfy user input
        while winner_pid == 0:
            # Type the winner's PID then press Enter:
            match_pair = (pid1,pid2)
            pid_prompt = '''\nType the winner's PID, {} vs. {}, and press Enter: '''.format(pid1,pid2)

            try:
                winner_pid = int(raw_input(pid_prompt))

            except (ValueError, KeyError, KeyboardInterrupt):
                print 'Not a valid response. Please try again.\n'
                winner_pid = 0
                continue

            else:

                # verify winner_pid in range (pid1,pid2)
                if winner_pid not in (match_pair):
                    print 'Input Error. The PID input is not in the match presented! Try again.\n'
                    winner_pid = 0
                    continue

                if winner_pid == pid1:
                    winner_name = name1
                    loser_pid = pid2
                    loser_name = name2
                else:
                    loser_pid = pid1
                    winner_name = name2
                    loser_name = name1

                # update the match
                tour.reportMatch(winner_pid, loser_pid, tid)
    return


def display_standings():
    '''
    display_standings(): display the win/loss statistics of matches in the
    current Tournament

    Argument: none

    Return: None - returns to main menu

    TODO: add round to header

    '''
    # get the current tid
    tid = getTid()

    # get round info
    current_round, round_complete, next_round = getRound(tid)

    # convert Long int
    current_round = int(current_round)

    print '='*80
    print '''{:^80}'''.format('PLAYER STANDINGS')
    print '''{:>39} {:>3d}'''.format('Round:', current_round)
    print '-'*80
    print '''{:^5}  {:^45}  {:^5}  {:^5}'''.format('PID','NAME','WINS','MATCHES')
    print '-'*80

    standings = tour.playerStandings(tid)

    for (pid,name,wins,matches) in standings:
        print ''' {0:^3d}  {1:<45}    {2:^3d}     {3:^3d}'''.\
                  format(pid,name,wins,matches)

    print '='*80
    queryEnter()
    return

def display_pairings(pause=True):
    '''
    display_pairings(): display the PID and Player names paired (matched)
    for the next round in the current Tournament

    TODO: Extra Credit - Prevent rematches between players in a tournament.

    TODO: Argument: pairings - object
              prompt - Boolean controls pausing display

    Return: None - returns to main menu
    '''
    # get Tournament ID, pairings, and round information
    tid = getTid()
    pairings = tour.swissPairings(tid)

    current_round, round_complete, next_round = getRound(tid)
    # convert Long int
    current_round = int(current_round)

    print '='*80
    print '''{:^80}'''.format('PLAYER PAIRING')
    print '''{:>39} {:>3d}'''.format('Round:', current_round)
    if current_round == 1:
        text = 'adjacent PID\'s'
        print '''{:>40} {:<{width}}'''.format('Pairing by: ', text, width=len(text))
    else:
        text = 'adjacent PID\'s'
        print '''{:>40} {:<{width}}'''.format('Pairing by: ', text, width=len(text))
    print '-'*80
    print '''  {:^9}  {:^25}  {:^5}  {:^9}  {:^25}'''.\
               format('PLAYER 1','NAME',' ','PLAYER 2','NAME')

    print ''' {:^9}  {:^31}  {:^9}'''.\
              format('PID','  ','PID')
    print '-'*80

    for (pid1,name1,pid2,name2) in pairings:
        print ''' {:^9d}  {:<25}  {:^5}  {:^9d}  {:<25}'''.\
                  format(pid1,name1,'vs.',pid2,name2)
    print '='*80

    # pause to allow the pairing table to be viewed
    if pause:
        queryEnter()

    return

def queryEnter():
    '''
    queryEnter(): query user for 'Enter' key input

    Argument: none

    Return: None
    '''
    result = '?'
    try:
        while result != '':
            result = int(raw_input("\nPress Enter to continue: "))
            if result != '':
                continue # ...to ask for an 'Enter' input
    # 'Enter' generates ValueError
    # Ctrl-C is a KeyboardInterrupt
    except (ValueError, KeyboardInterrupt):
        return
    else:
        print 'tournament::queryEnter(): ERROR! try-except-else else entered'
        return

    return

def getTid():
    '''
    getCurrentTid(): return the current Tournament ID

    Argument: None

    Return: current Tournament ID

    '''
    # create a header object, return Tournament ID
    header = tour.TournamentHeader()
    return header.tid

def dump_tables():
    return tour.dumpTables(tid=getTid())

def quit():
    '''
    quit() - exits the program

    Argument: None

    Return: None - returns to the command line interpreter
    '''
    sys.exit()

def tournament_app():
    '''
    tournament_app() - Command line application to manage and report Tournament
                       information.
    Argument: None

    Return: None - traverses the menu system until 'Quit' is selected.
    '''
    # dB is connectd/disconnected on each call to a function
    #   a query or a commit action is performed
    #   data is returned from or inserted into the dB
    #   the dB is closed
    #header_info = \
    #
    #{:^37}
    #
    #Current Tournament PID: {:>9}
    #Current Tournament Title: {:<45}'''.\
    #    format('TOURNAMENT MANAGER', tour.common.TID, tour.common.title)

    # create 'header' object with default Tournaments
    mainMenu = menu.Menu(tour.TournamentHeader.header, update=update_mainMenu)
    mainMenu.explicit()

    # main menu capabilities
    # 1. Display (Show) Tournaments in the dB
    #
    # 2. Select a Tournament as the object to query or add information to
    #   a. the 'Default Tounament, TID=100' is initially selected
    #   b. operations are prefaced with the current tournament ID
    #
    # 3. Select current tournament
    #   a. list Tournaments
    #   b. TID input by user
    #   c. New Tournament is selected
    #
    # 3. Create a new tournament
    #   a. TID assigned by app
    #   b. Name input by user
    #   c. New Tournament is automatically selected - TODO
    #
    # 2. Create a new Player
    #   a. PID assigned to current Tournament
    #   b. user inputs Player name
    #
    # 3. assign a winner/loser to a match
    #
    # 4. show next round pairing

    options = [
                {"name":"Display Tournament List","function":display_tournaments},
                {"name":"Select Tournament","function":select_tournament},
                {"name":"Add Tournament","function":new_tournament},
                {"name":"Display Player List","function":display_players},
                {"name":"Add Player","function":add_player},
                {"name":"Display Tournament Standings","function":display_standings},
                {"name":"Display Next Round Pairing","function":display_pairings},
                {"name":"Update Match","function":update_match},
                {"name":"Quit","function":quit},
            ]
    mainMenu.addOptions(options)
    mainMenu.open()

if __name__ == '__main__':
    tournament_app()

