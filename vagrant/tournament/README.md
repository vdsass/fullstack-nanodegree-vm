`README.md`

#Introduction

This is the markdown file that describes setup and use of the Tournament
project that runs under a Vagrant virtual machine (VM) prescribed by the
Udacity Project Guide. This description assumes you have Python 2 and
PostgreSQL installed on the local machine.

1. On the local machine navigate to the directory where the tournament
project files have been downloaded (i.e., in Windows:
   C:\Users\user\tournaments\; in OS X: /Users/user/tournaments/).

1. Using Git, clone the GitHub repository
    https://github.com/vdsass/fullstack-nanodegree-vm to the local directory.

1. On the local machine navigate from the cloned repository directory to
    ./vagrant/tournament/ where you will find the following files:

        a. menu.py - Python Package Index module
            (https://pypi.python.org/pypi/Menu). Provides an API to create
            a command line menu infrastructure.

        b. README.md - this file, the markdown file that describes the
            tournament project.

        c. tournament.py - module containing functions and methods for the
            tournament project.

        d. tournament_mgr.py - application that uses tournament.py to
            manage a set of Tournaments, the registered players, and
            matches between players.

        e. tournament.sql - script to initialize the database with tournaments and players.

        e. tournament_test.py - script to initially test the database and
            tournament.py.

## Test the Python and PostgreSQL Installation

1. Navigate to the local vagrant directory

    **$ cd vagrant/**

1. Launch vagrant

    **$ vagrant up**

    The stdout display shoud be similar to this:

        Bringing machine 'default' up with 'virtualbox' provider...
        --- default: Checking if box 'ubuntu/trusty32' is up to date...
        --- default: A newer version of the box 'ubuntu/trusty32' is available! You currently
        --- default: have version '20151119.0.0'. The latest is version '20151130.0.0'. Run
        --- default: `vagrant box update` to update.
        --- default: Clearing any previously set forwarded ports...
        --- default: Clearing any previously set network interfaces...
        --- default: Preparing network interfaces based on configuration...
            default: Adapter 1: nat
        --- default: Forwarding ports...
            default: 8000 => 8000 (adapter 1)
            default: 8080 => 8080 (adapter 1)
            default: 5000 => 5000 (adapter 1)
            default: 22 => 2222 (adapter 1)
        --- default: Booting VM...
        --- default: Waiting for machine to boot. This may take a few minutes...
            default: SSH address: 127.0.0.1:2222
            default: SSH username: vagrant
            default: SSH auth method: private key
            default: Warning: Connection timeout. Retrying...
        --- default: Machine booted and ready!
        --- default: Checking for guest additions in VM...
        --- default: Mounting shared folders...
            default: /vagrant => C:/Users/User/Documents/AAADevelop/udacity/FSND/fullstack/vagrant
        --- default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
        --- default: flag to force provisioning. Provisioners marked to run always will still run.

1. Log in to vagrant

    **$ vagrant ssh**

    The stdout display shoud be similar to this:

        Welcome to Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-65-generic i686)

         * Documentation:  https://help.ubuntu.com/

         System information disabled due to load higher than 1.0

          Get cloud support with Ubuntu Advantage Cloud Guest:
            http://www.ubuntu.com/business/services/cloud

        33 packages can be updated.
        19 updates are security updates.

        The shared directory is located at /vagrant
        To access your shared files: cd /vagrant
        Last login: Sun Nov 29 21:08:35 2015 from 10.0.2.2
        vagrant@vagrant-ubuntu-trusty-32:/vagrant$

1. Navigate to the tournament directory

    vagrant@vagrant-ubuntu-trusty-32:/vagrant$ **cd /vagrant/tournament/**

1. Run the tournament verification tests:

    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ **python2 tournament_test.py**

    A successful end-to-end test output looks like the following:

            1. Old matches can be deleted.
            2. Player records can be deleted.
            3. After deleting, countPlayers() returns zero.
            4. After registering a player, countPlayers() returns 1.
            5. Players can be registered and deleted.
            6. Newly registered players appear in the standings with no matches.
            7. After a match, players have updated standings.
            8. After one match, players with one win are paired.
            Success!  All tests pass!

    **NOTE**: Run tournament_test.py only once, at the beginning of
    vagrant setup. If you run tournament_test.py after entering
    data for Tournaments, Players, and Matches, tournament_test.py will
    delete any Tournament information that has been entered.

1. You are now able to use the Tournament Manager application. If you want to initialize the database with a set of tournaments and players perform the following steps. If you do not want to initialize the databasse, skip to 'Using Tournament Manager.'

    1. Run the PostgreSql application:
        vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ **psql**

            psql (9.3.9)
            Type "help" for help.
            vagrant=>

    1. Initialize the database:

        vagrant=> **\i tournament.sql**

        The response should look like:

            DROP DATABASE
            CREATE DATABASE
            You are now connected to database "tournament" as user "vagrant".
            psql:tournament.sql:15: NOTICE:  table "matches" does not exist, skipping
            DROP TABLE
            psql:tournament.sql:16: NOTICE:  table "players" does not exist, skipping
            DROP TABLE
            psql:tournament.sql:17: NOTICE:  table "tournaments" does not exist, skipping
            DROP TABLE
            CREATE TABLE
            ALTER SEQUENCE
            INSERT 0 1
            INSERT 0 1
            INSERT 0 1
            INSERT 0 1
            INSERT 0 1
            INSERT 0 1
            CREATE TABLE
            INSERT 0 1
            INSERT 0 1
            INSERT 0 1
            INSERT 0 1
            CREATE TABLE

    1. Exit the PostgreSql application:

        tournament=> **\q**

## Using Tournament Manager

To run the Tournament Manager application perform the following steps:


1. at a Bash command-line prompt type the following command:

    $ **python2 tournament_mgr.py**

    Tournament Manager will display an ASCII menu permitting a user to view
    and update the Tournament database. At the prompt, type the menu number
    to access the corresponding funtionality listed in the menu. The
    currently selected Tournament ID and name will be displayed below
    the application's title.

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

           >>> 1



### Menu Functions

1.  Menu item 1, Show Tournaments, lists Tournaments that have been
    created in the database. The display pauses at the end of the list
    and requires a 'Enter/Return' input to continue:

                TOURNAMENTS

             TID        TITLE
             100  Default Tournament
             101  San Diego Western Regionals
             102  Las Vegas Finals
             103  Kansas City Midwestern
             104  New York Eastern Championships
             105  Seattle NorthPac

            Press Enter to continue:

    **NOTE**: You can initialize the dababase with tournaments and players by running tournament.sql within the psql application:

        vagrant=> **\i tournament.sql**


1.  Menu item 2, Select Tournament, establishes the 'current' tournament
    for other commands to use. The function lists the defined Tournaments
    and permits a valid TID entry. The newly established Tournament is shown
    below the title:

            TOURNAMENTS

         TID        TITLE
         100  Default Tournament
         101  San Diego Western Regionals
         102  Las Vegas Finals
         103  Kansas City Midwestern
         104  New York Eastern Championships

        Type a valid ID and press Enter to continue: 102

                TOURNAMENT MANAGER

        Current Tournament PID  : 102
        Current Tournament Title: Las Vegas Finals

        1. Display Tournament List
        2. Select Tournament
        3. Add Tournament
        4. Display Player List
        5. Add Player
        6. Display Tournament Standings
        7. Display Next Round Pairing
        8. Update Match
        9. Quit

1.  Menu item 3, New Tournament, creates additional Tounaments. A user
    types the name and the database creates a Tournament ID.

             TOURNAMENTS

          TID        TITLE
          100  Default Tournament
          101  San Diego Western Regionals
          102  Las Vegas Finals
          103  Kansas City Midwestern
          104  New York Eastern Championships
          105  Seattle NorthPac

1.  Menu item 4, Show Players, for the current Tournament displays
    registered players by ID and name.

                    PLAYERS
          TID   PID                 NAME
          102    1   Billy Bob Thornton
          102    2   Christian Bale
          102    3   Johnny Depp
          102    4   Brad Pitt

         Press Enter to continue:

1.  Menu item 5, Add Player, accepts user input for a player name and
    creates an entry in the database for the player in the current Tournament.

            This Tournament only supports even numbers of players. This
            function will help you add two players at a time.

            Type the player's full name: Jon Hamm
            Type the player's full name: Kevin Bacon
                               PLAYERS
             TID   PID                 NAME
            ---------------------------------------------
             102    1   Billy Bob Thornton
             102    2   Christian Bale
             102    3   Johnny Depp
             102    4   Brad Pitt
             102    5   Jon Hamm
             102    6   Kevin Bacon

            Press Enter to continue:

1. Menu item 6, Display Tournament Standings, for each player in the
   current Tournament displays the number of wins and the number of matches
   played. For a Tournament that has not recorded any matches, Player
   Standings look like this:

                                                PLAYER STANDINGS
                                                 Round:   1
                --------------------------------------------------------------------------------
                 PID                       NAME                       WINS   MATCHES
                --------------------------------------------------------------------------------
                  1   Billy Bob Thornton                                0       0
                  2   Christian Bale                                    0       0
                  3   Johnny Depp                                       0       0
                  4   Brad Pitt                                         0       0
                  5   Jon Hamm                                          0       0
                  6   Kevin Bacon                                       0       0
                ================================================================================

                Press Enter to continue:

    There are no Wins or Matches shown until 'Update Matches' has been
    executed. The following display shows Tournament Standings Status after
    an update after one round of play. Note that round 2 is indicated.

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

1. Menu item 7, Show Next Round Pairing, for the current Tournament
   displays the pairs of players matched in the current round, or the next
   round if all player matches in the current round have been updated.

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

    After the first round update, match status looks like:

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
                                               Pairing by:  adjacent PID's
                   --------------------------------------------------------------------------------
                     PLAYER 1             NAME                    PLAYER 2             NAME
                       PID                                         PID
                   --------------------------------------------------------------------------------
                        1      Billy Bob Thornton          vs.       3      Johnny Depp
                        2      Christian Bale              vs.       4      Brad Pitt
                   ================================================================================

                   Press Enter to continue:

1. Menu item 8, Update Match, for the current Tournament allows the user to
   update win/loss information for each matched player pair.

                    TOURNAMENT MANAGER

           Current Tournament PID  : 102
           Current Tournament Title: Las Vegas Finals

           1. Display Tournament List
           2. Select Tournament
           3. Add Tournament
           4. Display Player List
           5. Add Player
           6. Display Tournament Standings
           7. Display Next Round Pairing
           8. Update Match
           9. Quit

           >>> 8

           ================================================================================
                                            PLAYER PAIRING
                                            Round:   2
                                       Pairing by:  adjacent PID's
           --------------------------------------------------------------------------------
             PLAYER 1             NAME                    PLAYER 2             NAME
               PID                                         PID
           --------------------------------------------------------------------------------
                2      Christian Bale              vs.       3      Johnny Depp
                6      Kevin Bacon                 vs.       1      Billy Bob Thornton
                4      Brad Pitt                   vs.       5      Jon Hamm
           ================================================================================

           Type the winner's PID, 2 vs. 3, and press Enter: 3

           Type the winner's PID, 6 vs. 1, and press Enter: 6

           Type the winner's PID, 4 vs. 5, and press Enter: 5

1. Menu item 9, Quit, exits Tournament Manager and returns to the prompt of
   the host operating system.

