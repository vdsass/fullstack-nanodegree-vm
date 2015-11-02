-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create db and connect
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- drop tables - because of FK, order is important
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- create tables

CREATE TABLE IF NOT exists players(
                                    pid serial primary key,
                                    name text
                                   );
INSERT INTO players (pid, name) values(0,'Nobody');
INSERT INTO players (name) values('Billy Bob Thorton');
INSERT INTO players (name) values('Christian Bale');
INSERT INTO players (name) values('Johnny Depp');
INSERT INTO players (name) values('Brad Pitt');
INSERT INTO players (name) values('Jon Ham');

/*
CREATE TABLE IF NOT exists matches (
    pid_1 integer REFERENCES players (pid),
    pid_2 integer REFERENCES players (pid),
    win_id integer REFERENCES players (pid)
);
--   MATCHES
-- 1 2 3 4 5  W
-- x x        2
-- x   x      1
-- x     x    4
--   x x      2
--   x   x    4
--     x x    4
--         X
-- INSERT INTO matches(pid_1, pid_2, win_id) values();
INSERT INTO matches (pid_1, pid_2, win_id) VALUES
    (0, 0, 0),
    (1, 2, 2),
    (1, 3, 1),
    (1, 4, 4),
    (2, 3, 2),
    (2, 4, 4),
    (3, 4, 4),
    (4, 0, 0),
    (5, 0, 0);
*/

CREATE TABLE IF NOT exists matches (
    winner integer REFERENCES players (pid),
    loser integer REFERENCES players (pid)
);

INSERT INTO matches (winner, loser) values(1,5);
INSERT INTO matches (winner, loser) values(4,2);
INSERT INTO matches (winner, loser) values(2,1);
INSERT INTO matches (winner, loser) values(5,4);
INSERT INTO matches (winner, loser) values(5,2);
INSERT INTO matches (winner, loser) values(5,1);

