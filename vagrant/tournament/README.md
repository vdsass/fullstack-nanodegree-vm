`README.md`

#Introduction

This is the markdown file that describes 'Tournament Manager.' It lists the file names that comprise the application, describes how to use them, and how to use the tournament application. The description indicates specific path naming conventions for PC and Mac installations.

This description assumes you have Python 2 and Postgresql installed.

1. Navigate to the directory where the tournament project files have been downloaded (i.e., in Windows:
   C:\Users\usr\tournaments\; in OsX: /Users/user/tournaments/).

   The tournament files are:

        a. tournament.py - module containing foundation functions and methods for the tournament project.

        b. tournament_mgr.py - application that uses tournament.py to manage a set of Tournaments, the registered players, and matches between players.

        c. tournament_test.py - script to initially test the database and tournament.py.

        d. menu.py - Python Package Index module (https://pypi.python.org/pypi/Menu) installed in local directory. Provides API to create a command line menu infrastructure.

        e. README.md - markdown file that describes the tournament project.

## Test the Python and PostgreSQL Installation

2. Run tournament_test.py to verify the architecture and organization of the files and database. This script will verify that the postgresql database schema supports the tests provided by Udemy. The stdout display should look like this:

        C:\> python2 tournament_test.py
        1. Old matches can be deleted.
        2. Player records can be deleted.
        3. After deleting, countPlayers() returns zero.
        4. After registering a player, countPlayers() returns 1.
        5. Players can be registered and deleted.
        6. Newly registered players appear in the standings with no matches.
        7. After a match, players have updated standings.
        8. After one match, players with one win are paired.
        Success!  All tests pass!

    **NOTE**: Do not run tournament_test.py after you enter data for Tournaments, Players, and Matches. Tournament_test.py will delete any Tournament information that has been entered.

## Using Tournament Manager

To run the Tournament Manager application perform the following steps:

   a. double click the file icon for tournament_mgr.py (it is assumed that
      a file with the '.py' extension will run the Python version 2.x interpreter)

   or,

   b. at a command-line prompt type the following command (it is assumed that
      the 'python' command runs the Python version 2.x interpreter):

        'Windows: C:\Users\user\tournaments > python tournament_mgr.py'
        'OsX: /Users/user/tournaments > python tournament_mgr.py'

In a command window on a PC, or terminal on a Mac, navigate to the directory/folder containg the tournament files. Type tournament_mgr.py and Return, to execute the application. Tournament Manager will display an ASCII menu permitting a user to view and update Tournament database tables. At the prompt, **>>>**, Input the menu number to access the corresponding funtionality listed in the menu.

                TOURNAMENT MANAGER

       Current Tournament TID  : 100
       Current Tournament Title: Default Tournament

       1. Show Tournaments
       2. Select Tournament
       3. New Tournament
       4. Show Players
       5. Add Player
       6. Display Tournament Standings
       7. Show Next Round Pairing
       8. Update Match
       9. Quit

       >>>

The currently selected Tournament ID and name are displayed below the application's title.

### Using Menu Functions

1.  Menu item 1, Show Tournaments, lists all the Tournaments that have been created in the database.

                TOURNAMENTS

             TID        TITLE
             100  Default Tournament
             101  San Diego Western Regionals
             102  Las Vegas Finals
             103  Kansas City Midwestern
             104  New York Eastern Championships
             105  Seattle NorthPac

            Press Enter to continue:

1.  Menu item 2, Select Tournament, establishes the 'current' tournament for other commands to use. The function lists the defined Tournaments and permits a valid TID entry.

             TOURNAMENTS

          TID        TITLE
          100  Default Tournament
          101  San Diego Western Regionals
          102  Las Vegas Finals
          103  Kansas City Midwestern
          104  New York Eastern Championships
          105  Seattle NorthPac

        Type a valid ID and press Enter to continue:

1.  Menu item 3, New Tournament, creates additional Tounaments. A user selects the name, and the database creates a Tournament ID.

             TOURNAMENTS

          TID        TITLE
          100  Default Tournament
          101  San Diego Western Regionals
          102  Las Vegas Finals
          103  Kansas City Midwestern
          104  New York Eastern Championships
          105  Seattle NorthPac

1.  Menu item 4, Show Players, for the current Tournament displays registered players by ID and name.

                    PLAYERS
          TID   PID                 NAME
          102    1   Billy Bob Thornton
          102    2   Christian Bale
          102    3   Johnny Depp
          102    4   Brad Pitt

         Press Enter to continue:

1.  Menu item 5, Add Player, accepts user input for player name and creates an entry in the database for the player in the selected Tournament.

    **NOTE**: Tournament Manager only supports an even number of Tournament players.

            Type the player's full name:                  **Return entered**
                               PLAYERS
             TID   PID                 NAME
            ---------------------------------------------
             102    1   Billy Bob Thornton
             102    2   Christian Bale
             102    3   Johnny Depp
             102    4   Brad Pitt
             102    5                                    **TODO** - can't have this!!

            Press Enter to continue:

    **TODO** - write something like: 'There are N players.' If the player number is odd, add another. If the player number is even, say something else.

1. Menu item 6, Display Tournament Standings, for the current Tournament for each player displays the number of wins and the number of matches played.

    For a Tournament that has not yet started, Player Standings look like this:

            ================================================================================
                                            PLAYER STANDINGS
                                             Round:   1
            --------------------------------------------------------------------------------
             PID                       NAME                       WINS   MATCHES
            --------------------------------------------------------------------------------
              1   Billy Bob Thornton                                0       0
              2   Christian Bale                                    0       0
              3   Johnny Depp                                       0       0
              4   Brad Pitt                                         0       0
            ================================================================================

            Press Enter to continue:

    There are no Wins or Matches shown until 'Update Matches' has been executed. The following display shows Tournament Standings Status after 'Update Match' is executed after one round of play. Note that round 2 is indicated.

                    TOURNAMENT MANAGER

           Current Tournament PID  : 102
           Current Tournament Title: Las Vegas Finals

           1. Show Tournaments
           2. Select Tournament
           3. New Tournament
           4. Show Players
           5. Add Player
           6. Display Tournament Standings
           7. Show Next Round Pairing
           8. Update Match
           9. Quit

           >>> 6

           ================================================================================
                                           PLAYER STANDINGS
                                            Round:   2
           --------------------------------------------------------------------------------
            PID                       NAME                       WINS   MATCHES
           --------------------------------------------------------------------------------
             1   Billy Bob Thornton                                1       1
             3   Johnny Depp                                       1       1
             2   Christian Bale                                    0       1
             4   Brad Pitt                                         0       1
           ================================================================================

           Press Enter to continue:

1. Menu item 7, Show Next Round Pairing, for the current Tournament displays the pairs of players matched in the current round, or the next round if all player matches in the current round have been updated.

    A first round pairing for 4 players looks like this:

               >>> 7

               ================================================================================
                                                PLAYER PAIRING
                                                Round:   1
                                           Pairing by:  adjacent PID's
               --------------------------------------------------------------------------------
                 PLAYER 1             NAME                    PLAYER 2             NAME
                   PID                                         PID
               --------------------------------------------------------------------------------
                    1      Billy Bob Thornton          vs.       2      Christian Bale
                    3      Johnny Depp                 vs.       4      Brad Pitt
               ================================================================================

               Press Enter to continue:

    After the  first round and an update of match status:

                            TOURNAMENT MANAGER

                   Current Tournament PID  : 102
                   Current Tournament Title: Las Vegas Finals

                   1. Show Tournaments
                   2. Select Tournament
                   3. New Tournament
                   4. Show Players
                   5. Add Player
                   6. Display Tournament Standings
                   7. Show Next Round Pairing
                   8. Update Match
                   9. Quit

                   >>> 7

                   ================================================================================
                                                    PLAYER PAIRING
                                                    Round:   2
                                              Pairing by:  Opponent Match Wins (OMW)
                   --------------------------------------------------------------------------------
                     PLAYER 1             NAME                    PLAYER 2             NAME
                       PID                                         PID
                   --------------------------------------------------------------------------------
                        1      Billy Bob Thornton          vs.       3      Johnny Depp
                        2      Christian Bale              vs.       4      Brad Pitt
                   ================================================================================

                   Press Enter to continue:

1. Menu item 8, Update Match, for the current Tournament allows the user to update win/loss information for each matched player pair.

    **NOTE**: A user must update all matches in a Tournament at the same time.

        >>> 8
                                                                        TODO:
        All matches must be updated at the same time. Continue? [Y/N]:  <<<<<==== A CR was entered!
        ================================================================================
                                         PLAYER PAIRING
                                         Round:   1
                                    Pairing by:  adjacent PID's
        --------------------------------------------------------------------------------
          PLAYER 1             NAME                    PLAYER 2             NAME
            PID                                         PID
        --------------------------------------------------------------------------------
             1      Billy Bob Thornton          vs.       2      Christian Bale
             3      Johnny Depp                 vs.       4      Brad Pitt
        ================================================================================
        update_match(): number_of_matches = 2
        Type a winner's PID and press Enter, or Enter to exit:   <<<<<== Ctrl-c works here!

1. Menu item 9, Quit, exits Tournament Manager and returns to the prompt of the host operating system.

